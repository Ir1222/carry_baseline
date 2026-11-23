"""The stalled console path must be impossible in training and policy playback."""
import io
from types import SimpleNamespace as NS
from unittest.mock import Mock

import pytest
import torch

from holosoma.agents.modules.logging_utils import LoggingHelper
from holosoma.carry.unified_ppo import UnifiedCarryPPO


def forbid_rich(monkeypatch):
    import rich.console
    import rich.live

    def forbidden(*args, **kwargs):
        raise AssertionError("PPO train/play must not enter dynamic Rich rendering")

    monkeypatch.setattr(rich.live.Live, "__enter__", forbidden)
    monkeypatch.setattr(rich.live.Live, "refresh", forbidden)
    monkeypatch.setattr(rich.console.Console, "render", forbidden)


@pytest.mark.parametrize("tty", [False, True])
def test_large_training_metrics_use_plain_bounded_output_and_keep_all_scalars(monkeypatch, tty):
    import holosoma.agents.modules.logging_utils as module

    forbid_rich(monkeypatch)
    wandb=Mock();monkeypatch.setattr(module,"wandb",wandb)
    writer=Mock()
    helper=LoggingHelper(writer,"/tmp/plain-log-test",num_envs=2,num_steps_per_env=24,
                         num_learning_iterations=15000,device="cpu")
    helper.rewbuffer.append(6.9);helper.lenbuffer.append(75.4)
    class Stream(io.StringIO):
        def isatty(self):
            return tty
    stream=Stream();monkeypatch.setattr("sys.stdout",stream)
    diagnostics={f"hoi/phase/carry/nonhand_link/link_{i}/force_n":torch.tensor([.1,.2])
                 for i in range(4096)}
    for it in (1301,1302):
        helper.episode_env_tensors.add(diagnostics)
        helper.ep_infos.append({"reward":torch.tensor([1.,2.])})
        helper.raw_ep_infos.append({"raw_reward":torch.tensor([2.,3.])})
        helper.collection_time=19.;helper.learn_time=.5
        helper.post_epoch_logging(it,{"Value":237.1,"KL":.0137},{})

    lines=stream.getvalue().splitlines()
    assert len(lines)==2 and all(len(line)<600 for line in lines)
    assert "Learning iteration 1301/15000" in lines[0]
    assert "completed_updates=1303" in lines[1]
    assert "link_4095" not in stream.getvalue()
    calls=writer.add_scalar.call_args_list
    assert sum(call.args[0].endswith("link_4095/force_n") for call in calls)==2
    assert all(len(call.args)>=2 for call in calls)
    assert wandb.log.call_count==2
    assert any(k.endswith("link_4095/force_n") for k in wandb.log.call_args.args[0])
    assert not helper.ep_infos and not helper.raw_ep_infos and not helper.episode_env_tensors.data
    assert helper.tot_timesteps==96 and helper.collection_time==0 and helper.learn_time==0


def test_native_policy_playback_never_enters_rich_logging(monkeypatch):
    forbid_rich(monkeypatch)
    class Actor(torch.nn.Module):
        def act_inference(self, obs):
            return torch.zeros(len(obs["actor_obs"]),29)
    class Env:
        num_envs=2
        steps=0
        def set_is_evaluating(self):
            self.is_evaluating=True
        def reset_all(self):
            return dict(actor_obs=torch.zeros(2,357),critic_obs=torch.zeros(2,207))
        def step(self,state):
            self.steps+=1
            return self.reset_all(),torch.zeros(2),torch.zeros(2,dtype=torch.bool),{}

    algo=UnifiedCarryPPO.__new__(UnifiedCarryPPO)
    algo.config=NS(eval_callbacks=None);algo.eval_callbacks=[];algo.env=Env()
    algo.device="cpu";algo.num_act=29;algo.empirical_normalization=False
    algo.actor=Actor();algo.critic=torch.nn.Identity()
    algo.actor_obs_normalizer=torch.nn.Identity();algo.critic_obs_normalizer=torch.nn.Identity()
    algo.actor_obs_keys=["actor_obs"];algo.critic_obs_keys=["critic_obs"]
    algo.evaluate_policy(max_eval_steps=10000)
    assert algo.env.steps==10000 and algo.env.is_evaluating


def test_completed_update_and_snapshot_are_durable_before_console_logging(tmp_path):
    from contextlib import nullcontext
    import json

    algo=UnifiedCarryPPO.__new__(UnifiedCarryPPO)
    algo.config=NS(num_learning_iterations=1,init_at_random_ep_len=False,
                   latest_save_interval=100,save_interval=2000)
    algo.current_learning_iteration=99;algo.device="cpu";algo.is_main_process=True
    algo.is_multi_gpu=False;algo.log_dir=tmp_path;algo.env=NS(reset_all=lambda:{"obs":torch.zeros(1)})
    algo._train_mode=lambda:None;algo._notify_training_step=lambda _:None
    algo._notify_rollout_end=lambda _:None;algo._rollout_step=lambda obs:obs
    algo.actor_optimizer=NS(step=lambda:None);algo.critic_optimizer=NS(step=lambda:None)
    algo.logging_helper=NS(record_collection_time=nullcontext,record_learn_time=nullcontext,
        set_run_start_learning_iteration=lambda _:None)
    def training_step():
        algo.actor_optimizer.step();algo.critic_optimizer.step()
        return {}
    algo._training_step=training_step
    saved=[];algo.save=lambda path:saved.append(path.name);algo.export=lambda path:None
    def logger_fails(*args):
        state=json.loads((tmp_path/"training_status.json").read_text())
        assert state["completed_updates"]==100
        assert "model.pt" in saved and "model_00099.pt" in saved
        raise RuntimeError("simulated console sink failure")
    algo._post_epoch_logging=logger_fails
    with pytest.raises(RuntimeError,match="console sink"):
        algo.learn()


