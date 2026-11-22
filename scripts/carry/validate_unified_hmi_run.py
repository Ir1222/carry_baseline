"""Read-only capacity/completion checks, never a policy physics-admission gate."""
import argparse
import json
import math
from pathlib import Path
import yaml
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
from holosoma.carry.checkpoints import validate,validate_export,digest,UNIFIED_CRITIC_DIM

REPO=Path(__file__).resolve().parents[2]

def validate_run(root,updates):
    configs=[p for p in root.rglob('holosoma_config.yaml') if '.wandb' not in p.parts]
    if len(configs)!=1:raise ValueError(f'Expected one HMI run, got {configs}')
    config_path=configs[0];config=yaml.safe_load(config_path.read_text());folder=config_path.parent
    if config['training']['num_envs']!=8192:raise ValueError('Expected 8192-env training')
    resumed_from=config['training']['checkpoint'];completed_before=0
    if resumed_from:
        completed_before=validate(Path(resumed_from))['completed_updates']
        if not config['algo']['config']['load_optimizer'] or config['algo']['config']['reset_policy_std_on_resume']:
            raise ValueError('Resume must preserve optimizers and learned action noise')
    if config['algo']['config']['num_learning_iterations']!=updates-completed_before:raise ValueError('Wrong remaining/total update count')
    if updates==15000 and config['algo']['config']['save_interval']!=2000:raise ValueError('Formal run must save every2000 updates')
    if config['algo']['config']['num_mini_batches'] not in (4,8,16):raise ValueError('Unexpected minibatch fallback')
    if config['algo']['config']['latest_save_interval']!=100:raise ValueError('Latest snapshots disabled')
    if config['simulator']['config']['scene']['env_spacing']!=4.:raise ValueError('Wrong spacing')
    motion=config['command']['setup_terms']['motion_command']['params']['motion_config']
    if motion['hybrid']['track_ratio']!=1.:raise ValueError('Gen is forbidden')
    data=REPO/'datasets/unified_hoi_v1';manifest=json.loads((data/'manifest.json').read_text())
    if Path(motion['motion_dir']).resolve()!=(data/'motions').resolve():raise ValueError('Wrong dataset/movebox override')
    for row in manifest['motions']:
        if digest(data/row['path'])!=row['sha256']:raise ValueError('Reference bytes changed')
    path=folder/f'model_{updates-1:05d}.pt';checkpoint=validate(path);validate_export(path.with_suffix('.onnx'))
    metadata=json.loads(path.with_suffix('.actor.json').read_text())
    if metadata['actor_dim']!=357 or metadata['critic_dim']!=UNIFIED_CRITIC_DIM or metadata['action_parameterization']!='joint_delta_v1':raise ValueError('Wrong HOI interface')
    if metadata['reference_manifest_sha256']!=digest(data/'manifest.json'):raise ValueError('Manifest mismatch')
    events=EventAccumulator(str(folder),size_guidance={'scalars':0});events.Reload();scalars={}
    for tag in events.Tags()['scalars']:
        values=events.Scalars(tag)
        if not all(math.isfinite(x.value) for x in values):raise ValueError('Nonfinite TensorBoard values: '+tag)
        if values:scalars[tag]=values[-1].value
    loss_tags=[tag for tag in scalars if tag.startswith('Loss/')]
    if not loss_tags or not all(events.Scalars(tag)[-1].step==updates-1 for tag in loss_tags):raise ValueError('Missing final PPO loss/update')
    fractions={name:scalars['Env/hoi/family_fraction/'+name] for name in manifest['family_weights']}
    if any(abs(fractions[k]-v)>1/8192+1e-5 for k,v in manifest['family_weights'].items()):raise ValueError('Motion family quota mismatch')
    for name in ['pickup','carry','putdown']:
        if scalars.get('Env/hoi/mode_fraction/'+name,0)<=0:raise ValueError('Task phase absent: '+name)
    if metadata['physics']['mass_kg'][0]<1.099 or metadata['physics']['mass_kg'][0]>1.101:raise ValueError('Wrong free-box mass')
    wandb_files_verified=None
    if config['logger']['type']=='wandb':
        files=list(folder.glob('.wandb/wandb/offline-run-*/files'))+list(folder.glob('.wandb/wandb/run-*/files'))
        expected=[path.name,path.with_suffix('.ready.json').name,path.with_suffix('.onnx').name,path.with_suffix('.actor.json').name,path.with_suffix('.export.json').name]
        wandb_files_verified=bool(files and all(any((f/name).is_file() for f in files) for name in expected))
    return dict(passed=True,scope='capacity/interface/numerical completion only, NOT physical policy success',
        updates=updates,resumed_from=resumed_from,completed_before=completed_before,num_envs=8192,log_dir=str(folder.resolve()),wandb_files_verified=wandb_files_verified,checkpoint=checkpoint,manifest_sha256=digest(data/'manifest.json'),
        reference_physics_status_unchanged=True,family_fractions=fractions,
        phase_fractions={name:scalars['Env/hoi/mode_fraction/'+name] for name in ['pickup','carry','putdown']},
        onnx_parity_max_abs_error=metadata['onnx_parity_max_abs_error'],last_scalars=scalars)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run',type=Path,required=True);p.add_argument('--updates',type=int,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=validate_run(a.run,a.updates);a.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='last_scalars'},indent=2))

if __name__=='__main__':main()
