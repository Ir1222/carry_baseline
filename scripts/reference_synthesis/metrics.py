"""Hard acceptance gates, computed from free-body physics rather than reference poses."""
from __future__ import annotations
import numpy as np
from scipy.spatial.transform import Rotation

THRESHOLDS=dict(min_box_clearance_m=.03,max_box_tracking_error_m=.04,max_hand_slip_m=.025,
    max_foot_slip_m=.03,max_root_tilt_rad=.25,max_joint_tracking_error_rad=.18,
    min_side_normal_n=.5,min_upward_friction_weight_ratio=.8,max_contact_gap_s=.02,
    max_other_box_contact_n=.5,max_joint_limit_violation_rad=.005,min_squat_excursion_m=.08,
    max_pelvis_tracking_error_m=.03,max_root_horizontal_error_m=.04,
    max_hand_relative_rotation_error_rad=.20,max_box_rotation_error_rad=.20,
    max_total_contact_loss_fraction=.01,max_end_height_error_m=.02,
    max_contact_side_error_m=.025,max_normal_vertical_fraction=.35,
    min_contact_height_above_box_bottom_m=.05,max_torque_limit_fraction=1.0001,max_joint_velocity_limit_fraction=1.01)


def longest_false_run(mask,dt):
    maximum=run=0
    for val in mask:
        run=0 if val else run+1
        maximum=max(maximum,run)
    return maximum*dt


