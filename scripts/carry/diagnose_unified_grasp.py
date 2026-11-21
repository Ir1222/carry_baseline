"""Bounded arm-only IK feasibility study. Output poses are NOT a motion or admitted dataset."""
import argparse,json,sys
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    repo=Path(__file__).resolve().parents[2];sys.path.insert(0,str(repo/'scripts/reference_synthesis'))
    from common import Kinematics,to_pin
    k=Kinematics();source=np.load(repo/'datasets/unified_hoi_v1/motions/full_sequence.npz');squat=np.load(repo/'datasets/unified_hoi_v1/motions/continuous_grasped_squat_stand.npz')
    k.fk(to_pin(squat['joint_pos'][0]));br=Rotation.from_quat(squat['object_quat_w'][0,[1,2,3,0]]);bp=squat['object_pos_w'][0]
    targets=[(br.inv().apply(k.frame(side+'_sphere_hand_link').translation-bp),br.as_matrix().T@k.frame(side+'_sphere_hand_link').rotation) for side in ['left','right']]
    rows=[];poses=[]
    for frame in [95,125,155,185,204]:
        q=to_pin(source['joint_pos'][frame]);initial=q[22:].copy();boxr=Rotation.from_quat(source['object_quat_w'][frame,[1,2,3,0]]);boxp=source['object_pos_w'][frame]
        def errors(x):
            candidate=q.copy();candidate[22:]=x;k.fk(candidate);out=[]
            for side,(pos,rot) in zip(['left','right'],targets):
                h=k.frame(side+'_sphere_hand_link');out.extend(100*(h.translation-boxp-boxr.apply(pos)));out.extend(10*Rotation.from_matrix((boxr.as_matrix()@rot).T@h.rotation).as_rotvec())
            return np.r_[out,.01*(x-initial)]
        lower=k.model.lowerPositionLimit[22:]+1e-5;upper=k.model.upperPositionLimit[22:]-1e-5
        # Two documented optimizer initial guesses only; never overwrite source poses.
        seeds=[initial,to_pin(squat['joint_pos'][0])[22:]]
        fits=[least_squares(errors,np.clip(seed,lower,upper),bounds=(lower,upper),max_nfev=80) for seed in seeds]
        fit=min(fits,key=lambda f:f.cost)
        q[22:]=fit.x;k.fk(q);poseerrors=[]
        for side,(pos,rot) in zip(['left','right'],targets):
            h=k.frame(side+'_sphere_hand_link');poseerrors.append(dict(position_m=float(np.linalg.norm(h.translation-boxp-boxr.apply(pos))),rotation_rad=float(Rotation.from_matrix((boxr.as_matrix()@rot).T@h.rotation).magnitude())))
        rows.append(dict(frame=frame,converged=bool(fit.success),evaluations=fit.nfev,optimizer_initial_guesses=['original arms','P0 arms, optimizer seed bounded inside hard limits'],
            initial_guess_costs=[float(f.cost) for f in fits],hand_errors=poseerrors,max_arm_change_rad=float(abs(fit.x-initial).max())))
        poses.append(q)
    np.savez_compressed(a.output/'diagnostic_pose_candidates.npz',q_pinocchio_xyzw=poses,source_frames=[95,125,155,185,204])
    report=dict(scope='arm-only pose IK feasibility, NOT physics validation or deployable controller',physics_validated=False,training_admitted=False,
        unchanged='root, all leg joints and waist fixed at each original source frame; box unchanged',missing_checks=['full timeline continuity','nonhand collisions','torque-limited contact dynamics','pickup/putdown root-foot balance'],results=rows)
    (a.output/'ik_diagnosis.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(rows))

if __name__=='__main__':main()
