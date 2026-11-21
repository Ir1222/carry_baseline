"""Pre-reset, per-family measurements. These buffers never affect task decisions."""
import torch


class Stage1DiagnosticLog:
    def __init__(self,num_envs,device):
        self.num_envs=num_envs;self.device=device
        self.steps=torch.zeros(num_envs,device=device)
        self.sums={};self.totals={}

    def clear_active(self):
        self.steps.zero_()
        for value in self.sums.values():value.zero_()

    @torch.no_grad()
    def observe(self,family_masks,values,duration,ended,causes):
        self.steps+=1
        for key,value in values.items():
            if key not in self.sums:self.sums[key]=torch.zeros_like(value)
            self.sums[key]+=value
        logs={}
        for family,mask in family_masks.items():
            prefix='stage1/'+family+'/'
            if mask.any():
                for key,value in values.items():logs[prefix+'step/'+key]=value[mask].mean()
                for cause,value in causes.items():logs[prefix+'step/termination/'+cause]=value[mask].float().mean()
            finished=mask & ended
            total=self.totals.setdefault(family,{})
            additions={'episodes':finished.float().sum(),'episode_length_s':duration[finished].sum(),
                'early_exit_le_0p2':(duration[finished]<=.2).float().sum()}
            additions.update({key:(value[finished]/self.steps[finished].clamp_min(1)).sum() for key,value in self.sums.items()})
            additions.update({'termination/'+key:value[finished].float().sum() for key,value in causes.items()})
            for key,value in additions.items():
                total[key]=total.get(key,torch.zeros((),device=self.device))+value
            count=total['episodes']
            logs[prefix+'completed_episodes']=count.clone()
            for key,value in total.items():
                if key!='episodes':logs[prefix+'completed/'+key]=value/count.clamp_min(1)
        self.steps[ended]=0
        for value in self.sums.values():value[ended]=0
        return logs


@torch.no_grad()
def record_stage1_diagnostics(env):
    from holosoma.carry.fullbody_rewards import physical_metrics
    from holosoma.carry.observations import simulator_box_state
    cmd=env.command_manager.get_state('motion_command')
    if not hasattr(env,'stage1_diagnostics'):
        env.stage1_diagnostics=Stage1DiagnosticLog(env.num_envs,env.device)
    rows=sorted(cmd.manifest['motions'],key=lambda r:r['name'])
    families={name:torch.isin(cmd.motion_ids,torch.tensor([i for i,row in enumerate(rows) if row['family']==name],device=env.device))
        for name in ('squat_stand','forward_carry')}
    metrics=physical_metrics(env);joint=env.action_manager.get_term('joint_control')
    torque_fraction=(joint.torques_substep.abs()>=env.torque_limits-1e-5).float().mean((1,2))
    values=dict(robot_tracking_error_m=(cmd.robot_body_pos_w-cmd.body_pos_relative_w).norm(dim=-1).mean(-1),
        object_tracking_error_m=(cmd.object_pos_w-simulator_box_state(env)[:,:3]).norm(dim=-1),
        contact_continuity=metrics['bilateral_contact'],hand_slip_speed_m_s=metrics['hand_slip_speed_m_s'],
        torque_clip_fraction=torque_fraction,
        left_hand_normal_n=metrics['left_hand_normal_n'],right_hand_normal_n=metrics['right_hand_normal_n'])
    causes={name:value for name,value in env.termination_manager.last_term_results.items()}
    causes.update({term+'/'+cause:value for term,items in env.termination_manager.last_term_breakdowns.items() for cause,value in items.items()})
    env.log_dict.update(env.stage1_diagnostics.observe(families,values,env.episode_length_buf*env.dt,
        env.reset_buf.bool(),causes))
