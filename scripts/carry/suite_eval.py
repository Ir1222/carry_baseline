"""First-episode physical evaluation. Capture terminal physics BEFORE auto reset."""
import argparse
from collections import Counter
from dataclasses import replace
import json
from pathlib import Path

from holosoma.carry.checkpoints import atomic_json

DEFAULT_GATES = dict(stage1_success=.8, support_ratio=.8, support_quality=.4,
    robot_error_m=.15, object_error_m=.15, robot_orientation_rad=.35, object_orientation_rad=.45, box_tilt_rad=.45,
    stage2_success=.8, steady_fraction=.9, velocity_error=.10, yaw_error=.15,
    height_error=.03, minimum_box_height=.4, maximum_separation=.9)

# Required curriculum level and commands within that level's trained ranges.
SCENARIOS = {
    'hold': (0, [(0, [0,0,0,.735])]),
    'forward': (1, [(0, [.10,0,0,.735])]),
    'backward': (2, [(0, [-.08,0,0,.735])]),
    'lateral_positive': (2, [(0, [0,.08,0,.735])]),
    'lateral_negative': (2, [(0, [0,-.08,0,.735])]),
    'yaw_positive': (3, [(0, [0,0,.20,.735])]),
    'yaw_negative': (3, [(0, [0,0,-.20,.735])]),
    'height_low': (4, [(0, [0,0,0,.715])]),
    'height_high': (4, [(0, [0,0,0,.755])]),
    'combined': (4, [(0, [.10,.06,.15,.745])]),
    'forward_stop_forward': (1, [(0,[.10,0,0,.735]), (6,[0,0,0,.735]), (12,[.10,0,0,.735])]),
    'multiple_changes': (4, [(0,[0,0,0,.735]),(3,[.1,0,0,.735]),(6,[0,-.08,0,.735]),
        (9,[0,0,.2,.735]),(12,[0,0,0,.715]),(15,[-.06,.04,-.15,.745])]),
}


