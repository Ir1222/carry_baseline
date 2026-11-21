"""Hard-limit Reset, physics/reference clock, and reference-free action semantics."""
import json
from types import SimpleNamespace as NS
import pytest
import torch
from holosoma.carry.stage1_command import Stage1TrackCommand
from holosoma.managers.command.terms.wbt import MotionCommand


def test_exact_reset_preserves_legal_hard_limit_and_rejects_invalid_data(tmp_path):
    cmd=Stage1TrackCommand.__new__(Stage1TrackCommand)
    cmd.reference_hard_limits=torch.tensor([[-1.,1.],[-2.,2.]])
    cmd._env=NS(dof_names=['wrist','waist'],stage1_diagnostic_dir=tmp_path,
        simulator=NS(dof_pos_limits=torch.tensor([[-.95,.95],[-1.9,1.9]])))
    ref=torch.tensor([[1.,-2.]])
    torch.testing.assert_close(cmd._prepare_reset_joint_positions(ref,ref,torch.tensor([0])),ref,atol=0,rtol=0)
    # Other MotionCommand tasks retain their original 95% reset margin.
    torch.testing.assert_close(MotionCommand._prepare_reset_joint_positions(cmd,ref,ref,None),torch.tensor([[.95,-1.9]]))
    invalid=torch.tensor([[1.001,0.]])
    with pytest.raises(ValueError,match='no pose was corrected'):
        cmd._prepare_reset_joint_positions(invalid,invalid,None)
    evidence=json.loads((tmp_path/'stage1_invalid_reference.json').read_text())
    assert evidence['violations'][0]['joint']=='wrist'
    assert invalid[0,0]>1.  # report; never silently clamp the input


def test_first_normal_and_boundary_reference_frames_advance_once_after_physics():
    cmd=Stage1TrackCommand.__new__(Stage1TrackCommand);cmd.device='cpu'
    cmd._env=NS(episode_length_buf=torch.tensor([0,0]))
    cmd.reference_episode_step=torch.zeros(2,dtype=torch.long)
    cmd.time_steps=torch.tensor([0,10]);cmd.motion_ids=torch.tensor([0,1])
    cmd.motion=NS(motion_end_idx=torch.tensor([3,12]));cmd.motion_cfg=NS(use_adaptive_timesteps_sampler=False)
    cmd._update_track_commands=lambda:None;cmd._update_relative_reference=lambda:None
    cmd.step();cmd.advance_reference_to_post_action();assert cmd.time_steps.tolist()==[0,10]
    cmd._env.episode_length_buf+=1
    cmd.advance_reference_to_post_action();assert cmd.time_steps.tolist()==[1,11]
    cmd.step();cmd.advance_reference_to_post_action();assert cmd.time_steps.tolist()==[1,11]
    cmd._env.episode_length_buf+=1
    cmd.advance_reference_to_post_action();assert cmd.time_steps.tolist()==[2,11]
    from holosoma.carry.termination import clip_timeout
    cmd.track_env_mask=torch.ones(2,dtype=torch.bool)
    assert clip_timeout(NS(command_manager=NS(get_state=lambda _:cmd))).all()
    cmd._env.episode_length_buf+=2
    with pytest.raises(RuntimeError,match='clock mismatch'):cmd.advance_reference_to_post_action()


def test_delta_target_samples_actual_q_once_and_uses_inherited_torque_clipping():
    from holosoma.carry.action import JointDeltaPositionActionTerm,position_target,DELTA
    from holosoma.carry.stage1_presets import g1_29dof_carry_stage1_joint as base
    from holosoma.carry.inference import CarryActor
    sim=NS(dof_pos=torch.zeros(2,29),dof_vel=torch.zeros(2,29))
    env=NS(num_envs=2,num_dof=29,device='cpu',simulator=sim,robot_config=base.robot,
        dof_names=base.robot.dof_names,default_dof_pos=torch.ones(2,29),
        torque_limits=torch.tensor(base.robot.dof_effort_limit_list),log_dict={},_randomize_ctrl_delay=False)
    term=JointDeltaPositionActionTerm(base.action.terms['joint_control'],env)
    action=torch.ones(2,29);term.process_actions(action)
    target=position_target(action,sim.dof_pos,env.default_dof_pos,term.action_scales,DELTA)
    torch.testing.assert_close(term._compute_torques(action),.25*env.torque_limits.expand(2,-1))
    sim.dof_pos+=.01  # physics moves, but center stays fixed throughout the PD window
    torch.testing.assert_close(term._position_action_center(),torch.zeros(2,29))
    expected=term.p_gains*(target-sim.dof_pos)
    torch.testing.assert_close(term._compute_torques(action),expected.clamp(-env.torque_limits,env.torque_limits))
    actor=CarryActor.__new__(CarryActor);actor.default_joint_pos=env.default_dof_pos
    actor.metadata={'action_parameterization':DELTA,'action_scales':term.action_scales.tolist(),'action_clip_value':100.}
    torch.testing.assert_close(actor.joint_position_target(action,torch.zeros(2,29)),target)
    # There is no Track/Gen/reference input in either decoder.
    torch.testing.assert_close(term._compute_torques(action*1000),env.torque_limits.expand(2,-1))


def test_future_fullbody_resume_refuses_a_different_action_decoder():
    from holosoma.carry.fullbody_environment import FullBodyCarryEnv
    env=FullBodyCarryEnv.__new__(FullBodyCarryEnv)
    env.action_manager=NS(get_term=lambda _:NS(parameterization='fixed_default_v1'))
    with pytest.raises(ValueError,match='Track and Gen must use the same'):
        env.load_checkpoint_state({'stage1_action_parameterization':'joint_delta_v1'})
