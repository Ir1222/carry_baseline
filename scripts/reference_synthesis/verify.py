"""Deterministic NPZ/FK/velocity/immutability/MotionLoader verification."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

import numpy as np
import pinocchio as pin
from scipy.spatial.transform import Rotation

from common import OUTPUT, ROOT, Kinematics, angular_velocity, derivative, dump, load, sha, to_pin


def verify_motion(path,k):
    d=load(path);q=d['joint_pos'];fps=float(d['fps'].item());n=len(q)
    assert q.shape==(n,36) and d['joint_vel'].shape==(n,35)
    assert d['joint_names'].tolist()==k.joint_names
    assert len(set(d['body_names'].tolist()))==len(d['body_names'])
    for key,value in d.items():
        if value.dtype.kind=='f':assert np.isfinite(value).all(),(path,key)
    for key in ['object_quat_w','body_quat_w']:
        assert np.max(abs(np.linalg.norm(d[key],axis=-1)-1))<1e-5,(path,key)
    assert np.max(abs(np.linalg.norm(q[:,3:7],axis=-1)-1))<1e-5
    assert np.max(abs(d['joint_vel'][:,:3]-derivative(q[:,:3],fps)))<2e-4
    assert np.max(abs(d['joint_vel'][:,6:]-derivative(q[:,7:],fps)))<2e-4
    assert np.max(abs(d['object_lin_vel_w']-derivative(d['object_pos_w'],fps)))<2e-4
    assert np.max(abs(d['object_ang_vel_w']-angular_velocity(d['object_quat_w'],fps)))<2e-4
    poserr=roterr=0.
    for t,pq in enumerate(to_pin(q)):
        k.fk(pq)
        for j,name in enumerate(d['body_names'].tolist()):
            f=k.frame(name)
            poserr=max(poserr,float(np.linalg.norm(f.translation-d['body_pos_w'][t,j])))
            roterr=max(roterr,float((Rotation.from_matrix(f.rotation)*Rotation.from_quat(d['body_quat_w'][t,j,[1,2,3,0]]).inv()).magnitude()))
    assert poserr<2e-6 and roterr<2e-6,(path,poserr,roterr)
    from holosoma.managers.command.terms.wbt import MotionLoader
    loader=MotionLoader(str(path.resolve()),k.base.robot.body_names,k.joint_names,device='cpu')
    assert loader.joint_pos.shape==(n,29) and loader.body_pos_w.shape==(n,len(k.base.robot.body_names),3)
    ranges=np.ptp(q[:,7:],axis=0)
    return dict(file=str(path.resolve()),sha256=sha(path),frames=n,fps=fps,duration_s=(n-1)/fps,
        fk_position_error_max_m=poserr,fk_rotation_error_max_rad=roterr,MotionLoader_compatible=True,
        pelvis_excursion_m=float(np.ptp(q[:,2])),minimum_box_bottom_m=float(k.bottom(d['object_pos_w'],d['object_quat_w']).min()),
        joint_range_rad=dict(zip(k.joint_names,map(float,ranges))),
        upper_body_moving_joint_count=int((ranges[12:]>.001).sum()),
        joint_velocity_max_rad_s=float(np.max(abs(d['joint_vel'][:,6:]))),
        joint_acceleration_max_rad_s2=float(np.max(abs(derivative(d['joint_vel'][:,6:],fps)))))


def main():
    p=argparse.ArgumentParser();p.add_argument('--output-root',type=Path,default=OUTPUT)
    p.add_argument('--report',type=Path);args=p.parse_args();root=args.output_root.resolve();k=Kinematics()
    immutable=json.loads((root/'immutable_sources.json').read_text());protected=json.loads((root/'protected_training_files.json').read_text())
    assert all(sha(ROOT/path)==digest for path,digest in immutable.items()),'Original data/model changed'
    assert all(sha(ROOT/path)==digest for path,digest in protected.items()),'Protected training logic changed'
    results=[verify_motion(path,k) for path in sorted((root/'motions_kinematic').glob('*.npz'))]
    for path in sorted((root/'validated_motions').glob('*.npz')):results.append(verify_motion(path,k))
    result=dict(original_sources_unchanged=True,protected_training_files_unchanged=True,motions=results)
    dump(args.report or root/'format_validation.json',result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
