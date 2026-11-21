"""Read-only Stage1 action audit and bounded free-box diagnostic rollouts.

Reference actions are a diagnostic probe, never a learned-policy evaluation.
No state writes occur except through the ordinary environment Reset.
"""
import argparse
from dataclasses import asdict, replace
import json
from pathlib import Path


def static_audit():
    import numpy as np
    from scipy.spatial.transform import Rotation
    from holosoma.carry.stage1_presets import DATA, g1_29dof_carry_stage1_joint as cfg
    reset=json.loads((DATA/'verified_side_grasp_reset.json').read_text())
    names=reset['joint_names'];default=np.array(reset['pd_target_joint_pos'])
    control=cfg.robot.control
    kp=np.array([next(reversed([v for k,v in control.stiffness.items() if k in n])) for n in names])
    kd=np.array([next(reversed([v for k,v in control.damping.items() if k in n])) for n in names])
    effort=np.array(cfg.robot.dof_effort_limit_list)
    scales=control.action_scale*effort/kp
    rows=[]
    for path in sorted((DATA/'motions').glob('*.npz')):
        with np.load(path,allow_pickle=False) as d:
            assert d['joint_names'].tolist()==names
            q=d['joint_pos'][:,7:];qd=d['joint_vel'][:,6:]
            a=(q-default)/scales
            zero_torque=kp*(default-q)-kd*qd
            damping_compensated=a+kd*qd/(kp*scales)
            lower=np.array(cfg.robot.dof_pos_lower_limit_list);upper=np.array(cfg.robot.dof_pos_upper_limit_list)
            center=(lower+upper)/2;half=(upper-lower)*cfg.robot.soft_dof_pos_limit/2
            reset_error=abs(np.clip(q,center-half,center+half)-q)
            yaw=Rotation.from_quat(d['body_quat_w'][:,0][:,[1,2,3,0]]).as_euler('xyz')[:,2]
            velocity=d['body_lin_vel_w'][:,0];omega=d['body_ang_vel_w'][:,0]
            goals=np.column_stack([np.cos(yaw)*velocity[:,0]+np.sin(yaw)*velocity[:,1],
                -np.sin(yaw)*velocity[:,0]+np.cos(yaw)*velocity[:,1],omega[:,2],d['body_pos_w'][:,0,2]])
            rows.append(dict(clip=path.stem,frames=len(q),a_min=a.min(0).tolist(),a_max=a.max(0).tolist(),
                action_clip_fraction=float((abs(a)>control.action_clip_value).mean()),
                damping_compensated_action_clip_fraction=float((abs(damping_compensated)>control.action_clip_value).mean()),
                reference_damping_torque_fraction_max=(abs(kd*qd)/effort).max(0).tolist(),
                zero_action_reset_torque_clip_fraction=(abs(zero_torque)>effort).mean(0).tolist(),
                max_action_rate_penalty_unweighted=float(np.square(np.diff(a,axis=0)).sum(-1).max()),
                action_rate_penalty_unweighted_mean=float(np.square(np.diff(a,axis=0)).sum(-1).mean()),
                reset_soft_clamp_error_max_rad=reset_error.max(0).tolist(),
                goal_min=goals.min(0).tolist(),goal_max=goals.max(0).tolist(),
                body_root_vs_qroot_pos_max_m=float(abs(d['body_pos_w'][:,0]-d['joint_pos'][:,:3]).max()),
                body_root_vs_qroot_lin_vel_max_m_s=float(abs(velocity-d['joint_vel'][:,:3]).max()),
                body_root_vs_qroot_ang_vel_max_rad_s=float(abs(omega-d['joint_vel'][:,3:6]).max()),
                ref_object_one_frame_displacement_max_m=float(np.linalg.norm(np.diff(d['object_pos_w'],axis=0),axis=-1).max()),
                ref_pelvis_one_frame_displacement_max_m=float(np.linalg.norm(np.diff(d['body_pos_w'][:,0],axis=0),axis=-1).max())))
    return dict(joint_names=names,q_default=default.tolist(),kp=kp.tolist(),kd=kd.tolist(),
        torque_limits=effort.tolist(),action_scales=scales.tolist(),control=asdict(control),
        reset_noise=asdict(cfg.command.setup_terms['motion_command'].params['motion_config'].noise_to_initial_pose),
        initial_policy_std=cfg.algo.config.init_noise_std,
        exploration_position_std=(scales*cfg.algo.config.init_noise_std).tolist(),
        exploration_torque_std_fraction=control.action_scale*cfg.algo.config.init_noise_std,
        robot_soft_dof_pos_limit=cfg.robot.soft_dof_pos_limit,termination=asdict(cfg.termination),clips=rows)


