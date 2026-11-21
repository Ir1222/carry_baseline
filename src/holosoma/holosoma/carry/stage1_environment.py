"""Stage1 reset returns the initial observation before applying the first policy action."""
import torch
from holosoma.carry.fullbody_environment import FullBodyCarryEnv


class Stage1CarryEnv(FullBodyCarryEnv):
    def __init__(self,tyro_config,*,device):
        from pathlib import Path
        self.stage1_diagnostic_dir=Path(tyro_config.logger.base_dir)/'stage1_failures'
        super().__init__(tyro_config,device=device)

    def _check_termination(self):
        self.command_manager.get_state('motion_command').advance_reference_to_post_action()
        super()._check_termination()
        from holosoma.carry.stage1_diagnostics import record_stage1_diagnostics
        record_stage1_diagnostics(self)

    def get_checkpoint_state(self):
        state=super().get_checkpoint_state()
        state['stage1_reference_protocol']='hard_reset_post_action_v1'
        state['stage1_action_parameterization']=getattr(self.action_manager.get_term('joint_control'),'parameterization','fixed_default_v1')
        return state

    def load_checkpoint_state(self,state):
        if state and state.get('stage1_reference_protocol')!='hard_reset_post_action_v1':
            raise ValueError('Stage1 checkpoint uses the old reset/reference timing protocol; start this experiment from scratch')
        mode=getattr(self.action_manager.get_term('joint_control'),'parameterization','fixed_default_v1')
        if state and state.get('stage1_action_parameterization')!=mode:raise ValueError('Checkpoint action parameterization differs')
        super().load_checkpoint_state(state)

    def reset_all(self):
        # BaseTask.reset_all() integrates one 20ms zero-action step. Normal
        # per-episode resets return the freshly initialized state without that
        # step. Grasping must use the same first-action timing in both cases.
        command=self.command_manager.get_state('motion_command')
        if hasattr(self,'stage1_diagnostics'):self.stage1_diagnostics.clear_active()
        command.init_buffers()
        ids=torch.arange(self.num_envs,device=self.device)
        self.reset_envs_idx(ids)
        self._refresh_envs_after_reset(ids)
        self._update_tasks_callback()
        self._compute_observations()
        self._post_compute_observations_callback()
        self._clip_observations()
        return self.obs_buf_dict
