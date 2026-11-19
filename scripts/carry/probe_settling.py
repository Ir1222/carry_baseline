"""Free-object PD hold sweep. No root/object state writes after initialization."""
import json
from dataclasses import replace
from pathlib import Path

from holosoma.config_values.wbt.g1.experiment import g1_29dof_wbt_hybrid_object as base
from holosoma.config_types.command import CommandTermCfg, NoiseToInitialPoseConfig
from holosoma.config_types.env import get_tyro_env_config
from holosoma.config_types.logger import DisabledLoggerConfig
from holosoma.config_types.randomization import RandomizationManagerCfg
from holosoma.config_values.wbt.g1.curriculum import g1_29dof_wbt_curriculum
from holosoma.config_values.wbt.g1.randomization import robot_state_dr_at_setup, object_state_dr_at_setup
from holosoma.train_agent import TrainingContext

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT.parent / "artifacts/carry_reference"
mc = base.command.setup_terms["motion_command"].params["motion_config"]
mc = replace(mc, motion_file=str(next((DATA / "motions").glob("*reframed.npz"))), motion_dir="",
             noise_to_initial_pose=NoiseToInitialPoseConfig(), use_adaptive_timesteps_sampler=False,
             enable_terminal_pose_hold=False, load_fixed_scene_from_motion=False,
             hybrid=replace(mc.hybrid, track_ratio=1.0))
materials = {}
for name, term in {**robot_state_dr_at_setup, **object_state_dr_at_setup}.items():
    if "material" in name:
        materials[name] = replace(term, params={"enabled": True, "static_friction_range": [0.9, 0.9],
            "dynamic_friction_range": [0.8, 0.8], "restitution_range": [0., 0.]})
config = replace(base,
    training=replace(base.training, num_envs=64, name="carry_settling"),
    logger=DisabledLoggerConfig(base_dir=str(ROOT.parent / "artifacts/training")),
    simulator=replace(base.simulator, _target_="holosoma.carry.simulator.IsaacSim"),
    robot=replace(base.robot, object=replace(base.robot.object, object_urdf_path=str(DATA / "carry_box.urdf"))),
    command=replace(base.command, setup_terms={"motion_command": CommandTermCfg(
        func=base.command.setup_terms["motion_command"].func, params={"motion_config": mc})}),
    randomization=RandomizationManagerCfg(setup_terms=materials), curriculum=g1_29dof_wbt_curriculum)

with TrainingContext(config):
    import torch
    from holosoma.envs.wbt.wbt_manager import WholeBodyTrackingManager
    env = WholeBodyTrackingManager(get_tyro_env_config(config), device="cuda:0")
    env.reset_all()
    cmd = env.command_manager.get_state("motion_command")
    ids = torch.arange(env.num_envs, device=env.device)
    frames = torch.linspace(0, 109, env.num_envs, device=env.device).long()
    cmd.motion_ids[:] = 0
    cmd.time_steps[:] = frames
    sim = env.simulator
    sim.robot_root_states[:, :3] = cmd.root_pos_w
    sim.robot_root_states[:, 3:7] = cmd.root_quat_w
    sim.robot_root_states[:, 7:] = 0
    sim.dof_pos[:] = cmd.joint_pos
    sim.dof_vel[:] = 0
    obj = torch.cat([cmd.object_pos_w, cmd.object_quat_w, torch.zeros(env.num_envs, 6, device=env.device)], -1)
    sim.set_actor_states(["object"], ids, obj)
    sim.set_actor_root_state_tensor(ids, sim.all_root_states)
    sim.set_dof_state_tensor(ids, sim.dof_state)
    sim.refresh_sim_tensors()
    actions = (cmd.joint_pos - env.default_dof_pos) / env.action_scales
    initial_obj = sim._object.data.root_pos_w.clone()
    min_root = torch.full((env.num_envs,), 10., device=env.device)
    max_drop = torch.zeros(env.num_envs, device=env.device)
    both_contact = torch.zeros(env.num_envs, device=env.device)
    support = torch.zeros(env.num_envs, device=env.device)
    rows = []
    for step in range(100):
        env._pre_physics_step(actions)
        env._physics_step()
        sim.refresh_sim_tensors()
        forces = sim.hand_box_forces()
        assert torch.isfinite(forces).all()
        root = sim.robot_root_states[:]
        box = sim._object.data.root_state_w
        assert torch.isfinite(root).all() and torch.isfinite(box).all()
        min_root = torch.minimum(min_root, root[:, 2])
        max_drop = torch.maximum(max_drop, initial_obj[:, 2] - box[:, 2])
        if step >= 10:
            both_contact += (torch.linalg.vector_norm(forces, dim=-1) > 0.5).all(dim=1)
            support += (-forces[:, :, 2].sum(dim=1)).clamp_min(0)
        if step in (9, 24, 49, 99):
            rows.append({"time_s": (step+1)*env.dt, "root_z": root[:, 2].tolist(),
                         "box_z": box[:, 2].tolist(), "hand_forces_w": forces.tolist()})
    score = (both_contact/90) - 3*max_drop - 2*(0.65-min_root).clamp_min(0)
    best = int(score.argmax())
    result = {"frames_in_crop": frames.tolist(), "original_frames": (frames+95).tolist(),
              "best_env": best, "best_original_frame": int(frames[best])+95,
              "min_root_z": min_root.tolist(), "max_box_drop": max_drop.tolist(),
              "both_contact_fraction_after_0_2s": (both_contact/90).tolist(),
              "mean_upward_box_support_n": (support/90).tolist(), "samples": rows,
              "box_mass_kg": sim._object.root_physx_view.get_masses().tolist()}
    (ROOT.parent / "artifacts/p2_settling_sweep.json").write_text(json.dumps(result, indent=2))
    print("SETTLING BEST", best, int(frames[best])+95, float(min_root[best]), float(max_drop[best]), float(both_contact[best]/90))
