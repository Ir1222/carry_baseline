"""Real physical failures, with geometric box clearance valid through squatting."""
import torch
from holosoma.managers.termination.base import TerminationTermBase
from holosoma.carry.observations import simulator_box_state
from holosoma.carry.fullbody_rewards import box_bottom,physical_metrics
from holosoma.utils.rotations import quaternion_to_matrix


def pose_failure_diagnostics(env):
    """Absolute pose checks; Unified Stage1 only terminates obvious inversion."""
    sim=env.simulator;root=sim.robot_root_states[:]
    up=quaternion_to_matrix(root[:,3:7],w_last=True)[:,2,2]
    feet=[sim.body_names.index(side+'_ankle_roll_link') for side in ('left','right')]
    foot_support=(sim.contact_forces[:,feet,2]>5).all(-1)
    return dict(root_up=up,root_too_low=root[:,2]-sim.scene.env_origins[:,2]<.45,
        upside_down=up<0,deep_lean_without_foot_support=(up<.5)&~foot_support,
        foot_support=foot_support)


class FullBodyFailure(TerminationTermBase):
    # Legacy FullBody-only experiment. UnifiedFailure overrides __call__ completely.
    def __init__(self,cfg,env):
        super().__init__(cfg,env)
        self.unsupported=torch.zeros(env.num_envs,device=env.device)
        self.causes={}

    def reset(self,env_ids=None):
        if env_ids is None:self.unsupported.zero_()
        else:self.unsupported[env_ids]=0

    def __call__(self,env,**_):
        root=env.simulator.robot_root_states[:];box=simulator_box_state(env)
        ground=env.simulator.scene.env_origins[:,2]
        m=physical_metrics(env)
        self.unsupported=torch.where(m['bilateral_contact']>.99,0.,self.unsupported+env.dt)
        grace=env.episode_length_buf*env.dt > .1
        self.causes=dict(fall=(root[:,2]-ground<.45)|(quaternion_to_matrix(root[:,3:7],w_last=True)[:,2,2]<.5),
            drop=box_bottom(env)<.03,
            separation=torch.linalg.vector_norm(box[:,:3]-root[:,:3],dim=-1)>.9,
            loss_of_grasp=grace & (self.unsupported>.02),
            body_support=grace & (m['nonhand_box_contact_n']>.5),
            nonfinite=~(torch.isfinite(root).all(-1)&torch.isfinite(box).all(-1)&torch.isfinite(env.simulator.dof_pos).all(-1)))
        return torch.stack(list(self.causes.values())).any(0)

    def get_last_breakdown(self):return self.causes