def summarize(rows, suite, gates, seconds, level):
    import numpy as np
    names = sorted(set(r['scenario'] for r in rows))
    groups = {}
    for name in names:
        trials = [r for r in rows if r['scenario'] == name]
        supported = suite == 'stage1' or SCENARIOS[name][0] <= level
        success = sum(r['success'] for r in trials)/len(trials)
        groups[name] = dict(seeds=len(trials), supported=supported, success_rate=success,
            survival_s=float(np.mean([r['survival_s'] for r in trials])),
            mean_abs_command_errors=np.mean([r['mean_abs_command_errors'] for r in trials], axis=0).tolist(),
            support_ratio=float(np.mean([r['support_ratio'] for r in trials])),
            mean_contact_quality=float(np.mean([r['mean_contact_quality'] for r in trials])),
            robot_error_m=float(np.mean([r['robot_error_m'] for r in trials])),
            object_error_m=float(np.mean([r['object_error_m'] for r in trials])),
            max_tilt_rad=max(r['max_tilt_rad'] for r in trials),
            min_box_height_m=min(r['min_box_height_m'] for r in trials),
            max_separation_m=max(r['max_separation_m'] for r in trials),
            failure_counts=dict(Counter(c for r in trials for c in r['failures'])))
    score = float(np.mean([x['success_rate'] for x in groups.values()])) if groups else 0.
    passed = bool(groups) and all(x['seeds'] >= 10 and x['success_rate'] >= gates[
        'stage1_success' if suite == 'stage1' else 'stage2_success'] for x in groups.values())
    if suite != 'stage1':
        passed &= seconds >= 20 and level == 4 and len(groups) == len(SCENARIOS)
    return dict(suite=suite, passed=bool(passed), score=score, curriculum_level=level,
                requested_seconds=seconds, thresholds=gates, scenarios=groups,
                failure_counts=dict(Counter(c for r in rows for c in r['failures'])),
                first_episode_only=True, reference_loader_forbidden=suite != 'stage1')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--suite', choices=['stage1','goal'], required=True)
    p.add_argument('--policy', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--seeds', type=int, default=10)
    p.add_argument('--seconds', type=float, default=20.)
    p.add_argument('--level', type=int, default=0)
    p.add_argument('--only', choices=list(SCENARIOS))
    p.add_argument('--gates', type=Path)
    p.add_argument('--seed-offset', type=int, default=1000)
    p.add_argument('--forbid-motion-loading', action='store_true')
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    gates = DEFAULT_GATES.copy()
    if args.gates:
        gates.update(json.loads(args.gates.read_text()))
    if args.suite == 'stage1' and args.forbid_motion_loading:
        p.error('Stage1 tracking needs references; only goal evaluation is reference-free')
    from holosoma.carry.presets import g1_29dof_wbt_hybrid_carry as base, DATA
    from holosoma.config_types.command import CommandManagerCfg, CommandTermCfg
    from holosoma.config_types.env import get_tyro_env_config
    from holosoma.config_types.observation import ObservationManagerCfg
    from holosoma.config_types.termination import TerminationManagerCfg
    from holosoma.train_agent import TrainingContext
    if args.suite == 'stage1':
        term = base.command.setup_terms['motion_command']
        motion = term.params['motion_config']
        motion = replace(motion, hybrid=replace(motion.hybrid, track_ratio=1.),
            eval_fixed_reset=replace(motion.eval_fixed_reset, enabled=True, motion_id=0, local_frame=0))
        command_cfg = replace(base.command, setup_terms={'motion_command': replace(term,
            params={**term.params, 'motion_config': motion})})
        termination = base.termination
    else:
        target = 'holosoma.carry.deployment:DeploymentCommand'
        command_cfg = CommandManagerCfg(setup_terms={'motion_command': CommandTermCfg(func=target,
            params={'reset_pose_file': str(DATA/'verified_reset.json')})},
            reset_terms={'motion_command': CommandTermCfg(func=target)},
            step_terms={'motion_command': CommandTermCfg(func=target)})
        termination = TerminationManagerCfg(terms={'physical_failure': base.termination.terms['physical_failure'],
            'body_proximity': base.termination.terms['body_proximity']})
    config = replace(base, training=replace(base.training, num_envs=args.seeds, headless=True),
        command=command_cfg, termination=termination,
        observation=ObservationManagerCfg(groups={'actor_obs':base.observation.groups['actor_obs']}),
        reward=replace(base.reward, terms={k:v for k,v in base.reward.terms.items()
            if k in ('velocity_tracking','yaw_tracking','height_tracking','stable_carry','hand_support','box_orientation')}))
    context = TrainingContext(config)
    context.__enter__()
    try:
        import torch
        import numpy as np
        import random
        from holosoma.carry.environment import CarryEnv
        from holosoma.carry.inference import CarryActor
        from holosoma.carry.observations import simulator_box_state
        from holosoma.carry.rewards import task_errors, contact_quality
        from holosoma.utils.rotations import quaternion_to_matrix, quat_error_magnitude
        if args.suite != 'stage1':
            from holosoma.managers.command.terms import wbt
            def forbidden(*a, **kw):
                raise AssertionError('Reference motion loading forbidden during goal evaluation')
            wbt.MotionLoader.__init__ = forbidden
            wbt.MultiMotionLoader.__init__ = forbidden
        env = CarryEnv(get_tyro_env_config(config), device='cuda:0')
        env.set_is_evaluating()
        actor = CarryActor(args.policy, args.seeds, 'cuda:0')
        command = env.command_manager.get_state('motion_command')
        original_check = env._check_termination
        captured = {}

        def capture():
            original_check()
            box = simulator_box_state(env)
            root = env.simulator.robot_root_states[:]
            forces = env.simulator.hand_box_forces()
            up = (-forces[:,:,2].sum(-1)).clamp_min(0)
            mass = env.simulator._object.root_physx_view.get_masses().to(env.device).flatten()
            bilateral = (torch.linalg.vector_norm(forces,dim=-1)>.5).all(-1)
            values = dict(errors=task_errors(env).abs(), contact=contact_quality(env),
                supported=bilateral & (up >= .5*mass*9.81),
                hand_forces=torch.linalg.vector_norm(forces,dim=-1), upward_weight_ratio=up/(mass*9.81),
                box_height=box[:,2]-env.simulator.scene.env_origins[:,2],
                root_height=root[:,2]-env.simulator.scene.env_origins[:,2],
                robot_tilt=torch.acos(quaternion_to_matrix(root[:,3:7],w_last=True)[:,2,2].clamp(-1,1)),
                tilt=torch.acos(quaternion_to_matrix(box[:,3:7],w_last=True)[:,2,2].abs().clamp(0,1)),
                separation=torch.linalg.vector_norm(box[:,:3]-root[:,:3],dim=-1),
                done=env.reset_buf.bool(), timeout=env.time_out_buf.bool())
            if args.suite == 'stage1':
                values['robot_error'] = torch.linalg.vector_norm(command.robot_body_pos_w-command.body_pos_relative_w,dim=-1).mean(-1)
                values['object_error'] = torch.linalg.vector_norm(box[:,:3]-command.object_pos_w,dim=-1)
                values['object_orientation_error'] = quat_error_magnitude(box[:,3:7],command.object_quat_w,w_last=True)
                values['robot_orientation_error'] = quat_error_magnitude(root[:,3:7],command.root_quat_w,w_last=True)
            else:
                values['robot_error'] = torch.zeros(args.seeds,device=env.device)
                values['object_error'] = torch.zeros(args.seeds,device=env.device)
                values['object_orientation_error'] = torch.zeros(args.seeds,device=env.device)
                values['robot_orientation_error'] = torch.zeros(args.seeds,device=env.device)
            captured.clear()
            captured.update({k:v.detach().cpu().numpy().copy() for k,v in values.items()})
            causes = {k:v for k,v in env.termination_manager.last_term_results.items() if k not in ('timeout','clip_timeout')}
            causes.update(env.termination_manager.last_term_breakdowns.get('physical_failure',{}))
            captured['causes'] = {k:v.detach().cpu().numpy().copy() for k,v in causes.items()}
            captured['rewards'] = {k:float(torch.as_tensor(v).float().mean()) for k,v in env.log_dict.items()
                if ('rew_' in k or 'reward' in k) and torch.isfinite(torch.as_tensor(v)).all()}
        env._check_termination = capture
        # Every episode has its own seeded 0.002-rad joint reset perturbation.
        # This is applied only through the normal reset path; no writes during rollout.
        original_reset = command.reset
        reset_generators = [torch.Generator(device=env.device).manual_seed(args.seed_offset+i) for i in range(args.seeds)]
        def reset(ids):
            original_reset(ids)
            ids = torch.arange(args.seeds,device=env.device) if ids is None else ids
            for index in ids.tolist():
                env.simulator.dof_pos[index] += .002*torch.randn(29,device=env.device,generator=reset_generators[index])
        command.reset = reset
        if args.suite == 'stage1':
            scenarios = [(f'clip_{i}', i, None) for i in range(int(command.motion.num_motions))]
        else:
            scenarios = [(k,None,v[1]) for k,v in SCENARIOS.items() if args.only is None or args.only == k]
        rows = []
        with (args.output/'steps.jsonl').open('x') as raw:
            for name, clip, schedule in scenarios:
                torch.manual_seed(args.seed_offset); np.random.seed(args.seed_offset); random.seed(args.seed_offset)
                reset_generators = [torch.Generator(device=env.device).manual_seed(args.seed_offset+i) for i in range(args.seeds)]
                if clip is not None:
                    command.motion_cfg = replace(command.motion_cfg, eval_fixed_reset=replace(
                        command.motion_cfg.eval_fixed_reset,motion_id=clip))
                    seconds = float(command.motion.motion_end_idx[clip]-command.motion.motion_start_idx[clip])*env.dt
                else:
                    seconds = args.seconds
                env.reset_all(); actor.reset()
                alive = np.ones(args.seeds,dtype=bool)
                data = [[] for _ in range(args.seeds)]
                failures = [[] for _ in range(args.seeds)]
                completed = np.zeros(args.seeds,dtype=bool)
                last_change = 0.
                for step in range(max(1,int(round(seconds/env.dt))) + (2 if clip is not None else 0)):
                    if step > 0:
                        if schedule:
                            for when, value in schedule:
                                if step == max(1,round(when/env.dt)):
                                    command.set_command(value); last_change = step*env.dt
                        action = actor.act(env.simulator.robot_root_states[:],env.simulator.dof_pos,env.simulator.dof_vel,
                            simulator_box_state(env),command.task_command,env.simulator.scene.env_origins[:,2])
                        assert torch.isfinite(action).all()
                        _, _, done, _ = env.step({'actions':action})
                        actor.reset(torch.where(done)[0])
                    snapshot = {k:v.tolist() for k,v in captured.items() if k not in ('causes','rewards')}
                    snapshot.update(scenario=name,step=step,causes={k:v.tolist() for k,v in captured['causes'].items()},
                        rewards=captured['rewards'], alive=alive.tolist())
                    raw.write(json.dumps(snapshot,allow_nan=False)+'\n')
                    for i in np.where(alive)[0]:
                        data[i].append(dict(errors=captured['errors'][i],contact=float(captured['contact'][i]),
                            supported=bool(captured['supported'][i]), box_height=float(captured['box_height'][i]),
                            tilt=float(captured['tilt'][i]), separation=float(captured['separation'][i]),
                            robot_error=float(captured['robot_error'][i]),object_error=float(captured['object_error'][i]),
                            robot_orientation_error=float(captured['robot_orientation_error'][i]),
                            object_orientation_error=float(captured['object_orientation_error'][i]),
                            steady=step*env.dt-last_change >= 1.))
                        causes = [k for k,v in captured['causes'].items() if v[i]]
                        if captured['done'][i]:
                            if clip is not None and captured['timeout'][i] and not causes:
                                completed[i] = True
                            else:
                                failures[i] = causes or ['physical_reset']
                            alive[i] = False
                    if not alive.any():
                        break
                for i, values in enumerate(data):
                    n = len(values)
                    support = float(np.mean([v['supported'] and v['contact']>=gates['support_quality'] for v in values]))
                    steady = [v for v in values if v['steady']]
                    errors = np.mean([v['errors'] for v in values],axis=0)
                    tracking_fraction = float(np.mean([bool(np.all(v['errors'] <= [gates['velocity_error'],gates['velocity_error'],
                        gates['yaw_error'],gates['height_error']])) for v in steady])) if steady else 0.
                    robot_error = float(np.mean([v['robot_error'] for v in values]))
                    object_error = float(np.mean([v['object_error'] for v in values]))
                    robot_orientation = float(np.mean([v['robot_orientation_error'] for v in values]))
                    object_orientation = float(np.mean([v['object_orientation_error'] for v in values]))
                    max_tilt = max(v['tilt'] for v in values)
                    min_height = min(v['box_height'] for v in values)
                    max_separation = max(v['separation'] for v in values)
                    complete = bool(completed[i]) if clip is not None else not failures[i] and n*env.dt >= seconds-.5*env.dt
                    physical = support>=gates['support_ratio'] and max_tilt<=gates['box_tilt_rad'] and min_height>=gates['minimum_box_height'] and max_separation<=gates['maximum_separation']
                    tracking = (robot_error<=gates['robot_error_m'] and object_error<=gates['object_error_m']
                        and robot_orientation<=gates['robot_orientation_rad'] and object_orientation<=gates['object_orientation_rad']) if clip is not None else tracking_fraction>=gates['steady_fraction']
                    reasons = failures[i].copy()
                    if not complete and not reasons: reasons.append('incomplete_reference' if clip is not None else 'short_episode')
                    if not physical: reasons.append('physical_metrics_gate')
                    if not tracking: reasons.append('tracking_quality_gate')
                    rows.append(dict(scenario=name,seed=args.seed_offset+i,success=bool(complete and physical and tracking),
                        reference_completed=complete if clip is not None else None,expected_duration_s=seconds,
                        survival_s=n*env.dt,support_ratio=support,mean_contact_quality=float(np.mean([v['contact'] for v in values])),
                        mean_abs_command_errors=errors.tolist(),steady_tracking_fraction=tracking_fraction,
                        robot_error_m=robot_error,object_error_m=object_error,max_tilt_rad=max_tilt,
                        robot_orientation_error_rad=robot_orientation,object_orientation_error_rad=object_orientation,
                        min_box_height_m=min_height,max_separation_m=max_separation,failures=reasons))
                atomic_json(args.output/'episodes.json',rows)
        result = summarize(rows,args.suite,gates,args.seconds,args.level)
        result['selection_score'] = float(np.mean([.6*r['success'] + .2*min(1.,r['survival_s']/r['expected_duration_s'])
            + .1*r['support_ratio'] + .1*np.exp(-r['object_error_m']/.15-r['robot_error_m']/.15) for r in rows]))
        result.update(policy=str(args.policy.resolve()),reset_joint_noise_std=.002)
        atomic_json(args.output/'summary.json',result)
        lines = [f'# {args.suite} physical evaluation',f'Gate passed: **{result["passed"]}**; score: {result["score"]:.3f}',
            'Each seed counts only its first continuous episode. Terminal metrics are captured before reset.',
            '| Scenario | Supported | Success | Survival (s) | Support | Failures |','|---|---|---:|---:|---:|---|']
        for name, s in result['scenarios'].items():
            lines.append(f'| {name} | {s["supported"]} | {s["success_rate"]:.0%} | {s["survival_s"]:.2f} | {s["support_ratio"]:.2f} | {s["failure_counts"]} |')
        lines += ['', 'Thresholds: '+json.dumps(gates), 'Full per-seed metrics: episodes.json; terminal physics: steps.jsonl.']
        (args.output/'report.md').write_text('\n\n'.join(lines[:3])+'\n\n'+'\n'.join(lines[3:]))
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(12,4))
        names = list(result['scenarios'])
        ax.bar(names,[result['scenarios'][n]['success_rate'] for n in names])
        ax.set(ylim=(0,1),ylabel='Physical success fraction',title=f'{args.suite}: first continuous episode')
        ax.tick_params(axis='x',rotation=35); fig.tight_layout(); fig.savefig(args.output/'physical_success.png'); plt.close(fig)
        print(json.dumps(result),flush=True)
    finally:
        context.__exit__(None,None,None)


if __name__ == '__main__':
    main()
