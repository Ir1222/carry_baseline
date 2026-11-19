"""Free-object PD hold sweep. No root/object state writes after initialization."""
import json
import argparse
from dataclasses import replace
from pathlib import Path

from holosoma.config_values.wbt.g1.experiment import g1_29dof_wbt_hybrid_object as base
from holosoma.config_types.command import CommandTermCfg, NoiseToInitialPoseConfig
from holosoma.config_types.env import get_tyro_env_config
from holosoma.config_types.logger import DisabledLoggerConfig
from holosoma.config_types.randomization import RandomizationManagerCfg
from holosoma.config_values.wbt.g1.curriculum import g1_29dof_wbt_curriculum
from holosoma.config_values.wbt.g1.randomization import robot_state_dr_at_setup, object_state_dr_at_setup, base_setup_terms
from holosoma.train_agent import TrainingContext

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT.parent / "artifacts/carry_reference"
parser = argparse.ArgumentParser()
parser.add_argument("--hold-search", action="store_true")
parser.add_argument("--under-support", action="store_true")
parser.add_argument("--data", type=Path, default=DATA)
parser.add_argument("--gravity-compensation", action="store_true")
parser.add_argument("--palm-placement", action="store_true")
parser.add_argument("--output", type=Path, default=ROOT.parent / "artifacts/p2_settling_sweep.json")
args = parser.parse_args()
DATA = args.data.resolve()
mc = base.command.setup_terms["motion_command"].params["motion_config"]
mc = replace(mc, motion_file=str(next((DATA / "motions").glob("*reframed.npz"))), motion_dir="",
             noise_to_initial_pose=NoiseToInitialPoseConfig(), use_adaptive_timesteps_sampler=False,
             enable_terminal_pose_hold=False, load_fixed_scene_from_motion=False,
             hybrid=replace(mc.hybrid, track_ratio=1.0))
materials = {}
materials["setup_action_delay_buffers"] = base_setup_terms["setup_action_delay_buffers"]
materials["actuator_randomizer_state"] = base_setup_terms["actuator_randomizer_state"]
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

