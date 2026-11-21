"""Compare actual training observations with the deployment adapter in one physics rollout."""
import argparse
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path


def main():
    p=argparse.ArgumentParser();p.add_argument('--checkpoint',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--steps',type=int,default=40)
    p.add_argument('--action-source',choices=['adapter','environment','sample'],default='adapter')
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    from holosoma.carry.fullbody_presets import g1_29dof_fullbody_carry as base
    from holosoma.config_types.env import get_tyro_env_config
    from holosoma.carry.runtime import simulation_context
    term=base.command.setup_terms['motion_command'];m=term.params['motion_config']
    m=replace(m,hybrid=replace(m.hybrid,track_ratio=1.),
        eval_fixed_reset=replace(m.eval_fixed_reset,enabled=True,motion_id=0,local_frame=0))
    config=replace(base,training=replace(base.training,num_envs=2,headless=True),
        command=replace(base.command,setup_terms={'motion_command':replace(term,params={**term.params,'motion_config':m})}))
    with simulation_context(config,a.output/'exception.txt'):
        import torch
        from holosoma.agents.modules.module_utils import setup_ppo_actor_module
        from holosoma.agents.ppo.ppo import EmpiricalNormalization
        from holosoma.carry.fullbody_environment import FullBodyCarryEnv
        from holosoma.carry.inference import CarryActor
        from holosoma.carry.observations import simulator_box_state
        from holosoma.carry.checkpoints import atomic_json
        env=FullBodyCarryEnv(get_tyro_env_config(config),device='cuda:0');env.set_is_evaluating()
        torch.manual_seed(1000)
        saved=torch.load(a.checkpoint,map_location='cpu',weights_only=True)
        policy=setup_ppo_actor_module({'actor_obs':348},deepcopy(base.algo.config.module_dict.actor),29,.3,'cuda:0',{'actor_obs':3})
        policy.load_state_dict(saved['actor_model_state_dict']);policy.eval()
        norm=EmpiricalNormalization(shape=348,device='cuda:0');norm.load_state_dict(saved['actor_obs_normalizer_state_dict']);norm.eval()
        adapter=CarryActor(a.checkpoint.with_suffix('.onnx'),2,'cuda:0')
        obs=env.reset_all();adapter.reset();rows=[]
        cmd=env.command_manager.get_state('motion_command')
        for i in range(a.steps):
            adapted=adapter.act(env.simulator.robot_root_states[:],env.simulator.dof_pos,env.simulator.dof_vel,
                simulator_box_state(env),cmd.task_command,env.simulator.scene.env_origins[:,2])
            raw=obs['actor_obs'].clone();adapter_raw=adapter.history.flatten(1)
            with torch.no_grad():
                expected=policy.act_inference({'actor_obs':norm(raw,update=False)})
                adapter_expected=policy.act_inference({'actor_obs':norm(adapter_raw,update=False)})
                sample=policy.act({'actor_obs':norm(raw,update=False)})
            error=(raw-adapter_raw).abs()
            rows.append(dict(step=i,history_max_error=float(error.max()),
                frame_errors=error.reshape(2,3,116).max(-1).values.tolist(),
                largest_feature=error.argmax(-1).tolist(),
                environment_vs_adapter_action_max_error=float((expected-adapted).abs().max()),
                same_input_torch_onnx_max_error=float((adapter_expected-adapted).abs().max()),
                env_obs_first=raw[0].tolist() if i<2 else None,
                adapter_obs_first=adapter_raw[0].tolist() if i<2 else None))
            action={'adapter':adapted,'environment':expected,'sample':sample}[a.action_source]
            obs,_,done,_=env.step({'actions':action})
            rows[-1]['done']=done.tolist()
            rows[-1]['physical_contact']=cmd.metrics['carry/bilateral_contact'].tolist()
            if done.any():break
        atomic_json(a.output/'audit.json',dict(action_source=a.action_source,steps=len(rows),rows=rows))
        print(json.dumps([{k:v for k,v in r.items() if k not in ['env_obs_first','adapter_obs_first']} for r in rows]),flush=True)


if __name__=='__main__':main()
