"""Persist measured outcomes and auto-commit the report when the bounded run exits."""
import argparse
import json
from pathlib import Path
import subprocess
import time

REPO=Path(__file__).resolve().parents[2]
BASE=REPO.parent/'artifacts/fullbody_goal_carry'


def report(root,state):
    goals=json.loads((BASE/'reference_v1/goal_limits.json').read_text())
    preflight=json.loads((BASE/'preflight.json').read_text())
    physics=json.loads((BASE/'physics_interface_gate_001.json').read_text())
    forward=json.loads((BASE/'forward_hold_diagnosis_003_data/validation.json').read_text())
    config=json.loads((root/'config.json').read_text())
    source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()
    quality={}
    from analyze_fullbody import analyze
    for path in (root/'evaluations').glob('*') if (root/'evaluations').exists() else []:
        if list(path.glob('*_rollout.npz')):
            quality[str(path)]=analyze(path,BASE/'reference_v1')
    text=['# FullBody Goal Carry — measured experiment report',
        f'Status: **{state.get("status")} / {state.get("stage")}**. '
        'This file is a progress report while RUNNING. Only independent physical acceptance grants a usable policy.',
        f'Branch: `{branch}`. Current source commit: `{source}`. P0 preservation commit: `ed106a7`. '
        f'Initial run source: `{config["source_commit"]}`. Additional source versions are retained as `source_*.tar`.',
        f'Run directory: `{root}`. PID, process identity and current command: '
        +json.dumps(state.get('active_job'),ensure_ascii=False),
        '## P0 and source integrity',
        json.dumps(preflight,indent=2),
        'P0 verification is controller-only. Source NPZ checksums and motion family priors are in '
        '`../artifacts/fullbody_goal_carry/reference_v1/manifest.json`. Original P0 assets, old resets and checkpoints were preserved.',
        '## Actual physics and controller interface',json.dumps(physics,indent=2),
        'The PPO actor supplies position offsets at 50Hz. PD runs at 1000Hz within the original torque limits. '
        'There is no P0 WBC/static-force feedforward, object attachment, gantry support or post-reset object pose write.',
        '## Reference admission and unresolved forward capability',
        'The direct forward trial failed its pre-motion grip gate. A separate 3-pose × 3-force diagnostic passed '
        f'{forward["summary"]["passed"]}/{forward["summary"]["tested"]} cases. '
        'Static pose diagnostics are not a certification of continuous forward locomotion. '
        'No forward motion is admitted; vx remains 0 rather than mixing a failed clip into training.',
        'Failure evidence: `forward_probe_001_data/rollout.npz`, `forward_probe_001_data/pre_motion_gate.json`, '
        '`forward_hold_diagnosis_003_data/validation.json`. Additional failed engineering runs are also retained.',
        '## Goal distribution and style',json.dumps(goals,indent=2),
        'Four-dimensional interface [vx,vy,yaw_rate,pelvis_height], 348D Actor and 184D Critic. Gen vy/yaw are zero. '
        'Six conditional modes sample vx/h independently in mixed mode; half the environments execute a continuous '
        'standing→squat→low hold→stand cycle. Height transitions use reference-derived bounded smoothstep rates. '
        'Style matches full-body posture and hand-box geometry using height, ascent/descent direction, vx and temporal continuity. '
        'Compatibility reduces its influence outside the reference distribution. Deployment does not load references.',
        '## Training configuration, resource benchmark and budgets',json.dumps(config,indent=2),
        json.dumps(state.get('benchmark',[]),indent=2),
        'Every job retains its exact command, source version, console, per-iteration timing and GPU samples. '
        'See `dashboard/` for TensorBoard and `jobs/*/iterations.jsonl` for simulation/learner timings. '
        'Training and evaluation use the GPU serially. Stage 1 starts from scratch; Stage 2 requires the physical Stage 1 gate.',
        '## Stage 1 measured evaluations',json.dumps(state.get('stage1_evaluations',[]),indent=2),
        '## Stage 2 measured evaluations',json.dumps(state.get('stage2_evaluations',[]),indent=2),
        '## Style ablation',json.dumps(state.get('style_ablation','Not executed; cannot claim an improvement'),indent=2),
        '## Motion-quality analysis',json.dumps(quality,indent=2),
        '## Best checkpoints, acceptance and inference artifacts',
        json.dumps({k:state.get(k) for k in ('best_stage1','best_stage2','valid_stage1','valid_stage2','final_checkpoint')},indent=2),
        'Unaccepted models stay in best_stage*/ and must not be presented as usable final policies. '
        'Accepted models, full config and ONNX metadata are copied into deliverables/. '
        'ONNX parity is tested at training export and the CPU exporter; per-model errors are in .actor.json. '
        'Viewer/interactive/evaluation/export commands are in README_FULLBODY_CARRY.md.',
        '## Stop reason, failures and remaining work',
        json.dumps({k:state.get(k) for k in ('blocker','gpu_seconds','stage1_corrections','stage2_corrections','last_job')},indent=2),
        'Unimplemented or unverified capabilities must be read from the measured acceptance tables, not inferred from '
        'finite PPO losses or rising rewards. Forward reference contact consistency is a known blocker. '
        'No unseen forward+height combinations, lateral motion or turning are certified. '
        'For vy/yaw extension, first admit compatible dynamic references and separately benchmark each command family. '
        'Failed policies and failed references are retained rather than hidden.',
        '## Reproduction',
        'See README_FULLBODY_CARRY.md for environment activation, validation, Stage 1/2, resume, automatic controller, '
        'TensorBoard, checkpoint evaluation, ONNX export, Viewer, interactive four-dimensional commands and goal grid. '
        'TensorBoard for this workspace: http://127.0.0.1:6011 .']
    target=REPO/'FULLBODY_GOAL_CARRY_FINAL_REPORT.md'
    target.write_text('\n\n'.join(text)+'\n')
    (root/target.name).write_text(target.read_text())


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=BASE/'current')
    p.add_argument('--watch',action='store_true');a=p.parse_args();root=a.root.resolve()
    started=time.monotonic()
    while True:
        state=json.loads((root/'training_status.json').read_text())
        if not a.watch or state.get('supervisor_exited'):break
        if time.monotonic()-started>52*3600:raise TimeoutError('Finite finalizer wait exceeded 52 hours')
        time.sleep(15)
    report(root,state)
    if a.watch and state.get('status') in ('COMPLETED','BLOCKED'):
        # Stage only our generated report. Never commit a user's concurrent edits.
        subprocess.run(['git','add','--','FULLBODY_GOAL_CARRY_FINAL_REPORT.md'],cwd=REPO,check=True)
        changed=subprocess.run(['git','diff','--cached','--quiet','--','FULLBODY_GOAL_CARRY_FINAL_REPORT.md'],cwd=REPO)
        if changed.returncode==1:
            subprocess.run(['git','commit','--only','-m','Record measured FullBody run outcome: '+state['status'],
                '--','FULLBODY_GOAL_CARRY_FINAL_REPORT.md'],cwd=REPO,check=True)
            head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
            (root/'report_commit.json').write_text(json.dumps(dict(commit=head,status=state['status']),indent=2)+'\n')


if __name__=='__main__':main()