context = TrainingContext(config)
context.__enter__()
try:
    import torch
    from holosoma.envs.wbt.wbt_manager import WholeBodyTrackingManager
    env = WholeBodyTrackingManager(get_tyro_env_config(config), device="cuda:0")
    env.reset_all()
    cmd = env.command_manager.get_state("motion_command")
    ids = torch.arange(env.num_envs, device=env.device)
    frames = torch.linspace(0, 109, env.num_envs, device=env.device).long()
    if args.hold_search:
        frames = torch.linspace(0, 109, 8, device=env.device).long().repeat_interleave(8)
        if args.under_support:
            frames = torch.tensor([5, 35, 65, 95], device=env.device).repeat_interleave(16)
    cmd.motion_ids[:] = 0
    cmd.time_steps[:] = frames
    sim = env.simulator
    print("ALL SENSOR BODIES", sim.contact_sensor.body_names, flush=True)
    from pxr import Usd, UsdPhysics, UsdGeom
    import omni.usd
    stage = omni.usd.get_context().get_stage()
    for body in ["Robot/left_wrist_yaw_link", "Robot/right_wrist_yaw_link", "Object/baseLink"]:
        prim = stage.GetPrimAtPath("/World/envs/env_0/"+body)
        for p in Usd.PrimRange(prim, Usd.TraverseInstanceProxies()):
            if p.HasAPI(UsdPhysics.CollisionAPI):
                print("COLLIDER", p.GetPath(), "enabled", UsdPhysics.CollisionAPI(p).GetCollisionEnabledAttr().Get(),
                    "approx", UsdPhysics.MeshCollisionAPI(p).GetApproximationAttr().Get() if p.IsA(UsdGeom.Mesh) else "primitive", flush=True)
                print("EXTENT", UsdGeom.Boundable(p).GetExtentAttr().Get(), flush=True)
    sim.robot_root_states[:, :3] = cmd.root_pos_w
    sim.robot_root_states[:, 3:7] = cmd.root_quat_w
    sim.robot_root_states[:, 7:] = 0
    sim.dof_pos[:] = cmd.joint_pos
    sim.dof_vel[:] = 0
    obj = torch.cat([cmd.object_pos_w, cmd.object_quat_w, torch.zeros(env.num_envs, 6, device=env.device)], -1)
    if args.hold_search:
        from holosoma.utils.rotations import quat_apply, quat_inverse, quat_mul, yaw_quat
        old_root = sim.robot_root_states[:].clone()
        new_q = yaw_quat(old_root[:, 3:7], w_last=True)
        delta_q = quat_mul(new_q, quat_inverse(old_root[:, 3:7], w_last=True), w_last=True)
        sim.robot_root_states[:, 3:7] = new_q
        sim.robot_root_states[:, 2] = 0.76
        obj[:, :3] = sim.robot_root_states[:, :3] + quat_apply(delta_q, obj[:, :3]-old_root[:, :3], w_last=True)
        obj[:, 3:7] = quat_mul(delta_q, obj[:, 3:7], w_last=True)
        sim.dof_pos[:, :12] = env.default_dof_pos[:, :12]
        squeeze = torch.linspace(-.12, .30, 8, device=env.device).repeat(8)
        if args.under_support:
            squeeze = torch.tensor([0., .04, .08, .12], device=env.device).repeat(16)
            obj[:, 2] += torch.tensor([.08, .12, .16, .2], device=env.device).repeat_interleave(4).repeat(4)
        sim.dof_pos[:, sim.dof_names.index("left_shoulder_roll_joint")] -= squeeze
        sim.dof_pos[:, sim.dof_names.index("right_shoulder_roll_joint")] += squeeze
        sim.dof_pos[:] = torch.clamp(sim.dof_pos, env.dof_pos_limits[:, 0], env.dof_pos_limits[:, 1])
    sim.set_actor_states(["object"], ids, obj)
    sim.set_actor_root_state_tensor(ids, sim.all_root_states)
    sim.set_dof_state_tensor(ids, sim.dof_state)
    sim.refresh_sim_tensors()
    target_q = sim.dof_pos.clone()
    if args.palm_placement:
        import pinocchio as pin
        import numpy as np
        from scipy.optimize import least_squares
        model = pin.buildModelFromUrdf(str(ROOT / "src/holosoma/holosoma/data/robots/g1/main_mesh_collision_halfspherehand.urdf"))
        pdata = model.createData()
        target_q[:] = env.default_dof_pos
        sim.robot_root_states[:, :3] = sim.scene.env_origins
        sim.robot_root_states[:, 2] = .76
        sim.robot_root_states[:, 3:7] = torch.tensor([0.,0.,0.,1.], device=env.device)
        mass = float(sim._object.root_physx_view.get_masses()[0, 0])
        arm_compensation = []
        for i in range(env.num_envs):
            desired = target_q[i].cpu().numpy().copy()
            x, y = .28+.02*(i//16), .12+.02*((i//4)%4)
            for side, sign, start in [("left",1,15),("right",-1,22)]:
                frame = model.getFrameId(side+"_sphere_hand_link", pin.FrameType.BODY)
                seed = cmd.joint_pos[i, start:start+7].cpu().numpy()
                def residual(angles):
                    desired[start:start+7] = angles
                    pin.framesForwardKinematics(model, pdata, desired)
                    return np.r_[10*(pdata.oMf[frame].translation-np.array([x,sign*y,-.04])), .03*(angles-seed)]
                fit = least_squares(residual, np.clip(seed, model.lowerPositionLimit[start:start+7], model.upperPositionLimit[start:start+7]),
                    bounds=(model.lowerPositionLimit[start:start+7],model.upperPositionLimit[start:start+7]),max_nfev=100)
                desired[start:start+7] = fit.x
            target_q[i] = torch.tensor(desired, device=env.device)
            obj[i, :3] = sim.scene.env_origins[i]+torch.tensor([x,0.,.76-.04+.035+.204],device=env.device)
            obj[i, 3:7] = torch.tensor([0.,0.,0.,1.],device=env.device)
            g = pin.computeGeneralizedGravity(model,pdata,desired).copy()
            for side in ("left","right"):
                jac = pin.computeFrameJacobian(model,pdata,desired,model.getFrameId(side+"_sphere_hand_link",pin.FrameType.BODY),pin.LOCAL_WORLD_ALIGNED)
                g += jac.T@np.array([0.,0.,mass*9.81/2,0.,0.,0.])
            g[:15] = 0
            arm_compensation.append(g*(i%4)*.5)
        sim.dof_pos[:] = target_q
        sim.set_actor_states(["object"], ids, obj)
        sim.set_actor_root_state_tensor(ids, sim.all_root_states)
        sim.set_dof_state_tensor(ids, sim.dof_state)
        sim.refresh_sim_tensors()
    initial_root = sim.robot_root_states[:].clone()
    initial_box = obj.clone()
    actions = (target_q - env.default_dof_pos) / env.action_scales
    if args.palm_placement:
        actions += torch.tensor(np.array(arm_compensation),device=env.device,dtype=torch.float32)/env.p_gains/env.action_scales
    if args.gravity_compensation:
        import pinocchio as pin
        import numpy as np
        model = pin.buildModelFromUrdf(str(ROOT / "src/holosoma/holosoma/data/robots/g1/main_mesh_collision_halfspherehand.urdf"), pin.JointModelFreeFlyer())
        pdata = model.createData()
        compensations = []
        for i in range(env.num_envs):
            configuration = np.r_[initial_root[i, :7].cpu().numpy(), target_q[i].cpu().numpy()]
            gravity = pin.computeGeneralizedGravity(model, pdata, configuration).copy()
            for side in ("left", "right"):
                j = pin.computeFrameJacobian(model, pdata, configuration, model.getFrameId(side+"_sphere_hand_link"), pin.LOCAL_WORLD_ALIGNED)
                gravity += j.T @ np.array([0., 0., 1.5*9.81/2, 0., 0., 0.])
            feet = [pin.computeFrameJacobian(model, pdata, configuration, model.getFrameId(side+"_foot_contact_point", pin.FrameType.BODY), pin.LOCAL_WORLD_ALIGNED).copy() for side in ("left","right")]
            contact = np.concatenate(feet, axis=0)
            wrench = np.linalg.lstsq(contact[:, :6].T, gravity[:6], rcond=None)[0]
            compensations.append((gravity-contact.T@wrench)[6:])
        tau = torch.tensor(np.array(compensations), device=env.device, dtype=torch.float32)
        actions += tau/env.p_gains/env.action_scales
    pd_targets = env.default_dof_pos + actions*env.action_scales
    initial_obj = sim._object.data.root_pos_w.clone()
    min_root = torch.full((env.num_envs,), 10., device=env.device)
    max_drop = torch.zeros(env.num_envs, device=env.device)
    both_contact = torch.zeros(env.num_envs, device=env.device)
    support = torch.zeros(env.num_envs, device=env.device)
    rows = []
    hand_ids = [sim.body_names.index(f"{side}_wrist_yaw_link") for side in ("left", "right")]
    ref_hand = cmd.motion.body_pos_w[frames][:, hand_ids] + sim.scene.env_origins[:, None]
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
        if step in (0, 4, 9, 24, 49, 99):
            rows.append({"time_s": (step+1)*env.dt, "root_z": root[:, 2].tolist(),
                         "box_z": box[:, 2].tolist(), "hand_forces_w": forces.tolist(),
                         "hand_positions_w": sim._rigid_body_pos[:, hand_ids].tolist(),
                         "hand_reference_w": ref_hand.tolist(),
                         "hand_net_forces_w": sim.contact_forces[:, hand_ids].tolist(),
                         "box_states_wxyz": box.tolist(),
                         "joint_error_max": (sim.dof_pos-cmd.joint_pos).abs().amax(-1).tolist()})
            print("CONTACT MAX", step, float(sim.contact_sensor.data.net_forces_w.abs().max()),
                  "sensor shapes", [list(sim.scene.sensors[f"{s}_box_contact"].data.force_matrix_w.shape) for s in ("left","right")], flush=True)
    score = (both_contact/90) - 3*max_drop - 2*(0.65-min_root).clamp_min(0)
    best = int(score.argmax())
    result = {"frames_in_crop": frames.tolist(), "original_frames": (frames+95).tolist(),
              "best_env": best, "best_original_frame": int(frames[best])+95,
              "min_root_z": min_root.tolist(), "max_box_drop": max_drop.tolist(),
              "both_contact_fraction_after_0_2s": (both_contact/90).tolist(),
              "mean_upward_box_support_n": (support/90).tolist(), "samples": rows,
              "box_mass_kg": sim._object.root_physx_view.get_masses().tolist()}
    result.update({"initial_joint_pos": target_q.tolist(), "initial_root_xyzw": initial_root.tolist(),
        "pd_target_joint_pos": pd_targets.tolist(),
        "initial_box_xyzw": initial_box.tolist(), "origins": sim.scene.env_origins.tolist(),
        "joint_names": sim.dof_names, "body_names": sim.body_names,
        "final_joint_pos": sim.dof_pos.tolist(), "final_root_xyzw": sim.robot_root_states[:].tolist(),
        "final_box_wxyz": sim._object.data.root_state_w.tolist(),
        "final_body_pos": sim._rigid_body_pos.tolist(), "final_body_quat_xyzw": sim._rigid_body_rot.tolist()})
    args.output.write_text(json.dumps(result, indent=2))
    print("SETTLING BEST", best, int(frames[best])+95, float(min_root[best]), float(max_drop[best]), float(both_contact[best]/90), flush=True)
except BaseException:
    import traceback
    traceback.print_exc()
    raise
finally:
    context.__exit__(None, None, None)
