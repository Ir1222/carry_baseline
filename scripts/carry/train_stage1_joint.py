"""Manual launch: one original HMI PPO learn() call, no resource/plateau supervisor."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from prepare_stage1_joint import verify_bundle

REPO=Path(__file__).resolve().parents[2]
BASE=REPO.parent/'artifacts/fullbody_stage1_joint'


def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--num-envs',type=int,default=8192)
    p.add_argument('--iterations',type=int,default=15000,help='Total desired PPO updates; default 15000')
    p.add_argument('--save-every',type=int,default=2000)
    p.add_argument('--num-mini-batches',type=int,default=4)
    p.add_argument('--seed',type=int,default=42)
    p.add_argument('--data',type=Path,default=REPO/'datasets/fullbody_carry_track_v2')
    p.add_argument('--run-dir',type=Path)
    p.add_argument('--resume',type=Path,help='Optional recovery after manual interruption/crash; never used automatically')
    p.add_argument('--dry-run',action='store_true')
    return p


def build_argv(a,root):
    if a.num_envs<2 or a.iterations<1 or a.save_every<1:raise ValueError('At least two environments and positive iterations/save interval required')
    completed=0
    if a.resume:
        from holosoma.carry.checkpoints import validate
        completed=validate(a.resume)['completed_updates']
    additional=a.iterations-completed
    if additional<=0:raise ValueError('Checkpoint already reached the requested total update count')
    argv=[sys.executable,str(REPO/'scripts/carry/train_worker.py'),
        'exp:g1-29dof-carry-stage1-joint','logger:disabled',
        f'--training.num-envs={a.num_envs}','--training.headless=True',f'--training.seed={a.seed}',
        '--training.name=stage1_joint_squat_walk',f'--logger.base-dir={root/"tensorboard"}',
        f'--algo.config.num-learning-iterations={additional}',f'--algo.config.save-interval={a.save_every}',
        '--algo.config.latest-save-interval=100',f'--algo.config.num-mini-batches={getattr(a,"num_mini_batches",4)}',
        '--algo.config.num-learning-epochs=5']
    if a.resume:argv.append('--training.checkpoint='+str(a.resume.resolve()))
    return argv


def main():
    a=parser().parse_args();a.data=a.data.resolve()
    motions=verify_bundle(a.data)
    root=(a.run_dir or BASE/('run_'+time.strftime('%Y%m%d_%H%M%S')+'_'+str(time.time_ns()%1000000))).resolve()
    argv=build_argv(a,root)
    plan=dict(stage='Stage1 Track-only joint squat/walk',total_updates=a.iterations,
        action_mode=os.environ.get('HMI_CARRY_ACTION_MODE','joint_delta'),
        track_ratio=1.,gen_ratio=0.,resource_time_budget=None,plateau_stop=False,
        automatic_stage2=False,automatic_restarts=False,segmented_training=False,
        argv=argv,run_dir=str(root),data=str(a.data),motions=motions)
    if a.dry_run:print(json.dumps(plan,indent=2));return
    gpu_lock=open('/tmp/g1-carry-gpu0.lock','a+')
    try:fcntl.flock(gpu_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:raise SystemExit('Another carry training process owns GPU0; no second training process was launched')
    # Keep the cooperative lock across execv for the entire single PPO process.
    os.set_inheritable(gpu_lock.fileno(),True)
    root.mkdir(parents=True,exist_ok=False)
    (root/'worker').mkdir()
    plan.update(pid=os.getpid(),started_at=time.time(),
        source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
        source_status=subprocess.check_output(['git','status','--porcelain'],cwd=REPO,text=True))
    (root/'launch.json').write_text(json.dumps(plan,indent=2)+'\n')
    (root/'dataset_manifest.json').write_text((a.data/'manifest.json').read_text())
    with (root/'source.tar').open('wb') as f:subprocess.run(['git','archive','HEAD'],cwd=REPO,stdout=f,check=True)
    if a.run_dir is None:
        BASE.mkdir(parents=True,exist_ok=True)
        link=BASE/('.latest_'+str(os.getpid()));link.symlink_to(root.name);os.replace(link,BASE/'latest')
    os.environ['CARRY_WORKER_OUTPUT']=str(root/'worker')
    os.environ['HMI_STAGE1_DATA']=str(a.data)
    print(json.dumps(plan,indent=2),flush=True)
    print('One uninterrupted PPO run. Checkpoints do not stop training. TensorBoard: '+str(root/'tensorboard'),flush=True)
    os.chdir(REPO)
    # Replace the launcher: no watchdog, timeout, early-stop, retraining or resume loop.
    os.execv(sys.executable,argv)


if __name__=='__main__':main()
