"""Regression tests exercise production support/termination/sampler implementations."""
from types import SimpleNamespace as NS
import os,signal,json
import pytest
import torch
from holosoma.carry.support import SupportState,advance_contact_gap,PRIVILEGED_FIELDS
from holosoma.carry.unified import UnifiedFailure,UnifiedCommand

def metrics():
    z=lambda:torch.zeros(1)
    return dict(bilateral_contact=z(),left_hand_normal_n=z(),right_hand_normal_n=z(),
        upward_friction_weight_ratio=z(),box_clearance_m=z(),nonhand_box_contact_n=z(),
        nonhand_upward_force_n=z(),continuous_no_contact_s=z(),object_speed_m_s=z(),
        object_angular_speed=z(),ground_support_weight_ratio=torch.ones(1),
        stable_support_sample=torch.ones(1,dtype=torch.bool))

def test_contact_flicker_does_not_accumulate_two_control_periods():
    gap=torch.zeros(1);required=torch.ones(1,dtype=torch.bool)
    for _ in range(2):
        for step in range(20):
            gap=advance_contact_gap(gap,torch.tensor([step!=19]),required,.001)
        assert gap.item()==pytest.approx(.001)
    for _ in range(99):gap=advance_contact_gap(gap,torch.tensor([False]),required,.001)
    assert gap.item()==pytest.approx(.1,abs=1e-6)

def test_release_hysteresis_and_real_departure():
    state=SupportState(1,"cpu");m=metrics()
    for _ in range(40):assert not state.update(m,.02).item()
    assert m["putdown_stable_success"].item()
    m["stable_support_sample"][:]=False
    assert not state.update(m,.02).item()
    assert m["stable_support"].item()
    # Sustained loss revokes support, and actual airborne departure requires hands.
    m["box_clearance_m"][:]=.12
    assert not state.update(m,.02).item()
    assert m["support_required"].item() and not m["stable_support"].item()
    m["continuous_no_contact_s"][:]=.1
    assert state.update(m,.02).item()

def test_airborne_rsi_never_acquired_is_not_exempt_and_reset_clears():
    state=SupportState(1,"cpu");m=metrics()
    m["stable_support_sample"][:]=False;m["box_clearance_m"][:]=.3
    for _ in range(5):
        m["continuous_no_contact_s"][:]=.1
        triggered=state.update(m,.02)
    assert triggered.item() and not state.acquired.item()
    state.reset(torch.tensor([0]))
    assert not state.required.item() and not state.age.item()
    assert not state.update(m,.02).item()

def test_actual_failure_is_idempotent_and_phase_independent(monkeypatch):
    import holosoma.carry.unified as u
    root=torch.zeros(1,13);root[:,2]=.49;root[:,6]=1
    box=root.clone();box[:,0]=.3
    env=NS(num_envs=1,device="cpu",dt=.02,episode_length_buf=torch.zeros(1,dtype=torch.long),
        carry_box_mass=torch.tensor([1.1]),simulator=NS(robot_root_states=root,dof_pos=torch.zeros(1,29),
            body_names=["left_ankle_roll_link","right_ankle_roll_link"],contact_forces=torch.zeros(1,2,3),
            scene=NS(env_origins=torch.zeros(1,3))),
        command_manager=NS(get_state=lambda _:NS(task_mode=mode)))
    mode=torch.tensor([0]);m=metrics()
    monkeypatch.setattr(u,"simulator_box_state",lambda _:box)
    monkeypatch.setattr(u,"box_ground_state",lambda _:m.copy())
    term=UnifiedFailure(NS(params={"loss_of_grasp_s":.1}),env)
    for step in range(40):
        env.episode_length_buf+=1
        assert not term(env).item()
    age=term.support.age.clone();term(env)
    torch.testing.assert_close(age,term.support.age)
    for phase in (1,2):
        mode[:]=phase;env.episode_length_buf+=1
        assert not term(env).item()
    # Incidental nonhand contact and low root remain diagnostics.
    m["nonhand_box_contact_n"][:]=1.;root[:,2]=.44;env.episode_length_buf+=1
    assert not term(env).item()
    assert env.hoi_metrics["root_too_low"].item()
    assert env.hoi_metrics["nonhand_contact"].item()
    m["box_clearance_m"][:]=-.03;env.episode_length_buf+=1
    assert term(env).item() and term.causes["severe_floor_penetration"].item()

