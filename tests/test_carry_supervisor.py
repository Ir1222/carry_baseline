"""Safety invariants for the autonomous controller (no Isaac/GPU required)."""
import importlib.util
import json
from pathlib import Path
import sys

import pytest
import torch

SCRIPTS=Path(__file__).resolve().parents[1]/'scripts/carry'
sys.path.insert(0,str(SCRIPTS))
import auto_train
from suite_eval import DEFAULT_GATES, SCENARIOS, summarize
from holosoma.carry.checkpoints import atomic_json, atomic_save, newest_valid, validate


def checkpoint():
    opt={'state':{0:{'step':torch.tensor(1.),'exp_avg':torch.zeros(1),'exp_avg_sq':torch.ones(1)}},
         'param_groups':[{'params':[0],'lr':1e-4}]}
    return dict(actor_model_state_dict={'input.weight':torch.zeros(4,348),'output.weight':torch.zeros(29,4)},
        critic_model_state_dict={'weight':torch.ones(1)},actor_optimizer_state_dict=opt,
        critic_optimizer_state_dict=opt,actor_obs_normalizer_state_dict={'mean':torch.zeros(348)},
        critic_obs_normalizer_state_dict={'mean':torch.zeros(184)},iter=3,
        env_state={'carry_schema_version':1,'carry_level':0})


def test_partial_corrupt_and_nonfinite_checkpoints_are_never_selected(tmp_path):
    good=tmp_path/'model_00003.pt'; atomic_save(checkpoint(),good)
    (tmp_path/'model_99999.pt').write_bytes(b'incomplete zip')
    selected,rejected=newest_valid(tmp_path)
    assert selected['path']==str(good) and rejected
    bad=checkpoint(); bad['actor_model_state_dict']['input.weight'][0,0]=float('nan')
    with pytest.raises(ValueError): atomic_save(bad,tmp_path/'model_00004.pt')
    assert not (tmp_path/'model_00004.pt').exists()
    with good.open('ab') as f: f.write(b'corrupted')
    with pytest.raises(ValueError,match='checksum'): validate(good)


def test_full_optimizer_and_normalization_required(tmp_path):
    state=checkpoint(); state['actor_optimizer_state_dict']['state']={}
    with pytest.raises(ValueError,match='optimizer'): atomic_save(state,tmp_path/'model_00003.pt')
    state=checkpoint(); state['actor_obs_normalizer_state_dict']=None
    with pytest.raises(ValueError,match='normalization'): atomic_save(state,tmp_path/'model_00003.pt')


def test_existing_gpu_owner_prevents_spawn(tmp_path,monkeypatch):
    atomic_json(tmp_path/'config.json',auto_train.DEFAULT)
    atomic_json(tmp_path/'training_status.json',{})
    supervisor=auto_train.Supervisor(tmp_path)
    monkeypatch.setattr(auto_train,'gpu_owners',lambda:[{'pid':123,'command':'other training'}])
    monkeypatch.setattr(auto_train.subprocess,'Popen',lambda *a,**k:pytest.fail('Must not spawn a second GPU job'))
    with pytest.raises(RuntimeError,match='GPU already owned'):
        supervisor.job('forbidden',['not-executed'],10)


def test_exhausted_budget_prevents_spawn(tmp_path,monkeypatch):
    atomic_json(tmp_path/'config.json',dict(auto_train.DEFAULT,stage1_gpu_hours=0))
    atomic_json(tmp_path/'training_status.json',{})
    supervisor=auto_train.Supervisor(tmp_path)
    monkeypatch.setattr(auto_train,'gpu_owners',lambda:[])
    monkeypatch.setattr(auto_train.subprocess,'Popen',lambda *a,**k:pytest.fail('Budget must prevent spawn'))
    with pytest.raises(RuntimeError,match='budget exhausted'):
        supervisor.job('forbidden',['not-executed'],10,stage='stage1')


def test_goal_suite_needs_all_commands_20_seconds_and_10_seeds():
    def row(name):
        return dict(scenario=name,success=True,survival_s=20.,mean_abs_command_errors=[0]*4,
            support_ratio=1.,mean_contact_quality=1.,robot_error_m=0.,object_error_m=0.,
            max_tilt_rad=0.,min_box_height_m=.8,max_separation_m=.5,failures=[])
    rows=[row(n) for n in SCENARIOS for _ in range(10)]
    assert summarize(rows,'goal',DEFAULT_GATES,20,4)['passed']
    assert not summarize(rows,'goal',DEFAULT_GATES,19,4)['passed']
    assert not summarize(rows,'goal',DEFAULT_GATES,20,3)['passed']
    assert not summarize(rows[:10],'goal',DEFAULT_GATES,20,4)['passed']
    assert not summarize([row('clip_0')]*9,'stage1',DEFAULT_GATES,20,0)['passed']


def test_metric_name_nonfinite_is_not_failure_but_actual_traceback_is():
    assert not auto_train.BAD.search('Mean episode termination/physical_failure/nonfinite: 0.0000')
    assert auto_train.BAD.search('Traceback (most recent call last):')
    assert auto_train.BAD.search('PhysX error: contact buffer overflow')


def test_user_fixed_4096_requires_stable_validation(tmp_path,monkeypatch):
    atomic_json(tmp_path/'config.json',dict(auto_train.DEFAULT,fixed_num_envs=4096))
    atomic_json(tmp_path/'training_status.json',{})
    supervisor=auto_train.Supervisor(tmp_path)
    monkeypatch.setattr(supervisor,'benchmark_report',lambda rows:None)
    rows=[dict(num_envs=2048,stable=True,steps_per_s=99999.)]
    with pytest.raises(RuntimeError,match='did not pass validation'):
        supervisor.select_benchmark(rows)
    rows.append(dict(num_envs=4096,stable=True,steps_per_s=1.))
    supervisor.select_benchmark(rows)
    assert supervisor.state['num_envs']==4096 and supervisor.state['stage']=='STAGE1'


def test_failed_final_assessment_cannot_advance_stage(tmp_path,monkeypatch):
    atomic_json(tmp_path/'config.json',auto_train.DEFAULT)
    atomic_json(tmp_path/'training_status.json',{'stage':'EVAL1'})
    supervisor=auto_train.Supervisor(tmp_path)
    monkeypatch.setattr(supervisor,'retain',lambda *a,**k:pytest.fail('Failed gate must not be accepted'))
    assert not supervisor.accept_final({'path':'unused'},'stage1',{'passed':False})
    assert supervisor.state['stage']=='EVAL1' and 'valid_stage1' not in supervisor.state


def test_plateau_assesses_best_checkpoint_then_preserves_failure(tmp_path,monkeypatch):
    atomic_json(tmp_path/'config.json',auto_train.DEFAULT)
    best={'path':'best_physical_policy.pt'}
    atomic_json(tmp_path/'training_status.json',{'stage':'EVAL1','best_stage1':best})
    evaluation=tmp_path/'evaluation'; evaluation.mkdir(); (evaluation/'report.md').write_text('Physical gate failed')
    supervisor=auto_train.Supervisor(tmp_path)
    def evaluate(checkpoint,stage,final=False):
        assert checkpoint==best and stage=='stage1' and final
        return dict(passed=False,directory=str(evaluation),score=.1)
    monkeypatch.setattr(supervisor,'evaluate',evaluate)
    assert not supervisor.assess_before_stop('stage1','plateau')
    result=json.loads((tmp_path/'stage1_final_assessment.json').read_text())
    assert not result['passed'] and result['stop_reason']=='plateau'
    assert 'valid_stage1' not in supervisor.state
