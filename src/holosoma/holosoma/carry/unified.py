"""One Track-only HOI task; mode is an intention, never a motion identifier."""
import json,os
from pathlib import Path
import torch
from holosoma.carry.stage1_command import Stage1TrackCommand
from holosoma.carry.fullbody_command import FullBodyCommand
from holosoma.carry.fullbody_environment import FullBodyCarryEnv
from holosoma.carry.stage1_environment import Stage1CarryEnv
from holosoma.carry.fullbody_termination import FullBodyFailure
from holosoma.carry.observations import actor_frame as carry_frame,critic_reference,simulator_box_state
from holosoma.carry.fullbody_rewards import physical_metrics,grasp,hand_slip
from holosoma.carry.stage1_diagnostics import Stage1DiagnosticLog
from holosoma.utils.rotations import quaternion_to_matrix,quat_error_magnitude

MODES=('pickup','carry','putdown')
FAMILIES=('full_sequence','loaded_locomotion','loaded_squat_stand')
FRAME_DIM=119
ACTOR_DIM=357
CRITIC_DIM=187

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
        super().init_buffers();self.task_mode=torch.zeros(self.num_envs,device=self.device,dtype=torch.long)

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

    def _sample_adaptive_reset_states(self,ids,groups):
        self._sample_motion_ids_for_reset(ids);mids=self.motion_ids[ids].clone();bins=torch.empty_like(mids);times=torch.empty_like(mids)
        for motion,row in enumerate(self.rows):
            mask=mids==motion;n=int(mask.sum())
            if not n:continue
            _,b,t=self.adaptive_timesteps_sampler.sample_from_motion_pool(0,torch.tensor([motion],device=self.device),n)
            # Full episodes plus balanced task-mode starts prevent pickup/release starvation.
            if row['family']=='full_sequence':
                modes=torch.randint(3,(n,),device=self.device);phase=self.phase_bank[self.eligible[motion]]
                for mode in range(3):
                    pool=self.eligible[motion][phase==mode];sub=modes==mode
                    if sub.any() and len(pool):t[sub]=pool[torch.randint(len(pool),(int(sub.sum()),),device=self.device)]
            else:
                valid=torch.isin(t,self.eligible[motion]);t[~valid]=self.eligible[motion][0]
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

def box_ground_state(env):
    m=physical_metrics(env);box=simulator_box_state(env)
    ground=env.simulator.scene.sensors['box_ground'].data.force_matrix_w[...,2].sum((1,2)).clamp_min(0)
    m.update(ground_support_weight_ratio=ground/(env.carry_box_mass*9.81),object_speed_m_s=box[:,7:10].norm(dim=-1),object_angular_speed=box[:,10:13].norm(dim=-1))
    m['stable_support_sample']=(m['ground_support_weight_ratio']>=.8)&(m['box_clearance_m']<.03)&(m['object_speed_m_s']<.08)&(m['object_angular_speed']<.3)
    return m

