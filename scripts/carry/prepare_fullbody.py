"""Create a separate immutable-source training bundle; never overwrite P0 or old runs."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import numpy as np
from scipy.spatial.transform import Rotation

REPO = Path(__file__).resolve().parents[2]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare(source, output):
    output.mkdir(parents=True, exist_ok=False)
    (output/'motions').mkdir()
    (output/'quarantine').mkdir()
    contract = json.loads((source/'model_contract.json').read_text())
    reset = json.loads((source/'verified_side_grasp_reset.json').read_text())
    assert reset['status'] == 'Physics validated'
    rows = []
    for name, status, weight in [('continuous_grasped_squat_stand', 'physics_validated', .4),
                                  ('repeated_grasped_squat_stand', 'physics_validated', .6),
                                  ('original_forward_carry', 'kinematic_only', 0.)]:
        src = source/('validated_motions' if weight else 'motions_kinematic')/(name+'.npz')
        dst = output/('motions' if weight else 'quarantine')/src.name
        shutil.copy2(src, dst)
        with np.load(src) as d:
            q = d['joint_pos']; fps = float(d['fps'])
            assert q.shape[1] == 36 and d['joint_vel'].shape[1] == 35 and fps == 50
            for key in ['body_pos_w','body_quat_w','body_lin_vel_w','body_ang_vel_w',
                        'object_pos_w','object_quat_w','object_lin_vel_w','object_ang_vel_w']:
                assert np.isfinite(d[key]).all()
            heading = Rotation.from_quat(q[:, [4,5,6,3]]).as_euler('xyz')[:, 2]
            vel = d['joint_vel'][:, :3]
            vx = np.cos(heading)*vel[:, 0]+np.sin(heading)*vel[:, 1]
            rows.append(dict(name=name, source=str(src.resolve()), path=str(dst.resolve()),
                sha256=digest(src), status=status, sampling_weight=weight, frames=len(q), fps=fps,
                duration_s=(len(q)-1)/fps, height_min=float(q[:,2].min()),
                height_max=float(q[:,2].max()), height_rate_max=float(abs(d['joint_vel'][:,2]).max()),
                vx_quantiles=np.quantile(vx,[0,.1,.5,.9,1]).tolist()))
    # Full 12cm amplitude; speed remains zero until forward dynamics admission.
    admitted = rows[:2]
    limits = dict(height_low=min(r['height_min'] for r in admitted),
        height_high=max(r['height_max'] for r in admitted),
        height_rate=max(r['height_rate_max'] for r in admitted), vx_high=0.,
        forward_admitted=False, reference_fps=50, episode_seconds=30.)
    qroot=reset['initial_root_xyzw']+[0.]*6
    b=reset['initial_box_wxyz']; box=b[:3]+b[4:7]+b[3:4]+[0.]*6
    adapted=dict(physics_verified=True, validation_scope='P0 controller only; PPO not validated',
        joint_names=contract['joint_names'], joint_pos=reset['initial_joint_pos'],
        pd_target_joint_pos=reset['initial_joint_pos'], root_xyzw=qroot, box_xyzw=box,
        source_sha256=digest(source/'verified_side_grasp_reset.json'), source=str(source.resolve()),
        physics_verified_policy=False)
    for filename,value in [('verified_side_grasp_reset.json',adapted),('goal_limits.json',limits),
                           ('model_contract.json',contract),('manifest.json',dict(motions=rows,
        p0_reset_sha256=digest(source/'verified_side_grasp_reset.json'),
        p0_evidence_sha256=digest(source/'evidence/repeated_12cm_001_data/validation.json'),
        source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
        correlation_note='Single and repeated share one action family. Family total weight 1; forward quarantined.'))]:
        (output/filename).write_text(json.dumps(value,indent=2)+'\n')
    shutil.copy2(source/'verified_side_grasp_reset.json', output/'p0_verified_side_grasp_reset.json')
    shutil.copy2(source/'evidence/repeated_12cm_001_data/physics_model.json', output/'p0_physics_model.json')
    print(json.dumps(dict(output=str(output),goals=limits,motions=rows),indent=2))


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,default=REPO.parent/'artifacts/carry_reference_synthesized')
    p.add_argument('--output',type=Path,default=REPO.parent/'artifacts/fullbody_goal_carry/reference_v1')
    a=p.parse_args(); prepare(a.source.resolve(),a.output.resolve())
