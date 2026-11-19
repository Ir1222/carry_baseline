"""Run the unmodified upstream CLI with runtime assertions and a JSON evidence file."""
import json
import math
import os
from pathlib import Path

from holosoma import train_agent

report_path = Path(os.environ["HMI_SMOKE_REPORT"])
report = {"physics_steps": 0, "ppo_updates": 0, "passed": False}
original_get_class = train_agent.get_class


def save():
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2))


def instrumented_get_class(target):
    cls = original_get_class(target)
    if target.endswith("WholeBodyTrackingManager"):
        class CheckedEnv(cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                import torch
                command = self.command_manager.get_state("motion_command")
                report["track_envs"] = int(command.track_env_mask.sum())
                report["gen_envs"] = int(command.gen_env_mask.sum())
                assert report["track_envs"] > 0 and report["gen_envs"] > 0
                report["dof_names"] = list(self.simulator.dof_names)
                assert len(report["dof_names"]) == 29
                box = self.simulator._object
                report["box_mass_range"] = [float(box.root_physx_view.get_masses().min()),
                                             float(box.root_physx_view.get_masses().max())]
                report["box_gravity_enabled"] = not box.cfg.spawn.rigid_props.disable_gravity
                report["box_free_base"] = not box.cfg.spawn.fix_base
                assert report["box_gravity_enabled"] and report["box_free_base"]
                assert torch.isfinite(box.data.root_state_w).all()
                from pxr import UsdPhysics
                prim = self.simulator.scene.stage.GetPrimAtPath("/World/envs/env_0/Object") if hasattr(self.simulator.scene, "stage") else None
                if prim is None:
                    import omni.usd
                    prim = omni.usd.get_context().get_stage().GetPrimAtPath("/World/envs/env_0/Object")
                from pxr import Usd
                collisions = [str(p.GetPath()) for p in Usd.PrimRange(prim, Usd.TraverseInstanceProxies())
                              if p.HasAPI(UsdPhysics.CollisionAPI)
                              and UsdPhysics.CollisionAPI(p).GetCollisionEnabledAttr().Get()]
                report["box_collision_prims"] = collisions
                assert collisions, "Box has no collision geometry"
                save()

            def step(self, state):
                import torch
                obs, rewards, dones, infos = super().step(state)
                assert all(torch.isfinite(v).all() for v in obs.values())
                assert torch.isfinite(rewards).all()
                assert torch.isfinite(self.simulator._object.data.root_state_w).all()
                assert torch.isfinite(self.simulator.robot_root_states[:]).all()
                report["observation_shapes"] = {k: list(v.shape) for k, v in obs.items()}
                report["physics_steps"] += 1
                report["reward_range"] = [float(rewards.min()), float(rewards.max())]
                save()
                return obs, rewards, dones, infos
        return CheckedEnv
    if target.endswith("PPO"):
        class CheckedPPO(cls):
            def _training_step(self):
                import torch
                before = [p.detach().clone() for p in self.actor.parameters()]
                result = super()._training_step()
                assert all(math.isfinite(float(v)) for v in result.values())
                assert all(torch.isfinite(p).all() for p in self.actor.parameters())
                assert any(not torch.equal(p, q) for p, q in zip(before, self.actor.parameters()))
                report["ppo_updates"] += 1
                report["losses"] = result
                report["cuda_peak_allocated_mib"] = torch.cuda.max_memory_allocated() / 2**20
                report["cuda_peak_reserved_mib"] = torch.cuda.max_memory_reserved() / 2**20
                save()
                return result

            def learn(self):
                super().learn()
                report["passed"] = report["ppo_updates"] >= 1 and report["physics_steps"] >= 24
                assert report["passed"]
                save()
        return CheckedPPO
    return cls


train_agent.get_class = instrumented_get_class
train_agent.main()
