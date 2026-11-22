"""One Track-only HOI task; mode is an intention, never a motion identifier."""
import json,os
from pathlib import Path
import torch
from holosoma.carry.stage1_command import Stage1TrackCommand
from holosoma.carry.fullbody_command import FullBodyCommand
from holosoma.carry.fullbody_environment import FullBodyCarryEnv
from holosoma.carry.stage1_environment import Stage1CarryEnv
from holosoma.carry.fullbody_termination import FullBodyFailure,pose_failure_diagnostics
from holosoma.carry.observations import actor_frame as carry_frame,critic_reference,simulator_box_state
from holosoma.carry.fullbody_rewards import physical_metrics,grasp,hand_slip
from holosoma.carry.stage1_diagnostics import Stage1DiagnosticLog
from holosoma.utils.rotations import quaternion_to_matrix,quat_error_magnitude

MODES=('pickup','carry','putdown')
FAMILIES=('full_sequence','loaded_locomotion','loaded_squat_stand')
FRAME_DIM=119
ACTOR_DIM=357
from holosoma.carry.support import SupportState,PRIVILEGED_FIELDS,PROTOCOL
CRITIC_DIM=119+68+len(PRIVILEGED_FIELDS)

def family_assignment(n,weights,device):
    if n<1:raise ValueError('At least one environment is required')
    minimum=1 if n>=len(weights) else 0  # small viewer/probe batches; training sizes cover every family
    w=torch.tensor(weights,device=device);counts=torch.floor(n*w/w.sum()).long().clamp_min(minimum)
    while counts.sum()<n:counts[(n*w/w.sum()-counts).argmax()]+=1
    while counts.sum()>n:
        candidates=torch.where(counts>minimum,counts-n*w/w.sum(),-torch.inf);counts[candidates.argmax()]-=1
    return torch.repeat_interleave(torch.arange(len(weights),device=device),counts)

class UnifiedCommand(Stage1TrackCommand):
    def init_buffers(self):
        sampler=getattr(self,'adaptive_timesteps_sampler',None)
        saved={k:getattr(sampler,k).clone() for k in ('bin_fail_ema','pending_visits','pending_failures')} if sampler else {}
        super().init_buffers()
        for key,value in saved.items():getattr(self.adaptive_timesteps_sampler,key).copy_(value)
        self.task_mode=torch.zeros(self.num_envs,device=self.device,dtype=torch.long)
        self.reset_start_frame=torch.zeros_like(self.task_mode)

    def reset(self,ids):
        super().reset(ids)
        self.reset_start_frame[ids]=self.time_steps[ids]-self.motion.motion_start_idx[self.motion_ids[ids]]

    def setup(self):
        if self.manifest['schema']!='unified_hoi_v1' or self.motion_cfg.hybrid.track_ratio!=1:raise ValueError('Unified HOI requires its own Track-only dataset')
        FullBodyCommand.setup(self)
        self.rows=sorted(self.manifest['motions'],key=lambda r:r['name'])
        self.family_ids=family_assignment(self.num_envs,[self.manifest['family_weights'][f] for f in FAMILIES],self.device)
        self.phase_bank=torch.tensor(sum([r['task_modes'] for r in self.rows],[]),device=self.device,dtype=torch.long)
        if len(self.phase_bank)!=self.motion.time_step_total:raise ValueError('Phase bank/frame mismatch')
        self.eligible=[torch.tensor(r['eligible_reset_frames'],device=self.device)+self.motion.motion_start_idx[i] for i,r in enumerate(self.rows)]
        sim=self._env.simulator;self.reference_hard_limits=sim._robot.root_physx_view.get_dof_limits()[0,sim.dof_ids].to(self.device)
        torch.testing.assert_close(self.reference_hard_limits,sim.hard_dof_pos_limits,atol=2e-6,rtol=0)
        self._validate_hard_positions(self.motion.joint_pos,'unified canonical motion bank')
        if self.gen_env_mask.any():raise ValueError('Gen forbidden in Unified Stage1')

    def _sample_motion_ids_for_reset(self,ids):
        for family_id,family in enumerate(FAMILIES):
            selected=ids[self.family_ids[ids]==family_id]
            weights=torch.tensor([r['sampling_weight'] if r['family']==family else 0 for r in self.rows],device=self.device)
            if len(selected):self.motion_ids[selected]=torch.multinomial(weights,len(selected),replacement=True)

    def _sample_uniform_reset_states(self,ids):
        self._sample_motion_ids_for_reset(ids)
        mids=self.motion_ids[ids].clone();times=torch.empty_like(mids)
        for motion in range(len(self.rows)):
            mask=mids==motion;n=int(mask.sum())
            if n:times[mask]=self.eligible[motion][torch.randint(len(self.eligible[motion]),(n,),device=self.device)]
        return mids,times

    def _sample_adaptive_reset_states(self,ids,groups):
        if (groups!=0).any():raise ValueError('Unified Stage1 only supports Track sampler group')
        self._sample_motion_ids_for_reset(ids);mids=self.motion_ids[ids].clone();bins=torch.empty_like(mids);times=torch.empty_like(mids)
        for motion,row in enumerate(self.rows):
            mask=mids==motion;n=int(mask.sum())
            if not n:continue
            _,b,t=self.adaptive_timesteps_sampler.sample_from_motion_pool(0,torch.tensor([motion],device=self.device),n)
            # Condition the upstream bin distribution on eligible frames. No phase override.
            # The bundled motions have contiguous eligible frames; rejection preserves
            # relative difficulty-bin probability, unlike mapping invalid draws to frame0.
            valid=torch.isin(t,self.eligible[motion])
            for _ in range(100):
                if valid.all(): break
                _,_,retry=self.adaptive_timesteps_sampler.sample_from_motion_pool(
                    0,torch.tensor([motion],device=self.device),int((~valid).sum()))
                t[~valid]=retry
                valid=torch.isin(t,self.eligible[motion])
            if not valid.all(): raise RuntimeError('Adaptive sampler has no eligible reset support')
            bins[mask]=self.adaptive_timesteps_sampler.time_step_to_bin(mids[mask],t);times[mask]=t
        return mids,bins,times

    def _update_track_commands(self):
        super()._update_track_commands()
        if hasattr(self,'phase_bank'):self.task_mode[:]=self.phase_bank[self.time_steps]

    def update_metrics(self):
        FullBodyCommand.update_metrics(self)
        for i,f in enumerate(FAMILIES):self.metrics['hoi/family_fraction/'+f]=torch.tensor([r['family']==f for r in self.rows],device=self.device)[self.motion_ids].float()
        for i,mode in enumerate(MODES):self.metrics['hoi/mode_fraction/'+mode]=(self.task_mode==i).float()

