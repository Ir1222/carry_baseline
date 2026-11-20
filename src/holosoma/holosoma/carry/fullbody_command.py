"""Whole-body Track with weighted clips, continuous independent Gen commands."""
import json
from pathlib import Path
import torch
from holosoma.carry.command import CarryCommand
from holosoma.carry.fullbody_sampling import sample, transition, validate_commands


class FullBodyCommand(CarryCommand):
    def __init__(self, cfg, env):
        self.limits = json.loads(Path(cfg.params['goal_limits_file']).read_text())
        self.manifest = json.loads(Path(cfg.params['manifest_file']).read_text())
        super().__init__(cfg, env)

    def init_buffers(self):
        super().init_buffers()
        self.task_command[:, 3] = self.limits['height_high']
        self.command_start[:] = self.task_command
        self.command_target[:] = self.task_command
        self.height_command_rate = torch.zeros(self.num_envs, device=self.device)
        self.goal_mode = torch.zeros(self.num_envs, device=self.device, dtype=torch.long)
        self.cycle_phase = torch.zeros(self.num_envs, device=self.device, dtype=torch.long)

    def _weights(self):
        rows = sorted([r for r in self.manifest['motions'] if r['sampling_weight'] > 0], key=lambda r:r['name'])
        if len(rows) != self.motion.num_motions:
            raise ValueError('Motion count differs from admitted manifest')
        return torch.tensor([r['sampling_weight'] for r in rows], device=self.device)

    def _sample_motion_ids_for_reset(self, env_ids):
        self.motion_ids[env_ids] = torch.multinomial(self._weights(), len(env_ids), replacement=True)

    def _sample_adaptive_reset_states(self, env_ids, group_ids):
        # Fixed family priors, adaptive difficulty within each selected clip.
        mids = torch.multinomial(self._weights(), len(env_ids), replacement=True)
        bins = torch.empty_like(mids); times = torch.empty_like(mids)
        for group in range(2):
            for motion in range(self.motion.num_motions):
                mask = (group_ids == group) & (mids == motion)
                n = int(mask.sum())
                if n:
                    _, bins[mask], times[mask] = self.adaptive_timesteps_sampler.sample_from_motion_pool(
                        group, torch.tensor([motion],device=self.device), n)
        return mids, bins, times

    def reset(self, env_ids):
        super().reset(env_ids)
        ids = self._ensure_index_tensor(env_ids)
        gen = ids[self.gen_env_mask[ids]]
        self.task_command[gen] = 0
        self.task_command[gen, 3] = self.limits['height_high']
        self.command_start[gen] = self.task_command[gen]
        self.command_target[gen] = self.task_command[gen]
        self.command_elapsed[gen] = 0
        self.dwell_remaining[gen] = 2.
        self.cycle_phase[gen] = 0
        self.height_command_rate[ids] = 0

    def sample_gen_commands(self, ids):
        if not len(ids):
            return
        target, modes = sample(len(ids), self.carry_level, self.device, self.limits)
        # Half the environments execute a mandatory high-low-high cycle within
        # one episode. The other half explore the independent mode sampler.
        cycle = (ids % 2 == 0)
        phase = self.cycle_phase[ids] % 4
        target[cycle, :3] = 0
        target[cycle, 3] = torch.where((phase[cycle] == 1) | (phase[cycle] == 2),
            self.limits['height_low'], self.limits['height_high'])
        self.command_start[ids] = self.task_command[ids]
        self.command_target[ids] = target
        self.command_elapsed[ids] = 0
        duration = 1.5*(target[:,3]-self.task_command[ids,3]).abs()/self.limits['height_rate']
        self.dwell_remaining[ids] = duration.clamp_min(.8)+2.+torch.rand(len(ids),device=self.device)
        self.goal_mode[ids] = modes
        self.cycle_phase[ids] += 1

    def set_command(self, commands, env_ids=None):
        ids = torch.where(self.gen_env_mask)[0] if env_ids is None else self._ensure_index_tensor(env_ids)
        if not self.gen_env_mask[ids].all():
            raise ValueError('External goals require Gen environments')
        value = torch.as_tensor(commands,device=self.device,dtype=torch.float32)
        if value.shape == (4,): value=value.expand(len(ids),-1)
        if value.shape != (len(ids),4): raise ValueError('Expected [N,4] goals')
        validate_commands(value,self.limits)
        self.command_start[ids] = self.task_command[ids]
        self.command_target[ids] = value
        self.command_elapsed[ids] = 0
        self.external_command[ids] = True

    def step(self):
        if self.motion_cfg.use_adaptive_timesteps_sampler:
            self._increment_adaptive_sampler_global_env_step()
        advance = self.track_env_mask & (self._env.episode_length_buf > 0)
        self.time_steps[advance] = torch.minimum(self.time_steps[advance]+1,
            self.motion.motion_end_idx[self.motion_ids[advance]]-1)
        self.last_clip_end_env_ids = torch.empty(0,dtype=torch.long,device=self.device)
        ids = torch.where(self.gen_env_mask)[0]
        self.dwell_remaining[ids] -= self._env.dt
        self.sample_gen_commands(ids[(self.dwell_remaining[ids] <= 0) & ~self.external_command[ids]])
        before = self.task_command[:,3].clone()
        self.command_elapsed[ids] += self._env.dt
        self.task_command[ids] = transition(self.command_start[ids],self.command_target[ids],
            self.command_elapsed[ids],self.limits['height_rate'])
        self.height_command_rate[:] = (self.task_command[:,3]-before)/self._env.dt
        self._update_track_commands()
        self._update_relative_reference()

    def update_metrics(self):
        # The legacy metric assumes a box mesh axis is vertical. Use the reset's
        # relative orientation and geometric bottom instead.
        from holosoma.carry.fullbody_rewards import physical_metrics
        from holosoma.carry.rewards import task_errors
        errors=task_errors(self._env)
        metrics=physical_metrics(self._env)
        active=self._env.episode_length_buf > 0
        self.episode_control_steps[active] += 1
        good=(errors[:,0].abs()<.1)&(errors[:,3].abs()<.03)&(metrics['bilateral_contact']>.99)
        self.episode_good_steps[active] += good[active]
        for i,name in enumerate(('vx','vy','yaw_rate','pelvis_height')):
            self.metrics[f'carry/error_{name}']=errors[:,i].abs()
            self.metrics[f'carry/command_{name}']=self.task_command[:,i]
        for key,value in metrics.items(): self.metrics['carry/'+key]=value
        self.metrics['carry/curriculum_level']=torch.tensor(float(self.carry_level),device=self.device)