def test_full_sequence_hard_bins_still_change_actual_reset_distribution():
    from holosoma.managers.command.terms.wbt import AdaptiveTimestepsSampler
    cmd=UnifiedCommand.__new__(UnifiedCommand);cmd.device="cpu"
    cmd.rows=[dict(family="full_sequence",sampling_weight=1.)]
    n=5000;cmd.family_ids=torch.zeros(n,dtype=torch.long);cmd.motion_ids=cmd.family_ids.clone()
    cmd.eligible=[torch.arange(99)]
    sampler=AdaptiveTimestepsSampler(torch.tensor([0]),torch.tensor([100]),"cpu",.02,["track"],bin_width_s=1.)
    cmd.adaptive_timesteps_sampler=sampler
    sampler.bin_fail_ema[0,0]=torch.tensor([.01,1.])
    torch.manual_seed(42)
    _,_,t=cmd._sample_adaptive_reset_states(torch.arange(n),torch.zeros(n,dtype=torch.long))
    assert (t>=50).float().mean()>.9
    assert torch.isin(t,cmd.eligible[0]).all()

def test_latest_discovery_uses_internal_updates_without_onnx(tmp_path):
    from test_carry_supervisor import checkpoint
    from holosoma.carry.checkpoints import atomic_save,newest_valid
    older=checkpoint();older["iter"]=3
    newer=checkpoint();newer["iter"]=17
    atomic_save(older,tmp_path/"model_99999.pt")
    atomic_save(newer,tmp_path/"model.pt")
    selected,_=newest_valid(tmp_path)
    assert selected["completed_updates"]==18 and selected["path"].endswith("/model.pt")

def test_safe_stop_finishes_update_and_saves_without_export_or_evaluation(tmp_path):
    from holosoma.carry.unified_ppo import UnifiedCarryPPO
    from contextlib import nullcontext
    algo=UnifiedCarryPPO.__new__(UnifiedCarryPPO)
    algo.config=NS(num_learning_iterations=3,init_at_random_ep_len=False,latest_save_interval=100,save_interval=2000)
    algo.device="cpu";algo.env=NS(reset_all=lambda:{"obs":torch.zeros(1)})
    algo.current_learning_iteration=0;algo.is_main_process=True;algo.is_multi_gpu=False;algo.log_dir=tmp_path
    algo._train_mode=lambda:None;algo._notify_training_step=lambda _:None;algo._notify_rollout_end=lambda _:None
    algo._rollout_step=lambda obs:obs;algo._post_epoch_logging=lambda *args:None
    algo.actor_optimizer=NS(step=lambda:None);algo.critic_optimizer=NS(step=lambda:None)
    algo.logging_helper=NS(set_run_start_learning_iteration=lambda _:None,
        record_collection_time=nullcontext,record_learn_time=nullcontext)
    stages=[];saved=[]
    def update():
        algo.actor_optimizer.step();os.kill(os.getpid(),signal.SIGTERM)
        stages.append("continued");algo.critic_optimizer.step()
        return {}
    algo._training_step=update
    algo.save=lambda path:saved.append((str(path),algo.optimizer_steps.copy(),list(stages)))
    algo.export=lambda path:pytest.fail("Interrupted latest snapshot must not require ONNX")
    with pytest.raises(SystemExit) as e:algo.learn()
    assert e.value.code==130 and saved[0][1]=={"actor":1,"critic":1}
    assert saved[0][2]==["continued"]
    status=json.loads((tmp_path/"training_status.json").read_text())
    assert status["status"]=="interrupted" and status["completed_updates"]==1

def test_grounded_preload_reward_is_nonzero_without_upward_friction(monkeypatch):
    import holosoma.carry.unified as u
    env=NS(num_envs=1,device="cpu",carry_box_vertices=torch.tensor([[-.2,-.3,-.1],[.2,.3,.1]]))
    box=torch.zeros(1,13);box[:,6]=1
    env.simulator=NS(_robot=NS(body_names=["left_sphere_hand_link","right_sphere_hand_link"],
        data=NS(body_pos_w=torch.tensor([[[0.,.31,0.],[0.,-.31,0.]]]))))
    env.command_manager=NS(get_state=lambda _:NS(task_mode=torch.tensor([0])))
    m=metrics();m["normal_vertical_fraction"]=torch.zeros(1);env.hoi_metrics=m
    monkeypatch.setattr(u,"simulator_box_state",lambda _:box)
    approaching=u.pickup_reward(env).item()
    m["left_hand_normal_n"][:]=20;m["right_hand_normal_n"][:]=20
    preload=u.pickup_reward(env).item()
    assert 0<approaching<preload<=1
    assert m["upward_friction_weight_ratio"].item()==0 and m["box_clearance_m"].item()==0
    m["left_hand_normal_n"][:]=200;m["right_hand_normal_n"][:]=200
    assert u.pickup_reward(env).item()<preload

