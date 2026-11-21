"""Versioned HMI Track admission, distinct from controller physics certification."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import numpy as np
from scipy.spatial.transform import Rotation

REPO=Path(__file__).resolve().parents[2]


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_bundle(root):
    manifest=json.loads((root/'manifest.json').read_text())
    assert manifest['schema']=='carry_track_training_v2'
    assert manifest['stage']==1 and manifest['track_ratio']==1.
    assert {r['family'] for r in manifest['motions']}=={'squat_stand','forward_carry'}
    assert abs(sum(r['sampling_weight'] for r in manifest['motions'])-1.)<1e-8
    actual={p.name for p in (root/'motions').glob('*.npz')}
    assert actual=={Path(r['path']).name for r in manifest['motions']}
    summary=[]
    for row in manifest['motions']:
        p=root/row['path'];assert sha(p)==row['sha256'],p
        with np.load(p,allow_pickle=False) as d:
            n=len(d['joint_pos']);assert d['joint_pos'].shape==(n,36) and d['joint_vel'].shape==(n,35)
            assert len(d['joint_names'])==29 and float(d['fps'].item())==50.
            for key in ['joint_pos','joint_vel','body_pos_w','body_quat_w','body_lin_vel_w',
                'body_ang_vel_w','object_pos_w','object_quat_w','object_lin_vel_w','object_ang_vel_w']:
                assert len(d[key])==n and np.isfinite(d[key]).all(),(p,key)
            for key in ['body_quat_w','object_quat_w']:
                assert np.max(abs(np.linalg.norm(d[key],axis=-1)-1))<1e-5
            assert np.max(abs(np.linalg.norm(d['joint_pos'][:,3:7],axis=-1)-1))<1e-5
        summary.append(dict(name=row['name'],family=row['family'],weight=row['sampling_weight'],
            physics_validation=row['physics_validation'],frames=n,sha256=row['sha256']))
    return summary


def prepare(source,output):
    output.mkdir(parents=True,exist_ok=False);(output/'motions').mkdir();(output/'provenance').mkdir()
    rows=[];heights=[];rates=[];velocities=[]
    for name,family,folder,weight,status in [
        ('continuous_grasped_squat_stand','squat_stand','validated_motions',.2,'P0_controller_validated'),
        ('repeated_grasped_squat_stand','squat_stand','validated_motions',.3,'P0_controller_validated'),
        ('original_forward_carry','forward_carry','motions_kinematic',.5,'kinematic_only_controller_admission_failed')]:
        src=source/folder/(name+'.npz');dst=output/'motions'/src.name;shutil.copy2(src,dst)
        with np.load(src,allow_pickle=False) as d:
            q=d['joint_pos'];fps=float(d['fps'].item());v=d['joint_vel']
            yaw=Rotation.from_quat(q[:,[4,5,6,3]]).as_euler('xyz')[:,2]
            vx=np.cos(yaw)*v[:,0]+np.sin(yaw)*v[:,1]
            heights.extend(q[:,2].tolist());rates.extend(abs(v[:,2]).tolist());velocities.extend(vx.tolist())
            rows.append(dict(name=name,family=family,path='motions/'+dst.name,sha256=sha(src),
                source='artifacts/carry_reference_synthesized/'+folder+'/'+src.name,
                sampling_weight=weight,training_admission='HMI_track_target',physics_validation=status,
                frames=len(q),fps=fps,duration_s=(len(q)-1)/fps,
                pelvis_range_m=[float(q[:,2].min()),float(q[:,2].max())],
                forward_velocity_range_m_s=[float(vx.min()),float(vx.max())]))
    # Reuse the original verified reset without asserting PPO reset stability.
    reset=json.loads((source/'verified_side_grasp_reset.json').read_text())
    contract=json.loads((source/'model_contract.json').read_text());box=reset['initial_box_wxyz']
    adapted=dict(physics_verified=True,physics_verified_policy=False,
        validation_scope='P0 controller only; Track resets use each selected reference frame',
        joint_names=contract['joint_names'],joint_pos=reset['initial_joint_pos'],
        pd_target_joint_pos=reset['initial_joint_pos'],root_xyzw=reset['initial_root_xyzw']+[0.]*6,
        box_xyzw=box[:3]+box[4:7]+box[3:4]+[0.]*6,source_sha256=sha(source/'verified_side_grasp_reset.json'))
    contract['object_urdf']='holosoma/data/motions/g1_29dof/whole_body_tracking/objects_largebox.urdf'
    contract['robot_urdf']='holosoma/data/robots/g1/main_mesh_collision_halfspherehand.urdf'
    limits=dict(height_low=min(heights),height_high=max(heights),height_rate=max(rates),
        vx_high=max(velocities),forward_admitted=False,forward_track_training_admitted=True,
        reference_fps=50,episode_seconds=30.,scope='Stage1 reference-derived values only; not Gen qualification')
    manifest=dict(schema='carry_track_training_v2',stage=1,track_ratio=1.,motions=rows,
        family_weights={'squat_stand':.5,'forward_carry':.5},
        sampling_strategy='Half of training environments track squat/stand, half track forward carry; '
            'conditional clip weights avoid short walking episodes losing their share of environment steps.',
        admission_policy='Track target admission requires format/FK/asset consistency, not prior success of the P0 controller. '
            'Forward is included under the user-authorized revised Track admission. Physics failures remain recorded. '
            'Neither reference admission nor training completion certifies a successful policy.',
        p0_reset_sha256=sha(source/'verified_side_grasp_reset.json'))
    for filename,value in [('manifest.json',manifest),('goal_limits.json',limits),
        ('verified_side_grasp_reset.json',adapted),('model_contract.json',contract)]:
        (output/filename).write_text(json.dumps(value,indent=2)+'\n')
    for name in ['immutable_sources.json','format_validation.json','motion_manifest.json']:
        shutil.copy2(source/name,output/'provenance'/name)
    shutil.copy2(source/'evidence/repeated_12cm_001_data/validation.json',output/'provenance/p0_repeated_validation.json')
    print(json.dumps(verify_bundle(output),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=REPO.parent/'artifacts/carry_reference_synthesized')
    p.add_argument('--output',type=Path,default=REPO/'datasets/fullbody_carry_track_v2')
    p.add_argument('--verify-only',action='store_true');a=p.parse_args()
    if a.verify_only:print(json.dumps(verify_bundle(a.output),indent=2))
    else:prepare(a.source.resolve(),a.output.resolve())
