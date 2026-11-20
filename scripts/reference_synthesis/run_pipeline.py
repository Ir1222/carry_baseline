"""Bounded, standalone reproduction. Only passed physical evidence can populate validated_motions/."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from common import ROOT, Kinematics, dump, sha

SCRIPTS=Path(__file__).resolve().parent


def select_reset(root,evidence):
    data=json.loads((evidence/'validation.json').read_text());candidates=json.loads((evidence/'candidates.json').read_text())
    passed=[i for i,r in enumerate(data['results']) if r['status']=='Physics validated']
    if not passed:raise RuntimeError('Stable side-grasp gate failed; no squat may start. Inspect evidence/hold_data/.')
    i=min(passed,key=lambda j:data['results'][j]['max_hand_slip_m']+data['results'][j]['max_box_tracking_error_m'])
    dump(root/'side_grasp_reset.json',dict(status='Physics validated',validation_scope='standing side-grasp hold',candidate=candidates[i],
        physics_evidence=str(evidence.resolve()),validation_sha256=sha(evidence/'validation.json'),metrics=data['results'][i],
        parameters=dict(mass_kg=1.1,dt=.001,gain=4,balance=.2)))
    return i


def promote(root,motion,evidence,name):
    result=json.loads((evidence/'validation.json').read_text())['results'][0]
    assert result['status']=='Physics validated',result
    model=json.loads((evidence/'physics_model.json').read_text())
    assert model['runtime_state_write_guards'] and model['box_free_dynamic']
    if (evidence/'pre_motion_gate.json').exists():assert json.loads((evidence/'pre_motion_gate.json').read_text())['passed']
    destination=root/'validated_motions'/name
    assert not destination.exists()
    shutil.copyfile(motion,destination)
    metadata=json.loads(motion.with_suffix('.json').read_text())
    metadata.update(status='Physics validated',physical_evidence=str(evidence.resolve()))
    dump(destination.with_suffix('.json'),metadata)
    dump(destination.with_suffix('.validation.json'),dict(status='Physics validated',reference_sha256=sha(destination),
        candidate_source=str(motion.resolve()),physical_evidence=str(evidence.resolve()),validation_sha256=sha(evidence/'validation.json'),metrics=result))
    return destination


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();root=args.output.resolve()
    if root.exists():raise FileExistsError('Choose a fresh output directory')
    env=dict(os.environ,PYTHONNOUSERSITE='1',OMNI_KIT_ACCEPT_EULA='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    for key in ['PYTHONPATH','PYTHONHOME','VIRTUAL_ENV','LD_LIBRARY_PATH']:env.pop(key,None)
    def cpu(script,*argv):
        subprocess.run([sys.executable,str(SCRIPTS/script),*map(str,argv)],env=env,check=True)
    def physics(name,*argv):
        evidence=root/'evidence'/f'{name}_data'
        subprocess.run([sys.executable,str(ROOT/'scripts/carry/run_bounded.py'),'--name',name,'--timeout','360',
            '--output-root',str(root/'evidence'),'--require-result',str(evidence/'validation.json'),'--',
            sys.executable,'-u',str(SCRIPTS/'physics.py'),'--output',str(evidence),*map(str,argv)],env=env,check=True)
        return evidence
    cpu('prepare.py','--output',root)
    hold=physics('hold','--candidates',root/'hold_candidates.json','--squeezes',12,20,28,'--gain',4,'--balance',.2,'--dt',.001)
    index=select_reset(root,hold)
    cpu('review.py','--evidence',hold,'--env',index)
    passed=[]
    for depth in [.10,.12]:
        name=f'squat_{int(depth*100)}cm';motion=root/'motions_kinematic'/f'{name}.npz'
        cpu('synthesize.py','--reset-state',root/'side_grasp_reset.json','--output',motion,'--depth',depth)
        evidence=physics(name,'--motion',motion,'--reset-state',root/'side_grasp_reset.json','--gain',4,'--balance',0,'--dt',.001,'--wbc')
        cpu('review.py','--evidence',evidence,'--motion',motion)
        status=json.loads((evidence/'validation.json').read_text())['results'][0]['status']
        if status=='Physics validated':
            promote(root,motion,evidence,motion.name);passed.append((depth,motion,evidence))
    if passed:
        depth,_,_=passed[-1];motion=root/'motions_kinematic'/f'repeated_{int(depth*100)}cm.npz'
        cpu('synthesize.py','--reset-state',root/'side_grasp_reset.json','--output',motion,'--depth',depth,'--cycles',2)
        evidence=physics('repeated','--motion',motion,'--reset-state',root/'side_grasp_reset.json','--gain',4,'--balance',0,'--dt',.001,'--wbc')
        cpu('review.py','--evidence',evidence,'--motion',motion)
        if json.loads((evidence/'validation.json').read_text())['results'][0]['status']=='Physics validated':
            promote(root,motion,evidence,motion.name)
    cpu('verify.py','--output-root',root)
    dump(root/'pipeline_result.json',dict(stable_grasp_passed=True,single_cycle_passed=len(passed),
        validated_motion_files=[p.name for p in (root/'validated_motions').glob('*.npz')],
        original_forward_carry_status='Kinematic only; not in validated_motions'))


if __name__=='__main__':main()
