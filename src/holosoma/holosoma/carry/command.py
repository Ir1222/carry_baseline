"""Hybrid imitation with reference-free external commands and continuous Gen time."""
import torch
from holosoma.managers.command.terms.wbt import HybridMotionCommand, MotionCommand
from holosoma.utils.rotations import quat_apply, quat_inverse, quat_mul, quat_rotate_inverse, yaw_quat
from holosoma.carry.sampling import sample_commands, smooth_commands


class CarryCommand(HybridMotionCommand):
    def __init__(self, cfg, env):
        super().__init__(cfg, env)
        self.carry_level = int(cfg.params.get("curriculum_level", 0))
        self.hold_frame = int(cfg.params.get("hold_frame", 5))
        self.curriculum_episodes = 0
        self.curriculum_successes = 0

    def init_buffers(self):
        super().init_buffers()
        self.task_command = torch.zeros(self.num_envs, 4, device=self.device)
        self.task_command[:, 3] = 0.735
        self.command_start = self.task_command.clone()
        self.command_target = self.task_command.clone()
        self.command_elapsed = torch.zeros(self.num_envs, device=self.device)
        self.dwell_remaining = torch.zeros(self.num_envs, device=self.device)
        self.external_command = torch.zeros(self.num_envs, dtype=torch.bool, device=self.device)
        self.episode_control_steps = torch.zeros(self.num_envs, device=self.device)
        self.episode_good_steps = torch.zeros(self.num_envs, device=self.device)

    def _on_goal_time_steps_updated(self, env_ids):
        # Upstream terminal goals are deliberately inert in this task.
        pass

    def _sample_uniform_reset_states(self, env_ids):
        motion_ids, times = super()._sample_uniform_reset_states(env_ids)
        gen = self.gen_env_mask[env_ids]
        times[gen] = self.motion.motion_start_idx[motion_ids[gen]] + self.hold_frame
        return motion_ids, times

    def _get_start_at_timestep_zero_probs(self, env_ids):
        p = super()._get_start_at_timestep_zero_probs(env_ids)
        p[self.gen_env_mask[env_ids]] = 0
        return p

    def reset(self, env_ids):
        ids = self._ensure_index_tensor(env_ids)
        if not ids.numel():
            return
        gen_ids = ids[self.gen_env_mask[ids]]
        completed = gen_ids[self.episode_control_steps[gen_ids] > 0]
        if completed.numel():
            lengths = self.episode_control_steps[completed]
            good = (lengths*self._env.dt >= 5.) & (self.episode_good_steps[completed]/lengths > 0.7)
            self.curriculum_episodes += int(completed.numel())
            self.curriculum_successes += int(good.sum())
        super().reset(ids)
        # Gen uses an already-carrying pose and zero initial velocities.
        if gen_ids.numel():
            sim = self._env.simulator
            sim.robot_root_states[gen_ids, 7:] = 0
            sim.dof_vel[gen_ids] = 0
            state = self._object_reset_states(gen_ids)
            state[:, 7:] = 0
            sim.set_actor_states([self.object_name], gen_ids, state)
        self.episode_control_steps[ids] = 0
        self.episode_good_steps[ids] = 0
        self.external_command[ids] = False
        self.task_command[ids] = 0
        self.task_command[ids, 3] = 0.735
        self.sample_gen_commands(gen_ids)
        self._update_track_commands()
        self._update_relative_reference()

    def sample_gen_commands(self, ids):
        self.command_start[ids] = self.task_command[ids]
        self.command_target[ids] = sample_commands(len(ids), self.carry_level, self.device)
        self.command_elapsed[ids] = 0
        self.dwell_remaining[ids] = 3 + 3*torch.rand(len(ids), device=self.device)

    def set_command(self, commands, env_ids=None):
        """Change commands without any physical write/reset; Gen only, SI units."""
        ids = torch.where(self.gen_env_mask)[0] if env_ids is None else self._ensure_index_tensor(env_ids)
        if not self.gen_env_mask[ids].all():
            raise ValueError("External commands are only valid for Gen environments")
        value = torch.as_tensor(commands, device=self.device, dtype=torch.float32)
        if value.shape == (4,):
            value = value.expand(len(ids), -1)
        if value.shape != (len(ids), 4) or not torch.isfinite(value).all():
            raise ValueError("Expected finite [N,4] commands [vx,vy,yaw_rate,pelvis_height]")
        if (value[:, 3] < 0.65).any() or (value[:, 3] > 0.8).any():
            raise ValueError("MVP pelvis height must be between 0.65 and 0.80 m")
        self.command_start[ids] = self.task_command[ids]
        self.command_target[ids] = value
        self.command_elapsed[ids] = 0
        self.external_command[ids] = True

    def _update_track_commands(self):
        heading = yaw_quat(self.root_quat_w, w_last=True)
        v = quat_rotate_inverse(heading, self.root_lin_vel_w, w_last=True)
        ref = torch.cat([v[:, :2], self.root_ang_vel_w[:, 2:3],
            self.root_pos_w[:, 2:3]-self._env.simulator.scene.env_origins[:, 2:3]], -1)
        self.task_command[self.track_env_mask] = ref[self.track_env_mask]

    def _update_relative_reference(self):
        fresh = (self._env.episode_length_buf == 0)[:, None]
        ref_pos = torch.where(fresh, self.root_pos_w, self.ref_pos_w)
        ref_q = torch.where(fresh, self.root_quat_w, self.ref_quat_w)
        robot_pos = torch.where(fresh, self.robot_root_pos_w, self.robot_ref_pos_w)
        robot_q = torch.where(fresh, self.robot_root_quat_w, self.robot_ref_quat_w)
        delta_q = yaw_quat(quat_mul(robot_q, quat_inverse(ref_q, w_last=True), w_last=True), w_last=True)
        n = len(self.motion_cfg.body_names_to_track)
        dq = delta_q[:, None].expand(-1, n, -1)
        self.body_quat_relative_w = quat_mul(dq, self.body_quat_w, w_last=True)
        delta_pos = ref_pos-robot_pos
        delta_pos[:, :2] = 0
        self.body_pos_relative_w = robot_pos[:, None] + delta_pos[:, None] + quat_apply(
            dq, self.body_pos_w-ref_pos[:, None], w_last=True)

    def step(self):
        # Do not call MotionCommand.step: its clip-end branch teleports the scene.
        if self.motion_cfg.use_adaptive_timesteps_sampler:
            self._increment_adaptive_sampler_global_env_step()
        advance = self.track_env_mask & (self._env.episode_length_buf > 0)
        self.time_steps[advance] = torch.minimum(self.time_steps[advance]+1,
            self.motion.motion_end_idx[self.motion_ids[advance]]-1)
        self.last_clip_end_env_ids = torch.empty(0, dtype=torch.long, device=self.device)
        gen_ids = torch.where(self.gen_env_mask)[0]
        self.dwell_remaining[gen_ids] -= self._env.dt
        due = gen_ids[(self.dwell_remaining[gen_ids] <= 0) & ~self.external_command[gen_ids]]
        self.sample_gen_commands(due)
        self.command_elapsed[gen_ids] += self._env.dt
        self.task_command[gen_ids] = smooth_commands(self.command_start[gen_ids], self.command_target[gen_ids],
            self.command_elapsed[gen_ids])
        self._update_track_commands()
        self._update_relative_reference()

    def update_metrics(self):
        # No terminal-position success metric or destination curriculum.
        from holosoma.carry.rewards import task_errors, contact_quality
        errors = task_errors(self._env)
        contact = contact_quality(self._env)
        active = self._env.episode_length_buf > 0
        self.episode_control_steps[active] += 1
        good = (errors[:, :2].square().sum(-1) < .15**2) & (errors[:, 2].abs() < .2) & (errors[:, 3].abs() < .04) & (contact > .4)
        self.episode_good_steps[active] += good[active]
        for i, name in enumerate(("vx", "vy", "yaw_rate", "pelvis_height")):
            self.metrics[f"carry/error_{name}"] = errors[:, i].abs()
            self.metrics[f"carry/command_{name}"] = self.task_command[:, i]
        self.metrics["carry/contact_quality"] = contact
        self.metrics["carry/curriculum_level"] = torch.tensor(float(self.carry_level), device=self.device)

    def on_training_step(self, training_step, **kwargs):
        super().on_training_step(training_step, **kwargs)
        if self.curriculum_episodes >= 100:
            if self.curriculum_successes/self.curriculum_episodes >= 0.7:
                self.carry_level = min(4, self.carry_level+1)
            self.curriculum_episodes = self.curriculum_successes = 0
