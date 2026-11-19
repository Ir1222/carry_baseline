"""Simulation deployment command: one static reset state, no reference motion loader."""
import json
from pathlib import Path
import torch
from holosoma.managers.command.base import CommandTermBase
from holosoma.carry.sampling import smooth_commands


class DeploymentCommand(CommandTermBase):
    def __init__(self, cfg, env):
        super().__init__(cfg, env)
        self.reset_pose = json.loads(Path(cfg.params["reset_pose_file"]).read_text())
        if not self.reset_pose.get("physics_verified"):
            raise ValueError("Deployment requires the verified static carry reset")
        self.carry_level = self.curriculum_episodes = self.curriculum_successes = 0

    def setup(self):
        self.num_envs, self.device = self.env.num_envs, self.env.device
        self.metrics = {}
        self.init_buffers()

    def init_buffers(self):
        self.track_env_mask = torch.zeros(self.num_envs, device=self.device, dtype=torch.bool)
        self.gen_env_mask = ~self.track_env_mask
        self.task_command = torch.zeros(self.num_envs, 4, device=self.device)
        self.task_command[:, 3] = .735
        self.start = self.task_command.clone()
        self.target = self.task_command.clone()
        self.elapsed = torch.zeros(self.num_envs, device=self.device)

    def reset(self, env_ids):
        ids = torch.arange(self.num_envs, device=self.device) if env_ids is None else env_ids.long()
        if not len(ids):
            return
        sim = self.env.simulator
        root = torch.tensor(self.reset_pose["root_xyzw"], device=self.device).repeat(len(ids), 1)
        box = torch.tensor(self.reset_pose["box_xyzw"], device=self.device).repeat(len(ids), 1)
        root[:, :3] += sim.scene.env_origins[ids]
        box[:, :3] += sim.scene.env_origins[ids]
        root[:, 7:] = 0; box[:, 7:] = 0
        sim.robot_root_states[ids] = root
        sim.dof_pos[ids] = torch.tensor(self.reset_pose["joint_pos"], device=self.device)
        sim.dof_vel[ids] = 0
        sim.set_actor_states(["object"], ids, box)
        self.task_command[ids] = 0; self.task_command[ids, 3] = .735
        self.start[ids] = self.task_command[ids]
        self.elapsed[ids] = 0

    def set_command(self, command, env_ids=None):
        ids = torch.arange(self.num_envs, device=self.device) if env_ids is None else env_ids.long()
        value = torch.as_tensor(command, device=self.device, dtype=torch.float32)
        if value.shape == (4,):
            value = value.expand(len(ids), -1)
        if value.shape != (len(ids), 4) or not torch.isfinite(value).all():
            raise ValueError("Commands must be finite [N,4] in SI units")
        self.start[ids] = self.task_command[ids]
        self.target[ids] = value
        self.elapsed[ids] = 0

    def step(self):
        self.elapsed += self.env.dt
        self.task_command[:] = smooth_commands(self.start, self.target, self.elapsed)

    def update_metrics(self):
        from holosoma.carry.rewards import task_errors, contact_quality
        error = task_errors(self.env)
        self.metrics = {f"carry/error_{name}": error[:, i].abs()
            for i, name in enumerate(("vx", "vy", "yaw_rate", "pelvis_height"))}
        self.metrics["carry/contact_quality"] = contact_quality(self.env)
