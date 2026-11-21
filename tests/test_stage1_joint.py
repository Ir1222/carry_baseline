"""Joint Track dataset, sampling and uninterrupted-iteration launch contracts."""
import json
from pathlib import Path
import sys
from types import SimpleNamespace as NS
import pytest
import torch

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/'scripts/carry'))
from prepare_stage1_joint import verify_bundle
from train_stage1_joint import parser,build_argv
from holosoma.carry.stage1_presets import DATA,g1_29dof_carry_stage1_joint as preset
from holosoma.carry.stage1_command import Stage1TrackCommand


def test_both_families_admitted_without_falsifying_physics_status():
    rows=verify_bundle(DATA)
    assert len(rows)==3
    weights={family:sum(r['weight'] for r in rows if r['family']==family) for family in ['squat_stand','forward_carry']}
    assert weights=={'squat_stand':.5,'forward_carry':.5}
    forward=next(r for r in rows if r['family']=='forward_carry')
    assert forward['physics_validation']=='kinematic_only_controller_admission_failed'


def test_real_motion_sampling_preserves_balanced_action_families():
    cmd=Stage1TrackCommand.__new__(Stage1TrackCommand)
    cmd.manifest=json.loads((DATA/'manifest.json').read_text())
    cmd.motion=NS(num_motions=3);cmd.device='cpu'
    cmd.motion_ids=torch.zeros(100000,dtype=torch.long)
    torch.manual_seed(42);cmd._sample_motion_ids_for_reset(torch.arange(100000))
    # Loader order is continuous, original_forward, repeated.
    counts=torch.bincount(cmd.motion_ids,minlength=3).float()/100000
    torch.testing.assert_close(counts,torch.tensor([.2,.5,.3]),atol=.006,rtol=0)
    assert (cmd.motion_ids[1::2]==1).all()
    assert (cmd.motion_ids[0::2]!=1).all()


def test_stage1_has_original_robot_object_imitation_and_no_gen_goals():
    cfg=preset.command.setup_terms['motion_command'].params['motion_config']
    assert cfg.hybrid.track_ratio==1. and cfg.start_at_timestep_zero_prob==.5
    assert preset.algo.config.num_learning_iterations==15000
    assert preset.randomization.setup_terms['fullbody_physics'].params['data']==str(DATA)
    assert len([k for k in preset.reward.terms if k.startswith('motion_')])==6
    assert 'object_global_ref_position_error_exp' in preset.reward.terms
    assert 'object_global_ref_orientation_error_exp' in preset.reward.terms
    assert not {'velocity_tracking','height_tracking','yaw_tracking','goal_compatible_style_reward'} & set(preset.reward.terms)
    cmd=Stage1TrackCommand.__new__(Stage1TrackCommand)
    cmd.sample_gen_commands(torch.tensor([],dtype=torch.long))
    with pytest.raises(RuntimeError):cmd.sample_gen_commands(torch.tensor([0]))
    with pytest.raises(RuntimeError):cmd.set_command([.2,0,0,.7])


def test_stage1_advances_each_clip_without_cross_clip_or_state_reset():
    cmd=Stage1TrackCommand.__new__(Stage1TrackCommand)
    cmd.device='cpu';cmd._env=NS(episode_length_buf=torch.tensor([1,1,0]))
    cmd.reference_episode_step=torch.zeros(3,dtype=torch.long)
    cmd.motion_cfg=NS(use_adaptive_timesteps_sampler=False)
    cmd.motion_ids=torch.tensor([0,1,2]);cmd.time_steps=torch.tensor([349,459,500])
    cmd.motion=NS(motion_end_idx=torch.tensor([351,461,1112]))
    called=[];cmd._update_track_commands=lambda:called.append('reference')
    cmd._update_relative_reference=lambda:called.append('relative')
    cmd.advance_reference_to_post_action()
    cmd._env.episode_length_buf[:2]+=1
    cmd.advance_reference_to_post_action()
    assert cmd.time_steps.tolist()==[350,460,500]
    assert called==['reference','relative','reference','relative']


def test_default_launch_is_one_15000_update_ppo_run():
    args=parser().parse_args([]);argv=build_argv(args,Path('/tmp/example_stage1'))
    assert '--algo.config.num-learning-iterations=15000' in argv
    assert '--algo.config.save-interval=500' in argv
    assert '--algo.config.num-mini-batches=128' in argv
    assert not any('checkpoint=' in v or 'auto_train' in v or 'timeout' in v for v in argv)


def test_initial_reset_does_not_run_an_uncontrolled_zero_action_step():
    from holosoma.carry.stage1_environment import Stage1CarryEnv
    env=Stage1CarryEnv.__new__(Stage1CarryEnv);env.num_envs=2;env.device='cpu'
    calls=[];cmd=NS(init_buffers=lambda:calls.append('command_buffers'))
    env.command_manager=NS(get_state=lambda name:cmd)
    env.reset_envs_idx=lambda ids:calls.append('physical_reset')
    env._refresh_envs_after_reset=lambda ids:calls.append('synchronize')
    env._update_tasks_callback=lambda:calls.append('reference')
    env._compute_observations=lambda:calls.append('observe')
    env._post_compute_observations_callback=lambda:None;env._clip_observations=lambda:None
    env.obs_buf_dict={'actor_obs':torch.zeros(2,348)}
    env.step=lambda *args:pytest.fail('reset_all must not advance physics with zero actions')
    assert env.reset_all()['actor_obs'].shape==(2,348)
    assert calls==['command_buffers','physical_reset','synchronize','reference','observe']


def test_optional_manual_resume_targets_total_not_another_15000(monkeypatch):
    import holosoma.carry.checkpoints as checkpoints
    monkeypatch.setattr(checkpoints,'validate',lambda path:{'completed_updates':5501})
    args=parser().parse_args(['--resume','/tmp/model.pt'])
    argv=build_argv(args,Path('/tmp/recovery'))
    assert '--algo.config.num-learning-iterations=9499' in argv
    args.iterations=5501
    with pytest.raises(ValueError,match='already reached'):build_argv(args,Path('/tmp/recovery'))


def test_full_stage1_acceptance_requires_walking_and_both_squat_clips():
    from holosoma.carry.acceptance import tracking_suite_passed
    expected={'clip_0','clip_1','clip_2'}
    good={name:{'success_rate':.8} for name in expected}
    assert tracking_suite_passed(good,expected,10)
    assert not tracking_suite_passed({k:v for k,v in good.items() if k!='clip_1'},expected,10)
    assert not tracking_suite_passed({**good,'clip_1':{'success_rate':.7}},expected,10)
    assert not tracking_suite_passed(good,expected,9)
