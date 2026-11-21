"""Immutable upstream audit, canonical full-body FK export and candidate phase labels."""
import argparse,hashlib,json,shutil,subprocess,sys
from pathlib import Path
import numpy as np
from scipy.spatial.transform import Rotation

REPO=Path(__file__).resolve().parents[2]
DEFAULT=REPO/'datasets/unified_hoi_v1'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def runs(mask,n=3):
    for i in range(len(mask)-n+1):
        if mask[i:i+n].all():return i
    return None

def verify(root):
    m=json.loads((root/'manifest.json').read_text());assert m['schema']=='unified_hoi_v1'
    assert set(m['family_weights'])=={'full_sequence','loaded_locomotion','loaded_squat_stand'}
    assert all(v>0 for v in m['family_weights'].values()) and abs(sum(m['family_weights'].values())-1)<1e-6
    for row in m['motions']:
        assert sha(root/row['path'])==row['sha256']
        with np.load(root/row['path']) as d:
            assert len(row['task_modes'])==len(d['joint_pos'])
            assert d['joint_pos'].shape[1]==36 and float(d['fps'].item())==50
            assert set(row['task_modes'])<={0,1,2}
            assert all(0<=f<len(d['joint_pos'])-1 for f in row['eligible_reset_frames'])
            for key in ['joint_pos','joint_vel','body_pos_w','body_quat_w','body_lin_vel_w','body_ang_vel_w','object_pos_w','object_quat_w','object_lin_vel_w','object_ang_vel_w']:
                assert np.isfinite(d[key]).all(),(row['name'],key)
    return m

