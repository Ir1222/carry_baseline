"""Offline motion-quality diagnostics and plots; never participates in actor control."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.spatial.transform import Rotation


def analyze(output,reference):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    bank=[]
    for p in sorted((reference/'motions').glob('*.npz')):
        with np.load(p) as d:
            q=d['joint_pos'];v=d['joint_vel']
            yaw=Rotation.from_quat(q[:,[4,5,6,3]]).as_euler('xyz')[:,2]
            vx=np.cos(yaw)*v[:,0]+np.sin(yaw)*v[:,1]
            bank.append(dict(q=q[:,7:],h=q[:,2],vz=v[:,2],vx=vx))
    bank={k:np.concatenate([b[k] for b in bank]) for k in bank[0]}
    summary={}
    for p in sorted(output.glob('*_rollout.npz')):
        with np.load(p) as d:
            metrics=[];dt=.02
            for i in range(d['q'].shape[1]):
                active=d['alive'][:,i].astype(bool)
                q=d['q'][active,i];root=d['root'][active,i];h=root[:,2]
                trend=np.gradient(h,dt) if len(h)>1 else np.zeros_like(h)
                goal=d['goal'][active,i]
                distance=((h[:,None]-bank['h'])/.04)**2+((trend[:,None]-bank['vz'])/.06)**2+((goal[:,0,None]-bank['vx'])/.15)**2
                distance+=5*(trend[:,None]*bank['vz']<-.0002)
                idx=distance.argmin(-1)
                error=q-bank['q'][idx]
                qd=d['qd'][active,i]
                accel=np.diff(qd,axis=0)/dt
                box=d['box'][active,i]
                rel=Rotation.from_quat(root[:,3:7]).inv().apply(box[:,:3]-root[:,:3])
                rotation=(Rotation.from_quat(root[:,3:7]).inv()*Rotation.from_quat(box[:,3:7]))
                angular=(rotation*rotation[0].inv()).magnitude()
                metrics.append(dict(seed_index=i,upper_body_style_rmse_rad=float(np.sqrt(np.mean(error[:,12:]**2))),
                    lower_body_style_rmse_rad=float(np.sqrt(np.mean(error[:,:12]**2))),
                    reference_compatibility_mean=float(np.exp(-.25*distance.min(-1)).mean()),
                    joint_acceleration_rms_rad_s2=float(np.sqrt(np.mean(accel**2))) if len(accel) else None,
                    box_relative_translation_drift_max_m=float(np.linalg.norm(rel-rel[0],axis=-1).max()),
                    box_relative_rotation_drift_max_rad=float(angular.max())))
            summary[p.stem]=metrics
            t=d['time'][:,0];mask=d['alive'][:,0].astype(bool);t=t[mask]
            fig,axes=plt.subplots(4,1,figsize=(9,9),sharex=True)
            axes[0].plot(t,d['root'][mask,0,2],label='actual pelvis');axes[0].plot(t,d['goal'][mask,0,3],label='command');axes[0].set_ylabel('height (m)')
            axes[1].plot(t,d['goal'][mask,0,0]+d['error'][mask,0,0],label='actual vx');axes[1].plot(t,d['goal'][mask,0,0],label='command');axes[1].set_ylabel('vx (m/s)')
            axes[2].plot(t,d['left_hand_normal_n'][mask,0],label='left normal');axes[2].plot(t,d['right_hand_normal_n'][mask,0],label='right normal');axes[2].set_ylabel('normal (N)')
            axes[3].plot(t,d['box_clearance_m'][mask,0],label='box bottom');axes[3].axhline(.03,color='r',ls='--',label='failure threshold');axes[3].set_ylabel('clearance (m)');axes[3].set_xlabel('time (s)')
            for ax in axes:ax.legend();ax.grid(alpha=.2)
            fig.suptitle(p.stem+' (includes terminal failure; seed 0)');fig.tight_layout();fig.savefig(output/(p.stem+'.png'),dpi=150);plt.close(fig)
    (output/'motion_quality.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    p.add_argument('--reference',type=Path,default=Path(__file__).resolve().parents[3]/'artifacts/fullbody_goal_carry/reference_v1')
    a=p.parse_args();print(json.dumps(analyze(a.output,a.reference),indent=2))
