"""Bounded carry integration assertions around the actual upstream training CLI."""
import json
import math
import os
from pathlib import Path
from holosoma import train_agent

path = Path(os.environ['HMI_SMOKE_REPORT'])
if path.exists():
    raise FileExistsError(path)
report = dict(passed=False, physics_steps=0, ppo_updates=0)
original_get_class = train_agent.get_class


def save():
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2))


def instrumented_get_class(target):
    cls = original_get_class(target)
    if target.endswith('CarryEnv'):
        class CheckedEnv(cls):
            def step(self, state):
                import torch
                obs, rewards, dones, infos = super().step(state)
                cmd = self.command_manager.get_state('motion_command')
                assert obs['actor_obs'].shape == (self.num_envs,348)
                assert obs['critic_obs'].shape == (self.num_envs,184)
                assert cmd.task_command.shape == (self.num_envs,4)
                assert all(torch.isfinite(v).all() for v in obs.values())
                assert torch.isfinite(rewards).all()
                assert (obs['critic_obs'][cmd.gen_env_mask,-68:] == 0).all()
                assert not (infos['time_outs'] & ~dones.bool()).any()
                report['physics_steps'] += 1
                report['shapes'] = {k:list(v.shape) for k,v in obs.items()}
                report['track_envs'] = int(cmd.track_env_mask.sum())
                report['gen_envs'] = int(cmd.gen_env_mask.sum())
                report['box_gravity_enabled'] = not self.simulator._object.cfg.spawn.rigid_props.disable_gravity
                assert report['box_gravity_enabled'] and not self.simulator._object.cfg.spawn.fix_base
                if not report.get('command_no_reset_checked') and cmd.gen_env_mask.any():
                    ids = torch.where(cmd.gen_env_mask)[0]
                    root = self.simulator.robot_root_states[:].clone()
                    box = self.simulator._object.data.root_state_w.clone()
                    q = self.simulator.dof_pos.clone()
                    lengths = self.episode_length_buf.clone()
                    cmd.set_command([.05,-.02,.1,.75],ids)
                    assert torch.equal(root,self.simulator.robot_root_states[:])
                    assert torch.equal(box,self.simulator._object.data.root_state_w)
                    assert torch.equal(q,self.simulator.dof_pos)
                    assert torch.equal(lengths,self.episode_length_buf)
                    old_times = cmd.time_steps.clone()
                    cmd.time_steps[ids] = cmd.motion.motion_end_idx[cmd.motion_ids[ids]]-1
                    times = cmd.time_steps[ids].clone()
                    cmd.step()
                    assert torch.equal(times,cmd.time_steps[ids]), 'Gen must not advance/reset clip time'
                    assert torch.equal(root,self.simulator.robot_root_states[:])
                    assert torch.equal(box,self.simulator._object.data.root_state_w)
                    cmd.time_steps[:] = old_times
                    cmd.external_command[ids] = False
                    cmd.sample_gen_commands(ids)
                    report['command_no_reset_checked'] = True
                    report['gen_clip_end_independence_checked'] = True
                save()
                return obs,rewards,dones,infos
        return CheckedEnv
    if target.endswith('CarryPPO'):
        class CheckedPPO(cls):
            def _training_step(self):
                import torch
                before = [p.detach().clone() for p in self.actor.parameters()]
                result = super()._training_step()
                assert all(math.isfinite(float(v)) for v in result.values())
                assert all(torch.isfinite(p).all() for p in self.actor.parameters())
                assert any(not torch.equal(p,q) for p,q in zip(before,self.actor.parameters()))
                report['ppo_updates'] += 1
                report['losses'] = result
                report['cuda_peak_allocated_mib'] = torch.cuda.max_memory_allocated()/2**20
                report['cuda_peak_reserved_mib'] = torch.cuda.max_memory_reserved()/2**20
                save()
                return result

            def load(self, *args, **kwargs):
                value = super().load(*args, **kwargs)
                report['checkpoint_loaded'] = True
                save()
                return value

            def learn(self):
                super().learn()
                report['passed'] = report['ppo_updates'] >= 1 and report['physics_steps'] >= 24
                assert report['passed']
                save()
        return CheckedPPO
    return cls


train_agent.get_class = instrumented_get_class
train_agent.main()
