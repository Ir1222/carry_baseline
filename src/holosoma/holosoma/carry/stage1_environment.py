"""Stage1 reset returns the initial observation before applying the first policy action."""
import torch
from holosoma.carry.fullbody_environment import FullBodyCarryEnv


class Stage1CarryEnv(FullBodyCarryEnv):
    def reset_all(self):
        # BaseTask.reset_all() integrates one 20ms zero-action step. Normal
        # per-episode resets return the freshly initialized state without that
        # step. Grasping must use the same first-action timing in both cases.
        command=self.command_manager.get_state('motion_command')
        command.init_buffers()
        ids=torch.arange(self.num_envs,device=self.device)
        self.reset_envs_idx(ids)
        self._refresh_envs_after_reset(ids)
        self._update_tasks_callback()
        self._compute_observations()
        self._post_compute_observations_callback()
        self._clip_observations()
        return self.obs_buf_dict