def actor_frame(env):
    cmd=env.command_manager.get_state('motion_command')
    return torch.cat([carry_frame(env),torch.nn.functional.one_hot(cmd.task_mode,3).float()],-1)

def critic_support(env):
    # At reset there is no integrated contact yet. State is explicitly zeroed.
    if not getattr(env,'hoi_metrics_valid',False):
        return torch.zeros(env.num_envs,len(PRIVILEGED_FIELDS),device=env.device)
    return torch.stack([env.hoi_metrics[k] for k in PRIVILEGED_FIELDS],-1)

def box_ground_state(env):
    m=physical_metrics(env);box=simulator_box_state(env)
    ground=getattr(env.simulator,'carry_ground',torch.zeros_like(box[:,:3]))[:,2].clamp_min(0)
    m.update(ground_support_weight_ratio=ground/(env.carry_box_mass*9.81),object_speed_m_s=box[:,7:10].norm(dim=-1),object_angular_speed=box[:,10:13].norm(dim=-1))
    m['stable_support_sample']=(m['ground_support_weight_ratio']>=.8)&(m['box_clearance_m']<.03)&(m['object_speed_m_s']<.08)&(m['object_angular_speed']<.3)
    return m

class UnifiedFailure(FullBodyFailure):
    def __init__(self,cfg,env):
        super().__init__(cfg,env)
        self.support=SupportState(env.num_envs,env.device,**cfg.params)
        self.last_step=torch.full((env.num_envs,),-1,device=env.device,dtype=torch.long)
        self.legacy_unsupported=torch.zeros(env.num_envs,device=env.device)
        self.legacy_acquired=torch.zeros(env.num_envs,device=env.device,dtype=torch.bool)
    def reset(self,env_ids=None):
        ids=slice(None) if env_ids is None else env_ids
        super().reset(env_ids);self.support.reset(ids);self.last_step[ids]=-1
        self.legacy_unsupported[ids]=0;self.legacy_acquired[ids]=False
        if hasattr(self.env,'hoi_metrics'):
            for value in self.env.hoi_metrics.values(): value[ids]=0
    def __call__(self,env,**kwargs):
        if torch.equal(self.last_step,env.episode_length_buf):
            return torch.stack(list(self.causes.values())).any(0)
        env.hoi_metrics_valid=False
        m=box_ground_state(env)
        loss=self.support.update(m,env.dt)
        sim=env.simulator
        if hasattr(sim,'carry_support_required'):
            entering=self.support.required & ~sim.carry_support_required
            sim.carry_gap[entering|~self.support.required]=0
            sim.carry_support_required.copy_(self.support.required)
        root=sim.robot_root_states[:];box=simulator_box_state(env)
        pose=pose_failure_diagnostics(env)
        up=pose['root_up'];root_low=pose['root_too_low'];upside=pose['upside_down']
        lean=pose['deep_lean_without_foot_support'];foot_support=pose['foot_support']
        grace=self.support.age>.1
        self.causes=dict(loss_of_grasp=loss,upside_down=upside,
            separation=(box[:,:3]-root[:,:3]).norm(dim=-1)>.9,
            object_uncontrolled=(m['object_speed_m_s']>5.)|(m['object_angular_speed']>20.),
            severe_floor_penetration=m['box_clearance_m']<-.02,
            nonfinite=~(torch.isfinite(root).all(-1)&torch.isfinite(box).all(-1)&torch.isfinite(sim.dof_pos).all(-1)&torch.isfinite(getattr(sim,'dof_vel',sim.dof_pos)).all(-1)))
        # Old judgments are diagnostic only, including mode-boundary failure.
        self.legacy_unsupported=torch.where(m['bilateral_contact']>.99,0.,self.legacy_unsupported+env.dt)
        mode=env.command_manager.get_state('motion_command').task_mode
        if hasattr(sim.scene,'sensors') and 'box_ground' in sim.scene.sensors:
            last_ground=sim.scene.sensors['box_ground'].data.force_matrix_w[...,2].sum((1,2)).clamp_min(0)/(env.carry_box_mass*9.81)
            last_other=sim.scene.sensors['box_other'].data.force_matrix_w.norm(dim=-1).sum((1,2))
        else:
            last_ground=m['ground_support_weight_ratio'];last_other=m['nonhand_box_contact_n']
        old_sample=(last_ground>=.8)&(m['box_clearance_m']<.03)&(m['object_speed_m_s']<.08)&(m['object_angular_speed']<.3)
        self.legacy_acquired|=(m['bilateral_contact']>.99)&(m['upward_friction_weight_ratio']>=.8)&(m['box_clearance_m']>.03)&(last_other<=.5)
        old_loaded=(mode==1)|((mode==0)&self.legacy_acquired)|((mode==2)&~old_sample)
        m.update(legacy_ground_last_weight_ratio=last_ground,legacy_nonhand_last_n=last_other,
            legacy_grasp_acquired=self.legacy_acquired.float(),root_too_low=root_low.float(),upside_down=upside.float(),
            deep_lean_without_foot_support=lean.float(),foot_support=foot_support.float(),
            nonhand_contact=(m['nonhand_box_contact_n']>.5).float(),
            nonhand_upward_load_proxy=(m['nonhand_upward_force_n']>.5*env.carry_box_mass*9.81).float(),
            legacy_loss_of_grasp=(grace&old_loaded&(self.legacy_unsupported>.02)).float(),
            legacy_fall=(root_low|torch.where(mode==1,up<.5,upside|lean)).float(),
            legacy_body_support=(grace&(last_other>.5)&((mode==1)|~old_sample)).float(),
            legacy_drop=((m['box_clearance_m']<.03)&((mode==1)|((mode==0)&self.legacy_acquired))).float())
        self.unsupported=m['continuous_no_contact_s']
        env.hoi_metrics=m;env.hoi_metrics_valid=True
        self.last_step.copy_(env.episode_length_buf)
        return torch.stack(list(self.causes.values())).any(0)

