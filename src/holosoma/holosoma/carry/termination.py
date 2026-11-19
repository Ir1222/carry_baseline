"""Physical failures in both groups, tracking failures only in Track."""
import torch
from holosoma.managers.termination.base import TerminationTermBase
from holosoma.managers.termination.terms.wbt import BadTrackingZOnly
from holosoma.carry.observations import simulator_box_state
from holosoma.utils.rotations import quaternion_to_matrix


def clip_timeout(env):
    command = env.command_manager.get_state("motion_command")
    return command.track_env_mask & (command.time_steps >= command.motion.motion_end_idx[command.motion_ids]-1)


class TrackFailure(BadTrackingZOnly):
    def __call__(self, env, **kwargs):
        failure = super().__call__(env, **kwargs)
        return failure & env.command_manager.get_state("motion_command").track_env_mask


class CarryFailure(TerminationTermBase):
    def __init__(self, cfg, env):
        super().__init__(cfg, env)
        self.unsupported = torch.zeros(env.num_envs, device=env.device)
        self.causes = {}

    def reset(self, env_ids=None):
        self.unsupported[:] = 0 if env_ids is None else self.unsupported
        if env_ids is not None:
            self.unsupported[env_ids] = 0

    def __call__(self, env, **kwargs):
        root = env.simulator.robot_root_states[:]
        box = simulator_box_state(env)
        ground = env.simulator.scene.env_origins[:, 2]
        forces = env.simulator.hand_box_forces()
        both = (torch.linalg.vector_norm(forces, dim=-1) > .5).all(-1)
        self.unsupported = torch.where(both, 0., self.unsupported+env.dt)
        grace_over = env.episode_length_buf*env.dt > .3
        tilt = quaternion_to_matrix(root[:, 3:7], w_last=True)[:, 2, 2]
        box_tilt = quaternion_to_matrix(box[:, 3:7], w_last=True)[:, 2, 2].abs()
        self.causes = {
            "fall": (root[:, 2]-ground < .45) | (tilt < .5),
            "drop": (box[:, 2]-ground < .35) | (box[:, 2] < root[:, 2]-.3),
            "separation": torch.linalg.vector_norm(box[:, :3]-root[:, :3], dim=-1) > 1.,
            "loss_of_support": grace_over & (self.unsupported > .35),
            "box_instability": grace_over & ((box_tilt < .5) |
                (torch.linalg.vector_norm(box[:, 10:13], dim=-1) > 8.)),
            "nonfinite": ~(torch.isfinite(root).all(-1) & torch.isfinite(box).all(-1)),
        }
        return torch.stack(list(self.causes.values())).any(0)

    def get_last_breakdown(self):
        return self.causes
