"""First-episode free-box probes or policy evaluation. Never chains clips by teleport."""
import argparse,json
from dataclasses import replace
from pathlib import Path

CASE_NAMES=('A_pickup','B_loaded_walk','C_single_squat','D_repeated_squat','E_full_pick_carry_putdown',
    'pickup_carry_boundary','carry_putdown_boundary','release_tail_stability','pickup_contact_probe','putdown_support_probe','release_probe')

def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--probe',action='store_true');g.add_argument('--policy',type=Path)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--seeds',type=int,default=2)
    p.add_argument('--view',action='store_true');p.add_argument('--video',action='store_true');p.add_argument('--only')
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    if not a.only:
        # Independent scenarios must not share PhysX contact/warm-start history.
        # One child at a time also prevents concurrent Isaac processes on GPU0.
        import subprocess,sys
        if a.view:p.error('Use --only CASE with the interactive viewer')
        groups={};trials=[];resets=[];sources=[];physics=None;ground=False
        for name in CASE_NAMES:
            child=a.output/name;argv=[sys.executable,str(Path(__file__).resolve()),'--probe'] if a.probe else [sys.executable,str(Path(__file__).resolve()),'--policy',str(a.policy.resolve())]
            argv+=['--output',str(child.resolve()),'--only',name,'--seeds',str(a.seeds)]
            if a.video:argv+=['--video']
            with (a.output/(name+'.log')).open('w') as log:subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=240)
            file=child/'evaluation.json'
            if not file.exists():raise RuntimeError('Isaac child returned without its evaluation artifact: '+str(file))
            result=json.loads(file.read_text());groups.update(result['groups']);trials+=result['trials'];resets+=result['resets'];sources.append(str(file));physics=result['physics'];ground|=result['ground_sensor_verified']
            print(json.dumps(dict(case=name,result=groups[name])),flush=True)
        required=CASE_NAMES[:5];passed=bool(not a.probe and a.seeds>=10 and all(groups[k]['success_rate']>=.8 for k in required))
        result=dict(kind='reference_position_probe' if a.probe else 'policy_evaluation',passed=passed,policy_success_claim=passed,
            independent_scenes=True,groups=groups,trials=trials,resets=resets,physics=physics,ground_sensor_verified=ground,evidence_files=sources,
            unavailable={'F_walk_squat_walk':'No validated continuous transition reference; not silently concatenated'})
        (a.output/'evaluation.json').write_text(json.dumps(result,indent=2)+'\n');return
    from holosoma.carry.unified_presets import g1_29dof_unified_hoi_stage1 as base,DATA
    from holosoma.config_types.env import get_tyro_env_config
    from holosoma.carry.runtime import simulation_context
    cfg=replace(base,training=replace(base.training,num_envs=a.seeds,headless=not a.view),logger=replace(base.logger,base_dir=str(a.output),
        headless_recording=a.video,video=replace(base.logger.video,enabled=a.video,interval=1,trigger='episode',clip_duration_s=15.)))
    with simulation_context(cfg,a.output/'exception.txt'):
        import numpy as np
        import torch
        from holosoma.carry.unified import UnifiedCarryEnv,MODES
        from holosoma.carry.unified_inference import UnifiedActor
        from holosoma.carry.observations import simulator_box_state
        from holosoma.carry.acceptance import physical_failures
        from holosoma.utils.rotations import quat_error_magnitude,quat_rotate_inverse
        env=UnifiedCarryEnv(get_tyro_env_config(cfg),device='cuda:0');env.set_is_evaluating();cmd=env.command_manager.get_state('motion_command')
        actor=None if a.probe else UnifiedActor(a.policy,a.seeds,'cuda:0')
        if actor:
            from holosoma.carry.checkpoints import digest
            if actor.metadata['reference_manifest_sha256']!=digest(DATA/'manifest.json'):raise ValueError('Evaluation dataset does not match checkpoint')
        byname={r['name']:i for i,r in enumerate(cmd.rows)}
        cases={'A_pickup':('full_sequence',0,95),'B_loaded_walk':('loaded_locomotion',0,110),
            'C_single_squat':('continuous_grasped_squat_stand',0,351),'D_repeated_squat':('repeated_grasped_squat_stand',0,651),
            'E_full_pick_carry_putdown':('full_sequence',0,325),
            'pickup_carry_boundary':('full_sequence',90,103),'carry_putdown_boundary':('full_sequence',200,213),
            'release_tail_stability':('full_sequence',310,325),
            'pickup_contact_probe':('full_sequence',25,65),'putdown_support_probe':('full_sequence',271,325),
            'release_probe':('full_sequence',285,325)}
        if a.only:cases={a.only:cases[a.only]}
        snap={};original=env._check_termination
        handids=[env.simulator._robot.body_names.index(s+'_sphere_hand_link') for s in ['left','right']]
        def capture():
            original();box=simulator_box_state(env);hp=env.simulator._robot.data.body_pos_w[:,handids]
            hand=quat_rotate_inverse(box[:,None,3:7].expand(-1,2,-1).reshape(-1,4),(hp-box[:,None,:3]).reshape(-1,3),w_last=True).reshape(-1,2,3)
            values=dict(**env.hoi_metrics,mode=cmd.task_mode,frame=cmd.time_steps-cmd.motion.motion_start_idx[cmd.motion_ids],
                root=env.simulator.robot_root_states[:],box=box,q=env.simulator.dof_pos,qd=env.simulator.dof_vel,hand_local=hand,
                ground_force=env.simulator.scene.sensors['box_ground'].data.force_matrix_w.sum((1,2)),
                box_net_normal=env.simulator.scene.sensors['box_ground'].data.net_forces_w.sum(1),
                robot_error_m=(cmd.robot_body_pos_w-cmd.body_pos_relative_w).norm(dim=-1).mean(-1),object_error_m=(box[:,:3]-cmd.object_pos_w).norm(dim=-1),
                object_error_rad=quat_error_magnitude(box[:,3:7],cmd.object_quat_w,w_last=True),failed=env.termination_manager.terminated,timeout=env.time_out_buf)
            snap.clear();snap.update({k:v.detach().cpu().numpy().copy() for k,v in values.items()})
            snap['causes']={f'{term}/{cause}':x.cpu().numpy().copy() for term,items in env.termination_manager.last_term_breakdowns.items() for cause,x in items.items()}
        env._check_termination=capture;rows=[];reset_rows=[]
        for name,(clip,start,end) in cases.items():
            mid=byname[clip];cmd.motion_cfg=replace(cmd.motion_cfg,eval_fixed_reset=replace(cmd.motion_cfg.eval_fixed_reset,enabled=True,motion_id=mid,local_frame=start))
            torch.manual_seed(1000)
            original_reset=cmd.reset
            def seeded_reset(ids):
                original_reset(ids)
                for i in ids.tolist():
                    g=torch.Generator(device=env.device).manual_seed(1000+i)
                    env.simulator.dof_vel[i]+=.001*torch.randn(29,device=env.device,generator=g)
            if actor:cmd.reset=seeded_reset
            obs=env.reset_all();cmd.reset=original_reset
            torch.testing.assert_close(env.simulator.dof_pos,cmd.joint_pos,atol=2e-6,rtol=0)
            assert obs['actor_obs'].shape==(a.seeds,357) and obs['critic_obs'].shape==(a.seeds,env.critic_dim)
            reset_rows.append(dict(case=name,q_error=float((env.simulator.dof_pos-cmd.joint_pos).abs().max()),root_error=float((cmd.root_pos_w-cmd.robot_root_pos_w).abs().max()),
                box_error=float((simulator_box_state(env)[:,:3]-cmd.object_pos_w).abs().max())))
            if actor:actor.reset()
            alive=np.ones(a.seeds,bool);records=[];causes=[set() for _ in range(a.seeds)]
            for step in range(end-start-1):
                before=cmd.time_steps.clone()
                if a.probe:
                    target=torch.minimum(before+1,cmd.motion.motion_end_idx[cmd.motion_ids]-1)
                    action=(cmd.motion.joint_pos[target]-env.simulator.dof_pos)/env.action_scales
                else:action=actor.act(env.simulator.robot_root_states[:],env.simulator.dof_pos,env.simulator.dof_vel,simulator_box_state(env),cmd.task_command,
                    env.simulator.scene.env_origins[:,2],cmd.task_mode)
                env.step({'actions':action})
                record={k:v for k,v in snap.items() if k!='causes'};record['alive']=alive.copy();records.append(record)
                for i in np.where(alive&snap['failed'])[0]:causes[i].update(k for k,v in snap['causes'].items() if v[i])
                alive &= ~(snap['failed']|snap['timeout'])
                if a.view and step%25==0:print(name,MODES[int(snap['mode'][0])],'h',float(snap['root'][0,2]),flush=True)
                if not alive.any():break
            arrays={k:np.stack([r[k] for r in records]) for k in records[0]};np.savez_compressed(a.output/(name+'.npz'),**arrays)
            for i in range(a.seeds):
                mask=arrays['alive'][:,i];carry=mask&(arrays['mode'][:,i]==1);last=np.where(mask)[0][-1]
                row=dict(case=name,seed=1000+i if actor else None,replica=i,steps=int(mask.sum()),survival_s=float(mask.sum()*.02),failures=sorted(causes[i]),
                    robot_error_m=float(arrays['robot_error_m'][mask,i].mean()),object_error_m=float(arrays['object_error_m'][mask,i].mean()),
                    object_orientation_error_rad=float(arrays['object_error_rad'][mask,i].mean()),modes_seen=sorted(set(arrays['mode'][mask,i].tolist())),
                    pelvis_amplitude=float(np.ptp(arrays['root'][mask,i,2])),stable_putdown=bool(arrays['putdown_stable_success'][last,i]),
                    phases={mode:dict(steps=int((mask&(arrays['mode'][:,i]==j)).sum()),
                        metrics={k:float(arrays[k][mask&(arrays['mode'][:,i]==j),i].mean()) for k in ['bilateral_contact','left_hand_normal_n','right_hand_normal_n','upward_friction_weight_ratio',
                            'hand_slip_speed_m_s','box_clearance_m','ground_support_weight_ratio','object_speed_m_s','nonhand_box_contact_n',
                            'torque_clip_fraction','joint_hard_limit_violation','joint_acceleration_rms','foot_sliding_m_s']} if (mask&(arrays['mode'][:,i]==j)).any() else {}) for j,mode in enumerate(MODES)})
                finished=int(arrays['frame'][last,i])>=end-1 and not causes[i]
                row['success']=finished and row['robot_error_m']<.1 and row['object_error_m']<.04 and row['object_orientation_error_rad']<.2
                if carry.any():
                    loc=arrays['hand_local'][carry,i];physical=dict(survived=finished,contact_continuity=float(arrays['bilateral_contact'][carry,i].mean()),
                        max_hand_slip_m=float(np.linalg.norm(loc-loc[0],axis=-1).max()),min_box_clearance_m=float(arrays['box_clearance_m'][carry,i].min()),
                        friction_weight_ratio_mean=float(arrays['upward_friction_weight_ratio'][carry,i].mean()),normal_vertical_fraction_max=float(arrays['normal_vertical_fraction'][carry,i].max()),
                        contact_height_above_bottom_min_m=float(arrays['min_contact_height_above_bottom_m'][carry,i].min()),nonhand_box_contact_max_n=float(arrays['nonhand_box_contact_n'][carry,i].max()))
                    row['carry_physical']=physical;row['failures']+=physical_failures(physical);row['success'] &= not physical_failures(physical)
                if name.startswith(('C_','D_')):row['success'] &= row['pelvis_amplitude']>.10
                if name=='A_pickup':row['success'] &= bool(arrays['grasp_acquired'][last,i]) and float(arrays['box_clearance_m'][last,i])>.03
                if name=='E_full_pick_carry_putdown':row['success'] &= row['modes_seen']==[0,1,2] and row['stable_putdown']
                rows.append(row)
        expected=['A_pickup','B_loaded_walk','C_single_squat','D_repeated_squat','E_full_pick_carry_putdown']
        groups={name:dict(success_rate=sum(r['success'] for r in rows if r['case']==name)/a.seeds,trials=a.seeds) for name in cases}
        result=dict(kind='reference_position_probe' if a.probe else 'policy_evaluation',policy_success_claim=False,
            passed=bool(not a.probe and a.seeds>=10 and set(expected)<=set(groups) and all(groups[k]['success_rate']>=.8 for k in expected)),
            groups=groups,trials=rows,resets=reset_rows,physics=env.fullbody_physics,
            unavailable={'F_walk_squat_walk':'No validated continuous transition reference; not silently concatenated'},
            ground_filter_paths=env.simulator.hoi_ground_filter_paths,
            nonhand_link_names=env.simulator.carry_other_links,
            contact_statistics='mean over all 20 physics substeps; continuous no-contact timer advances by sim_dt',
            initial_joint_velocity_perturbation_std_rad_s=.001 if actor else 0.,
            ground_sensor_verified=any(r['phases']['putdown']['metrics'].get('ground_support_weight_ratio',0)>.5 for r in rows))
        result['policy_success_claim']=result['passed']
        (a.output/'evaluation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(groups),flush=True)

if __name__=='__main__':main()