def summarize(a,entries,limits,k,args):
    dt=args.dt; results=[]; t=a['time']; evalmask=t>=.10
    initial_root=np.array([e['q_pin'][:3] for e in entries])
    initial_box=np.array([e['box_wxyz'][:3] for e in entries])
    for i,e in enumerate(entries):
        n=a['normal_force_on_hand'][:,i]; f=a['friction_force_on_hand'][:,i]
        normal=np.linalg.norm(n,axis=-1)
        inward=np.array(e['inward_normals'])
        side_compression=-np.sum(n*inward[None],axis=-1)
        upward=-f[:,:,2].sum(-1)/(1.1*9.81)
        contact=side_compression>THRESHOLDS['min_side_normal_n']
        slip=np.linalg.norm(a['hand_local'][:,i]-a['hand_local'][0,i],axis=-1)
        box_rot=Rotation.from_quat(a['object'][:,i][:,[4,5,6,3]])
        hand_rot=[]
        for j in range(2):
            relative=box_rot.inv()*Rotation.from_quat(a['hand_quat'][:,i,j][:,[1,2,3,0]])
            hand_rot.append((relative*relative[0].inv()).magnitude())
        feet=np.linalg.norm(a['foot_pos'][:,i,:,:2]-a['foot_pos'][0,i,:,:2],axis=-1)
        root=a['root'][:,i]; obj=a['object'][:,i]; q=a['joint_pos'][:,i]
        tilt=np.linalg.norm(Rotation.from_quat(root[:,[4,5,6,3]]).as_euler('xyz')[:,:2],axis=-1)
        jerr=np.max(np.abs(q-a['target_joint_pos'][:,i]),axis=-1)
        jlimit=np.maximum(k.model.lowerPositionLimit[7:]-q,q-k.model.upperPositionLimit[7:])
        target_obj=np.tile(initial_box[i],(len(t),1))
        target_rot=Rotation.from_quat(np.tile(np.array(e['box_wxyz'])[[4,5,6,3]],(len(t),1)))
        if args.motion:
            from common import load
            m=load(args.motion);mt=a.get('motion_time',t)
            idx=np.minimum(np.round(mt*float(m['fps'].item())).astype(int),len(m['joint_pos'])-1)
            target_obj=m['object_pos_w'][idx]
            target_rot=Rotation.from_quat(m['object_quat_w'][idx][:,[1,2,3,0]])
        berr=np.linalg.norm(obj[:,:3]-target_obj,axis=-1)
        gaps=[longest_false_run(contact[evalmask,j],dt) for j in range(2)]
        cp=a['contact_pos'][:,i]
        contact_local=np.stack([box_rot.inv().apply(cp[:,j]-obj[:,:3]) for j in range(2)],axis=1)
        obb_contact=contact_local@k.obb[:3,:3].T+k.obb[:3,3]
        valid=np.isfinite(cp).all(-1)&contact
        side_error=np.abs(obb_contact[:,:,0]-np.array([1.,-1.])[None]*k.obb_size[0]/2)
        vertical=np.abs(n[:,:,2])/np.maximum(normal,1e-6)
        clearance=cp[:,:,2]-a['box_bottom'][:,i,None]
        values=dict(candidate_id=e['id'],squeeze_n=e['squeeze_n'],duration_s=float(t[-1]),
            min_box_clearance_m=float(a['box_bottom'][:,i].min()),max_box_tracking_error_m=float(berr.max()),
            max_hand_slip_m=float(slip.max()),max_foot_slip_m=float(feet.max()),max_root_tilt_rad=float(tilt.max()),
            max_joint_tracking_error_rad=float(jerr.max()),max_joint_limit_violation_rad=float(max(0.,jlimit.max())),
            contact_fraction=contact[evalmask].mean(0).tolist(),max_contact_gap_s=gaps,
            min_side_normal_n=side_compression[evalmask].min(0).tolist(),
            mean_upward_friction_weight_ratio=float(upward[evalmask].mean()),
            min_upward_friction_weight_ratio=float(upward[evalmask].min()),
            max_other_box_contact_n=float(np.linalg.norm(a['other_box_normal'][:,i],axis=-1).max()),
            root_height_min_m=float(root[:,2].min()),root_height_max_m=float(root[:,2].max()),
            pelvis_excursion_m=float(root[:,2].max()-root[:,2].min()),
            torque_limit_fraction_max=float(np.max(np.abs(a['torque'][:,i])/limits)),
            max_torque_limit_fraction=float(np.max(np.abs(a['torque'][:,i])/limits)),
            max_joint_velocity_limit_fraction=float(np.max(np.abs(a['joint_vel'][:,i])/np.array(k.base.robot.dof_vel_limit_list))),
            max_pelvis_tracking_error_m=float(np.max(abs(root[:,2]-a['target_root'][:,i,2]))),
            max_root_horizontal_error_m=float(np.linalg.norm(root[:,:2]-a['target_root'][:,i,:2],axis=-1).max()),
            max_hand_relative_rotation_error_rad=float(np.max(hand_rot)),
            max_box_rotation_error_rad=float((box_rot*target_rot.inv()).magnitude().max()),
            max_total_contact_loss_fraction=float(1-contact[evalmask].mean(0).min()),
            max_end_height_error_m=float(abs(root[-1,2]-a['target_root'][-1,i,2])),
            max_contact_side_error_m=float(side_error[valid].max()) if valid.any() else 1.,
            max_normal_vertical_fraction=float(vertical[valid].max()) if valid.any() else 1.,
            min_contact_height_above_box_bottom_m=float(clearance[valid].min()) if valid.any() else 0.,
            foot_ground_contact_fraction=(np.linalg.norm(a['foot_normal'][evalmask,i],axis=-1)>5).mean(0).tolist(),
            initial_transient=dict(seconds=.1,contact_fraction=contact[~evalmask].mean(0).tolist()),
            final_box_velocity_m_s=float(np.linalg.norm(obj[-1,7:10])),final_root_velocity_m_s=float(np.linalg.norm(root[-1,7:10])))
        failures=[]
        for key,threshold in THRESHOLDS.items():
            if key in values and key.startswith('max_') and np.max(values[key])>threshold:
                failures.append(key)
        if values['min_box_clearance_m']<THRESHOLDS['min_box_clearance_m']: failures.append('box_ground_clearance')
        if max(gaps)>THRESHOLDS['max_contact_gap_s']: failures.append('contact_interruption')
        if values['mean_upward_friction_weight_ratio']<THRESHOLDS['min_upward_friction_weight_ratio']: failures.append('insufficient_friction_support')
        if args.motion and values['pelvis_excursion_m']<THRESHOLDS['min_squat_excursion_m']: failures.append('insufficient_squat_excursion')
        if not args.motion and abs(root[-1,2]-initial_root[i,2])>.03: failures.append('standing_height_drift')
        if values['final_box_velocity_m_s']>.12: failures.append('not_settled_box')
        if values['final_root_velocity_m_s']>.10: failures.append('not_settled_robot')
        if min(values['foot_ground_contact_fraction'])<.95: failures.append('foot_contact_loss')
        if values['min_contact_height_above_box_bottom_m']<THRESHOLDS['min_contact_height_above_box_bottom_m']:failures.append('contact_near_box_bottom')
        if args.motion:
            import json
            meta=json.loads(args.motion.with_suffix('.json').read_text())
            phase=np.array(meta['phases'])[idx]
            if 'motion_time' in a:
                phase=phase.astype('<U8');phase[a['motion_time']<=0]='Warmup'
            values['phases']=[]
            starts=np.r_[0,np.where(phase[1:]!=phase[:-1])[0]+1]
            ends=np.r_[starts[1:],len(phase)]
            for begin,end in zip(starts,ends):
                label=str(phase[begin]);segment=root[begin:end,2]
                values['phases'].append(dict(phase=label,start_s=float(t[begin]),end_s=float(t[end-1]),
                    pelvis_start_m=float(segment[0]),pelvis_end_m=float(segment[-1]),height_range_m=float(np.ptp(segment)),
                    box_bottom_min_m=float(a['box_bottom'][begin:end,i].min())))
                if label=='B' and segment[0]-segment[-1]<.08:failures.append('incomplete_squat_down')
                if label=='D' and segment[-1]-segment[0]<.08:failures.append('incomplete_stand_up')
                if label=='C' and np.ptp(segment)>.015:failures.append('unstable_low_hold')
            if not set('ABCDE').issubset(set(phase)):failures.append('missing_phase')
        values['failures']=failures;values['status']='Physics validation failed' if failures else 'Physics validated'
        results.append(values)
    best=min(range(len(results)),key=lambda i:(len(results[i]['failures']),results[i]['max_hand_slip_m']+results[i]['max_box_tracking_error_m']))
    return dict(thresholds=THRESHOLDS,acceptance_scope='Full interval ground/limits/slip; first 0.1 s contact engagement recorded separately, then <=20ms contact gap; friction support is episode mean after engagement.',
        summary=dict(passed=sum(x['status']=='Physics validated' for x in results),tested=len(results),best_env=best,best=results[best]),results=results)
