"""Generate A-B-C-D-E whole-body trajectories only after the standing grasp gate passes."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

import numpy as np
import pinocchio as pin
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation

from common import Kinematics, SIDES, dump, load, sha


def quintic(u):
    return 10*u**3-15*u**4+6*u**5


def schedule(t,cycles,hold=1.,move=2.,low=1.):
    if t<hold: return 0.,'A'
    u=t-hold
    period=2*move+low+hold
    cycle=min(int(u/period),cycles-1)
    v=u-cycle*period
    if v<move: return quintic(v/move),'B'
    if v<move+low: return 1.,'C'
    if v<2*move+low: return 1-quintic((v-move-low)/move),'D'
    return 0.,'E'


def main():
    p=argparse.ArgumentParser();p.add_argument('--reset-state',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--depth',type=float,default=.10)
    p.add_argument('--cycles',type=int,default=1);p.add_argument('--move-seconds',type=float,default=2.)
    args=p.parse_args();reset=json.loads(args.reset_state.read_text())
    assert reset['status']=='Physics validated' and reset['validation_scope']=='standing side-grasp hold'
    assert not args.output.exists(),'Never overwrite a reference'
    k=Kinematics();q0=np.array(reset['candidate']['q_pin']);bp0=np.array(reset['candidate']['box_wxyz'][:3])
    br0=Rotation.from_quat(np.array(reset['candidate']['box_wxyz'])[ [4,5,6,3]])
    k.fk(q0)
    feet=[pin.SE3(k.frame(f'{s}_ankle_roll_link')) for s in SIDES]
    palms=[pin.SE3(k.frame(f'{s}_sphere_hand_link')) for s in SIDES]
    hand_local=[pin.SE3(br0.as_matrix().T@h.rotation,br0.inv().apply(h.translation-bp0)) for h in palms]
    nominal_rpy=Rotation.from_quat(q0[3:7]).as_euler('xyz')
    fps=50.;duration=1.+args.cycles*(2*args.move_seconds+2.)
    times=np.arange(int(round(duration*fps))+1)/fps
    lower=np.r_[q0[0]-.12,q0[1]-.08,[-.22,-.25,-.2],k.model.lowerPositionLimit[7:]+.0001,
                 bp0-[.06,.04,args.depth+.03],[-.1,-.1,-.1]]
    upper=np.r_[q0[0]+.12,q0[1]+.08,[.22,.25,.2],k.model.upperPositionLimit[7:]-.0001,
                 bp0+[.06,.04,.03],[.1,.1,.1]]
    x=np.r_[q0[:2],nominal_rpy,q0[7:],bp0,np.zeros(3)]
    qs=[];boxes=[];bquats=[];logs=[];phases=[]
    mass=sum(i.mass for i in k.model.inertias)
    initial_com=pin.centerOfMass(k.model,k.data,q0).copy()
    target_com=(mass*initial_com+1.1*bp0)/(mass+1.1)
    for i,t in enumerate(times):
        h,phase=schedule(t,args.cycles,move=args.move_seconds)
        depth=args.depth*h;height=q0[2]-depth
        target_bp=bp0+np.array([-.015*h,0.,-depth])
        # Waist, trunk, and arms remain optimization variables. Original grasp geometry is constrained in SE(3).
        target_j=q0[7:].copy();target_j[14]+=.06*h;target_j[12]+=.015*np.sin(np.pi*h)
        target_j[3]+=.40*h;target_j[9]+=.40*h
        def unpack(z):
            q=np.r_[z[:2],height,Rotation.from_euler('xyz',z[2:5]).as_quat(),z[5:34]]
            return q,z[34:37],Rotation.from_rotvec(z[37:40])*br0
        def residual(z):
            q,bp,br=unpack(z);k.fk(q);r=[]
            for side,foot,hl in zip(SIDES,feet,hand_local):
                f=k.frame(f'{side}_ankle_roll_link')
                r.extend(150*(f.translation-foot.translation));r.extend(20*pin.log3(foot.rotation.T@f.rotation))
                palm=k.frame(f'{side}_sphere_hand_link');tar=pin.SE3(br.as_matrix()@hl.rotation,bp+br.apply(hl.translation))
                r.extend(150*(palm.translation-tar.translation));r.extend(15*pin.log3(tar.rotation.T@palm.rotation))
            com=pin.centerOfMass(k.model,k.data,q);combined=(mass*com+1.1*bp)/(mass+1.1)
            r.extend(25*(combined[:2]-target_com[:2]))
            r.extend(5*(z[2:5]-nominal_rpy));r.extend(.8*(z[5:34]-target_j))
            r.extend(2*(z[17:20]-target_j[12:15]))
            r.extend(20*(bp-target_bp));r.extend(5*z[37:40])
            r.extend(1.*(z-x))
            r.extend(150*k.collision_residual(bp,br))
            return np.array(r)
        step_limits=np.r_[.003,.003,[.01,.01,.01],np.full(29,.025),[.003,.003,.003],[.01,.01,.01]]
        local_lower=np.maximum(lower,x-step_limits);local_upper=np.minimum(upper,x+step_limits)
        fit=least_squares(residual,np.clip(x,local_lower+1e-8,local_upper-1e-8),bounds=(local_lower,local_upper),max_nfev=50,ftol=1e-8,xtol=1e-8)
        x=fit.x.copy();q,bp,br=unpack(x)
        qs.append(q);boxes.append(bp);bquats.append(br.as_quat()[[3,0,1,2]]);phases.append(phase)
        k.fk(q)
        errors=[np.linalg.norm(k.frame(f'{s}_sphere_hand_link').translation-(bp+br.apply(hl.translation))) for s,hl in zip(SIDES,hand_local)]
        torque,wrench=k.static_torque(q,1.1,reset['candidate']['squeeze_n'],np.array(reset['candidate']['inward_normals']))
        logs.append(dict(frame=i,phase=phase,cost=float(fit.cost),palm_position_error_m=list(map(float,errors)),
            inverse_static_torque_limit_fraction=float(np.max(np.abs(torque)/np.array(k.base.robot.dof_effort_limit_list))),
            foot_vertical_support_n=wrench.reshape(2,6)[:,2].tolist()))
        if i%50==0: print(i,phase,'depth',depth,'palm errors',errors,flush=True)
    out=k.export(args.output,qs,boxes,bquats,fps)
    dump(args.output.with_suffix('.json'),dict(status='Kinematic only',reset_state=str(args.reset_state.resolve()),
        reset_sha256=sha(args.reset_state),cycles=args.cycles,requested_pelvis_excursion_m=args.depth,
        actual_reference_excursion_m=float(np.ptp(out['joint_pos'][:,2])),frames=len(qs),fps=fps,
        phases=phases,move_seconds=args.move_seconds,optimization='Per-frame full 29-DoF + floating pelvis + box SE(3) nonlinear least squares; fixed feet, hand-box SE(3), COM, torso collision, continuity, limits; inverse statics audit',
        per_frame_optimization=logs))


if __name__=='__main__':main()
