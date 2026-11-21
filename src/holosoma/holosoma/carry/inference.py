"""ONNX actor deployment: physical tensors plus four commands, no simulator/reference imports."""
import json
from pathlib import Path
import numpy as np
import onnxruntime as ort
import torch
from holosoma.carry.observations import physical_frame, FRAME_DIM, HISTORY_LENGTH


class CarryActor:
    def __init__(self, policy, num_envs=1, device="cpu"):
        policy = Path(policy)
        self.metadata = json.loads(policy.with_suffix(".actor.json").read_text())
        if self.metadata["carry_schema_version"] != 1:
            raise ValueError("Unsupported carry actor schema")
        self.session = ort.InferenceSession(str(policy), providers=["CPUExecutionProvider"])
        inputs = self.session.get_inputs()
        if len(inputs) != 1 or inputs[0].name != "actor_obs":
            raise ValueError("Expected a policy-only physical-observation ONNX actor")
        self.default_joint_pos = torch.tensor(self.metadata["default_joint_pos"], device=device)
        self.history = torch.zeros(num_envs, HISTORY_LENGTH, FRAME_DIM, device=device)
        self.previous_action = torch.zeros(num_envs, 29, device=device)

    def reset(self, env_ids=None):
        if env_ids is None:
            self.history.zero_(); self.previous_action.zero_()
        else:
            self.history[env_ids] = 0; self.previous_action[env_ids] = 0

    def joint_position_target(self,actions,current_joint_pos):
        # Tensor-only deployment decoding; no Reference Loader is needed.
        mode=self.metadata.get('action_parameterization','fixed_default_v1')
        if mode not in ('fixed_default_v1','joint_delta_v1'):raise ValueError('Unknown carry action parameterization')
        center=current_joint_pos if mode=='joint_delta_v1' else self.default_joint_pos
        scale=torch.as_tensor(self.metadata['action_scales'],device=current_joint_pos.device)
        limit=self.metadata.get('action_clip_value',100.)
        return center+actions.clamp(-limit,limit)*scale

    def act(self, root_xyzw, joint_pos, joint_vel, box_xyzw, commands, ground_height):
        frame = physical_frame(root_xyzw, joint_pos, joint_vel, self.default_joint_pos,
            self.previous_action, box_xyzw, commands, ground_height).clamp(-100, 100)
        self.history[:, :-1] = self.history[:, 1:].clone()
        self.history[:, -1] = frame
        obs = self.history.flatten(1).detach().cpu().numpy().astype(np.float32)
        # HMI exports a fixed batch of one. Iterate for small evaluation batches.
        actions = np.concatenate([self.session.run(["action"], {"actor_obs": row[None]})[0] for row in obs])
        self.previous_action = torch.as_tensor(actions, device=joint_pos.device)
        return self.previous_action