def playback_fixture(tmp_path,monkeypatch):
    import copy
    import holosoma.carry.checkpoints as checkpoints
    algo=UnifiedCarryPPO.__new__(UnifiedCarryPPO)
    algo.device="cpu";algo.empirical_normalization=True
    algo.actor=torch.nn.Linear(357,29);algo.critic=torch.nn.Linear(207,1)
    algo.actor_obs_normalizer=torch.nn.LayerNorm(357);algo.critic_obs_normalizer=torch.nn.LayerNorm(207)
    state=dict(unified_schema=2,actor_dim=357,critic_dim=207,fullbody_manifest_sha256="dataset",
        fullbody_limits={"h":.7},stage1_reference_protocol="hard_reset_post_action_v1",
        stage1_action_parameterization="joint_delta_v1",
        task_contract=dict(protocol="measured_support_v2",actor_dim=357,critic_dim=207,
            physics={"mass":1.1},p_gains=[10.],d_gains=[1.],action_scales=[.1],
            action={"decoder":"joint_delta_v1"},sampling={"eval_bin":None}))
    current=copy.deepcopy(state);current["task_contract"]["sampling"]={"eval_bin":0}
    algo.env=NS(get_checkpoint_state=lambda:current,task_contract=lambda:current["task_contract"])
    payload=dict(env_state=state,iter=1299,actor_model_state_dict=algo.actor.state_dict(),
        critic_model_state_dict=algo.critic.state_dict(),
        actor_obs_normalizer_state_dict=algo.actor_obs_normalizer.state_dict(),
        critic_obs_normalizer_state_dict=algo.critic_obs_normalizer.state_dict())
    path=tmp_path/"model.pt";torch.save(payload,path)
    checked=[];monkeypatch.setattr(checkpoints,"validate",lambda p:checked.append(p))
    return algo,path,current,checked


def test_play_can_change_eval_sampling_but_cannot_become_training_resume(tmp_path,monkeypatch):
    algo,path,current,checked=playback_fixture(tmp_path,monkeypatch)
    with pytest.raises(ValueError,match="matching v2"):
        algo.load(path)
    algo.load_for_evaluation(path)
    assert checked and algo._evaluation_only_loaded
    assert algo.current_learning_iteration==1299 and not algo.actor.training
    with pytest.raises(ValueError,match="Evaluation-only"):
        algo.learn()


@pytest.mark.parametrize("field",["actor_dim","fullbody_manifest_sha256","stage1_action_parameterization","p_gains"])
def test_play_still_rejects_incompatible_observation_control_or_dataset(tmp_path,monkeypatch,field):
    algo,path,current,checked=playback_fixture(tmp_path,monkeypatch)
    if field=="p_gains":current["task_contract"][field]=[20.]
    else:current[field]="incompatible"
    with pytest.raises(ValueError,match="Playback"):
        algo.load_for_evaluation(path)
    assert checked


def test_play_wrapper_refuses_an_owned_gpu_before_launching_isaac(tmp_path):
    import fcntl
    import subprocess
    from pathlib import Path
    checkpoint=tmp_path/"model.pt";checkpoint.touch()
    script=Path(__file__).resolve().parents[1]/"scripts/carry/play_unified_hoi.sh"
    with open("/tmp/g1-carry-gpu0.lock","a") as lock:
        try:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            pass  # an existing GPU task already supplies the owned-lock case
        result=subprocess.run(["bash",str(script),str(checkpoint)],capture_output=True,text=True,timeout=5)
    assert result.returncode==1 and "GPU0 is owned" in result.stderr


def test_play_preloads_viser_before_isaac_can_shadow_websocket_modules(monkeypatch):
    import holosoma.eval_agent as entry
    import holosoma.utils.viser_helper as viewer
    events=[]
    monkeypatch.setattr(viewer,"prepare_viser_imports",lambda:events.append("web_dependencies"))
    class ReachedSimulation(Exception):
        pass
    def setup(config):
        events.append("simulation")
        raise ReachedSimulation()
    monkeypatch.setattr(entry,"setup_simulation_environment",setup)
    from dataclasses import replace
    from holosoma.config_types.eval_callback import EvalCallbacksConfig
    callbacks=EvalCallbacksConfig()
    callbacks=replace(callbacks,viser=replace(callbacks.viser,config=replace(callbacks.viser.config,enabled=True)))
    with pytest.raises(ReachedSimulation):
        entry.run_eval_with_tyro(NS(),None,None,None,eval_cbs_cfg=callbacks)
    assert events==["web_dependencies","simulation"]
