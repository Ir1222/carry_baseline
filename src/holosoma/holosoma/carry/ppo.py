"""Same HMI shared PPO; export only the physical-observation actor."""
from pathlib import Path
import json
import os
import tempfile
from holosoma.agents.ppo.ppo import PPO
from holosoma.utils.inference_helpers import export_policy_as_onnx, attach_onnx_metadata


class CarryPPO(PPO):
    def save(self, path, infos=None):
        from holosoma.carry.checkpoints import atomic_save
        original = self.logging_helper.save_checkpoint_artifact
        self.logging_helper.save_checkpoint_artifact = atomic_save
        try:
            super().save(path, infos)
        finally:
            self.logging_helper.save_checkpoint_artifact = original

    def load(self, ckpt_path):
        if ckpt_path is None:
            return None
        from holosoma.carry.checkpoints import validate
        validate(ckpt_path)
        result = super().load(ckpt_path)
        # Upstream stores the last completed index, then restarts that index.
        self.current_learning_iteration += 1
        return result

    def export(self, onnx_file_path):
        from holosoma.carry.checkpoints import atomic_json, digest, validate_export
        final = Path(onnx_file_path)
        fd, temporary = tempfile.mkstemp(prefix='.'+final.stem, suffix='.onnx', dir=final.parent)
        os.close(fd)
        try:
            self._export_actor(temporary)
            validate_export(temporary)
            os.replace(temporary, final)
            os.replace(Path(temporary).with_suffix('.actor.json'), final.with_suffix('.actor.json'))
            atomic_json(final.with_suffix('.export.json'), dict(onnx_sha256=digest(final),
                metadata_sha256=digest(final.with_suffix('.actor.json'))))
        finally:
            for path in (Path(temporary),Path(temporary).with_suffix('.actor.json')):
                path.unlink(missing_ok=True)

    def _export_actor(self, onnx_file_path):
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
