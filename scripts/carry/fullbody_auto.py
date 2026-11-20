"""Finite FullBody controller reusing the existing single-GPU persistent supervisor."""
import argparse
from collections import Counter
import fcntl
import json
import os
from pathlib import Path
import shutil
import statistics
import subprocess
import sys
import time
import auto_train as legacy
from holosoma.carry.checkpoints import atomic_json,newest_valid

REPO=legacy.REPO
BASE=REPO.parent/'artifacts/fullbody_goal_carry'


class FullBodySupervisor(legacy.Supervisor):
    def train_argv(self,name,n,updates,ratio,checkpoint=None,log_group=None):
        argv=super().train_argv(name,n,updates,ratio,checkpoint,log_group)
        argv=[v.replace('exp:g1-29dof-wbt-hybrid-carry','exp:g1-29dof-fullbody-carry') for v in argv]
        correction=self.state.get('correction',{})
        if name.startswith('stage'):
            argv+=correction.get('arguments',[])
        return argv

    def benchmark(self):
        rows=self.state.setdefault('benchmark',[])
        for n in self.config['candidates']:
            if any(r['num_envs']==n for r in rows):continue
            if rows and n>4096 and rows[-1].get('peak_gpu_memory_mib',0)>13000:
                self.event('Skip 8192: measured 4096 memory leaves insufficient predicted headroom')
                break
            self.save(stage='BENCHMARK',num_envs=n)
            row=dict(num_envs=n,stable=False,samples_per_iteration=n*24,minibatches=n//64,epochs=5)
            try:
                out,result=self.job(f'benchmark_{n}',self.train_argv(f'bench{n}',n,
                    self.config['warmup_updates']+self.config['benchmark_updates'],1.,log_group='benchmark'),
                    self.config['benchmark_timeout_s'],worker=True)
                iterations=[json.loads(s) for s in (out/'iterations.jsonl').read_text().splitlines()]
                measured=iterations[self.config['warmup_updates']:]
                if len(measured)<self.config['benchmark_updates']:raise RuntimeError('Incomplete benchmark')
                for key in ('steps_per_s','rollout_s','simulation_s','update_s'):
                    row[key]=statistics.median(i[key] for i in measured)
                row.update(stable=True,iterations_per_s=1/(row['rollout_s']+row['update_s']),
                    peak_gpu_memory_mib=result['peak_gpu_memory_mib'],evidence=str(out),
                    physx_errors=0,nan_errors=0,crash_exit_code=0)
            except legacy.Stop:raise
            except Exception as error:
                row.update(evidence=str(error),peak_gpu_memory_mib=self.state.get('last_job',{}).get('peak_gpu_memory_mib',0))
            rows.append(row);self.save(benchmark=rows);self.benchmark_report(rows)
            self.record_experiment('scaling',row,'retain' if row['stable'] else 'reject')
            if not row['stable']:break
        self.select_benchmark(rows)

    def evaluate(self,checkpoint,stage,final=False):
        self.save(stage='EVAL1' if stage=='stage1' else 'EVAL2')
        dest=self.root/'evaluations'/f'{stage}_{time.time_ns()}'
        args=[sys.executable,str(REPO/'scripts/carry/evaluate_fullbody.py'),'--suite',
            'stage1' if stage=='stage1' else 'goal','--policy',str(Path(checkpoint['path']).with_suffix('.onnx')),
            '--output',str(dest),'--seeds',str(self.config['final_seeds'] if final else self.config['evaluation_seeds']),
            '--seconds','24']
        self.job(stage+'_evaluation',args,self.config['evaluation_timeout_s'],stage=stage)
        result=legacy.read_json(dest/'evaluation.json')
        if not result or not result['terminal_state_before_reset']:raise RuntimeError('No pre-reset physical evidence')
        from analyze_fullbody import analyze
        result['motion_quality']=analyze(dest,BASE/'reference_v1')
        trials=result['trials']
        survival=statistics.mean(min(1,r['survival_s']/(13 if stage=='stage1' else 24)) for r in trials)
        contact=statistics.mean(r['contact_continuity'] for r in trials)
        result.update(directory=str(dest),checkpoint=checkpoint['path'],final=final,
            selection_score=result['score']+.2*survival+.1*contact,
            failure_counts=dict(Counter(c for r in trials for c in r['failures'])),scenarios=result['groups'])
        self.save(latest_evaluation=result)
        shutil.copy2(dest/'report.md',self.root/f'{stage}_evaluation.md')
        for key in ('score','selection_score','passed'):
            self.scalars({f'evaluation/{stage}/{key}':result[key]},checkpoint['completed_updates'])
        self.event('Measured free-box evaluation',stage=stage,passed=result['passed'],score=result['score'],
            selection_score=result['selection_score'],failures=result['failure_counts'])
        self.record_experiment('evaluation',dict(stage=stage,checkpoint=checkpoint,metrics=result),
            'accepted' if result['passed'] else 'not accepted')
        return result

    def record_experiment(self,kind,evidence,decision):
        with (self.root/'autoresearch.jsonl').open('a') as f:
            f.write(json.dumps(dict(time=time.time(),kind=kind,evidence=evidence,decision=decision))+'\n')

    def retain(self,checkpoint,stage,result,force=False):
        super().retain(checkpoint,stage,result,force)
        best=self.state.get('best_'+stage)
        if best and best['sha256']==checkpoint['sha256'] and Path(checkpoint['path']).parent.joinpath('holosoma_config.yaml').exists():
            shutil.copy2(Path(checkpoint['path']).parent/'holosoma_config.yaml',Path(best['path']).parent/'holosoma_config.yaml')

    def accept_final(self,checkpoint,stage,result):
        accepted=super().accept_final(checkpoint,stage,result)
        if accepted:
            dest=self.root/'deliverables';dest.mkdir(exist_ok=True)
            source=Path(self.state['valid_'+stage]['path'])
            for suffix in ('.pt','.ready.json','.onnx','.actor.json','.export.json'):
                if source.with_suffix(suffix).exists():
                    shutil.copy2(source.with_suffix(suffix),dest/f'best_{stage}_model{suffix}')
            shutil.copy2(source.parent/'holosoma_config.yaml',dest/f'best_{stage}_config.yaml')
            if stage=='stage2':
                # Camera evaluation is serialized after training and the final
                # multi-seed evaluation; failure to render cannot fake physics.
                video_dest=self.root/'viewer_evaluation'
                self.job('final_policy_video',[sys.executable,str(REPO/'scripts/carry/evaluate_fullbody.py'),
                    '--suite','goal','--only','continuous_cycle','--policy',str(source.with_suffix('.onnx')),
                    '--output',str(video_dest),'--seeds','1','--seconds','24','--video'],1800,stage=stage)
        return accepted

    def diagnose(self,stage,history):
        latest=history[-1]
        rows=latest['trials']
        diagnostic=dict(stage=stage,evaluation=latest['directory'],failures=latest['failure_counts'],
            mean_contact=statistics.mean(r['contact_continuity'] for r in rows),
            mean_survival_s=statistics.mean(r['survival_s'] for r in rows),
            mean_friction_ratio=statistics.mean(r['friction_weight_ratio_mean'] for r in rows),
            max_nonhand_contact_n=max(r['nonhand_box_contact_max_n'] for r in rows),
            correction_attempt=self.state.get('correction_attempt',0))
        atomic_json(self.root/'diagnosis_metrics.json',diagnostic)
        (self.root/'root_cause_diagnosis.md').write_text('# Measured stagnation diagnosis\n\n'+json.dumps(diagnostic,indent=2))

    def training_stage(self,stage):
        if stage=='stage2' and not self.state.get('style_ablation'):
            self.style_ablation()
        while True:
            try:
                return super().training_stage(stage)
            except RuntimeError as error:
                if 'progress stagnated' not in str(error):raise
                attempt=self.state.get(stage+'_corrections',0)
                if attempt>=self.config['max_corrections']:raise
                diagnostic=legacy.read_json(self.root/'diagnosis_metrics.json',{})
                # These are hypotheses, not guaranteed fixes. All evaluation
                # gates and physical parameters remain identical.
                if diagnostic.get('mean_contact',1)<.99 and attempt==0:
                    correction=dict(reason='Measured bilateral contact below 99%; increase physical grasp objective',
                        arguments=['--reward.terms.grasp.weight=6.0','--reward.terms.hand-slip.weight=2.0'])
                elif stage=='stage1' and attempt<=1:
                    correction=dict(reason='No full clip completion; increase high-pose starts while retaining adaptive low-frame training',
                        arguments=['--reward.terms.grasp.weight=6.0',
                            '--command.setup-terms.motion-command.params.motion-config.start-at-timestep-zero-prob=0.5'])
                else:
                    correction=dict(reason='Physical selection score stagnant; test smaller PPO learning rate',
                        arguments=['--reward.terms.grasp.weight=6.0','--algo.config.actor-learning-rate=0.00005',
                            '--algo.config.critic-learning-rate=0.00005'])
                attempt+=1
                atomic_json(self.root/f'{stage}_correction_{attempt}.json',dict(diagnostic=diagnostic,**correction))
                self.record_experiment('correction',dict(stage=stage,attempt=attempt,**correction),'test next comparable window')
                self.save(**{stage+'_corrections':attempt,stage+'_stagnant':0},correction=correction)
                # Exact same fresh/resume/ONNX checks, reduced PPO run before
                # committing the revised allocation to a longer window.
                current,_=newest_valid(self.root/'dashboard'/stage)
                self.job(f'{stage}_correction_{attempt}_smoke',self.train_argv(stage+'_correction_smoke',64,3,
                    1. if stage=='stage1' else .5,current['path'],'correction_smoke'),300,stage=stage,worker=True)

    def style_ablation(self):
        """Same Stage1 checkpoint, seed and budget; neither arm is a final policy."""
        initial=self.state['valid_stage1']['path'];results={}
        for label,weight in [('without_style',0.),('with_style',.5)]:
            argv=self.train_argv('stage2_ablation_'+label,self.state['num_envs'],128,.5,initial,'ablation_'+label)
            argv+=['--training.seed=42',f'--reward.terms.goal-compatible-style-reward.weight={weight}']
            out,_=self.job('style_ablation_'+label,argv,self.remaining('stage2'),stage='stage2',worker=True)
            checkpoint,_=newest_valid(legacy.read_json(out/'worker_result.json')['log_dir'],require_export=True)
            results[label]=self.evaluate(checkpoint,'stage2')
        atomic_json(self.root/'style_ablation.json',results)
        self.save(style_ablation=results)
        self.record_experiment('style_ablation',results,'compare physical/goal/joint smoothness metrics; no presumed improvement')

    def run(self):
        # Parent owns the existing GPU lock and reaps only its recorded children.
        legacy.BASE=BASE
        try:super().run()
        finally:self.write_report()

    def write_report(self):
        status=legacy.read_json(self.root/'training_status.json',self.state)
        lines=['# FullBody Goal Carry measured run report',
            'Status: '+status.get('status','unknown'),
            'No checkpoint is accepted unless its independent multi-seed physical evaluation passes.',
            'Branch: '+subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip(),
            'Source commit: '+self.config['source_commit'],
            'Run directory: '+str(self.root),
            'Reference version and physics contract: '+str(BASE/'reference_v1'),
            'Forward reference admission: '+json.dumps(legacy.read_json(BASE/'reference_v1/goal_limits.json')),
            'Environment throughput benchmark: '+json.dumps(status.get('benchmark',[]),indent=2),
            'Stage 1 results: '+json.dumps(status.get('stage1_evaluations',[]),indent=2),
            'Stage 2 results: '+json.dumps(status.get('stage2_evaluations',[]),indent=2),
            'Best Stage 1: '+json.dumps(status.get('best_stage1'),indent=2),
            'Best Stage 2: '+json.dumps(status.get('best_stage2'),indent=2),
            'Blocker: '+str(status.get('blocker')),
            'Budget consumed (wall seconds including startup/evaluation): '+json.dumps(status.get('gpu_seconds',{})),
            'Limitations: forward remains excluded unless independently admitted. P0 controller validation is not PPO validation. '
            'All failed jobs, commands, source snapshots, GPU traces and physical rollouts are retained in this run directory. '
            'Style ablation is only meaningful after Stage 1 passes; absent results must not be read as a style benefit. '
            'Future vy/yaw require physically feasible reference coverage and separately measured curriculum admission.']
        (self.root/'FULLBODY_GOAL_CARRY_FINAL_REPORT.md').write_text('\n\n'.join(lines)+'\n')
        # This is explicitly a status report until all final gates pass.
        shutil.copy2(self.root/'FULLBODY_GOAL_CARRY_FINAL_REPORT.md',REPO/'FULLBODY_GOAL_CARRY_FINAL_REPORT.md')


def initialize():
    BASE.mkdir(exist_ok=True)
    root=BASE/('run_'+time.strftime('%Y%m%d_%H%M%S'))
    root.mkdir(exist_ok=False)
    defaults=dict(legacy.DEFAULT)
    defaults.update(candidates=[4096,8192],fixed_num_envs=None,warmup_updates=4,benchmark_updates=12,
        stage1_gpu_hours=24.,stage2_gpu_hours=24.,first_eval_updates=500,eval_every=500,
        checkpoint_every=500,stage1_max_updates=15000,stage2_max_updates=20000,
        evaluation_seeds=10,final_seeds=10,max_corrections=3,poll_seconds=10,report_seconds=60,
        source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip())
    atomic_json(root/'config.json',defaults)
    atomic_json(root/'training_status.json',dict(stage='BENCHMARK',status='CREATED',gpu_seconds={},root=str(root)))
    with (root/'source.tar').open('wb') as f:subprocess.run(['git','archive','HEAD'],cwd=REPO,stdout=f,check=True)
    (root/'autoresearch.md').write_text('Hypothesis: PPO can acquire the P0-validated 12cm side-grasp reference under 50Hz position actions. '
        'No P0 force feedforward or WBC is used. Decision metrics are free-box multi-seed physical rollouts. '
        'Stage 1 max15000 /24h, Stage 2 max20000 /24h; max3 evidence-based corrections. '
        'Primary failure criteria, gravity and collisions never change.\n')
    (root/'autoresearch.sh').write_text('#!/bin/bash\nset -euo pipefail\nbash '+str(REPO/'scripts/carry/train_fullbody_auto.sh')+' resume\n')
    current=BASE/'current';tmp=BASE/('.current_'+str(os.getpid()));tmp.symlink_to(root.name);os.replace(tmp,current)
    print(root)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['init','run']);p.add_argument('--root',type=Path)
    a=p.parse_args()
    if a.action=='init':initialize()
    else:FullBodySupervisor((a.root or BASE/'current').resolve()).run()
