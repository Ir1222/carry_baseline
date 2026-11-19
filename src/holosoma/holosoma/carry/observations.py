"""Reference-free physical actor interface, usable without Isaac Sim or motion files.

All quaternions here are xyzw. Commands use SI units. History is three frames,
oldest first, zero padded on reset. Per-frame features have dimension 116.
"""
import torch
from holosoma.utils.rotations import quat_inverse, quat_mul, quat_rotate_inverse, quaternion_to_matrix, yaw_quat

FRAME_DIM = 116
HISTORY_LENGTH = 3
ACTOR_DIM = FRAME_DIM * HISTORY_LENGTH


def physical_frame(root, joint_pos, joint_vel, default_joint_pos, previous_action, box, command, ground_height):
    """Tensor-only API: root/box [N,13], q/qd/actions [N,29], commands [N,4]."""
    heading = yaw_quat(root[:, 3:7], w_last=True)
    rotate = lambda x: quat_rotate_inverse(heading, x, w_last=True)
    gravity = torch.zeros_like(root[:, :3])
    gravity[:, 2] = -1
    rel_pos = box[:, :3] - root[:, :3]
    yaw_omega = torch.zeros_like(root[:, 10:13])
    yaw_omega[:, 2] = root[:, 12]
    rel_vel = box[:, 7:10] - root[:, 7:10] - torch.linalg.cross(yaw_omega, rel_pos)
    box_q = quat_mul(quat_inverse(heading, w_last=True), box[:, 3:7], w_last=True)
    box_rotation_6d = quaternion_to_matrix(box_q, w_last=True)[:, :, :2].reshape(-1, 6)
    return torch.cat([
        rotate(root[:, 7:10]), rotate(root[:, 10:13]),
        quat_rotate_inverse(root[:, 3:7], gravity, w_last=True),
        (root[:, 2] - ground_height).unsqueeze(1),
        joint_pos-default_joint_pos, 0.1*joint_vel, previous_action,
        rotate(rel_pos), box_rotation_6d, rotate(rel_vel), rotate(box[:, 10:13]-yaw_omega),
        command,
    ], dim=-1)


def simulator_box_state(env):
    state = env.simulator._object.data.root_state_w.clone()
    state[:, 3:7] = state[:, [4, 5, 6, 3]]  # Isaac Lab wxyz -> HMI xyzw
    return state


def actor_frame(env):
    return physical_frame(env.simulator.robot_root_states[:], env.simulator.dof_pos,
        env.simulator.dof_vel, env.default_dof_pos, env.action_manager.action,
        simulator_box_state(env), env.command_manager.get_state("motion_command").task_command,
        env.simulator.scene.env_origins[:, 2])


def critic_reference(env):
    """Training-only 68D reference error and Track indicator; exactly zero in Gen."""
    cmd = env.command_manager.get_state("motion_command")
    root = env.simulator.robot_root_states[:]
    heading = yaw_quat(root[:, 3:7], w_last=True)
    rot = quat_mul(quat_inverse(heading, w_last=True), cmd.object_quat_w, w_last=True)
    reference = torch.cat([cmd.joint_pos-env.simulator.dof_pos,
        0.1*(cmd.joint_vel-env.simulator.dof_vel),
        quat_rotate_inverse(heading, cmd.object_pos_w-simulator_box_state(env)[:, :3], w_last=True),
        quaternion_to_matrix(rot, w_last=True)[:, :, :2].reshape(-1, 6),
        torch.ones(env.num_envs, 1, device=env.device)], -1)
    return torch.where(cmd.track_env_mask[:, None], reference, torch.zeros_like(reference))
