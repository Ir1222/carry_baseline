"""Reference-free joint-position action decoding shared by imitation and goal RL."""
from holosoma.managers.action.terms.joint_control import JointPositionActionTerm

FIXED='fixed_default_v1'
DELTA='joint_delta_v1'


def position_target(actions,current_joint_pos,default_joint_pos,action_scales,parameterization):
    if parameterization not in (FIXED,DELTA):raise ValueError('Unknown carry action parameterization')
    center=current_joint_pos if parameterization==DELTA else default_joint_pos
    return center+actions*action_scales


class JointDeltaPositionActionTerm(JointPositionActionTerm):
    """Sample q at policy time, hold q+scale*a through all 20 PD substeps.

    No motion, phase, goal, Track/Gen flag, or default-pose switching is used.
    Gains, effort-based scales, torque limits and torque clipping are inherited.
    """
    parameterization=DELTA

    def __init__(self,cfg,env):
        super().__init__(cfg,env)
        self.position_center=env.simulator.dof_pos.clone()

    def process_actions(self,actions):
        self.position_center.copy_(self.env.simulator.dof_pos)
        super().process_actions(actions)

    def _position_action_center(self):
        return self.position_center
