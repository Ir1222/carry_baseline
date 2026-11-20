"""Real Isaac Sim interface/physics gate; does not certify a learned policy."""
import argparse
from dataclasses import replace
import json
from pathlib import Path


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():raise FileExistsError(a.output)
    from holosoma.carry.fullbody_presets import g1_29dof_fullbody_carry as base
    from holosoma.config_types.env import get_tyro_env_config
    from holosoma.train_agent import TrainingContext
    term=base.command.setup_terms['motion_command'];motion=term.params['motion_config']
    motion=replace(motion,hybrid=replace(motion.hybrid,track_ratio=1.),
        eval_fixed_reset=replace(motion.eval_fixed_reset,enabled=True,motion_id=0,local_frame=0))
    config=replace(base,training=replace(base.training,num_envs=8,headless=True),
        command=replace(base.command,setup_terms={'motion_command':replace(term,params={**term.params,'motion_config':motion})}))
    from holosoma.carry.runtime import simulation_context
    with simulation_context(config,a.output.with_suffix('.exception.txt')):
        import torch
        from pxr import UsdPhysics,PhysxSchema
        from holosoma.carry.fullbody_environment import FullBodyCarryEnv
        from holosoma.carry.fullbody_rewards import box_bottom,carrying_gate,box_orientation
        from holosoma.carry.checkpoints import atomic_json
        env=FullBodyCarryEnv(get_tyro_env_config(config),device='cuda:0');env.set_is_evaluating()
        cmd=env.command_manager.get_state('motion_command');results=[]
        for frame in (0,175):
            cmd.motion_cfg=replace(cmd.motion_cfg,eval_fixed_reset=replace(cmd.motion_cfg.eval_fixed_reset,local_frame=frame))
            obs=env.reset_all()
            assert obs['actor_obs'].shape==(8,348) and obs['critic_obs'].shape==(8,184)
            env._check_termination()
            physical=env.termination_manager.last_term_results['physical_failure']
            assert not physical.any(),(frame,env.termination_manager.last_term_breakdowns)
            assert (carrying_gate(env)==1).all()
            assert (box_orientation(env)>.9).all()
            results.append(dict(frame=frame,pelvis_height=env.simulator.robot_root_states[:,2].tolist(),
                box_clearance=box_bottom(env).tolist(),physical_failure=physical.tolist()))
        view=env.simulator._object.root_physx_view
        assert torch.allclose(view.get_masses(),torch.full_like(view.get_masses(),1.1),atol=1e-6)
        inertia=view.get_inertias().reshape(-1,3,3)
        assert torch.allclose(inertia[:,[0,1,2],[0,1,2]],torch.full_like(inertia[:,0,:],.022),atol=1e-6)
        boxprim=env.simulator.sim.stage.GetPrimAtPath('/World/envs/env_0/Object/baseLink')
        flags=dict(kinematic=UsdPhysics.RigidBodyAPI(boxprim).GetKinematicEnabledAttr().Get(),
            rigid_enabled=UsdPhysics.RigidBodyAPI(boxprim).GetRigidBodyEnabledAttr().Get(),
            disable_gravity=PhysxSchema.PhysxRigidBodyAPI(boxprim).GetDisableGravityAttr().Get())
        assert not flags['kinematic'] and not flags['disable_gravity'] and flags['rigid_enabled']
        model=env.fullbody_physics
        model.update(p_gains=env.p_gains.tolist(),d_gains=env.d_gains.tolist(),action_scales=env.action_scales.tolist())
        a.output.parent.mkdir(parents=True,exist_ok=True)
        atomic_json(a.output,dict(passed=True,policy_success=False,scope='Physics/model/shape/legitimate high-low states',
            physics=model,object_flags=flags,states=results))
        print(json.dumps(dict(passed=True,states=results)),flush=True)


if __name__=='__main__':main()