class UnifiedFailure(FullBodyFailure):
    def __init__(self,cfg,env):
        super().__init__(cfg,env);self.acquired=torch.zeros(env.num_envs,device=env.device,dtype=torch.bool)
        self.support_time=torch.zeros(env.num_envs,device=env.device);self.release_time=torch.zeros_like(self.support_time)
    def reset(self,env_ids=None):
        super().reset(env_ids);ids=slice(None) if env_ids is None else env_ids
        self.acquired[ids]=False;self.support_time[ids]=0;self.release_time[ids]=0
    def __call__(self,env,**kwargs):
        super().__call__(env,**kwargs);m=box_ground_state(env);mode=env.command_manager.get_state('motion_command').task_mode
        for name in ('fall','drop','loss_of_grasp','body_support'):
            m['raw_carry_'+name+'_flag']=self.causes[name].float()
        acquired=(m['bilateral_contact']>.99)&(m['upward_friction_weight_ratio']>=.8)&(m['box_clearance_m']>.03)&(m['nonhand_box_contact_n']<=.5)
        self.acquired|=acquired
        self.support_time=torch.where(m['stable_support_sample'],self.support_time+env.dt,0.)
        stable=self.support_time>=.2
        released=(m['left_hand_normal_n']<.5)&(m['right_hand_normal_n']<.5)
        self.release_time=torch.where(stable&released&(m['nonhand_box_contact_n']<=.5),self.release_time+env.dt,0.)
        # Carry keeps every old gate. Pickup pre-contact and genuinely supported putdown are different tasks.
        loaded=(mode==1)|((mode==0)&self.acquired)|((mode==2)&~m['stable_support_sample'])
        root=env.simulator.robot_root_states[:];up=quaternion_to_matrix(root[:,3:7],w_last=True)[:,2,2]
        feet=[env.simulator.body_names.index(s+'_ankle_roll_link') for s in ['left','right']]
        feet_support=(env.simulator.contact_forces[:,feet,2]>5).all(-1)
        ground=env.simulator.scene.env_origins[:,2]
        noncarry_fall=(root[:,2]-ground<.45)|(up<0)|((up<.5)&~feet_support)
        self.causes['fall']=torch.where(mode==1,self.causes['fall'],noncarry_fall)
        # Incidental contact with a supported stationary box is penalized, but is
        # not load-bearing body support. Never exempt it during loaded carry.
        self.causes['body_support'] &= (mode==1)|~m['stable_support_sample']
        self.causes['loss_of_grasp'] &= loaded
        self.causes['drop'] &= (mode==1)|((mode==0)&self.acquired)
        self.causes['severe_floor_penetration']=m['box_clearance_m']<-.02
        m.update(grasp_acquired=self.acquired.float(),stable_support=stable.float(),released=released.float(),
            foot_support=feet_support.float(),raw_undesired_contact=(m['nonhand_box_contact_n']>.5).float(),
            release_stable_s=self.release_time,putdown_stable_success=((mode==2)&(self.release_time>=.5)).float())
        env.hoi_metrics=m
        return torch.stack(list(self.causes.values())).any(0)

def phase_grasp(env):
    mode=env.command_manager.get_state('motion_command').task_mode
    return grasp(env)*((mode!=2)|(env.hoi_metrics['stable_support']<.5))
def phase_slip(env):
    mode=env.command_manager.get_state('motion_command').task_mode
    return hand_slip(env)*((mode==1)|((mode==0)&(env.hoi_metrics['grasp_acquired']>.5))|((mode==2)&(env.hoi_metrics['stable_support']<.5)))
def pickup_reward(env):
    mode=env.command_manager.get_state('motion_command').task_mode;m=env.hoi_metrics
    return (mode==0)*m['grasp_acquired']*(m['box_clearance_m']/.15).clamp(0,1)*(m['nonhand_box_contact_n']<=.5)
def putdown_reward(env):
    return (env.command_manager.get_state('motion_command').task_mode==2)*(env.hoi_metrics['stable_support']+env.hoi_metrics['putdown_stable_success'])

class UnifiedCarryEnv(Stage1CarryEnv):
    actor_frame_dim=119
    actor_dim=357
    critic_dim=187
    def get_video_overlay_text(self,env_id=0):
        mode=int(self.command_manager.get_state('motion_command').task_mode[env_id])
        return 'Mode='+MODES[mode]+' | '+super().get_video_overlay_text(env_id)
    def reset_all(self):
        if hasattr(self,'hoi_log'):self.hoi_log.clear_active()
        return super().reset_all()
    def _check_termination(self):
        cmd=self.command_manager.get_state('motion_command');cmd.advance_reference_to_post_action()
        FullBodyCarryEnv._check_termination(self)
        if not hasattr(self,'hoi_log'):self.hoi_log=Stage1DiagnosticLog(self.num_envs,self.device);self.hoi_steps={}
        m=self.hoi_metrics;box=simulator_box_state(self);joint=self.action_manager.get_term('joint_control')
        values={k:v.float() for k,v in m.items() if v.ndim==1}
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
        self.log_dict.update(self.hoi_log.observe({k:v for k,v in masks.items() if k.startswith('family/')},values,
            self.episode_length_buf*self.dt,self.reset_buf.bool(),self.termination_manager.last_term_results))
    def get_checkpoint_state(self):
        state=super().get_checkpoint_state();state.update(unified_schema=1,actor_dim=357,critic_dim=187)
        return state
    def load_checkpoint_state(self,state):
        if state and state.get('unified_schema')!=1:raise ValueError('Unified HOI must start from scratch or resume a matching unified checkpoint')
        super().load_checkpoint_state(state)