def test_reset_all_buffer_initialization_preserves_restored_sampler(monkeypatch):
    from holosoma.carry.stage1_command import Stage1TrackCommand
    from holosoma.managers.command.terms.wbt import AdaptiveTimestepsSampler
    cmd=UnifiedCommand.__new__(UnifiedCommand);cmd.device="cpu";cmd.num_envs=1
    sampler=AdaptiveTimestepsSampler(torch.tensor([0]),torch.tensor([100]),"cpu",.02,["track"])
    sampler.bin_fail_ema[:]=.37;sampler.pending_visits[:]=7;sampler.pending_failures[:]=3
    cmd.adaptive_timesteps_sampler=sampler
    monkeypatch.setattr(Stage1TrackCommand,"init_buffers",lambda _:sampler.init_buffers())
    cmd.init_buffers()
    assert (sampler.bin_fail_ema==.37).all() and (sampler.pending_visits==7).all()
    assert (sampler.pending_failures==3).all()

def test_legacy_training_checkpoint_rejected_before_model_loading():
    from holosoma.carry.unified_ppo import UnifiedCarryPPO
    from pathlib import Path
    old=Path(__file__).resolve().parents[2]/"artifacts/unified_hoi_hmi_stage1/formal_8192_15000_002_save2000/training/logs/WholeBodyTracking/20261121_110128-unified_hoi_stage1-locomotion/model_02000.pt"
    if not old.exists():pytest.skip("Local diagnostic checkpoint not part of Git")
    algo=UnifiedCarryPPO.__new__(UnifiedCarryPPO)
    algo.env=NS(task_contract=lambda:{})
    with pytest.raises(ValueError,match="matching v2"):algo.load(old)


def test_command_physics_metrics_pass_real_ppo_log_aggregation(monkeypatch):
    import holosoma.carry.fullbody_rewards as rewards
    import holosoma.carry.rewards as goals
    from holosoma.utils.average_meters import TensorAverageMeterDict

    env=NS(episode_length_buf=torch.ones(2,dtype=torch.long))
    cmd=UnifiedCommand.__new__(UnifiedCommand)
    cmd._env=env;cmd.device="cpu";cmd.metrics={};cmd.carry_level=0
    cmd.episode_control_steps=torch.zeros(2,dtype=torch.long)
    cmd.episode_good_steps=torch.zeros(2,dtype=torch.long)
    cmd.task_command=torch.zeros(2,4)
    cmd.rows=[dict(family="full_sequence"),dict(family="loaded_locomotion")]
    cmd.motion_ids=torch.tensor([0,1]);cmd.task_mode=torch.tensor([0,2])
    supported=torch.tensor([True,False])
    physics=dict(bilateral_contact=torch.ones(2),stable_support_sample=supported,
        nonhand_link_force_w=torch.ones(2,3,3),object_speed_m_s=torch.tensor([.02,.04]))
    monkeypatch.setattr(rewards,"physical_metrics",lambda _:physics)
    monkeypatch.setattr(goals,"task_errors",lambda _:torch.zeros(2,4))
    meter=TensorAverageMeterDict()
    for _ in range(2):
        cmd.update_metrics()
        meter.add(cmd.metrics)
    averaged=meter.mean_and_clear()
    assert averaged["carry/stable_support_sample"].item()==pytest.approx(.5)
    assert averaged["carry/object_speed_m_s"].item()==pytest.approx(.03)
    assert "carry/nonhand_link_force_w" not in averaged
    assert supported.dtype==torch.bool  # logging must not change physical predicates
    assert not meter.data


@pytest.mark.parametrize("status,process_exit,expected",[
    ("interrupted",0,130),("interrupted",130,130),("running",0,1),
    ("complete",0,0),("complete",1,1)])
def test_wrapper_exit_guard_uses_durable_status(tmp_path,status,process_exit,expected):
    from holosoma.carry.run_status import training_exit_code
    (tmp_path/"training_status.json").write_text(json.dumps(dict(status=status)))
    assert training_exit_code(tmp_path,process_exit)==expected
