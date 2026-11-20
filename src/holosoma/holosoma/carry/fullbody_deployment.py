"""Reference-free FullBody command; static reset and limits only."""
import json
from pathlib import Path
import torch
from holosoma.carry.deployment import DeploymentCommand
from holosoma.carry.fullbody_sampling import transition,validate_commands


class FullBodyDeploymentCommand(DeploymentCommand):
    def __init__(self,cfg,env):
        super().__init__(cfg,env)
        self.limits=json.loads(Path(cfg.params['goal_limits_file']).read_text())

    def init_buffers(self):
        super().init_buffers()
        self.task_command[:,3]=self.limits['height_high']
        self.start[:]=self.task_command;self.target[:]=self.task_command

    def reset(self,env_ids):
        super().reset(env_ids)
        ids=torch.arange(self.num_envs,device=self.device) if env_ids is None else env_ids.long()
        self.task_command[ids,3]=self.limits['height_high']
        self.start[ids]=self.task_command[ids];self.target[ids]=self.task_command[ids]

    def set_command(self,command,env_ids=None):
        value=torch.as_tensor(command,device=self.device,dtype=torch.float32)
        if value.ndim==1:value=value[None]
        validate_commands(value,self.limits)
        super().set_command(command,env_ids)

    def step(self):
        self.elapsed+=self.env.dt
        self.task_command[:]=transition(self.start,self.target,self.elapsed,self.limits['height_rate'])

    def update_metrics(self):
        from holosoma.carry.rewards import task_errors
        from holosoma.carry.fullbody_rewards import physical_metrics
        e=task_errors(self.env)
        self.metrics={f'carry/error_{name}':e[:,i].abs() for i,name in enumerate(('vx','vy','yaw_rate','pelvis_height'))}
        self.metrics.update({'carry/'+k:v for k,v in physical_metrics(self.env).items()})
