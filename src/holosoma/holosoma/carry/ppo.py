"""Same HMI shared PPO; export only the physical-observation actor."""
from pathlib import Path
import json
from holosoma.agents.ppo.ppo import PPO
from holosoma.utils.inference_helpers import export_policy_as_onnx, attach_onnx_metadata


class CarryPPO(PPO):
    def export(self, onnx_file_path):
        was_training = self.actor.training
        self._eval_mode()
        export_policy_as_onnx(self.actor_onnx_wrapper, onnx_file_path,
                             {"actor_obs": self._get_zero_input()})
        metadata = {"carry_schema_version": 1, "commands": ["vx", "vy", "yaw_rate", "pelvis_height"],
                    "command_units": ["m/s", "m/s", "rad/s", "m"],
                    "frame_dim": 116, "history_length": 3, "history_order": "oldest_first_zero_padded",
                    "quaternion_order": "xyzw", "joint_names": self.env.simulator.dof_names,
                    "default_joint_pos": self.env.default_dof_pos[0].tolist(),
                    "action_scales": self.env.action_scales.tolist(), "control_dt": self.env.dt,
                    "p_gains": self.env.p_gains.tolist(), "d_gains": self.env.d_gains.tolist()}
        attach_onnx_metadata(onnx_file_path, metadata)
        Path(onnx_file_path).with_suffix(".actor.json").write_text(json.dumps(metadata, indent=2))
        self.logging_helper.save_to_wandb(onnx_file_path)
        if was_training:
            self._train_mode()
