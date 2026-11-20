"""Read durable controller status without initializing Isaac or owning the GPU."""
import argparse
import json
from pathlib import Path
import time


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[3]/'artifacts/fullbody_goal_carry/current')
    p.add_argument('--watch',action='store_true');p.add_argument('--interval',type=float,default=30.)
    a=p.parse_args()
    while True:
        d=json.loads((a.root/'training_status.json').read_text());m=d.get('latest_training_metrics',{})
        summary=dict(stage=d.get('stage'),status=d.get('status'),iteration=d.get('current_iteration'),
            stage_progress=d.get('completed_updates'),num_envs=d.get('num_envs'),gpu=d.get('gpu'),
            live_episode_s=m.get('mean_live_episode_s'),steps_per_s=m.get('steps_per_s'),
            curriculum=m.get('curriculum_level'),physical=m.get('physical'),
            best_stage1=d.get('best_stage1'),best_stage2=d.get('best_stage2'),blocker=d.get('blocker'))
        print(json.dumps(summary,indent=2),flush=True)
        if not a.watch or d.get('supervisor_exited'):return
        time.sleep(max(1,a.interval))


if __name__=='__main__':main()