def phase_grasp(env):
    mode=env.command_manager.get_state('motion_command').task_mode
    return grasp(env)*((mode!=2)|(env.hoi_metrics['stable_support']<.5))
def phase_slip(env):
    mode=env.command_manager.get_state('motion_command').task_mode
    return hand_slip(env)*((mode==1)|((mode==0)&(env.hoi_metrics['grasp_acquired']>.5))|((mode==2)&(env.hoi_metrics['stable_support']<.5)))
def pickup_reward(env):
    # Pre-lift terms do not multiply either clearance or upward friction.
    from holosoma.utils.rotations import quat_rotate_inverse
    mode=env.command_manager.get_state('motion_command').task_mode;m=env.hoi_metrics
    box=simulator_box_state(env);sim=env.simulator
    ids=[sim._robot.body_names.index(s+'_sphere_hand_link') for s in ('left','right')]
    rel=sim._robot.data.body_pos_w[:,ids]-box[:,None,:3]
    local=quat_rotate_inverse(box[:,None,3:7].expand(-1,2,-1).reshape(-1,4),rel.reshape(-1,3),w_last=True).reshape(-1,2,3)
    lower=env.carry_box_vertices.min(0).values;upper=env.carry_box_vertices.max(0).values
    distance=(local-local.clamp(lower,upper)).norm(dim=-1)
    approach=torch.exp(-distance.square()/.10**2).mean(-1)
    force=torch.minimum(m['left_hand_normal_n'],m['right_hand_normal_n'])
    side=torch.exp(-m['normal_vertical_fraction'].square()/.35**2)
    contact=(force/5.).clamp(0,1)*side
    excess=(torch.maximum(m['left_hand_normal_n'],m['right_hand_normal_n'])-45.).clamp_min(0)
    bounded=torch.exp(-excess.square()/30.**2)
    preload=(force/20.).clamp(0,1)*side*bounded
    return (mode==0)*(.3*approach+.3*contact*bounded+.4*preload)

