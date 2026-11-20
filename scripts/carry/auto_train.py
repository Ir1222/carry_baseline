"""Persistent, finite-budget single-GPU carry experiment controller.

Launch via carryctl.sh. All decisions use measured physics, never an LLM.
"""
import argparse
import csv
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import signal
import socket
import statistics
import subprocess
import sys
import time

from holosoma.carry.checkpoints import atomic_json, newest_valid, validate

REPO = Path(__file__).resolve().parents[2]
BASE = REPO.parent/'artifacts/auto_training'
DEFAULT = dict(candidates=[4096], fixed_num_envs=4096, warmup_updates=2, benchmark_updates=8,
    benchmark_timeout_s=1800, stage1_gpu_hours=24., stage2_gpu_hours=24., eval_every=2000,
    first_eval_updates=2000, checkpoint_every=50, evaluation_seeds=10, final_seeds=30,
    evaluation_timeout_s=1800, minimum_free_gib=15., headroom_mib=4096,
    stage1_max_updates=15000,stage2_max_updates=15000,stagnation_windows=3,
    minimum_improvement=.01,poll_seconds=60,report_seconds=300)
BAD = re.compile(r'Traceback \(most recent call last\)|CUDA out of memory|CUDA error:|'
    r'PhysX.*(?:error|overflow)|(?:error|overflow).*PhysX|'
    r'GPU.*(?:buffer.*overflow|capacity.*exceeded)|found nan|nonfinite (?:state|action|tensor)|invalid transform',re.I)


class Stop(Exception):
    pass


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def gpu_sample():
    value = subprocess.check_output(['nvidia-smi','--query-gpu=memory.used,memory.total,utilization.gpu',
        '--format=csv,noheader,nounits'],text=True,timeout=10).strip().splitlines()[0]
    used,total,util = [int(x.strip()) for x in value.split(',')]
    return dict(memory_mib=used,total_mib=total,utilization_pct=util)


def gpu_owners():
    result = subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader,nounits'],text=True,timeout=10)
    owners=[]
    for line in result.splitlines():
        if not line.strip().isdigit(): continue
        pid=int(line)
        try:
            command = Path(f'/proc/{pid}/cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')
        except FileNotFoundError:
            continue
        if 'gnome-remote-desktop-daemon' not in command:
            owners.append(dict(pid=pid,command=command))
    return owners


def identity(pid):
    try:
        return Path(f'/proc/{pid}/stat').read_text().split(') ')[1].split()[19]
    except (FileNotFoundError,IndexError):
        return None


def stop_group(pid, fingerprint):
    if identity(pid) != fingerprint: return
    try:
        os.killpg(pid,signal.SIGTERM)
        for _ in range(20):
            if identity(pid) != fingerprint: return
            time.sleep(.5)
        os.killpg(pid,signal.SIGKILL)
    except ProcessLookupError:
        pass


