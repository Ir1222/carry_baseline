"""Continuous task rewards; no destination or one-time success bonus."""
import torch
from holosoma.carry.observations import simulator_box_state
from holosoma.utils.rotations import quat_rotate_inverse, quaternion_to_matrix, yaw_quat


def task_errors(env):
    root = env.simulator.robot_root_states[:]
    velocity = quat_rotate_inverse(yaw_quat(root[:, 3:7], w_last=True), root[:, 7:10], w_last=True)
    state = torch.cat([velocity[:, :2], root[:, 12:13],
        root[:, 2:3]-env.simulator.scene.env_origins[:, 2:3]], -1)
    return state - env.command_manager.get_state("motion_command").task_command


def contact_quality(env):
    forces = env.simulator.hand_box_forces()
    each = torch.linalg.vector_norm(forces, dim=-1)
    # Sensor force is on the hand; its negative is the force on the box.
    upward = (-forces[:, :, 2].sum(-1)).clamp_min(0)
    if not hasattr(env, "carry_box_mass"):
        env.carry_box_mass = env.simulator._object.root_physx_view.get_masses().to(env.device).flatten()
    bilateral = (each.min(dim=-1).values/(.35*env.carry_box_mass*9.81)).clamp(0, 1)
    return bilateral * (upward/(env.carry_box_mass*9.81)).clamp(0, 1)


def carrying_gate(env):
    root = env.simulator.robot_root_states[:]
    box = simulator_box_state(env)
    above_ground = (box[:, 2]-env.simulator.scene.env_origins[:, 2]) > .4
    close = torch.linalg.vector_norm(box[:, :3]-root[:, :3], dim=-1) < .9
    return (above_ground & close).float()


def velocity_tracking(env, sigma=0.2):
    e = task_errors(env)
    return torch.exp(-e[:, :2].square().sum(-1)/sigma**2)*carrying_gate(env)


def yaw_tracking(env, sigma=0.3):
    return torch.exp(-task_errors(env)[:, 2].square()/sigma**2)*carrying_gate(env)


def height_tracking(env, sigma=0.05):
    return torch.exp(-task_errors(env)[:, 3].square()/sigma**2)*carrying_gate(env)


def stable_carry(env):
    root = env.simulator.robot_root_states[:]
    box = simulator_box_state(env)
    rel = box[:, :3]-root[:, :3]
    omega = torch.zeros_like(root[:, 10:13]); omega[:, 2] = root[:, 12]
    v = box[:, 7:10]-root[:, 7:10]-torch.linalg.cross(omega, rel)
    height_error = (rel[:, 2]-.25).abs().sub(.25).clamp_min(0)
    return torch.exp(-v.square().sum(-1)/.5**2-height_error.square()/.1**2)*carrying_gate(env)


def box_orientation(env):
    box = simulator_box_state(env)
    root = env.simulator.robot_root_states[:]
    # Reference mesh is carried with local Z down. Both faces are physically level.
    vertical = quaternion_to_matrix(box[:, 3:7], w_last=True)[:, 2, 2].abs()
    relative_omega = box[:, 10:13]-root[:, 10:13]
    return torch.exp(-(1-vertical)/.08-relative_omega.square().sum(-1)/2.0**2)*carrying_gate(env)


def hand_support(env):
    return contact_quality(env)*carrying_gate(env)
