"""One fresh shared HMI PPO; no automatic budget, plateau loop, or Stage2."""
import fcntl,json,os,subprocess,sys,time,tarfile,hashlib
from pathlib import Path
from train_stage1_joint import parser,build_argv,REPO
from prepare_unified_hoi import verify,DEFAULT

def main():
    p=parser();p.set_defaults(num_envs=256,data=DEFAULT);a=p.parse_args();a.data=a.data.resolve();m=verify(a.data)
    if a.num_envs not in (256,1024,4096,8192):p.error('Supported training sizes: 256,1024,4096,8192 (capacity is hardware-dependent)')
    os.environ['HMI_UNIFIED_DATA']=str(a.data);os.environ['HMI_CARRY_ACTION_MODE']='joint_delta'
    if a.resume:
        import torch
        from holosoma.carry.checkpoints import validate,digest
        validate(a.resume);state=torch.load(a.resume,map_location='cpu',weights_only=True)['env_state']
        if state.get('unified_schema')!=1 or state.get('fullbody_manifest_sha256')!=digest(a.data/'manifest.json'):raise ValueError('Only an identical unified experiment may resume')
    root=(a.run_dir or REPO.parent/'artifacts/unified_hoi_stage1'/('run_'+time.strftime('%Y%m%d_%H%M%S'))).resolve()
    argv=build_argv(a,root);argv=[x.replace('exp:g1-29dof-carry-stage1-joint','exp:g1-29dof-unified-hoi-stage1').replace('stage1_joint_squat_walk','unified_hoi_stage1') for x in argv]
    plan=dict(argv=argv,run_dir=str(root),data=str(a.data),stage='unified Track-only',actor_dim=357,critic_dim=187,
        goal=['vx','vy','yaw_rate','pelvis_height'],task_modes=['pickup','carry','putdown'],full_training_ready=m['full_training_ready'])
    if a.dry_run:print(json.dumps(plan,indent=2));return
    if a.iterations>32 and not m['full_training_ready']:raise ValueError('Reference physics admission is incomplete; bounded <=32-update diagnostics only until readiness is established')
    lock=open('/tmp/g1-carry-gpu0.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);os.set_inheritable(lock.fileno(),True)
    root.mkdir(parents=True,exist_ok=False);(root/'worker').mkdir()
    plan.update(pid=os.getpid(),source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
        source_status=subprocess.check_output(['git','status','--porcelain'],cwd=REPO,text=True))
    (root/'launch.json').write_text(json.dumps(plan,indent=2)+'\n');(root/'manifest.json').write_text((a.data/'manifest.json').read_text())
    with (root/'source.tar').open('wb') as f:subprocess.run(['git','archive','HEAD'],cwd=REPO,stdout=f,check=True)
    (root/'source.patch').write_bytes(subprocess.check_output(['git','diff','HEAD'],cwd=REPO))
    paths=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=REPO).decode().split('\0')
    hashes={}
    with tarfile.open(root/'source_worktree_text.tar.gz','w:gz') as snapshot:
        for name in sorted(set(paths)):
            file=REPO/name
            if file.is_file() and file.suffix in ('.py','.sh','.json','.md','.toml','.yaml','.yml'):
                snapshot.add(file,arcname=name);hashes[name]=hashlib.sha256(file.read_bytes()).hexdigest()
    (root/'source_worktree_sha256.json').write_text(json.dumps(hashes,indent=2)+'\n')
    os.environ['CARRY_WORKER_OUTPUT']=str(root/'worker');os.chdir(REPO);print(json.dumps(plan,indent=2),flush=True)
    os.execv(sys.executable,argv)

if __name__=='__main__':main()
