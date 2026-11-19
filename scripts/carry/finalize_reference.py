"""Validate INITIAL settling and retarget the carry-only crop to the MVP carton.

This does not certify sustained open-loop balance or a trained carrying policy.
Only reference targets are retargeted: runtime box motion is always free physics.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

import numpy as np
import pinocchio as pin
from scipy.spatial.transform import Rotation

ROOT = Path(__file__).resolve().parents[2]


def angular_velocity(quats, fps):
    r = Rotation.from_quat(quats[:, [1, 2, 3, 0]])
    a = np.maximum(np.arange(len(quats))-1, 0)
    b = np.minimum(np.arange(len(quats))+1, len(quats)-1)
    return (r[b]*r[a].inv()).as_rotvec() * (fps/(b-a))[:, None]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--settling-report', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = json.loads(args.settling_report.read_text())
    sample = next(s for s in report['samples'] if abs(s['time_s']-.2) < 1e-6)
    box = np.array(sample['box_states_wxyz'])
    forces = np.array(sample['hand_forces_w'])
    assert len(box) == 64 and np.isfinite(box).all() and np.isfinite(forces).all()
    drop = np.array(report['initial_box_xyzw'])[:, 2]-box[:, 2]
    support = -forces[:, :, 2].sum(-1)
    mass = np.array(report['box_mass_kg']).reshape(-1)
    assert max(drop) < .02, 'Initial settling drop exceeds 2 cm'
    assert min(sample['root_z']) > .70
    assert np.linalg.norm(forces, axis=-1).min() > 1., 'Each hand must support the box'
    assert np.min(support/(mass*9.81)) > .65
    assert np.min(1-2*(box[:, 4]**2+box[:, 5]**2)) > .98
    assert np.linalg.norm(box[:, 7:10], axis=-1).max() < .6
    assert np.linalg.norm(box[:, 10:13], axis=-1).max() < 1.5
    assert not report['balance_feedback'], 'Initial settling must use fixed PD targets only'
    manifest = json.loads((args.source/'manifest.json').read_text())
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output/'motions').mkdir()
    root = np.array(report['initial_root_xyzw'][0]); root[:3] -= report['origins'][0]
    obj = np.array(report['initial_box_xyzw'][0]); obj[:3] -= report['origins'][0]
    pose = dict(physics_verified=True, validation_scope='64 resets; first 0.2 s fixed PD initial settling only',
        sustained_hold_verified=False, root_xyzw=root.tolist(), box_xyzw=obj.tolist(),
        joint_pos=report['initial_joint_pos'][0], pd_target_joint_pos=report['pd_target_joint_pos'][0],
        joint_names=report['joint_names'], p_gains=report['p_gains'], d_gains=report['d_gains'],
        box_mass_kg=manifest['box_mass_kg'], box_size_m=manifest['box_size_m'],
        evidence_sha256=hashlib.sha256(args.settling_report.read_bytes()).hexdigest(),
        initial_settling_metrics=dict(max_drop_m=float(max(drop)), min_root_height_m=float(min(sample['root_z'])),
            min_hand_force_n=float(np.linalg.norm(forces,axis=-1).min()),
            min_support_weight_ratio=float(np.min(support/(mass*9.81)))))
    (args.output/'verified_reset.json').write_text(json.dumps(pose, indent=2))
    shutil.copyfile(args.source/'carry_box.urdf', args.output/'carry_box.urdf')
    model = pin.buildModelFromUrdf(str(ROOT/'src/holosoma/holosoma/data/robots/g1/main_mesh_collision_halfspherehand.urdf'), pin.JointModelFreeFlyer())
    pdata = model.createData()
    from holosoma.config_values.wbt.g1.experiment import g1_29dof_wbt_hybrid_object
    names = g1_29dof_wbt_hybrid_object.robot.body_names
    frame_ids = [model.getFrameId(n, pin.FrameType.BODY) for n in names]
    assert max(frame_ids) < model.nframes
    assert list(model.names)[2:] == pose['joint_names']
    box_local = Rotation.from_quat(root[3:7]).inv().apply(obj[:3]-root[:3])
    box_local_rot = Rotation.from_quat(root[3:7]).inv()*Rotation.from_quat(obj[3:7])

    def rebuild(q, fps):
        n = len(q)
        pos = np.empty((n, len(names), 3)); quat = np.empty((n, len(names), 4))
        for t in range(n):
            pq = np.r_[q[t, :3], q[t, [4, 5, 6, 3]], q[t, 7:]]
            pin.framesForwardKinematics(model, pdata, pq)
            for b, f in enumerate(frame_ids):
                pos[t, b] = pdata.oMf[f].translation
                quat[t, b] = Rotation.from_matrix(pdata.oMf[f].rotation).as_quat()[[3, 0, 1, 2]]
        rot = Rotation.from_quat(q[:, [4, 5, 6, 3]])
        opos = q[:, :3]+rot.apply(np.broadcast_to(box_local,(n,3)))
        oq = (rot*box_local_rot).as_quat()[:, [3,0,1,2]]
        body_vel = np.gradient(pos, 1/fps, axis=0)
        body_ang = np.stack([angular_velocity(quat[:, i],fps) for i in range(len(names))],axis=1)
        return dict(fps=np.array([fps]), joint_names=np.array(pose['joint_names']),body_names=np.array(names),
            joint_pos=q.astype(np.float32), joint_vel=np.column_stack([np.gradient(q[:,:3],1/fps,axis=0),
                angular_velocity(q[:,3:7],fps),np.gradient(q[:,7:],1/fps,axis=0)]).astype(np.float32),
            body_pos_w=pos.astype(np.float32), body_quat_w=quat.astype(np.float32),
            body_lin_vel_w=body_vel.astype(np.float32),body_ang_vel_w=body_ang.astype(np.float32),
            object_pos_w=opos.astype(np.float32), object_quat_w=oq.astype(np.float32),
            object_lin_vel_w=np.gradient(opos,1/fps,axis=0).astype(np.float32),object_ang_vel_w=angular_velocity(oq,fps).astype(np.float32))

    outputs = []
    for source in sorted((args.source/'motions').glob('*.npz')):
        data = np.load(source); q = data['joint_pos'].copy()
        # Keep measured carry-only root and leg motion; regenerate torso, arms,
        # every tracked body transform and object reference for the smaller box.
        q[:, 7+12:] = np.array(pose['joint_pos'])[12:]
        result = rebuild(q,float(data['fps'].item()))
        np.savez_compressed(args.output/'motions'/source.name, **result)
        outputs.append(dict(file=source.name,frames=len(q),kind='retargeted carry-only root/legs'))
    holdq = np.r_[root[:3],root[[6,3,4,5]],pose['joint_pos']]
    result = rebuild(np.tile(holdq,(200,1)),50.)
    np.savez_compressed(args.output/'motions'/'verified_hold.npz', **result)
    outputs.append(dict(file='verified_hold.npz',frames=200,kind='static reset imitation target; not a learned hold policy'))
    manifest['retargeting'] = dict(outputs=outputs,description='MVP palm support posture + FK; original carry-only root/legs preserved',
        limitation='Moving retargeted clips remain kinematic references, not certified dynamically feasible trajectories')
    manifest['reset_validation'] = pose['initial_settling_metrics']
    (args.output/'manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps(dict(output=str(args.output),initial_settling=pose['initial_settling_metrics'],motions=outputs),indent=2))


if __name__ == '__main__':
    main()
