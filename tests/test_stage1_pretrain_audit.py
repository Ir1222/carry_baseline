"""Diagnostic counters must measure terminal episodes before Reset without changing inputs."""
from pathlib import Path
import sys
from types import SimpleNamespace as NS
import torch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts/carry'))
from audit_stage1_pretrain import static_audit
from holosoma.carry.stage1_diagnostics import Stage1DiagnosticLog


def test_family_diagnostics_include_terminal_step_and_clear_only_finished():
    log=Stage1DiagnosticLog(2,'cpu')
    families={'squat_stand':torch.tensor([True,False]),'forward_carry':torch.tensor([False,True])}
    values={'contact':torch.tensor([1.,0.])};causes={'loss_of_grasp':torch.tensor([False,False])}
    log.observe(families,values,torch.tensor([.02,.02]),torch.tensor([False,False]),causes)
    values={'contact':torch.tensor([.5,1.])};before=values['contact'].clone()
    out=log.observe(families,values,torch.tensor([.04,.04]),torch.tensor([True,False]),causes)
    assert out['stage1/squat_stand/completed/contact']==.75
    torch.testing.assert_close(values['contact'],before)
    assert log.steps.tolist()==[0,2]
    out=log.observe(families,{'contact':torch.tensor([0.,1.])},torch.tensor([.02,.06]),
        torch.tensor([True,True]),{'loss_of_grasp':torch.tensor([True,True])})
    assert out['stage1/squat_stand/completed_episodes']==2
    assert out['stage1/squat_stand/completed/termination/loss_of_grasp']==.5
    torch.testing.assert_close(out['stage1/forward_carry/completed/contact'],torch.tensor(2/3))
    log.clear_active();assert log.steps.sum()==0
    assert log.totals['squat_stand']['episodes']==2


def test_reference_action_audit_uses_verified_reset_default_and_actual_clip_limit():
    result=static_audit()
    assert len(result['joint_names'])==29 and len(result['clips'])==3
    assert result['control']['action_clip_value']==100.
    assert all(row['action_clip_fraction']==0 for row in result['clips'])
    kp=torch.tensor(result['kp']);scale=torch.tensor(result['action_scales']);limit=torch.tensor(result['torque_limits'])
    torch.testing.assert_close(kp*scale,.25*limit)
    assert result['robot_soft_dof_pos_limit']==.95  # audit records the existing initialization margin


def test_reference_commands_use_heading_velocity_world_z_omega_and_ground_relative_height():
    from holosoma.carry.command import CarryCommand
    cmd=NS(root_quat_w=torch.tensor([[0.,0.,2**-.5,2**-.5]]),root_lin_vel_w=torch.tensor([[0.,1.,0.]]),
        root_ang_vel_w=torch.tensor([[1.,2.,.3]]),root_pos_w=torch.tensor([[10.,20.,1.2]]),
        _env=NS(simulator=NS(scene=NS(env_origins=torch.tensor([[10.,20.,.5]])))),
        task_command=torch.zeros(1,4),track_env_mask=torch.tensor([True]))
    CarryCommand._update_track_commands(cmd)
    torch.testing.assert_close(cmd.task_command,torch.tensor([[1.,0.,.3,.7]]),atol=1e-6,rtol=0)


def test_diagnostic_hook_checks_real_termination_once(monkeypatch):
    from holosoma.carry.stage1_environment import Stage1CarryEnv
    from holosoma.carry.fullbody_environment import FullBodyCarryEnv
    import holosoma.carry.stage1_diagnostics as diagnostics
    calls=[]
    monkeypatch.setattr(FullBodyCarryEnv,'_check_termination',lambda self:calls.append('termination'))
    monkeypatch.setattr(diagnostics,'record_stage1_diagnostics',lambda env:calls.append('log'))
    env=Stage1CarryEnv.__new__(Stage1CarryEnv)
    env.command_manager=NS(get_state=lambda name:NS(advance_reference_to_post_action=lambda:calls.append('reference')))
    Stage1CarryEnv._check_termination(env)
    assert calls==['reference','termination','log']
