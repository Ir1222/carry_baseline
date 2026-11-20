"""Export measured physics motion, figures, per-step CSV, and an evidence summary."""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation

from common import OUTPUT, Kinematics, dump, load, to_pin


def main():
    p=argparse.ArgumentParser();p.add_argument('--evidence',type=Path,required=True)
    p.add_argument('--env',type=int);p.add_argument('--motion',type=Path)
    args=p.parse_args();evidence=args.evidence.resolve()
    a=load(evidence/'rollout.npz');v=json.loads((evidence/'validation.json').read_text())
    entries=json.loads((evidence/'candidates.json').read_text());i=args.env if args.env is not None else v['summary']['best_env']
    t=a['time'];dt=float(t[1]-t[0]);k=Kinematics();c=entries[i]
    indices=np.arange(0,len(t),max(1,int(round(.02/dt))))
    q=np.c_[a['root'][indices,i,:7],a['joint_pos'][indices,i]]
    k.export(evidence/f'actual_motion_env_{i:03d}.npz',to_pin(q),a['object'][indices,i,:3],a['object'][indices,i,3:7],50.)
    if args.motion:
        m=load(args.motion);mi=np.minimum(np.round(a.get('motion_time',t)*float(m['fps'].item())).astype(int),len(m['joint_pos'])-1)
        bp=m['object_pos_w'][mi];reference=str(args.motion.resolve())
    else:
        bp=np.tile(np.array(c['box_wxyz'][:3]),(len(t),1));reference=None
        k.export(evidence/'hold_reference.npz',np.tile(c['q_pin'],(101,1)),np.tile(c['box_wxyz'][:3],(101,1)),np.tile(c['box_wxyz'][3:7],(101,1)))
    normal=np.linalg.norm(a['normal_force_on_hand'][:,i],axis=-1)
    support=-a['friction_force_on_hand'][:,i,:,2]
    slip=np.linalg.norm(a['hand_local'][:,i]-a['hand_local'][0,i],axis=-1)
    jerror=np.abs(a['joint_pos'][:,i]-a['target_joint_pos'][:,i]).max(-1)
    berror=np.linalg.norm(a['object'][:,i,:3]-bp,axis=-1)
    rpy=Rotation.from_quat(a['root'][:,i][:,[4,5,6,3]]).as_euler('xyz')
    brot=Rotation.from_quat(a['object'][:,i][:,[4,5,6,3]])
    angles=[]
    for h in range(2):
        relative=brot.inv()*Rotation.from_quat(a['hand_quat'][:,i,h][:,[1,2,3,0]])
        angles.append((relative*relative[0].inv()).magnitude())
    cols=dict(time_s=t,pelvis_height_m=a['root'][:,i,2],target_pelvis_height_m=a['target_root'][:,i,2],
        box_center_height_m=a['object'][:,i,2],target_box_center_height_m=bp[:,2],box_bottom_m=a['box_bottom'][:,i],
        left_normal_n=normal[:,0],right_normal_n=normal[:,1],left_upward_friction_n=support[:,0],right_upward_friction_n=support[:,1],
        left_slip_m=slip[:,0],right_slip_m=slip[:,1],left_relative_rotation_rad=angles[0],right_relative_rotation_rad=angles[1],
        joint_tracking_max_rad=jerror,box_tracking_m=berror,root_roll_rad=rpy[:,0],root_pitch_rad=rpy[:,1],
        other_box_contact_max_n=np.linalg.norm(a['other_box_normal'][:,i],axis=-1).max(-1))
    with (evidence/f'metrics_env_{i:03d}.csv').open('w') as f:
        writer=csv.writer(f);writer.writerow(cols);writer.writerows(zip(*cols.values()))
    figures=evidence/'figures';figures.mkdir(exist_ok=True)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.2,'legend.frameon':False})
    colors=['#0077BB','#EE7733','#009988','#CC3311']
    fig,axs=plt.subplots(3,2,figsize=(12,10),layout='constrained')
    ax=axs[0,0];ax.plot(t,cols['pelvis_height_m'],color=colors[0],label='Measured pelvis');ax.plot(t,cols['target_pelvis_height_m'],'--',color=colors[1],label='Reference');ax.set_ylabel('Pelvis height (m)');ax.legend()
    ax=axs[0,1]
    for j,s in enumerate(['Left','Right']):ax.plot(t,normal[:,j],color=colors[j],label=s)
    ax.set_ylabel('Hand normal force (N)');ax.legend()
    ax=axs[1,0];ax.plot(t,cols['box_center_height_m'],color=colors[0],label='Measured box center');ax.plot(t,bp[:,2],'--',color=colors[1],label='Reference box center');ax.plot(t,cols['box_bottom_m'],color=colors[2],label='Measured box bottom');ax.axhline(.03,color=colors[3],ls=':');ax.set_ylabel('Height (m)');ax.legend()
    ax=axs[1,1]
    for j,s in enumerate(['Left','Right']):ax.plot(t,support[:,j],color=colors[j],alpha=.7,label=s)
    ax.axhline(1.1*9.81,color=colors[2],ls='--',label='Box weight (total)');ax.set_ylabel('Upward friction on box (N)');ax.legend()
    ax=axs[2,0]
    for j,s in enumerate(['Left','Right']):ax.plot(t,slip[:,j]*1000,color=colors[j],label=s)
    ax.axhline(25,color=colors[3],ls=':');ax.set_ylabel('Hand-box translation drift (mm)');ax.legend()
    ax=axs[2,1];ax.plot(t,jerror,color=colors[0],label='Joint max error (rad)');ax.plot(t,berror,color=colors[1],label='Box position error (m)');ax.set_ylabel('Tracking error');ax.legend()
    for ax in axs.flat:ax.set_xlabel('Time (s)')
    fig.suptitle(f"{c['id']} | {v['results'][i]['status']} | actual free-body physics")
    fig.savefig(figures/f'metrics_env_{i:03d}.png',dpi=450);fig.savefig(figures/f'metrics_env_{i:03d}.svg');plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,3),layout='constrained')
    for j,s in enumerate(['Left','Right']):ax.plot(t,np.degrees(angles[j]),color=colors[j],label=s)
    ax.set(xlabel='Time (s)',ylabel='Hand-box orientation drift (degrees)');ax.legend()
    fig.savefig(figures/f'relative_orientation_env_{i:03d}.png',dpi=450);fig.savefig(figures/f'relative_orientation_env_{i:03d}.svg');plt.close(fig)
    dump(evidence/'viewer.json',dict(env=i,actual_motion=f'actual_motion_env_{i:03d}.npz',reference=reference or str(evidence/'hold_reference.npz'),
        status=v['results'][i]['status'],sampled_physics_indices=indices.tolist(),physics_metrics=v['results'][i]))
    print(json.dumps(dict(evidence=str(evidence),env=i,status=v['results'][i]['status']),indent=2))


if __name__=='__main__':main()