def run_rollouts(args):
    from holosoma.carry.stage1_presets import g1_29dof_carry_stage1_joint as base
    from holosoma.config_types.env import get_tyro_env_config
    from holosoma.carry.runtime import simulation_context
    cfg=replace(base,training=replace(base.training,num_envs=args.num_envs,headless=True),
        logger=replace(base.logger,base_dir=str(args.output/'sim')))
    with simulation_context(cfg,args.output/'exception.txt'):
        import numpy as np
        import torch
        from holosoma.carry.stage1_environment import Stage1CarryEnv
        from holosoma.carry.fullbody_rewards import physical_metrics
        from holosoma.carry.observations import simulator_box_state
        from holosoma.utils.rotations import yaw_quat,quat_rotate_inverse,quat_error_magnitude
        env=Stage1CarryEnv(get_tyro_env_config(cfg),device='cuda:0')
        cmd=env.command_manager.get_state('motion_command');joint=env.action_manager.get_term('joint_control')
        result=dict(physics=env.fullbody_physics,conditions=[],policy_success_claim=False)
        result['nonhand_link_names']=[name for name in env.robot_config.body_names
            if 'sphere_hand' not in name and 'foot_contact_point' not in name]
        # Preserve actual reset state, not a re-created kinematic clone.
        result['runtime_arrays']={k:getattr(env,k).detach().cpu().tolist() for k in ['p_gains','d_gains','action_scales','torque_limits']}
        original_check=env._check_termination;snapshot={}
        def capture():
            original_check()
            m=physical_metrics(env)
            index=cmd.time_steps.clone()
            next_index=torch.minimum(index+1,cmd.motion.motion_end_idx[cmd.motion_ids]-1)
            box=simulator_box_state(env)
            target=joint._actions_after_delay[:,None,:]*env.action_scales+env.default_dof_pos[:,None,:]
            raw=joint._kp_scale[:,None,:]*env.p_gains*(target-joint.dof_pos_substep)-joint._kd_scale[:,None,:]*env.d_gains*joint.dof_vel_substep
            expected=quat_rotate_inverse(yaw_quat(cmd.root_quat_w,w_last=True),cmd.root_lin_vel_w,w_last=True)
            goal=torch.cat([expected[:,:2],cmd.root_ang_vel_w[:,2:3],
                cmd.root_pos_w[:,2:3]-env.simulator.scene.env_origins[:,2:3]],-1)
            fields=dict(motion_id=cmd.motion_ids,ref_index=index,episode_s=env.episode_length_buf*env.dt,
                pelvis_height_m=env.simulator.robot_root_states[:,2]-env.simulator.scene.env_origins[:,2],
                reference_goal=cmd.task_command,
                failed=env.termination_manager.terminated,timeout=env.time_out_buf,
                robot_error_m=(cmd.robot_body_pos_w-cmd.body_pos_relative_w).norm(dim=-1).mean(-1),
                object_error_m=(cmd.object_pos_w-box[:,:3]).norm(dim=-1),
                object_next_error_m=(cmd.motion.object_pos_w[next_index]+env.simulator.scene.env_origins-box[:,:3]).norm(dim=-1),
                object_error_rad=quat_error_magnitude(cmd.object_quat_w,box[:,3:7],w_last=True),
                q_error_rad=(cmd.joint_pos-env.simulator.dof_pos).abs().max(-1).values,
                command_error=(cmd.task_command-goal).abs().max(-1).values,
                torque_clip_fraction=(raw.abs()>env.torque_limits).float().mean((1,2)),
                torque_clip_by_joint=(raw.abs()>env.torque_limits).float().mean(1),
                nonhand_force_by_link=env.simulator.scene.sensors['box_other'].data.force_matrix_w.norm(dim=-1).sum(1),
                unsupported_s=env.termination_manager._term_instances['physical_failure'].unsupported,
                raw_last_substep_bilateral=(env.simulator.raw_contacts()[0].norm(dim=-1)>.5).all(-1).float(),
                **m)
            snapshot.clear();snapshot.update({k:v.detach().cpu().numpy().copy() for k,v in fields.items()})
            snapshot['causes']={f'{term}/{cause}':v.detach().cpu().numpy().copy()
                for term,items in env.termination_manager.last_term_breakdowns.items() for cause,v in items.items()}
            snapshot['terms']={k:v.detach().cpu().numpy().copy() for k,v in env.termination_manager.last_term_results.items()}
        env._check_termination=capture
        modes=args.modes or (['zero','reference_current','reference_next']+(['old_policy'] if args.policy else []))
        for mode in modes:
            adapter=None
            if mode=='old_policy':
                from holosoma.carry.inference import CarryActor
                meta=json.loads(args.policy.with_suffix('.actor.json').read_text())
                for key,actual in [('default_joint_pos',env.default_dof_pos[0]),('p_gains',env.p_gains),
                    ('d_gains',env.d_gains),('action_scales',env.action_scales)]:
                    torch.testing.assert_close(torch.tensor(meta[key],device=env.device),actual,atol=1e-5,rtol=0)
                assert abs(meta['control_dt']-env.dt)<1e-9
                adapter=CarryActor(args.policy,args.num_envs,'cuda:0')
            for condition in args.conditions:
                env.is_evaluating=condition!='training_reset'
                mid,frame={'training_reset':(0,0),'squat_high':(0,0),'squat_low':(0,175),
                    'walking_start':(1,0),'repeated_start':(2,0)}[condition]
                cmd.motion_cfg=replace(cmd.motion_cfg,eval_fixed_reset=replace(cmd.motion_cfg.eval_fixed_reset,
                    enabled=True,motion_id=mid,local_frame=frame))
                torch.manual_seed(args.seed);obs=env.reset_all()
                if adapter:adapter.reset()
                mids=cmd.motion_ids.detach().cpu().numpy().copy();starts=cmd.time_steps.clone()
                initial=dict(q_max_error_rad=float((env.simulator.dof_pos-cmd.joint_pos).abs().max()),
                    object_position_error_m=float((simulator_box_state(env)[:,:3]-cmd.object_pos_w).norm(dim=-1).max()),
                    actor_shape=list(obs['actor_obs'].shape),critic_shape=list(obs['critic_obs'].shape),
                    root_position_error_m=float((cmd.robot_root_pos_w-cmd.root_pos_w).norm(dim=-1).max()))
                initial['joint_clamp_max_error_rad']=(env.simulator.dof_pos-cmd.joint_pos).abs().max(0).values.cpu().tolist()
                initial['q_default_error_rad']=float((env.default_dof_pos[0]-torch.tensor(static_audit()['q_default'],device=env.device)).abs().max())
                alive=np.ones(args.num_envs,bool);records=[];failures=[[] for _ in range(args.num_envs)]
                for step in range(round(args.seconds/env.dt)):
                    index=cmd.time_steps
                    if mode=='zero':action=torch.zeros(args.num_envs,29,device=env.device)
                    elif mode.startswith('reference'):
                        if mode=='reference_next':index=torch.minimum(index+1,cmd.motion.motion_end_idx[cmd.motion_ids]-1)
                        action=(cmd.motion.joint_pos[index]-env.default_dof_pos)/env.action_scales
                    else:
                        action=adapter.act(env.simulator.robot_root_states[:],env.simulator.dof_pos,env.simulator.dof_vel,
                            simulator_box_state(env),cmd.task_command,env.simulator.scene.env_origins[:,2])
                    before=cmd.time_steps.clone()
                    obs,_,_,_=env.step({'actions':action})
                    record={k:v for k,v in snapshot.items() if k not in ['causes','terms']}
                    record['alive']=alive.copy();record['step']=np.full(args.num_envs,step+1)
                    records.append(record)
                    for i in np.where(alive & snapshot['failed'])[0]:
                        failures[i]=[k for k,v in snapshot['causes'].items() if v[i]]
                        failures[i]+=[k for k,v in snapshot['terms'].items() if v[i] and k not in ['physical_failure','track_failure','body_proximity']]
                    # Confirm reward/termination used the same index as the pre-action command.
                    assert np.array_equal(snapshot['ref_index'],before.cpu().numpy())
                    continuing=~torch.as_tensor(snapshot['failed']|snapshot['timeout'],device=env.device)
                    expected_after=torch.minimum(before+1,cmd.motion.motion_end_idx[cmd.motion_ids]-1)
                    assert torch.equal(cmd.time_steps[continuing],expected_after[continuing])
                    alive &= ~(snapshot['failed']|snapshot['timeout'])
                    if not alive.any():break
                arrays={k:np.stack([r[k] for r in records]) for k in records[0]}
                path=args.output/(mode+'_'+condition+'.npz');np.savez_compressed(path,**arrays)
                trials=[]
                for i in range(args.num_envs):
                    mask=arrays['alive'][:,i];last=np.where(mask)[0][-1]
                    trials.append(dict(env=i,motion_id=int(mids[i]),local_start_frame=int(starts[i]-cmd.motion.motion_start_idx[int(mids[i])]),
                        survival_s=float(arrays['episode_s'][last,i]),censored=bool(alive[i]),failures=failures[i],
                        timed_out=bool(arrays['timeout'][last,i]),
                        contact_mean=float(arrays['bilateral_contact'][mask,i].mean()),
                        robot_error_m=float(arrays['robot_error_m'][mask,i].mean()),object_error_m=float(arrays['object_error_m'][mask,i].mean()),
                        torque_clip_fraction=float(arrays['torque_clip_fraction'][mask,i].mean())))
                item=dict(mode=mode,condition=condition,initial=initial,trials=trials,rollout_file=str(path))
                result['conditions'].append(item)
                (args.output/'rollouts.json').write_text(json.dumps(result,indent=2)+'\n')
                print(json.dumps(dict(mode=mode,condition=condition,initial=initial,
                    median_survival_s=float(np.median([r['survival_s'] for r in trials])),surviving=int(alive.sum()))),flush=True)
        result['complete']=True
        (args.output/'rollouts.json').write_text(json.dumps(result,indent=2)+'\n')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--runtime',action='store_true');p.add_argument('--num-envs',type=int,default=64)
    p.add_argument('--seconds',type=float,default=2.);p.add_argument('--seed',type=int,default=1000)
    p.add_argument('--policy',type=Path)
    p.add_argument('--modes',nargs='+',choices=['zero','reference_current','reference_next','old_policy'])
    p.add_argument('--conditions',nargs='+',choices=['training_reset','squat_high','squat_low','walking_start','repeated_start'],
        default=['training_reset','squat_high','squat_low','walking_start','repeated_start'])
    args=p.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    if args.modes and 'old_policy' in args.modes and not args.policy:p.error('old_policy requires --policy')
    (args.output/'static.json').write_text(json.dumps(static_audit(),indent=2)+'\n')
    if args.runtime:run_rollouts(args)


if __name__=='__main__':main()