def goal_ranges(root,rows):
    bymode={i:[] for i in range(3)}
    for row in rows:
        with np.load(root/row['path']) as d:
            q=d['joint_pos'];v=d['joint_vel'];yaw=Rotation.from_quat(q[:,[4,5,6,3]]).as_euler('xyz')[:,2]
            goal=np.column_stack([np.cos(yaw)*v[:,0]+np.sin(yaw)*v[:,1],-np.sin(yaw)*v[:,0]+np.cos(yaw)*v[:,1],v[:,5],q[:,2]])
            for mode in range(3):
                mask=np.array(row['task_modes'])==mode
                if mask.any():bymode[mode].append(goal[mask])
    ranges={['pickup','carry','putdown'][i]:dict(min=np.concatenate(v).min(0).tolist(),max=np.concatenate(v).max(0).tolist()) for i,v in bymode.items() if v}
    return ranges

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=DEFAULT)
    p.add_argument('--family-weights',type=float,nargs=3,default=[.3,.35,.35],metavar=('FULL','WALK','SQUAT'))
    p.add_argument('--verify-only',action='store_true');a=p.parse_args()
    if a.verify_only:print(json.dumps(verify(a.output)['family_weights']));return
    if min(a.family_weights)<=0:raise ValueError('Each motion family requires positive sampling weight')
    a.output.mkdir(parents=True,exist_ok=False);(a.output/'motions').mkdir();(a.output/'audit').mkdir()
    sys.path.insert(0,str(REPO/'scripts/reference_synthesis'))
    from common import Kinematics,to_pin
    k=Kinematics();rows=[];audits=[]
    upstream=subprocess.check_output(['git','rev-parse','upstream/main'],cwd=REPO,text=True).strip()
    prefix='src/holosoma/holosoma/data/motions/g1_29dof/whole_body_tracking/'
    for file in ['sub3_largebox_003_mj_w_obj.npz','movebox/sub3_largebox_003_mj_w_obj_reframed.npz','movebox/sub3_largebox_003_mj_w_obj_reframed_mirrored.npz']:
        path=REPO/prefix/file;raw=subprocess.check_output(['git','show',upstream+':'+prefix+file],cwd=REPO)
        if raw!=path.read_bytes():raise ValueError('Local source differs from pinned upstream: '+file)
        with np.load(path) as src:d={key:src[key].copy() for key in src.files}
        n=len(d['joint_pos']);bottom=k.bottom(d['object_pos_w'],d['object_quat_w']);gaps=[];fkerr=0.
        palm=k.palm[np.unique(np.r_[np.linspace(0,len(k.palm)-1,128).astype(int),k.palm.argmin(0),k.palm.argmax(0)])]
        for i,q in enumerate(to_pin(d['joint_pos'])):
            k.fk(q);br=Rotation.from_quat(d['object_quat_w'][i,[1,2,3,0]]);g=[]
            for side in ['left','right']:
                h=k.frame(side+'_sphere_hand_link');cloud=br.inv().apply(palm@h.rotation.T+h.translation-d['object_pos_w'][i])
                g.append(float((cloud@k.hull_equations[:,:3].T+k.hull_equations[:,3]).max(-1).min()))
            gaps.append(g)
            for j,name in enumerate(d['body_names']):
                if name in k.ids:fkerr=max(fkerr,float(np.linalg.norm(k.frame(name).translation-d['body_pos_w'][i,j])))
        gaps=np.array(gaps);speed=np.linalg.norm(d['object_lin_vel_w'],axis=1)
        near=(gaps<.03).all(-1);contact=runs(near);lift=runs(bottom>.03)
        settled=runs((np.arange(n)>205)&(abs(bottom)<.015)&(speed<.03),10)
        release=runs((np.arange(n)> (settled or n))&(gaps>.03).all(-1),3)
        phases=([dict(name='approach_reach_candidate',start=0,end=contact),
            dict(name='contact_acquisition_candidate',start=contact,end=lift),
            dict(name='lifting_candidate',start=lift,end=95)] if contact is not None and lift is not None else [dict(name='pickup_intent_unresolved',start=0,end=95)])+[
            dict(name='loaded_carry_candidate',start=95,end=205),
            dict(name='lowering_candidate',start=205,end=settled or n)]
        if settled is not None:phases.append(dict(name='support_transfer_candidate',start=settled,end=release or n))
        if release is not None:phases.append(dict(name='release_candidate',start=release,end=n))
        audit=dict(source=file,upstream_commit=upstream,source_sha256=sha(path),upstream_byte_identical=True,
            frames=n,fps=50,duration_s=(n-1)/50,original_body_fk_max_error_m=fkerr,
            contact_candidate_frame=contact,liftoff_candidate_frame=lift,settled_candidate_frame=settled,release_candidate_frame=release,
            annotation_status='kinematic candidates, not measured contact or policy success',phases=phases,
            box_bottom_min_m=float(bottom.min()),box_bottom_max_m=float(bottom.max()),
            root_translation_m=float(np.linalg.norm(d['joint_pos'][-1,:2]-d['joint_pos'][0,:2])),
            missing=['carry_squat_walk_transition']+(['contact_acquisition'] if contact is None else [])+(['support_transfer'] if settled is None else [])+(['release'] if release is None else []),ambiguous=['approach is primarily reach/crouch; not a demonstrated long walking approach'])
        audits.append(audit)
        tag=Path(file).stem
        np.savez_compressed(a.output/'audit'/('timeline_'+tag+'.npz'),frame=np.arange(n),time=np.arange(n)/50,
            box_bottom=bottom,object_speed=speed,hand_vertex_signed_gap=gaps,root=d['joint_pos'][:,:7],object_pos=d['object_pos_w'],object_quat=d['object_quat_w'])
        if 'reframed' not in file:continue
        suffix='_mirrored' if 'mirrored' in file else ''
        for family,start,end,weight in [('full_sequence',0,n,.15),('loaded_locomotion',95,205,.175)]:
            name=family+suffix;dest=a.output/'motions'/(name+'.npz')
            k.export(dest,to_pin(d['joint_pos'][start:end]),d['object_pos_w'][start:end],d['object_quat_w'][start:end],50)
            modes=np.where(np.arange(start,end)<95,0,np.where(np.arange(start,end)<205,1,2)).tolist()
            rows.append(dict(name=name,family=family,path='motions/'+dest.name,sha256=sha(dest),sampling_weight=weight,
                source=file,source_sha256=sha(path),source_interval=[start,end],physics_validation='unvalidated',
                training_admission='audited_kinematic_target_only',derivation='root/joints/object poses preserved to float32; all body FK and velocities recomputed; no grasp retargeting',
                task_modes=modes,phases=phases if start==0 else [dict(name='loaded_carry_candidate',start=0,end=end-start)],
                eligible_reset_frames=list(range(end-start-1))))
    old=REPO/'datasets/fullbody_carry_track_v2'
    for name in ['continuous_grasped_squat_stand','repeated_grasped_squat_stand']:
        dest=a.output/'motions'/(name+'.npz');shutil.copy2(old/'motions'/dest.name,dest)
        n=len(np.load(dest)['joint_pos']);rows.append(dict(name=name,family='loaded_squat_stand',path='motions/'+dest.name,
            sha256=sha(dest),sampling_weight=.175,physics_validation='P0_controller_validated_not_policy',training_admission='audited_target',
            derivation='bit-exact validated P0 copy',task_modes=[1]*n,phases=[dict(name='loaded_squat_stand',start=0,end=n)],eligible_reset_frames=list(range(n-1))))
    for file in ['model_contract.json','verified_side_grasp_reset.json','goal_limits.json']:shutil.copy2(old/file,a.output/file)
    ranges=goal_ranges(a.output,rows);limits=json.loads((a.output/'goal_limits.json').read_text())
    limits.update(height_low=min(v['min'][3] for v in ranges.values()),height_high=max(v['max'][3] for v in ranges.values()),
        reference_goal_ranges_by_mode=ranges,scope='Stage1 reference-derived values, including pickup/putdown; not Gen admission')
    (a.output/'goal_limits.json').write_text(json.dumps(limits,indent=2)+'\n')
    families=['full_sequence','loaded_locomotion','loaded_squat_stand'];weights={f:w/sum(a.family_weights) for f,w in zip(families,a.family_weights)}
    for row in rows:
        row['sampling_weight']=weights[row['family']]/sum(r['family']==row['family'] for r in rows)
    manifest=dict(schema='unified_hoi_v1',base_commit='6c3eed6462ddbcc9a4d4870c1bc06146d54b3dae',upstream_commit=upstream,
        task_modes=['pickup','carry','putdown'],family_weights=weights,
        motions=rows,source_audits=audits,full_training_ready=False,
        blockers=['Original grasp physical compatibility unverified/failed earlier crop probes','No validated walking-squat-walking transition',
            'Floor overlap in original reference (millimetres); reference FK differs from collision URDF; canonical FK only is not physical repair'])
    (a.output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (a.output/'audit/phase_annotations.json').write_text(json.dumps(audits,indent=2)+'\n')
    lines=['# Full HMI motion timeline (kinematic candidates only)','',f'Pinned upstream: {upstream}. All three local source files byte-identical.','']
    for audit in audits:
        lines+=['## '+audit['source'],'',f"FK mismatch before canonical export: {audit['original_body_fk_max_error_m']:.6f}m. Box bottom minimum {audit['box_bottom_min_m']:.4f}m.",'', '| Candidate phase | Frames [start,end) | Time seconds |','|---|---|---|']
        lines += [f"| {x['name']} | {x['start']}–{x['end']} | {x['start']/50:.2f}–{(x['end']-1)/50:.2f} |" for x in audit['phases']]
        lines+=['',f"Contact/lift/settle/release candidate frames: {audit['contact_candidate_frame']}, {audit['liftoff_candidate_frame']}, {audit['settled_candidate_frame']}, {audit['release_candidate_frame']}. No force inference is certified by these labels.",'']
    (a.output/'audit/MOTION_TIMELINE.md').write_text('\n'.join(lines).rstrip()+'\n');verify(a.output)
    print(json.dumps([dict(source=x['source'],contact=x['contact_candidate_frame'],lift=x['liftoff_candidate_frame'],settle=x['settled_candidate_frame'],release=x['release_candidate_frame']) for x in audits]))

if __name__=='__main__':main()
