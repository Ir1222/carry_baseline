"""Carry-specific lifecycle and checkpoint state on the upstream WBT environment."""
from holosoma.envs.wbt.wbt_manager import WholeBodyTrackingManager
import torch


class CarryEnv(WholeBodyTrackingManager):
    def get_video_overlay_text(self, env_id=0):
        command = self.command_manager.get_state("motion_command").task_command[env_id].tolist()
        return "Carry vx={:.2f} vy={:.2f} yaw={:.2f} height={:.3f}".format(*command)

    def _draw_debug_vis(self):
        # Upstream overlays show reference/terminal-goal objects. Carry viewers
        # display the actual robot/box and the four-command text overlay.
        pass

    def _configure_default_dof_pos(self):
        super()._configure_default_dof_pos()
        command = self.command_manager.get_state("motion_command")
        pose = command.reset_pose
        if pose["joint_names"] != self.simulator.dof_names:
            raise ValueError("Verified reset joint order does not match the simulator")
        self.default_dof_pos_base = torch.tensor(pose["pd_target_joint_pos"], device=self.device).unsqueeze(0)
        self.default_dof_pos = self.default_dof_pos_base.repeat(self.num_envs, 1).clone()

    def _check_termination(self):
        super()._check_termination()
        # Failure wins over coincident time limit: no bootstrap from failed state.
        failures = self.termination_manager.last_term_results
        for name in ("physical_failure", "track_failure", "body_proximity"):
            if name in failures:
                self.time_out_buf[failures[name]] = False

    def get_checkpoint_state(self):
        command = self.command_manager.get_state("motion_command")
        return {"carry_schema_version": 1, "carry_level": command.carry_level,
                "carry_curriculum_episodes": command.curriculum_episodes,
                "carry_curriculum_successes": command.curriculum_successes}

    def load_checkpoint_state(self, state):
        if not state:
            return
        if state.get("carry_schema_version") != 1:
            raise ValueError("Incompatible carry checkpoint schema")
        command = self.command_manager.get_state("motion_command")
        command.carry_level = int(state["carry_level"])
        command.curriculum_episodes = int(state.get("carry_curriculum_episodes", 0))
        command.curriculum_successes = int(state.get("carry_curriculum_successes", 0))
