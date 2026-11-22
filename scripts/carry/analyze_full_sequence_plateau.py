"""Read-only historical/current training comparison. No GPU simulation or policy mutations."""
from pathlib import Path
from collections import defaultdict
import json,sys,subprocess,time,yaml
import numpy as np
from tensorboard.backend.event_processing.event_file_loader import RawEventFileLoader
from tensorboard.compat.proto.event_pb2 import Event
REPO=Path(__file__).resolve().parents[2];BASE=REPO.parent/'artifacts';OUT=BASE/'unified_hoi_hmi_stage1/diagnosis_full_sequence_20261122'
OUT.mkdir(parents=True,exist_ok=True)
families=['full_sequence','loaded_locomotion','loaded_squat_stand']
series_tags={'Train/mean_reward','Train/mean_episode_length','Loss/KL','Loss/Value'}
for family in families:
 prefix='Env/stage1/family/'+family
 series_tags|={prefix+'/completed_episodes',prefix+'/completed/episode_length_s'}
 series_tags|={prefix+'/completed/termination/'+term for term in ['physical_failure','track_failure','clip_timeout','body_proximity']}

def read_events(folder):
 series=defaultdict(dict);last={};records=0
 for file in sorted(folder.glob('events.out.tfevents.*')):
  for raw in RawEventFileLoader(str(file)).Load():
   e=Event.FromString(raw)
   for v in e.summary.value:
    if not v.HasField('simple_value'):continue
    value=float(v.simple_value);last[v.tag]={'step':int(e.step),'value':value}
    if v.tag in series_tags:series[v.tag][int(e.step)]=value
   records+=1
 return series,last,records

def snap(series,step):
 out={}
 for family in families:
  p='Env/stage1/family/'+family
  n=series[p+'/completed_episodes'].get(step)
  if n is None:continue
  out[family]={'episodes_cumulative_tboard_mean':n,'episode_length_s_cumulative':series[p+'/completed/episode_length_s'].get(step)}
  out[family].update({c:series[p+'/completed/termination/'+c].get(step) for c in ['physical_failure','track_failure','clip_timeout','body_proximity']})
 return out

def window(series,start,end):
 out={}
 for family in families:
  p='Env/stage1/family/'+family
  n0=series[p+'/completed_episodes'].get(start);n1=series[p+'/completed_episodes'].get(end)
  if n0 is None or n1 is None or n1<=n0:continue
  out[family]={'approx_episodes':n1-n0}
  for c in ['physical_failure','track_failure','clip_timeout','body_proximity']:
   a=series[p+'/completed/termination/'+c].get(start);b=series[p+'/completed/termination/'+c].get(end)
   if a is not None and b is not None:out[family][c]=(b*n1-a*n0)/(n1-n0)
 return out

paths={
 'pre_reboot':BASE/'unified_hoi_hmi_stage1/formal_8192_15000_002_save2000/training/logs/WholeBodyTracking/20261121_110128-unified_hoi_stage1-locomotion',
 'resumed':BASE/'unified_hoi_hmi_stage1/formal_8192_15000_003_resume02000_20261122/training/logs/WholeBodyTracking/20261122_055618-unified_hoi_stage1-locomotion'}
result={}
for label,folder in paths.items():
 series,last,records=read_events(folder);steps=sorted(series['Env/stage1/family/full_sequence/completed_episodes']);end=steps[-1]
 anchors=([0,100,500,1000,1500,2000,2500,3000,3500] if label=='pre_reboot' else [2001,2050,2100,2200,2300,2400,2500,2600])+[end]
 anchors=sorted(set(x for x in anchors if x in steps));windows={}
 for a,b in zip(anchors[:-1],anchors[1:]):
  if b-a>=40:windows[f'{a+1}..{b}']=window(series,a,b)
 keep_last={k:v for k,v in last.items() if k.startswith(('Env/hoi/phase/','Env/hoi/family/','Env/hoi/mode_fraction/','Env/hoi/family_fraction/','Env/stage1/','Loss/','Train/','Policy/'))}
 result[label]=dict(folder=str(folder),records=records,last_step=end,anchors={str(x):snap(series,x) for x in anchors},
  approx_windows=windows,window_caveat='Approximate: TensorBoard logs mean cumulative counters/ratios over24 steps; endpoint product ignores within-update covariance. Causes can overlap.',latest_metrics=keep_last)
 print(label,'last',end,'snapshots',json.dumps({x:result[label]['anchors'][str(x)] for x in anchors[-3:]},ensure_ascii=False),flush=True)
 print(label,'last_window',list(windows.items())[-1:] if windows else [],flush=True)
 for family in families:
  series_map={tag:list(sorted(values.items())) for tag,values in series.items() if '/'+family+'/' in tag}
  (OUT/(label+'_'+family+'_series.json')).write_text(json.dumps(series_map)+'\n')
 (OUT/'current_training_analysis.json').write_text(json.dumps(result,indent=2)+'\n')

old=BASE/'fullbody_goal_carry/run_20261120_133333';state=json.loads((old/'training_status.json').read_text())
history=[]
for p in sorted(old.glob('jobs/stage1_training_*/worker_result.json')):
 d=json.loads(p.read_text());m=d.get('latest',{});q=m.get('physical',{})
 history.append(dict(path=str(p),iteration=m.get('iteration'),updates=d.get('updates'),metrics={k:v for k,v in q.items() if k.startswith(('carry/','termination/','reward/episode/termination/')) or k=='average_episode_length'}))
evals=[]
for e in state.get('stage1_evaluations',[]):
 rows=e.get('trials',[]);evals.append(dict(completed_updates=e.get('completed_updates'),checkpoint=e.get('checkpoint'),groups=e.get('groups'),
  survival_s_mean=np.mean([x['survival_s'] for x in rows]) if rows else None,
  contact_mean=np.mean([x['contact_continuity'] for x in rows]) if rows else None,failures={f:sum(f in x.get('failures',[]) for x in rows) for f in set(sum([x.get('failures',[]) for x in rows],[]))}))
old_summary=dict(root=str(old),stage=state['stage'],blocker=state['blocker'],completed_updates=state['completed_updates'],last_iteration=state['current_iteration'],evaluations=evals,training_segments=history)
(OUT/'historical_fullbody_20261120.json').write_text(json.dumps(old_summary,indent=2)+'\n')
print('Historical fullbody:',state['completed_updates'],state['current_iteration'],len(evals),'evaluations allfail',all(all(v['success_rate']==0 for v in e['groups'].values()) for e in evals),flush=True)
