"""Isaac Sim exact Reset and post-action reference clock assertions; no training."""
import argparse
from dataclasses import replace
import json
from pathlib import Path


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=False)
    from holosoma.carry.stage1_presets import g1_29dof_carry_stage1_joint as base
    from holosoma.config_types.env import get_tyro_env_config
    from holosoma.carry.runtime import simulation_context
    cfg=replace(base,training=replace(base.training,num_envs=16,headless=True),logger=replace(base.logger,base_dir=str(a.output)))
    with simulation_context(cfg,a.output/'exception.txt'):
        import torch
        from holosoma.carry.stage1_environment import Stage1CarryEnv
        from holosoma.carry.observations import simulator_box_state
        from holosoma.carry.fullbody_rewards import physical_metrics
        env=Stage1CarryEnv(get_tyro_env_config(cfg),device='cuda:0');env.set_is_evaluating()
        cmd=env.command_manager.get_state('motion_command');limits_before=env.simulator.dof_pos_limits.clone()
        capture={};check=env._check_termination
        def checked():
            check()
            capture.clear();capture.update(index=cmd.time_steps.clone(),motion_ids=cmd.motion_ids.clone(),
                timeout=env.time_out_buf.clone(),failed=env.termination_manager.terminated.clone(),
                contact=physical_metrics(env)['bilateral_contact'].clone(),
                root=env.simulator.robot_root_states[:].clone(),box=simulator_box_state(env).clone())
        env._check_termination=checked
        rows=[]
        for clip in range(3):
            n=int(cmd.motion.motion_end_idx[clip]-cmd.motion.motion_start_idx[clip])
            for frame in [0,n//4,n//2,n-2]:
                cmd.motion_cfg=replace(cmd.motion_cfg,eval_fixed_reset=replace(cmd.motion_cfg.eval_fixed_reset,
                    enabled=True,motion_id=clip,local_frame=frame))
                obs=env.reset_all();q=env.simulator.dof_pos;box=simulator_box_state(env);root=env.simulator.robot_root_states[:]
                torch.testing.assert_close(q,cmd.joint_pos,atol=2e-6,rtol=0)
                reset_q_error=float((q-cmd.joint_pos).abs().max())
                torch.testing.assert_close(env.simulator.dof_vel,cmd.joint_vel,atol=2e-6,rtol=0)
                for actual,target in [(root[:,:3],cmd.root_pos_w),(root[:,3:7],cmd.root_quat_w),
                    (root[:,7:10],cmd.root_lin_vel_w),(root[:,10:13],cmd.root_ang_vel_w),
                    (box[:,:3],cmd.object_pos_w),(box[:,3:7],cmd.object_quat_w),
                    (box[:,7:10],cmd.motion.object_lin_vel_w[cmd.time_steps]),
                    (box[:,10:13],cmd.motion.object_ang_vel_w[cmd.time_steps])]:
                    torch.testing.assert_close(actual,target,atol=2e-6,rtol=0)
                assert obs['actor_obs'].shape==(16,348) and obs['critic_obs'].shape==(16,184)
                start=cmd.time_steps.clone()
                target=torch.minimum(start+1,cmd.motion.motion_end_idx[cmd.motion_ids]-1)
                joint=env.action_manager.get_term('joint_control')
                center=q if getattr(joint,'parameterization','fixed_default_v1')=='joint_delta_v1' else env.default_dof_pos
                action=(cmd.motion.joint_pos[target]-center)/env.action_scales
                env.step({'actions':action})
                assert torch.equal(capture['index'],target),'post-action tracking target is not k+1'
                at_end=frame==n-2
                if at_end:assert capture['timeout'].all() and not capture['failed'].any()
                else:assert torch.equal(cmd.time_steps,target),'reference advanced twice or reset unexpectedly'
                row=dict(clip=clip,frame=frame,q_error_max_rad=reset_q_error,
                    reset_robot_object_pose_velocity_matched=True,post_action_target_matched=True,
                    natural_end=at_end,terminal_contact_mean=float(capture['contact'].mean()))
                rows.append(row)
        torch.testing.assert_close(limits_before,env.simulator.dof_pos_limits,atol=0,rtol=0)
        result=dict(passed=True,policy_success=False,rows=rows,physics=env.fullbody_physics,
            actual_hard_limits=cmd.reference_hard_limits.tolist(),soft_limits_unchanged=True)
        (a.output/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(dict(passed=True,resets=len(rows),natural_ends=3)),flush=True)


if __name__=='__main__':main()