def putdown_reward(env):
    return (env.command_manager.get_state('motion_command').task_mode==2)*(env.hoi_metrics['stable_support']+env.hoi_metrics['putdown_stable_success'])

class UnifiedCarryEnv(Stage1CarryEnv):
    actor_frame_dim=119
    actor_dim=357
    critic_dim=CRITIC_DIM
    def __init__(self,tyro_config,*,device):
        super().__init__(tyro_config,device=device)
        self.critic_dim=actor_frame(self).shape[-1]+critic_reference(self).shape[-1]+critic_support(self).shape[-1]
        if self.critic_dim!=CRITIC_DIM:raise ValueError('Privileged observation contract mismatch')
    def get_video_overlay_text(self,env_id=0):
        mode=int(self.command_manager.get_state('motion_command').task_mode[env_id])
        return 'Mode='+MODES[mode]+' | '+super().get_video_overlay_text(env_id)
    def reset_all(self):
        self.hoi_metrics_valid=False
        if hasattr(self,'hoi_log'):self.hoi_log.clear_active()
        return super().reset_all()
    def _check_termination(self):
        cmd=self.command_manager.get_state('motion_command');cmd.advance_reference_to_post_action()
        FullBodyCarryEnv._check_termination(self)
        if not hasattr(self,'hoi_log'):self.hoi_log=Stage1DiagnosticLog(self.num_envs,self.device);self.hoi_steps={}
        m=self.hoi_metrics;box=simulator_box_state(self);joint=self.action_manager.get_term('joint_control')
        values={k:v.float() for k,v in m.items() if v.ndim==1}
        for i,name in enumerate(self.simulator.carry_other_links):
            force=m['nonhand_link_force_w'][:,i]
            values['nonhand_link/'+name+'/force_n']=force.norm(dim=-1)
            for j,axis in enumerate('xyz'): values['nonhand_link/'+name+'/'+axis+'_n']=force[:,j]
        values.update(robot_error_m=(cmd.robot_body_pos_w-cmd.body_pos_relative_w).norm(dim=-1).mean(-1),
            object_error_m=(box[:,:3]-cmd.object_pos_w).norm(dim=-1),
            object_orientation_error_rad=quat_error_magnitude(box[:,3:7],cmd.object_quat_w,w_last=True),
            joint_hard_limit_violation=((self.simulator.dof_pos<cmd.reference_hard_limits[:,0]-1e-5)|(self.simulator.dof_pos>cmd.reference_hard_limits[:,1]+1e-5)).float().mean(-1),
            joint_acceleration_rms=((joint.dof_vel_substep[:,1:]-joint.dof_vel_substep[:,:-1])/self.sim_dt).square().mean((1,2)).sqrt(),
            torque_clip_fraction=(joint.torques_substep.abs()>=self.torque_limits-1e-5).float().mean((1,2)))
        feet=[self.simulator.body_names.index(s+'_ankle_roll_link') for s in ['left','right']]
        values['foot_sliding_m_s']=(self.simulator._rigid_body_vel[:,feet,:2].norm(dim=-1)*(self.simulator.contact_forces[:,feet,2]>5)).max(-1).values
        for key in ('torque_clip_fraction','joint_hard_limit_violation','joint_acceleration_rms','foot_sliding_m_s'):
            self.hoi_metrics[key]=values[key]
        masks={f'family/{f}':torch.tensor([r['family']==f for r in cmd.rows],device=self.device)[cmd.motion_ids] for f in FAMILIES}
        masks.update({f'phase/{name}':cmd.task_mode==i for i,name in enumerate(MODES)})
        # Phase step counts are exact; complete episode aggregates use family labels only to avoid phase mixing.
        for key,mask in masks.items():
            self.hoi_steps[key]=self.hoi_steps.get(key,0)+int(mask.sum())
            self.log_dict['hoi/observed_steps/'+key]=torch.tensor(float(self.hoi_steps[key]),device=self.device)
            if key.startswith('family/'):
                complete=mask&self.reset_buf.bool();name='completed/'+key
                self.hoi_steps[name]=self.hoi_steps.get(name,0)+int(self.episode_length_buf[complete].sum())
                self.log_dict['hoi/completed_episode_steps/'+key]=torch.tensor(float(self.hoi_steps[name]),device=self.device)
            if mask.any():
                for name,value in values.items():self.log_dict['hoi/'+key+'/'+name]=value[mask].mean()
                for term,result in self.termination_manager.last_term_results.items():self.log_dict['hoi/'+key+'/termination/'+term]=result[mask].float().mean()
                for term,causes in self.termination_manager.last_term_breakdowns.items():
                    for cause,result in causes.items():self.log_dict['hoi/'+key+'/termination/'+term+'/'+cause]=result[mask].float().mean()
        # One deterministic first failure label per completed episode; breakdowns
        # above still retain overlapping causes. Clip-end is not physical success.
        remaining=self.reset_buf.bool() & self.termination_manager.terminated
        for term,causes in self.termination_manager.last_term_breakdowns.items():
            for cause,result in causes.items():
                first=remaining & result
                for label,mask in masks.items():
                    self.log_dict['hoi/'+label+'/first_failure/'+term+'/'+cause]=first[mask & self.reset_buf.bool()].float().mean() if (mask & self.reset_buf.bool()).any() else torch.zeros((),device=self.device)
                remaining=remaining & ~first
        for label,mask in (('frame0',cmd.reset_start_frame==0),('rsi',cmd.reset_start_frame!=0)):
            ended=mask & self.reset_buf.bool()
            count='completed_'+label;reached='clip_end_'+label
            self.hoi_steps[count]=self.hoi_steps.get(count,0)+int(ended.sum())
            self.hoi_steps[reached]=self.hoi_steps.get(reached,0)+int((ended & self.time_out_buf).sum())
            self.log_dict['hoi/'+label+'/completed_episodes']=torch.tensor(float(self.hoi_steps[count]),device=self.device)
            self.log_dict['hoi/'+label+'/reference_end_rate']=torch.tensor(self.hoi_steps[reached]/max(1,self.hoi_steps[count]),device=self.device)
        self.log_dict.update(self.hoi_log.observe({k:v for k,v in masks.items() if k.startswith('family/')},values,
            self.episode_length_buf*self.dt,self.reset_buf.bool(),self.termination_manager.last_term_results))
    def task_contract(self):
        from dataclasses import asdict
        # Store resolved control/reward/termination/sampling contracts, not just a HEAD.
        return dict(protocol=PROTOCOL,actor_dim=self.actor_dim,critic_dim=self.critic_dim,
            physics=self.fullbody_physics,p_gains=self.p_gains.tolist(),d_gains=self.d_gains.tolist(),
            action_scales=self.action_scales.tolist(),
            reward=json.loads(json.dumps(asdict(self.reward_manager.cfg),default=str)),
            termination=json.loads(json.dumps(asdict(self.termination_manager.cfg),default=str)),
            action=json.loads(json.dumps(asdict(self.action_manager.cfg),default=str)),
            sampling=json.loads(json.dumps(asdict(self.command_manager.get_state('motion_command').motion_cfg),default=str)),
            support=self.termination_manager._term_instances['physical_failure'].support.settings)
    def get_checkpoint_state(self):
        state=super().get_checkpoint_state();state.update(unified_schema=2,actor_dim=self.actor_dim,critic_dim=self.critic_dim,
            support_protocol=PROTOCOL,task_contract=self.task_contract())
        return state
    def load_checkpoint_state(self,state):
        if state and (state.get('unified_schema')!=2 or state.get('task_contract')!=self.task_contract()):raise ValueError('Unified HOI must start from scratch or resume a matching unified checkpoint')
        super().load_checkpoint_state(state)