class Supervisor:
    def __init__(self, root):
        self.root=root.resolve()
        self.config=read_json(root/'config.json')
        self.state=read_json(root/'training_status.json',{})
        self.state.update(supervisor_pid=os.getpid(),supervisor_identity=identity(os.getpid()),host=socket.gethostname())
        self.stopping=False
        self.child=None
        self.writer=None
        signal.signal(signal.SIGTERM,self.signal)
        signal.signal(signal.SIGINT,self.signal)
        self.last_report=0

    def signal(self,*_):
        self.stopping=True

    def save(self,**kwargs):
        self.state.update(kwargs,updated_at=time.strftime('%Y-%m-%dT%H:%M:%S%z'))
        atomic_json(self.root/'training_status.json',self.state)

    def event(self,message,**values):
        with (self.root/'events.jsonl').open('a') as f:
            f.write(json.dumps(dict(time=time.time(),message=message,**values),allow_nan=False)+'\n')
        print(message, json.dumps(values),flush=True)

    def scalars(self,values,step=None):
        if self.writer is None:
            from torch.utils.tensorboard import SummaryWriter
            self.writer=SummaryWriter(str(self.root/'dashboard/supervisor'))
        for key,value in values.items():
            if isinstance(value,(float,int)):
                self.writer.add_scalar(key,value,global_step=step if step is not None else self.state.get('completed_updates',0))
        self.writer.flush()

    def report(self):
        if time.time()-self.last_report < self.config['report_seconds']: return
        self.last_report=time.time()
        fields={k:self.state.get(k) for k in ('stage','status','num_envs','completed_updates','active_job','gpu',
            'gpu_seconds','best_stage1','best_stage2','blocker','latest_evaluation')}
        path=self.root/'status_reports'/f'{time.time_ns()}.json'
        atomic_json(path,fields)
        self.event('Quantitative status',**fields)

    def check_resources(self):
        if self.stopping: raise Stop('Stop requested; valid checkpoints retained')
        if shutil.disk_usage(self.root).free/2**30 < self.config['minimum_free_gib']:
            raise RuntimeError('Disk free space below configured floor')

    def remaining(self,stage):
        return self.config[f'{stage}_gpu_hours']*3600-self.state.get('gpu_seconds',{}).get(stage,0.)

    def reload_training_limits(self):
        # Apply edits at training-window boundaries without interrupting PPO.
        disk=read_json(self.root/'config.json')
        keys=('stage1_max_updates','stage2_max_updates','first_eval_updates','eval_every',
              'stagnation_windows','minimum_improvement')
        if not disk or any(not isinstance(disk.get(k),(int,float)) or disk[k]<=0 for k in keys):
            raise ValueError('Training limits must be finite positive numbers')
        import math
        if any(not math.isfinite(disk[k]) for k in keys):
            raise ValueError('Training limits must be finite')
        changes={k:disk[k] for k in keys if self.config.get(k)!=disk[k]}
        if changes:
            self.config.update(changes)
            self.event('Reloaded training limits at window boundary',**changes)
        self.save(training_limits={k:self.config[k] for k in keys})

    def job(self,name,argv,timeout,stage=None,worker=False,extra_env=None):
        self.check_resources()
        owners=gpu_owners()
        if owners:
            raise RuntimeError(f'GPU already owned; refusing second task: {owners}')
        if stage:
            timeout=min(timeout,self.remaining(stage))
            if timeout<=0: raise RuntimeError(f'{stage} GPU-hour budget exhausted')
        out=self.root/'jobs'/f'{name}_{time.time_ns()}'
        out.mkdir(parents=True)
        env=os.environ.copy()
        for key in ('PYTHONPATH','PYTHONHOME','VIRTUAL_ENV','LD_LIBRARY_PATH'):
            env.pop(key,None)
        env.update(PYTHONNOUSERSITE='1',OMNI_KIT_ACCEPT_EULA='1',WANDB_MODE='disabled',
            PATH=str(Path(sys.executable).parent)+':'+env.get('PATH',''),CARRY_WORKER_OUTPUT=str(out))
        env.update(extra_env or {})
        atomic_json(out/'command.json',dict(argv=argv,cwd=str(REPO),stage=stage,timeout=timeout))
        start=time.monotonic(); wall_start=time.time(); peak=0; samples=[]; last_poll=0
        log=(out/'console.log').open('w')
        process=subprocess.Popen(argv,cwd=REPO,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        self.child=process
        fp=identity(process.pid)
        self.save(active_job=dict(name=name,pid=process.pid,identity=fp,output=str(out),started_at=wall_start,stage=stage),status='RUNNING')
        error=None
        try:
            while process.poll() is None:
                self.check_resources()
                elapsed=time.monotonic()-start
                if elapsed>timeout: raise RuntimeError(f'Job timeout/budget reached: {name}')
                gpu=gpu_sample(); peak=max(peak,gpu['memory_mib']); samples.append(dict(seconds=elapsed,**gpu))
                if gpu['total_mib']-gpu['memory_mib']<self.config['headroom_mib']:
                    raise RuntimeError(f'GPU memory headroom below 4 GiB: {name}')
                if time.time()-last_poll>=self.config['poll_seconds']:
                    last_poll=time.time()
                    log.flush()
                    evidence=BAD.search((out/'console.log').read_text(errors='replace')[-200000:])
                    if evidence: raise RuntimeError(f'Unsafe log evidence: {evidence.group()}')
                    result=read_json(out/'worker_result.json',{})
                    latest=result.get('latest',{})
                    self.save(gpu=gpu,active_elapsed_s=elapsed,current_iteration=latest.get('iteration'),
                        latest_training_metrics=latest)
                    self.scalars({f'system/{k}':v for k,v in gpu.items()})
                    self.scalars({'system/active_elapsed_s':elapsed,'system/num_envs':self.state.get('num_envs',0)})
                    self.scalars({'system/stage_id':{'BENCHMARK':0,'STAGE1':1,'EVAL1':2,'STAGE2':3,'EVAL2':4,
                        'COMPLETED':5,'BLOCKED':6}.get(self.state.get('stage'),-1)})
                    self.writer.add_text('status/stage',self.state.get('stage','unknown'),
                        global_step=self.state.get('completed_updates',0))
                    if latest:
                        self.scalars({f'worker/{k}':v for k,v in latest.items() if isinstance(v,(float,int))},latest['iteration'])
                        self.scalars({f'worker/loss/{k}':v for k,v in latest.get('losses',{}).items()},latest['iteration'])
                        self.scalars({f'physical/{k}':v for k,v in latest.get('physical',{}).items()},latest['iteration'])
                    self.report()
                time.sleep(1.)
        except BaseException as exc:
            error=exc
            stop_group(process.pid,fp)
        finally:
            process.wait(); log.close(); self.child=None
            seconds=time.monotonic()-start
            if stage:
                usage=self.state.setdefault('gpu_seconds',{})
                usage[stage]=usage.get(stage,0.)+seconds
            result=read_json(out/'worker_result.json',{})
            evidence=BAD.findall((out/'console.log').read_text(errors='replace'))
            summary=dict(exit_code=process.returncode,wall_seconds=seconds,peak_gpu_memory_mib=peak,
                error=str(error) if error else None,failure_evidence=evidence,worker=result)
            atomic_json(out/'gpu_samples.json',samples)
            atomic_json(out/'result.json',summary)
            self.save(active_job=None,last_job=dict(output=str(out),**summary))
        if error: raise error
        if process.returncode or evidence or (worker and not result.get('passed')):
            raise RuntimeError(f'Failed GPU task {name}: see {out}')
        return out,summary

    def train_argv(self,name,n,updates,ratio,checkpoint=None,log_group=None):
        args=[sys.executable,str(REPO/'scripts/carry/train_worker.py'),'exp:g1-29dof-wbt-hybrid-carry','logger:disabled',
            f'--training.num-envs={n}','--training.headless=True',f'--training.name={name}',
            f'--logger.base-dir={self.root/"dashboard"/(log_group or name)}',
            f'--algo.config.num-learning-iterations={updates}',f'--algo.config.save-interval={self.config["checkpoint_every"]}',
            '--algo.config.latest-save-interval=0',f'--algo.config.num-mini-batches={n//64}',
            '--algo.config.num-learning-epochs=5',
            f'--command.setup-terms.motion-command.params.motion-config.hybrid.track-ratio={ratio}']
        if checkpoint: args.append(f'--training.checkpoint={checkpoint}')
        return args

    def benchmark_report(self,rows):
        columns=['num_envs','stable','steps_per_s','rollout_s','simulation_s','update_s','peak_gpu_memory_mib','samples_per_iteration',
            'minibatches','minibatch_samples','epochs','resume_verified','physx_errors','nan_errors','crash_exit_code','evidence']
        with (self.root/'benchmark_results.csv').open('w') as f:
            writer=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore'); writer.writeheader(); writer.writerows(rows)
        lines=['# Environment benchmark','Real physics + PPO; solver/contact configuration unchanged.',
            '24 steps/environment, 1536 samples/minibatch, five epochs. Samples/update scale with environment count; this is a throughput comparison, not evidence of equivalent learning curves.',
            '| Envs | Stable | Steps/s | GPU MiB | PPO s | Sim s | Evidence |','|---:|---|---:|---:|---:|---:|---|']
        for r in rows:
            lines.append(f'| {r["num_envs"]} | {r["stable"]} | {r.get("steps_per_s",0):.0f} | {r.get("peak_gpu_memory_mib",0)} | {r.get("update_s",0):.3f} | {r.get("simulation_s",0):.3f} | {r.get("evidence","")} |')
        if self.state.get('num_envs'):
            reason='fixed by explicit user instruction after validation' if self.config.get('fixed_num_envs') else 'maximum stable measured throughput'
            lines.append(f'\nSelected environments: {self.state["num_envs"]}; {reason}.')
        (self.root/'benchmark_report.md').write_text('\n\n'.join(lines[:3])+'\n\n'+'\n'.join(lines[3:]))
        if rows:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            fig,axes=plt.subplots(1,2,figsize=(10,4))
            valid=[r for r in rows if r['stable']]
            axes[0].plot([r['num_envs'] for r in valid],[r['steps_per_s'] for r in valid],'o-')
            axes[0].set(xlabel='Environments',ylabel='PPO transitions/s')
            axes[1].plot([r['num_envs'] for r in rows],[r.get('peak_gpu_memory_mib',0) for r in rows],'o-')
            axes[1].set(xlabel='Environments',ylabel='Whole GPU memory MiB')
            fig.tight_layout(); fig.savefig(self.root/'benchmark.png'); plt.close(fig)

    def benchmark(self):
        rows=self.state.setdefault('benchmark',[])
        if rows and not rows[-1]['stable']:
            self.select_benchmark(rows); return
        for n in self.config['candidates']:
            if any(r['num_envs']==n for r in rows): continue
            self.save(stage='BENCHMARK',num_envs=n)
            row=dict(num_envs=n,stable=False,samples_per_iteration=n*24,minibatches=n//64,minibatch_samples=1536,epochs=5)
            try:
                smoke,smoke_summary=self.job(f'benchmark_{n}_smoke',self.train_argv(f'bench{n}_smoke',n,1,1.,log_group='benchmark'),
                    self.config['benchmark_timeout_s'],worker=True)
                ckpt,_=newest_valid(read_json(smoke/'worker_result.json')['log_dir'],require_export=True)
                # A different environment count must exactly restore model,
                # optimizer, normalization and curriculum before its PPO step.
                previous=self.state.get('benchmark_checkpoint')
                peaks=[smoke_summary['peak_gpu_memory_mib']]
                if previous:
                    resume,resume_summary=self.job(f'resume_changed_envs_{n}',self.train_argv(f'resume{n}',n,1,1.,previous,'benchmark'),
                        self.config['benchmark_timeout_s'],worker=True)
                    if not read_json(resume/'worker_result.json')['resume_verified']:
                        raise RuntimeError('Changed-num_envs resume was not verified')
                    row['resume_verified']=True
                    peaks.append(resume_summary['peak_gpu_memory_mib'])
                measured,summary=self.job(f'benchmark_{n}_throughput',self.train_argv(f'bench{n}',n,
                    self.config['warmup_updates']+self.config['benchmark_updates'],1.,log_group='benchmark'),
                    self.config['benchmark_timeout_s'],worker=True)
                iterations=[json.loads(x) for x in (measured/'iterations.jsonl').read_text().splitlines()]
                iterations=iterations[self.config['warmup_updates']:]
                if len(iterations)<self.config['benchmark_updates']: raise RuntimeError('Missing measured PPO updates')
                for key in ('steps_per_s','rollout_s','simulation_s','update_s'):
                    row[key]=statistics.median(x[key] for x in iterations)
                peaks.append(summary['peak_gpu_memory_mib'])
                row.update(stable=True,peak_gpu_memory_mib=max(peaks),evidence=str(measured),
                    physx_errors=0,nan_errors=0,crash_exit_code=0)
                self.save(benchmark_checkpoint=ckpt['path'])
                self.scalars({f'benchmark/{k}':v for k,v in row.items() if isinstance(v,(float,int))},n)
            except Stop:
                raise
            except Exception as exc:
                row['evidence']=str(exc)
                row['peak_gpu_memory_mib']=self.state.get('last_job',{}).get('peak_gpu_memory_mib',0)
                last=self.state.get('last_job',{})
                row.update(physx_errors=sum('physx' in x.lower() for x in last.get('failure_evidence',[])),
                    nan_errors=sum('nan' in x.lower() or 'nonfinite' in x.lower() for x in last.get('failure_evidence',[])),
                    crash_exit_code=last.get('exit_code'))
                self.event('Scaling stopped',num_envs=n,error=str(exc))
            rows.append(row); self.save(benchmark=rows); self.benchmark_report(rows)
            with (self.root/'autoresearch.jsonl').open('a') as f:
                f.write(json.dumps(dict(type='benchmark',decision='retain measured stable candidate' if row['stable'] else 'reject; stop scaling',**row))+'\n')
            if not row['stable']: break
        self.select_benchmark(rows)

    def select_benchmark(self,rows):
        valid=[r for r in rows if r['stable']]
        if not valid: raise RuntimeError('No stable environment benchmark candidate')
        fixed=self.config.get('fixed_num_envs')
        if fixed is not None:
            choices=[r for r in valid if r['num_envs']==fixed]
            if not choices:
                raise RuntimeError(f'User-requested {fixed} environments did not pass validation; refusing to force unsafe training')
            best=choices[0]
        else:
            best=max(valid,key=lambda r:r['steps_per_s'])
        self.save(num_envs=best['num_envs'],stage='STAGE1',completed_updates=0)
        self.benchmark_report(rows)

    def evaluate(self,checkpoint,stage,final=False):
        self.save(stage='EVAL1' if stage=='stage1' else 'EVAL2')
        seeds=self.config['final_seeds'] if final else self.config['evaluation_seeds']
        dest=self.root/('final_goal_suite' if stage=='stage2' and final else 'evaluations')/f'{stage}_{time.time_ns()}'
        argv=[sys.executable,str(REPO/'scripts/carry/evaluate.py'),'--suite','stage1' if stage=='stage1' else 'goal',
            '--policy',str(Path(checkpoint['path']).with_suffix('.onnx')),'--output',str(dest),
            '--seeds',str(seeds),'--level',str(checkpoint['curriculum_level']),'--seconds','20',
            '--gates',str(self.root/'gates.json')]
        if stage=='stage2': argv.append('--forbid-motion-loading')
        self.job(f'{stage}_evaluation',argv,self.config['evaluation_timeout_s'],stage=stage)
        result=read_json(dest/'summary.json')
        if not result or result.get('first_episode_only') is not True: raise RuntimeError('Missing valid physical evaluation result')
        result.update(directory=str(dest),checkpoint=checkpoint['path'],final=final)
        self.save(latest_evaluation=result)
        shutil.copyfile(dest/'report.md',self.root/f'{stage}_evaluation.md')
        self.scalars({f'evaluation/{stage}/score':result['score'],f'evaluation/{stage}/gate':result['passed'],
            f'evaluation/{stage}/selection_score':result['selection_score']},checkpoint['completed_updates'])
        for name,metrics in result['scenarios'].items():
            self.scalars({f'evaluation/{stage}/{name}/{k}':v for k,v in metrics.items()
                if isinstance(v,(int,float))},checkpoint['completed_updates'])
        self.event('Physical evaluation',stage=stage,passed=result['passed'],score=result['score'],directory=str(dest))
        return result

    def retain(self,checkpoint,stage,result,force=False):
        old=self.state.get(f'best_{stage}')
        if not force and old and old['selection_score']>=result['selection_score']: return
        dest=self.root/f'best_{stage}'/f'iteration_{checkpoint["iteration"]}_{time.time_ns()}'
        dest.mkdir(parents=True)
        src=Path(checkpoint['path'])
        for suffix in ('.pt','.ready.json','.onnx','.actor.json','.export.json'):
            if not src.with_suffix(suffix).exists(): continue
            shutil.copy2(src.with_suffix(suffix),dest/f'model{suffix}')
        info=validate(dest/'model.pt'); info.update(selection_score=result['selection_score'],passed=result['passed'],
            evaluation=result['directory'])
        atomic_json(dest/'selection.json',info)
        atomic_json(self.root/f'best_{stage}'/'selection.json',info)
        self.save(**{f'best_{stage}':info})

    def accept_final(self,checkpoint,stage,result):
        if not result['passed']:
            return False
        self.retain(checkpoint,stage,result,force=True)
        valid=self.state[f'best_{stage}']
        self.save(**{f'valid_{stage}':valid})
        if stage=='stage1':
            self.save(stage='STAGE2',best_stage1=valid,completed_updates=checkpoint['completed_updates'])
        else:
            self.save(stage='COMPLETED',status='COMPLETED',blocker=None,final_checkpoint=valid)
        return True

    def assess_before_stop(self,stage,reason):
        """Assess the best physical checkpoint, even when stopping unsuccessfully."""
        best=self.state.get(f'best_{stage}')
        if not best or self.remaining(stage)<=0:
            self.event('Final assessment unavailable',stage=stage,reason=reason,
                best_checkpoint=bool(best),remaining_seconds=self.remaining(stage))
            return False
        result=self.evaluate(best,stage,final=True)
        self.save(**{f'{stage}_final_assessment':dict(result,stop_reason=reason)})
        atomic_json(self.root/f'{stage}_final_assessment.json',dict(result,stop_reason=reason))
        shutil.copyfile(Path(result['directory'])/'report.md',self.root/f'{stage}_final_assessment.md')
        self.event('Final assessment before stopping',stage=stage,reason=reason,passed=result['passed'],
            checkpoint=best['path'],directory=result['directory'])
        return self.accept_final(best,stage,result)

    def diagnose(self,stage,history):
        import numpy as np
        latest=history[-1]
        measurements={}
        trace=Path(latest['directory'])/'steps.jsonl'
        for line in trace.read_text().splitlines():
            step=json.loads(line)
            alive=np.asarray(step['alive'],dtype=bool)
            for key in ('hand_forces','upward_weight_ratio','root_height','robot_tilt','box_height','tilt',
                        'separation','contact','robot_error','object_error'):
                if key in step:
                    measurements.setdefault(key,[]).extend(np.asarray(step[key])[alive].reshape(-1).tolist())
        diagnostic={k:dict(mean=float(np.mean(v)),p10=float(np.quantile(v,.1)),p90=float(np.quantile(v,.9)),
            minimum=float(np.min(v)),maximum=float(np.max(v))) for k,v in measurements.items() if v}
        last_worker=self.state.get('last_training_metrics',self.state.get('latest_training_metrics',{}))
        hypothesis=[]
        if diagnostic.get('upward_weight_ratio',{}).get('p10',1)<.5:
            hypothesis.append('Measured upward hand support frequently falls below half the box weight; contact geometry/reference compatibility is a likely bottleneck.')
        if diagnostic.get('robot_tilt',{}).get('p90',0)>.35:
            hypothesis.append('Measured robot tilt exceeds 0.35 rad at the 90th percentile; balance is a likely bottleneck.')
        if diagnostic.get('object_error',{}).get('p90',0)>.15:
            hypothesis.append('Object reference position error exceeds the 0.15 m gate at the 90th percentile.')
        if latest['failure_counts'].get('track_failure',0):
            hypothesis.append('Reference tracking termination is present; reference orientation/body compatibility must be resolved before extending reference duration.')
        atomic_json(self.root/'diagnosis_metrics.json',dict(physical_distributions=diagnostic,
            latest_training=last_worker,failure_counts=latest['failure_counts'],hypotheses=hypothesis))
        lines=[f'# {stage} stagnation diagnosis','No threshold or physics change has been applied.',
            'Three consecutive evaluation windows failed to improve the measured physical selection score.',
            f'Failure counts: {latest["failure_counts"]}',
            'Evidence-based hypotheses: '+json.dumps(hypothesis),
            'Measured contact/balance/tracking distributions: '+json.dumps(diagnostic,indent=2),
            'Latest reward/PPO diagnostics: '+json.dumps(last_worker,indent=2),
            'Reference compatibility: two 2.2 s moving clips retain fast root/leg trajectories (up to approximately 0.78 m/s and 1.94 rad/s) with retargeted arms; dynamic feasibility is not certified.',
            'Reset limitation: prior fixed-PD evidence certified only the first 0.2 s and observed roughly 0.10 m drops by 0.5 s.',
            'Inspect per-step bilateral forces, upward/weight ratio, box tilt/height, robot/object tracking, and reward components in steps.jsonl alongside training iterations.jsonl.',
            'Corrective experiments performed: none. No automatic physics/reward/reference changes are authorized by this controller; it stops for review rather than spends the remaining budget.',
            'Quantitative windows:',json.dumps([{k:x.get(k) for k in ('score','selection_score','failure_counts','directory','scenarios')} for x in history[-4:]],indent=2)]
        (self.root/'root_cause_diagnosis.md').write_text('\n\n'.join(lines))

    def training_stage(self,stage):
        ratio=1. if stage=='stage1' else .5
        group=self.root/'dashboard'/stage
        history=self.state.setdefault(f'{stage}_evaluations',[])
        if self.state['stage'] in ('EVAL1','EVAL2') and self.state.get('pending_checkpoint'):
            checkpoint=self.state['pending_checkpoint']
        else:
            checkpoint=None
        while True:
            self.check_resources()
            self.reload_training_limits()
            if self.remaining(stage)<=0: raise RuntimeError(f'{stage} GPU-hour budget exhausted')
            if checkpoint is None:
                try:
                    current,_=newest_valid(group,require_export=False)
                except ValueError:
                    current=self.state.get('best_stage1') if stage=='stage2' else None
                base_updates=self.state.get('stage2_initial_updates',current['completed_updates'] if current and stage=='stage2' else 0)
                if stage=='stage2' and 'stage2_initial_updates' not in self.state:
                    self.save(stage2_initial_updates=base_updates)
                completed=current['completed_updates'] if current else 0
                local_updates=completed-base_updates
                if local_updates>=self.config[f'{stage}_max_updates']:
                    if self.assess_before_stop(stage,'iteration_cap'):
                        return
                    raise RuntimeError(f'{stage} finite iteration cap exhausted')
                target=self.config['first_eval_updates'] if not history else history[-1]['completed_updates']-base_updates+self.config['eval_every']
                updates=min(max(1,target-local_updates),self.config[f'{stage}_max_updates']-local_updates)
                self.save(stage='STAGE1' if stage=='stage1' else 'STAGE2',completed_updates=completed,pending_checkpoint=None)
                out,_=self.job(f'{stage}_training',self.train_argv(stage,self.state['num_envs'],updates,ratio,
                    current['path'] if current else None,stage),self.remaining(stage),stage=stage,worker=True)
                self.save(last_training_metrics=read_json(out/'worker_result.json').get('latest',{}))
                checkpoint,rejected=newest_valid(read_json(out/'worker_result.json')['log_dir'],require_export=True)
                self.save(completed_updates=checkpoint['completed_updates'],pending_checkpoint=checkpoint,rejected_checkpoints=rejected)
            result=self.evaluate(checkpoint,stage)
            result['completed_updates']=checkpoint['completed_updates']
            self.retain(checkpoint,stage,result)
            history.append(result)
            self.save(**{f'{stage}_evaluations':history},pending_checkpoint=None)
            if result['passed']:
                final=self.evaluate(checkpoint,stage,final=True)
                if self.accept_final(checkpoint,stage,final):
                    return
            # Track improvements against an explicit running high-water mark.
            previous=self.state.get(f'{stage}_high_score',-1.)
            stagnant=0 if result['selection_score']>previous+self.config['minimum_improvement'] else self.state.get(f'{stage}_stagnant',0)+1
            self.save(**{f'{stage}_high_score':max(previous,result['selection_score']),f'{stage}_stagnant':stagnant})
            if stagnant>=self.config['stagnation_windows']:
                self.diagnose(stage,history)
                if self.assess_before_stop(stage,'three_stagnant_physical_evaluation_windows'):
                    return
                raise RuntimeError(f'{stage} physical progress stagnated for three windows; root_cause_diagnosis.md')
            checkpoint=None

    def run(self):
        self.root.mkdir(parents=True,exist_ok=True)
        lock=(BASE/'supervisor.lock').open('a+')
        gpu_lock=open('/tmp/g1-carry-gpu0.lock','a+')
        try:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            fcntl.flock(gpu_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit('Another carry supervisor owns the process/GPU lock')
        self.save(status='STARTING',supervisor_exited=False)
        active=self.state.get('active_job')
        if active and identity(active['pid'])==active['identity']:
            self.event('Reaping interrupted owned job',pid=active['pid'])
            stop_group(active['pid'],active['identity'])
        if active and active.get('stage'):
            usage=self.state.setdefault('gpu_seconds',{})
            # Conservatively charge elapsed time including downtime after abrupt interruption.
            usage[active['stage']]=usage.get(active['stage'],0.)+max(0,time.time()-active['started_at'])
        self.save(active_job=None,status='RUNNING',blocker=None)
        try:
            if self.state.get('stage')=='COMPLETED': return
            if self.state.get('stage')=='BLOCKED':
                self.save(stage=self.state.get('resume_stage','BENCHMARK'))
            if self.state.get('stage','BENCHMARK')=='BENCHMARK': self.benchmark()
            if self.state['stage'] in ('STAGE1','EVAL1'): self.training_stage('stage1')
            if self.state['stage'] in ('STAGE2','EVAL2'):
                if not self.state.get('valid_stage1',{}).get('passed'):
                    raise RuntimeError('Stage2 forbidden: Stage1 final physical gate missing')
                self.training_stage('stage2')
        except Stop as exc:
            self.save(status='STOPPED',blocker=str(exc))
            self.event('Supervisor stopped safely',reason=str(exc))
        except Exception as exc:
            self.save(resume_stage=self.state.get('stage'),stage='BLOCKED',status='BLOCKED',blocker=str(exc))
            self.event('Supervisor blocked',reason=str(exc))
        finally:
            if self.writer: self.writer.close()
            self.save(supervisor_exited=True)


def initialize(config_file=None):
    BASE.mkdir(parents=True,exist_ok=True)
    current=BASE/'current'
    if current.exists():
        state=read_json(current/'training_status.json',{})
        if state.get('status') not in ('BLOCKED','COMPLETED','STOPPED'):
            raise SystemExit('Existing run is active. Use status, stop, or resume.')
    root=BASE/f'run_{time.strftime("%Y%m%d_%H%M%S")}_{time.time_ns()%1000000:06d}'
    root.mkdir()
    config=DEFAULT.copy()
    if config_file: config.update(read_json(config_file))
    if config['evaluation_seeds']<10 or config['final_seeds']<30: raise ValueError('Minimum evaluation seeds: 10 periodic / 30 final')
    atomic_json(root/'config.json',config)
    from suite_eval import DEFAULT_GATES
    atomic_json(root/'gates.json',DEFAULT_GATES)
    atomic_json(root/'training_status.json',dict(stage='BENCHMARK',status='CREATED',gpu_seconds={},created_at=time.time(),
        log_directory=str(root/'dashboard'),root=str(root),engineering_validated=True,
        validation=read_json(BASE/'validation_success.json',{})))
    shutil.copyfile(REPO/'AUTO_TRAIN_README.md',root/'AUTO_TRAIN_README.md')
    shutil.copyfile(REPO/'AUTO_TRAIN_README.md',BASE/'AUTO_TRAIN_README.md')
    (root/'autoresearch.md').write_text('Bounded carry experiment loop. Baseline 10-seed evaluation: no full clip completed; approximate moving survival 0.55-0.57 s and static survival 1.05 s. Reference-free hold survived about 1.42 s.\n'
        'Hypothesis: physically gated PPO can improve these baselines. No dynamic feasibility is assumed.\n'
        'Keep/reject decisions, measured evidence and all failed candidates are recorded in autoresearch.jsonl and benchmark_report.md.\n')
    (root/'autoresearch.sh').write_text('#!/usr/bin/env bash\nset -euo pipefail\ncd '+str(REPO)+'\nbash scripts/carry/carryctl.sh resume\n')
    for folder in ('best_stage1','best_stage2','final_goal_suite','status_reports'):
        (root/folder).mkdir()
    for name in ('benchmark_report.md','stage1_evaluation.md','stage2_evaluation.md'):
        (root/name).write_text('Pending measured results. No learned capability is claimed.\n')
    (root/'training_audit.md').write_text('Engineering preflight evidence: ../validation_20261119/.\n'
        'Actor contract unchanged: 348 physical history values; only external command [vx, vy, yaw_rate, pelvis_height].\n'
        'Physics and contact solver unchanged. From-scratch Stage1; Stage2 requires 30-seed Stage1 gate.\n'
        'Budget accounting conservatively uses GPU task wall time including startup/evaluation.\n'
        'No policy quality has been established.\n')
    tmp=BASE/f'.current_{os.getpid()}'
    tmp.symlink_to(root.name); os.replace(tmp,current)
    for name in ('training_status.json','benchmark_report.md','stage1_evaluation.md','stage2_evaluation.md',
                 'training_audit.md','best_stage1','best_stage2','final_goal_suite'):
        target=BASE/name
        if not target.exists() and not target.is_symlink(): target.symlink_to('current/'+name)
    return root


def main():
    p=argparse.ArgumentParser()
    p.add_argument('action',choices=['init','run'])
    p.add_argument('--root',type=Path)
    p.add_argument('--config',type=Path)
    args=p.parse_args()
    if args.action=='init': print(initialize(args.config)); return
    root=(args.root or BASE/'current').resolve()
    if not (root/'config.json').is_file(): p.error('Initialize a versioned experiment first')
    Supervisor(root).run()


if __name__=='__main__': main()
