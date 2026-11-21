"""First-episode free-box evaluation; capture failures before the environment auto-reset."""
import argparse
from dataclasses import replace
import json
from pathlib import Path
import queue
import threading


def schedules(limits):
    h,l=limits['height_high'],limits['height_low'];v=limits['vx_high']
    return dict(standing=[(0,[0,0,0,h])],low_hold=[(0,[0,0,0,l])],
        squat=[(0,[0,0,0,h]),(3,[0,0,0,l])],
        stand_up=[(0,[0,0,0,l]),(10,[0,0,0,h])],
        forward_slow=[(0,[v*.4,0,0,h])],forward_fast=[(0,[v*.9,0,0,h])],
        forward_squat=[(0,[v*.5,0,0,h]),(5,[v*.5,0,0,l])],
        forward_stand=[(0,[v*.5,0,0,l]),(10,[v*.5,0,0,h])],
        continuous_cycle=[(0,[0,0,0,h]),(3,[0,0,0,l]),(8,[0,0,0,h]),(13,[0,0,0,l]),(18,[0,0,0,h])],
        goal_switching=[(0,[0,0,0,h]),(3,[v*.6,0,0,h]),(7,[0,0,0,h]),(11,[0,0,0,l]),(17,[0,0,0,h])])


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--suite',choices=['stage1','goal'],required=True)
    p.add_argument('--policy',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--seeds',type=int,default=10)
    p.add_argument('--seed-offset',type=int,default=1000)
    p.add_argument('--seconds',type=float,default=24.)
    p.add_argument('--only')
    p.add_argument('--view',action='store_true')
    p.add_argument('--interactive',action='store_true')
    p.add_argument('--video',action='store_true')
    p.add_argument('--data',type=Path,help='Optional reference bundle override, checked against actor metadata')
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    policy_meta=json.loads(a.policy.with_suffix('.actor.json').read_text())
    if policy_meta.get('fullbody_schema')!=1:
        raise ValueError('Refusing a legacy palm-support ONNX policy in the FullBody scene')
    joint_stage1=policy_meta.get('reference_bundle_schema')=='carry_track_training_v2'
    import os
    mode=policy_meta.get('action_parameterization','fixed_default_v1')
    if mode not in ('fixed_default_v1','joint_delta_v1'):raise ValueError('Unknown actor action parameterization')
    os.environ['HMI_CARRY_ACTION_MODE']='joint_delta' if mode=='joint_delta_v1' else 'fixed'
    if joint_stage1:
        if a.suite!='stage1':p.error('Joint Stage1 actor is evaluated with --suite stage1; Gen command control is a Stage2 task')
        bundle=a.data or Path(policy_meta.get('reference_bundle',''))
        if bundle.is_dir():
            import os
            os.environ['HMI_STAGE1_DATA']=str(bundle.resolve())
        from holosoma.carry.stage1_presets import g1_29dof_carry_stage1_joint as base,DATA
        from holosoma.carry.checkpoints import digest
        if digest(DATA/'manifest.json')!=policy_meta['reference_manifest_sha256']:
            raise ValueError('Evaluation references differ from the exported actor training bundle')
    else:
        from holosoma.carry.fullbody_presets import g1_29dof_fullbody_carry as base,DATA
    from holosoma.config_types.command import CommandManagerCfg,CommandTermCfg
    from holosoma.config_types.observation import ObservationManagerCfg
    from holosoma.config_types.termination import TerminationManagerCfg
    from holosoma.config_types.env import get_tyro_env_config
    from holosoma.config_types.video import CartesianCameraConfig
    limits=json.loads((DATA/'goal_limits.json').read_text())
    if a.suite=='stage1':
        term=base.command.setup_terms['motion_command'];m=term.params['motion_config']
        m=replace(m,hybrid=replace(m.hybrid,track_ratio=1.),
            eval_fixed_reset=replace(m.eval_fixed_reset,enabled=True,motion_id=0,local_frame=0))
        command=replace(base.command,setup_terms={'motion_command':replace(term,params={**term.params,'motion_config':m})})
        termination=base.termination
    else:
        target='holosoma.carry.fullbody_deployment:FullBodyDeploymentCommand'
        command=CommandManagerCfg(setup_terms={'motion_command':CommandTermCfg(func=target,params=dict(
            reset_pose_file=str(DATA/'verified_side_grasp_reset.json'),goal_limits_file=str(DATA/'goal_limits.json')))},
            reset_terms={'motion_command':CommandTermCfg(func=target)},step_terms={'motion_command':CommandTermCfg(func=target)})
        termination=TerminationManagerCfg(terms={k:v for k,v in base.termination.terms.items() if k in ('physical_failure','body_proximity')})
    config=replace(base,training=replace(base.training,num_envs=a.seeds,headless=not a.view),command=command,
        termination=termination,observation=ObservationManagerCfg(groups={'actor_obs':base.observation.groups['actor_obs']}),
        reward=replace(base.reward,terms={k:v for k,v in base.reward.terms.items() if k in
            ('velocity_tracking','yaw_tracking','height_tracking','stable_carry','grasp','hand_slip','box_orientation','nonhand_contact')}),
        logger=replace(base.logger,base_dir=str(a.output),headless_recording=a.video,
            video=replace(base.logger.video,enabled=a.video,interval=1,trigger='episode',clip_duration_s=a.seconds,
                camera=CartesianCameraConfig(offset=[1.6,-1.6,.8],target_offset=[.2,0.,0.],smoothing=0.,tracking_body_name='pelvis'))))
    from holosoma.carry.runtime import simulation_context
    with simulation_context(config,a.output/'exception.txt'):
        import numpy as np
        import torch
        from holosoma.carry.fullbody_environment import FullBodyCarryEnv
        from holosoma.carry.inference import CarryActor
        from holosoma.carry.observations import simulator_box_state
        from holosoma.carry.rewards import task_errors
        from holosoma.carry.fullbody_rewards import physical_metrics
        from holosoma.carry.checkpoints import atomic_json
        from holosoma.utils.rotations import quat_rotate_inverse,quat_error_magnitude
        if a.suite=='goal':
            from holosoma.managers.command.terms import wbt
            def forbidden(*args,**kwargs):raise AssertionError('Motion loading forbidden during deployment')
            wbt.MotionLoader.__init__=forbidden;wbt.MultiMotionLoader.__init__=forbidden
        if joint_stage1:
            from holosoma.carry.stage1_environment import Stage1CarryEnv
            env=Stage1CarryEnv(get_tyro_env_config(config),device='cuda:0')
        else:
            env=FullBodyCarryEnv(get_tyro_env_config(config),device='cuda:0')
        env.set_is_evaluating()
        if abs(policy_meta['control_dt']-env.dt)>1e-9:
            raise ValueError('Policy action frequency differs from the physical scene')
        torch.testing.assert_close(torch.tensor(policy_meta['default_joint_pos'],device=env.device),
            env.default_dof_pos[0],atol=1e-6,rtol=0)
        torch.testing.assert_close(torch.tensor(policy_meta['action_scales'],device=env.device),
            env.action_scales,atol=1e-6,rtol=0)
        cmd=env.command_manager.get_state('motion_command')
        actor=CarryActor(a.policy,a.seeds,'cuda:0')
        if a.suite=='stage1':scenarios={f'clip_{i}':None for i in range(cmd.motion.num_motions)}
        else:scenarios=schedules(limits)
        expected_scenarios=set(scenarios)
        if a.only:scenarios={a.only:scenarios[a.only]}
        pending=queue.SimpleQueue()
        if a.interactive:
            def read():
                while True:
                    try:pending.put(list(map(float,input('vx vy yaw_rate pelvis_height> ').split())))
                    except EOFError:return
                    except ValueError:print('Enter four SI values',flush=True)
            threading.Thread(target=read,daemon=True).start()
        snapshot={};original=env._check_termination
        handids=[env.simulator._robot.body_names.index(s+'_sphere_hand_link') for s in ('left','right')]
        footids=[env.simulator._body_list.index(s+'_ankle_roll_link') for s in ('left','right')]
        def capture():
            original()
            root=env.simulator.robot_root_states[:];box=simulator_box_state(env)
            hp=env.simulator._robot.data.body_pos_w[:,handids]
            rel=quat_rotate_inverse(box[:,None,3:7].expand(-1,2,-1).reshape(-1,4),
                (hp-box[:,None,:3]).reshape(-1,3),w_last=True).reshape(-1,2,3)
            values=dict(root=root,box=box,q=env.simulator.dof_pos,qd=env.simulator.dof_vel,
                hand_local=rel,goal=cmd.task_command,error=task_errors(env),
                failed=env.termination_manager.terminated,timeout=env.time_out_buf,
                foot_slip_speed=(env.simulator._rigid_body_vel[:,footids,:2].norm(dim=-1)*
                    (env.simulator.contact_forces[:,footids,2]>5)).max(-1).values,
                **physical_metrics(env))
            if a.suite=='stage1':
                values.update(robot_tracking_error_m=(cmd.robot_body_pos_w-cmd.body_pos_relative_w).norm(dim=-1).mean(-1),
                    object_tracking_error_m=(box[:,:3]-cmd.object_pos_w).norm(dim=-1),
                    object_tracking_error_rad=quat_error_magnitude(box[:,3:7],cmd.object_quat_w,w_last=True))
            snapshot.clear();snapshot.update({k:v.detach().cpu().numpy().copy() for k,v in values.items()})
            snapshot['causes']={f'{term}/{cause}':v.cpu().numpy().copy() for term,items in
                env.termination_manager.last_term_breakdowns.items() for cause,v in items.items()}
        env._check_termination=capture
        rows=[]
        for name,schedule in scenarios.items():
            torch.manual_seed(a.seed_offset)
            seconds=a.seconds
            if a.suite=='stage1':
                clip=int(name.split('_')[-1]);m=cmd.motion_cfg
                cmd.motion_cfg=replace(m,eval_fixed_reset=replace(m.eval_fixed_reset,motion_id=clip))
                seconds=float(cmd.motion.motion_end_idx[clip]-cmd.motion.motion_start_idx[clip])*env.dt
            original_reset=cmd.reset
            def reset(ids):
                original_reset(ids)
                ids=torch.arange(a.seeds,device=env.device) if ids is None else ids
                for i in ids.tolist():
                    g=torch.Generator(device=env.device).manual_seed(a.seed_offset+i)
                    env.simulator.dof_pos[i]+=.001*torch.randn(29,device=env.device,generator=g)
            cmd.reset=reset
            env.reset_all();actor.reset();cmd.reset=original_reset
            alive=np.ones(a.seeds,dtype=bool);records=[];causes=[set() for _ in range(a.seeds)]
            for step in range(int(round(seconds/env.dt))+1):
                if schedule:
                    for when,goal in schedule:
                        if step==round(when/env.dt):
                            cmd.set_command(goal)
                if not pending.empty():cmd.set_command(pending.get())
                action=actor.act(env.simulator.robot_root_states[:],env.simulator.dof_pos,env.simulator.dof_vel,
                    simulator_box_state(env),cmd.task_command,env.simulator.scene.env_origins[:,2])
                env.step({'actions':action})
                if not snapshot:raise RuntimeError('Terminal physics capture missing')
                record={k:v for k,v in snapshot.items() if k!='causes'}
                record.update(alive=alive.copy(),time=np.full(a.seeds,(step+1)*env.dt))
                records.append(record)
                for i in np.where(alive & snapshot['failed'])[0]:
                    causes[i].update(k for k,v in snapshot['causes'].items() if v[i])
                alive &= ~(snapshot['failed'] | snapshot['timeout'])
                if a.view and step%25==0:
                    print(name,'goal',snapshot['goal'][0].tolist(),'actual vx,h',
                        float(snapshot['goal'][0,0]+snapshot['error'][0,0]),float(snapshot['root'][0,2]),flush=True)
                if not alive.any():break
            arrays={k:np.stack([r[k] for r in records]) for k in records[0]}
            np.savez_compressed(a.output/(name+'_rollout.npz'),**arrays)
            for i in range(a.seeds):
                mask=arrays['alive'][:,i];t=arrays['time'][mask,i];err=abs(arrays['error'][mask,i])
                height=arrays['root'][mask,i,2]
                slip=np.linalg.norm(arrays['hand_local'][mask,i]-arrays['hand_local'][0,i],axis=-1).max()
                contact=float(arrays['bilateral_contact'][mask,i].mean())
                steady=t>3.
                mae=err.mean(0);steady_mae=err[steady].mean(0) if steady.any() else mae
                survived=float(t[-1])>=seconds-env.dt*2 and not causes[i]
                row=dict(scenario=name,seed=a.seed_offset+i,survival_s=float(t[-1]),survived=survived,
                    command_mae=mae.tolist(),steady_command_mae=steady_mae.tolist(),
                    contact_continuity=contact,max_hand_slip_m=float(slip),
                    min_box_clearance_m=float(arrays['box_clearance_m'][mask,i].min()),
                    pelvis_amplitude_m=float(np.ptp(height)),
                    normal_forces_mean_n=[float(arrays[k][mask,i].mean()) for k in ('left_hand_normal_n','right_hand_normal_n')],
                    friction_weight_ratio_mean=float(arrays['upward_friction_weight_ratio'][mask,i].mean()),
                    normal_vertical_fraction_max=float(arrays['normal_vertical_fraction'][mask,i].max()),
                    contact_height_above_bottom_min_m=float(arrays['min_contact_height_above_bottom_m'][mask,i].min()),
                    nonhand_box_contact_max_n=float(arrays['nonhand_box_contact_n'][mask,i].max()),
                    foot_slip_speed_mean_m_s=float(arrays['foot_slip_speed'][mask,i].mean()),
                    joint_speed_rms=float(np.sqrt(np.mean(arrays['qd'][mask,i]**2))),
                    failures=sorted(causes[i]))
                # Same side-grasp/friction gates as P0; normal-force magnitude
                # alone must not admit palm-up support.
                from holosoma.carry.acceptance import physical_failures
                row['failures']+=physical_failures(row)
                row['success']=not row['failures']
                if a.suite=='stage1':
                    row['robot_tracking_error_m']=float(arrays['robot_tracking_error_m'][mask,i].mean())
                    row['object_tracking_error_m']=float(arrays['object_tracking_error_m'][mask,i].mean())
                    row['object_tracking_error_rad_max']=float(arrays['object_tracking_error_rad'][mask,i].max())
                    start=int(cmd.motion.motion_start_idx[clip]);end=int(cmd.motion.motion_end_idx[clip])
                    expected_amplitude=float(cmd.motion.body_pos_w[start:end,0,2].max()-cmd.motion.body_pos_w[start:end,0,2].min())
                    row['reference_pelvis_amplitude_m']=expected_amplitude
                    row['success'] &= row['robot_tracking_error_m']<.10 and row['object_tracking_error_m']<.04 and row['object_tracking_error_rad_max']<=.20
                    if expected_amplitude>.08:row['success'] &= row['pelvis_amplitude_m']>.10
                else:
                    row['success'] &= bool(steady_mae[0]<.10 and steady_mae[3]<.03)
                    requires_forward=name.startswith('forward') or name=='goal_switching'
                    row['reference_supported']=not requires_forward or limits['forward_admitted']
                    if not row['reference_supported']:
                        row['success']=False;row['failures'].append('forward_reference_not_admitted')
                    if name in ('squat','stand_up','forward_squat','forward_stand','continuous_cycle','goal_switching'):
                        row['success'] &= row['pelvis_amplitude_m']>.10
                    # Whole segments, including unsuccessful switches, are retained.
                    row['command_segments']=[]
                    actual=arrays['goal'][mask,i]+arrays['error'][mask,i]
                    down=[];up=[]
                    for j,(when,goal) in enumerate(schedule):
                        end=schedule[j+1][0] if j+1<len(schedule) else seconds
                        sm=(t>=when)&(t<end)
                        target_error=abs(actual-np.array(goal))
                        hit=sm&(target_error[:,0]<.1)&(target_error[:,3]<.03)
                        tail=sm&(t>=max(when,end-1.))
                        reached=bool(tail.any() and target_error[tail,0].mean()<.1 and target_error[tail,3].mean()<.03)
                        completed=bool(end<=t[-1]+env.dt)
                        row['command_segments'].append(dict(start_s=when,goal=goal,
                            observed=bool(sm.any()),completed=completed,target_reached=reached,
                            first_tracking_latency_s=float(t[hit][0]-when) if hit.any() else None))
                        row['success'] &= completed and reached
                        if j and schedule[j-1][1][3]-goal[3]>.08:down.append(completed and reached)
                        if j and goal[3]-schedule[j-1][1][3]>.08:up.append(completed and reached)
                    row['squat_completion_rate']=float(np.mean(down)) if down else None
                    row['stand_completion_rate']=float(np.mean(up)) if up else None
                rows.append(row)
            atomic_json(a.output/'trials.json',rows)
        groups={name:dict(success_rate=float(np.mean([r['success'] for r in rows if r['scenario']==name])),
            trials=len([r for r in rows if r['scenario']==name])) for name in scenarios}
        score=float(np.mean([g['success_rate'] for g in groups.values()]))
        complete_suite=set(groups)==expected_scenarios
        from holosoma.carry.acceptance import tracking_suite_passed
        passed=tracking_suite_passed(groups,expected_scenarios,a.seeds)
        if a.suite=='goal':passed &= limits['forward_admitted'] and limits['vx_high']>0 and len(groups)==10 and a.seconds>=20
        result=dict(passed=passed,score=score,suite=a.suite,groups=groups,trials=rows,goal_limits=limits,
            reference_free=a.suite=='goal',terminal_state_before_reset=True,physical_model=env.fullbody_physics,
            complete_suite=complete_suite,expected_scenarios=sorted(expected_scenarios),joint_stage1=joint_stage1,
            accepted_policy=False if not passed else True)
        if joint_stage1:
            result['motion_families']={f'clip_{i}':r['family'] for i,r in
                enumerate(sorted(cmd.manifest['motions'],key=lambda r:r['name']))}
        atomic_json(a.output/'evaluation.json',result)
        (a.output/'report.md').write_text('# Measured FullBody evaluation\n\n'+json.dumps(result,indent=2)+'\n')
        print(json.dumps(dict(passed=passed,score=score,groups=groups)),flush=True)


if __name__=='__main__':main()
