"""Instrument real Holosoma PPO; write durable evidence outside the Isaac logger."""
import json
import math
import os
from pathlib import Path
import time

from holosoma import train_agent
from holosoma.carry.checkpoints import atomic_json

output = Path(os.environ['CARRY_WORKER_OUTPUT'])
output.mkdir(parents=True, exist_ok=True)
original_get_class = train_agent.get_class
report = dict(passed=False, updates=0, resume_verified=False)
timing = dict(simulation_s=0.)


def identical(actual, expected):
    import torch
    if isinstance(expected, torch.Tensor):
        torch.testing.assert_close(actual.cpu(), expected.cpu(), rtol=0, atol=0)
    elif isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for k in expected:
            identical(actual[k], expected[k])
    elif isinstance(expected, (list, tuple)):
        assert len(actual) == len(expected)
        for a, b in zip(actual, expected):
            identical(a, b)
    else:
        assert actual == expected, (actual, expected)


def instrument(target):
    cls = original_get_class(target)
    if target.endswith('CarryEnv'):
        class MeasuredEnv(cls):
            def _physics_step(self):
                import torch
                torch.cuda.synchronize()
                start = time.monotonic()
                value = super()._physics_step()
                torch.cuda.synchronize()
                timing['simulation_s'] += time.monotonic() - start
                return value

            def step(self, state):
                import torch
                value = super().step(state)
                obs, rewards, _, _ = value
                assert obs['actor_obs'].shape == (self.num_envs, getattr(self,'actor_dim',348))
                assert obs['critic_obs'].shape == (self.num_envs, getattr(self,'critic_dim',184))
                assert all(torch.isfinite(x).all() for x in obs.values())
                assert torch.isfinite(rewards).all()
                return value
        return MeasuredEnv
    if target.endswith('CarryPPO'):
        class MeasuredPPO(cls):
            def load(self, path):
                value = super().load(path)
                if path:
                    import torch
                    saved = torch.load(path, map_location='cpu', weights_only=True)
                    for name, key in [('actor', 'actor_model_state_dict'),
                                      ('critic', 'critic_model_state_dict'),
                                      ('actor_optimizer', 'actor_optimizer_state_dict'),
                                      ('critic_optimizer', 'critic_optimizer_state_dict'),
                                      ('actor_obs_normalizer', 'actor_obs_normalizer_state_dict'),
                                      ('critic_obs_normalizer', 'critic_obs_normalizer_state_dict')]:
                        identical(getattr(self, name).state_dict(), saved[key])
                    # New optional sampler keys are preserved; legacy carry states remain adoptable.
                    state = self.env.get_checkpoint_state()
                    for k, v in saved['env_state'].items():
                        identical(state[k], v)
                    assert self.current_learning_iteration == saved['iter'] + 1
                    report['resume_verified'] = True
                    report['resumed_from'] = str(path)
                    atomic_json(output / 'worker_result.json', report)
                return value

            def _rollout_step(self, obs):
                import torch
                torch.cuda.synchronize()
                self.rollout_started = time.monotonic()
                timing['simulation_s'] = 0.
                value = super()._rollout_step(obs)
                torch.cuda.synchronize()
                self.rollout_s = time.monotonic() - self.rollout_started
                return value

            def _training_step(self):
                import torch
                torch.cuda.synchronize()
                start = time.monotonic()
                losses = super()._training_step()
                torch.cuda.synchronize()
                update_s = time.monotonic() - start
                assert all(math.isfinite(float(v)) for v in losses.values())
                assert all(torch.isfinite(p).all() for model in (self.actor, self.critic) for p in model.parameters())
                metrics = {}
                for k, v in self.env.log_dict.items():
                    try:
                        number = float(torch.as_tensor(v).float().mean())
                        if math.isfinite(number):
                            metrics[k] = number
                    except (TypeError, ValueError):
                        pass
                for section in ('episode','raw_episode'):
                    for k,v in self.env.extras.get(section,{}).items():
                        try:
                            number = float(torch.as_tensor(v).float().mean())
                            if math.isfinite(number):
                                metrics[f'reward/{section}/{k}'] = number
                        except (TypeError,ValueError):
                            pass
                command = self.env.command_manager.get_state('motion_command')
                row = dict(iteration=self.current_learning_iteration, num_envs=self.env.num_envs,
                    samples=self.env.num_envs*self.config.num_steps_per_env,
                    minibatches=self.config.num_mini_batches, epochs=self.config.num_learning_epochs,
                    rollout_s=self.rollout_s, update_s=update_s, simulation_s=timing['simulation_s'],
                    steps_per_s=self.env.num_envs*self.config.num_steps_per_env/(self.rollout_s+update_s),
                    cuda_reserved_mib=torch.cuda.max_memory_reserved()/2**20,
                    curriculum_level=command.carry_level, losses={k:float(v) for k,v in losses.items()},
                    physical=metrics, mean_live_episode_s=float(self.env.episode_length_buf.float().mean()*self.env.dt))
                with (output / 'iterations.jsonl').open('a') as f:
                    f.write(json.dumps(row, allow_nan=False)+'\n')
                    f.flush()
                report.update(updates=report['updates']+1, latest=row, log_dir=str(self.log_dir))
                atomic_json(output / 'worker_result.json', report)
                return losses

            def learn(self):
                super().learn()
                report['passed'] = report['updates'] >= 1
                atomic_json(output / 'worker_result.json', report)
        return MeasuredPPO
    return cls


train_agent.get_class = instrument
train_agent.main()
