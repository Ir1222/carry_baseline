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
                for name, term in self.reward_manager.cfg.terms.items():
                    assert 'reached_once' not in name
                    if term.func == 'holosoma.carry.rewards:track_imitation':
                        from holosoma.carry.rewards import track_imitation
                        values = track_imitation(self, **term.params)
                        assert (values[cmd.gen_env_mask] == 0).all()
                report['reward_masks_checked'] = True
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
            def _rollout_step(self, obs_dict):
                import torch
                env = self.env
                cmd = env.command_manager.get_state('motion_command')
                ids = torch.where(cmd.gen_env_mask)[0]
                if report.get('bootstrap_semantics_checked') or len(ids) < 2:
                    return super()._rollout_step(obs_dict)
                # One real time limit and one simultaneous fall/time limit.
                timeout_id, failure_id = ids[:2]
                env.episode_length_buf[ids[:2]] = int(env.max_episode_length)
                env.simulator.robot_root_states[failure_id, 2] = .25
                env.simulator.set_actor_root_state_tensor(ids[1:2], env.simulator.all_root_states)
                env.simulator.refresh_sim_tensors()
                expected = []
                original_step = env.step
                def checked_step(state):
                    result = original_step(state)
                    obs, rewards, done, info = result
                    if not expected:
                        assert done[timeout_id] and info['time_outs'][timeout_id]
                        assert done[failure_id] and not info['time_outs'][failure_id]
                        assert 'final_observations' in info
                        assert (obs['actor_obs'][ids[:2],:232] == 0).all()
                        assert torch.isfinite(info['final_observations']['critic_obs'][ids[:2]]).all()
                    value = torch.zeros_like(rewards)
                    if info['time_outs'].any():
                        final = torch.cat([info['final_observations'][k] for k in self.critic_obs_keys],dim=1)
                        value = self.critic.evaluate({'critic_obs':self._normalize_critic_obs(final,update=False)}).squeeze(1)
                    expected.append((rewards+self.config.gamma*value*info['time_outs']).clone())
                    return result
                env.step = checked_step
                try:
                    result = super()._rollout_step(obs_dict)
                    torch.testing.assert_close(self.storage['rewards'].squeeze(-1),torch.stack(expected))
                    report['bootstrap_semantics_checked'] = True
                    report['failure_overrides_timeout_checked'] = True
                    report['reset_history_cleared_checked'] = True
                    save()
                    return result
                finally:
                    env.step = original_step

            def export(self, onnx_file_path):
                import torch
                import numpy as np
                import onnxruntime as ort
                super().export(onnx_file_path)
                session = ort.InferenceSession(str(onnx_file_path), providers=['CPUExecutionProvider'])
                assert [i.name for i in session.get_inputs()] == ['actor_obs']
                assert [o.name for o in session.get_outputs()] == ['action']
                x = torch.randn(1,348,device=self.device)
                with torch.no_grad():
                    expected = self.actor_onnx_wrapper(x).cpu().numpy()
                actual = session.run(['action'], {'actor_obs':x.cpu().numpy()})[0]
                np.testing.assert_allclose(actual,expected,rtol=2e-4,atol=2e-5)
                report['onnx_actor_equivalence_checked'] = True
                report['onnx_max_abs_error'] = float(np.max(np.abs(actual-expected)))
                save()

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
