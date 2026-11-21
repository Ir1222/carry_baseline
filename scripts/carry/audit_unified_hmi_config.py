"""Compare resolved HMI Object Stage1 and Unified HOI without tuning either."""
import argparse
import dataclasses
import json
from pathlib import Path
from holosoma.config_values.wbt.g1.experiment import g1_29dof_wbt_hybrid_object
from holosoma.carry.unified_presets import g1_29dof_unified_hoi_stage1
from holosoma.envs.wbt.config_utils import apply_wbt_robot_defaults
from holosoma.carry.checkpoints import digest

FIELDS=('num_mini_batches','num_learning_epochs','init_noise_std','num_steps_per_env','actor_learning_rate',
 'critic_learning_rate','schedule','desired_kl','gamma','lam','clip_param','entropy_coef','max_grad_norm',
 'empirical_normalization','use_symmetry','init_at_random_ep_len','save_interval','latest_save_interval','num_learning_iterations')

def snapshot(cfg,upstream=False):
    c=dataclasses.asdict(apply_wbt_robot_defaults(cfg));m=c['command']['setup_terms']['motion_command']['params']['motion_config']
    # Reproduce explicit overrides in upstream README Object Stage1, or this run.
    c['training']['num_envs']=8192;c['training']['checkpoint']=None
    c['algo']['config']['num_learning_iterations']=15000;c['simulator']['config']['scene']['env_spacing']=4.
    m['hybrid']['track_ratio']=1.
    if upstream:
        m['motion_dir']='holosoma/data/motions/g1_29dof/whole_body_tracking/movebox'
        m['start_at_timestep_zero_prob']=.05;m['hybrid']['size_randomization']['enabled']=False
    return c

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    old=snapshot(g1_29dof_wbt_hybrid_object,True);new=snapshot(g1_29dof_unified_hoi_stage1)
    rows={k:dict(upstream_object_stage1=old['algo']['config'][k],unified_actual=new['algo']['config'][k]) for k in FIELDS}
    motion=new['command']['setup_terms']['motion_command']['params']['motion_config']
    result=dict(base_commit='38109772247c4498b93252500a79218bb52f5583',entry='src/holosoma/holosoma/train_agent.py',
        ppo_comparison=rows,num_envs=8192,env_spacing=4.,track_ratio=motion['hybrid']['track_ratio'],
        unified_motion=motion,upstream_motion=old['command']['setup_terms']['motion_command']['params']['motion_config'],
        action=new['action'],robot_control=new['robot']['control'],reward=new['reward'],termination=new['termination'],
        actor_dim=357,critic_dim=187,manifest_sha256=digest(Path(motion['motion_dir']).parent/'manifest.json'),
        changes_to_ppo_hyperparameters='Only user-requested checkpoint interval2000; existing Unified 128 minibatches and0.3 noise retained',
        logger=dict(type='wandb',mode='offline',video_enabled=False,reason='Online credential validation returned HTTP403; TensorBoard and offline W&B retained'))
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(rows,indent=2))

if __name__=='__main__':main()
