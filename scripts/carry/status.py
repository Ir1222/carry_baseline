"""Read durable supervisor metadata without importing Torch or Isaac."""
import argparse
import json
from pathlib import Path
import time

BASE=Path(__file__).resolve().parents[3]/'artifacts/auto_training'


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path,default=BASE/'current')
    p.add_argument('--watch',action='store_true')
    p.add_argument('--json',action='store_true')
    args=p.parse_args()
    while True:
        try:
            state=json.loads((args.root/'training_status.json').read_text())
            if args.json:
                print(json.dumps(state,indent=2))
            else:
                pid=state.get('supervisor_pid')
                live=bool(pid and Path(f'/proc/{pid}').exists() and not state.get('supervisor_exited'))
                print(f"{state.get('stage')} / {state.get('status')} | supervisor {pid} ({'alive' if live else 'stopped'}) | envs {state.get('num_envs','pending')} | updates {state.get('completed_updates',0)} | current iteration {state.get('current_iteration')}")
                print('Updated:',state.get('updated_at'),'GPU:',state.get('gpu'))
                print('GPU-hours:',{k:round(v/3600,3) for k,v in state.get('gpu_seconds',{}).items()})
                job=state.get('active_job')
                if job: print('Active:',job['name'],'PID:',job['pid'],'log:',job['output']+'/console.log')
                for stage in ('stage1','stage2'):
                    best=state.get(f'best_{stage}',{})
                    print(f'Best {stage}:',best.get('path','none'), 'physical gate:',best.get('passed',False))
                print('Run:',args.root.resolve())
                print('TensorBoard:',json.loads((BASE/'dashboard.json').read_text()).get('url') if (BASE/'dashboard.json').is_file() else 'not started')
                if state.get('blocker'): print('Blocker:',state['blocker'])
        except (FileNotFoundError,json.JSONDecodeError) as exc:
            print('No readable experiment state:',exc)
        if not args.watch: break
        time.sleep(60)


if __name__=='__main__': main()
