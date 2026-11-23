
"""Finite GPU diagnostic. Never optimizes weights; never supplies a training initializer."""
import os,sys,json,time,runpy,random,hashlib
from pathlib import Path
import numpy as np
import torch
from holosoma.carry.unified_ppo import UnifiedCarryPPO
from holosoma.carry.checkpoints import atomic_json,validate
OUT=Path(os.environ["HMI_CAUSAL_OUT"])
CURRENT=Path(os.environ["HMI_CAUSAL_CURRENT"])
OLD=Path(os.environ["HMI_CAUSAL_OLD"])
ROLLOUTS=3
FIELDS=("bilateral_contact","hand_slip_speed_m_s","left_hand_normal_n","right_hand_normal_n",
        "continuous_no_contact_s","nonhand_box_contact_n","grasp_acquired","stable_support")
FAMILIES=("full_sequence","loaded_locomotion","loaded_squat_stand")
MODES=("pickup","carry","putdown")

def tensor_hash(*values):
    h=hashlib.sha256()
    for value in values:h.update(value.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()

def gradients(self):
    rows=[]
    params=list(self.actor.parameters())
    assert params[0] is self.actor.std
    for minibatch in self.storage.mini_batch_generator(self.config.num_mini_batches,1):
        losses=self._compute_ppo_loss(minibatch)
        surrogate=torch.autograd.grad(losses["surrogate_loss"],params,retain_graph=True)
        entropy=torch.autograd.grad(-self.config.entropy_coef*losses["entropy_loss"],self.actor.std,retain_graph=True)[0]
        total=torch.autograd.grad(losses["actor_loss"],params)
        sg=surrogate[0].detach();eg=entropy.detach();tg=total[0].detach()
        sn=torch.stack([g.detach().square().sum() for g in surrogate]).sum().sqrt()
        tn=torch.stack([g.detach().square().sum() for g in total]).sum().sqrt()
        rows.append(dict(samples=len(minibatch["actions"]),surrogate_std_gradient=sg.cpu().tolist(),
            entropy_std_gradient=eg.cpu().tolist(),total_std_gradient=tg.cpu().tolist(),
            surrogate_actor_gradient_norm=float(sn),total_actor_gradient_norm=float(tn),
            entropy_flips_shrink_to_expand=int(((sg>0)&(tg<0)).sum()),
            surrogate_expands=int((sg<0).sum()),total_expands=int((tg<0).sum()),
            surrogate_loss=float(losses["surrogate_loss"]),entropy=float(losses["entropy_loss"]),
            value_loss=float(losses["value_loss"]),kl=float(losses["kl_mean"])))
    raw=self.storage["returns"]-self.storage["values"]
    return dict(minibatches=rows,raw_advantage_std=float(raw.std()),raw_advantage_mean=float(raw.mean()),
        return_mean=float(self.storage["returns"].mean()),return_std=float(self.storage["returns"].std()),
        value_mean=float(self.storage["values"].mean()),reward_mean=float(self.storage["rewards"].mean()))

def probe(self):
    started=time.monotonic()
    current_info=validate(CURRENT);old_info=validate(OLD)
    frozen=torch.load(CURRENT,map_location="cpu",weights_only=True)
    previous=torch.load(OLD,map_location="cpu",weights_only=True)
    checkpoints={"current":current_info,"old":old_info}
    result=dict(scope="finite causal diagnostic; no optimizer updates; not final physical acceptance",
        num_envs=self.env.num_envs,rollouts_per_arm=ROLLOUTS,checkpoints=checkpoints,arms={})
    assert self.env.num_envs==8192 and self.config.num_steps_per_env==24 and self.config.num_mini_batches==4
    arms=[("current_native",False,False,False),("current_std1300",False,True,False),
          ("current_mean",False,False,True),("old_mean",True,False,True),
          ("old_native",True,False,False)]
    arms=[row for row in arms if row[0]==os.environ["HMI_CAUSAL_ARM"]]
    assert len(arms)==1
    reference_hash=os.environ["HMI_CAUSAL_EXPECT_REF"]
    for name,use_old,lower_std,deterministic in arms:
        print("CAUSAL_ARM_BEGIN",name,flush=True)
        self.load(CURRENT)
        source=previous if use_old else frozen
        self.actor.load_state_dict(source["actor_model_state_dict"])
        self.critic.load_state_dict(source["critic_model_state_dict"])
        self.actor_obs_normalizer.load_state_dict(source["actor_obs_normalizer_state_dict"])
        self.critic_obs_normalizer.load_state_dict(source["critic_obs_normalizer_state_dict"])
        if lower_std:
            with torch.no_grad():self.actor.std.copy_(previous["actor_model_state_dict"]["std"].to(self.device))
        self._train_mode()
        random.seed(314159);np.random.seed(314159);torch.manual_seed(314159);torch.cuda.manual_seed_all(314159)
        with torch.inference_mode():
            obs={k:v.to(self.device) for k,v in self.env.reset_all().items()}
        cmd=self.env.command_manager.get_state("motion_command")
        identity=tensor_hash(cmd.motion_ids,cmd.time_steps)
        if reference_hash is None:reference_hash=identity
        assert identity==reference_hash,"Paired arms did not start from identical reference states"
        arm=dict(reference_hash=identity,initial_pose_hash=tensor_hash(self.env.simulator.dof_pos),
            std=self.actor.std.detach().cpu().tolist(),deterministic=deterministic,rollouts=[],steps=0)
        alive=torch.ones(self.env.num_envs,device=self.device,dtype=torch.bool)
        first_reward=torch.zeros(self.env.num_envs,device=self.device)
        first_steps=torch.zeros_like(first_reward)
        first_cause={}
        metric_sums={f:torch.zeros_like(first_reward) for f in FIELDS}
        metric_sums["object_error_m"]=torch.zeros_like(first_reward)
        metric_sums["robot_error_m"]=torch.zeros_like(first_reward)
        modes=torch.zeros(self.env.num_envs,len(MODES),device=self.device)
        phase_sums={k:torch.zeros(len(MODES),device=self.device) for k in ("steps","bilateral_contact","hand_slip_speed_m_s")}
        last_mask=None
        original_check=self.env._check_termination
        original_step=self.env.step
        original_act=self.actor.act
        def measured_check():
            nonlocal last_mask
            value=original_check()
            last_mask=alive.clone()
            first_steps.add_(alive)
            for key in FIELDS:metric_sums[key].add_(torch.where(alive,self.env.hoi_metrics[key],0.))
            from holosoma.carry.observations import simulator_box_state
            object_error=(simulator_box_state(self.env)[:,:3]-cmd.object_pos_w).norm(dim=-1)
            robot_error=(cmd.robot_body_pos_w-cmd.body_pos_relative_w).norm(dim=-1).mean(-1)
            metric_sums["object_error_m"].add_(torch.where(alive,object_error,0.))
            metric_sums["robot_error_m"].add_(torch.where(alive,robot_error,0.))
            for j in range(len(MODES)):
                mask=alive&(cmd.task_mode==j)
                phase_sums["steps"][j]+=mask.sum()
                phase_sums["bilateral_contact"][j]+=self.env.hoi_metrics["bilateral_contact"][mask].sum()
                phase_sums["hand_slip_speed_m_s"][j]+=self.env.hoi_metrics["hand_slip_speed_m_s"][mask].sum()
            ended=alive&self.env.reset_buf.bool()
            for key,v in self.env.termination_manager.last_term_results.items():
                first_cause.setdefault(key,torch.zeros_like(alive))
                first_cause[key]|=ended&v
            for term,items in self.env.termination_manager.last_term_breakdowns.items():
                for cause,v in items.items():
                    key=term+"/"+cause;first_cause.setdefault(key,torch.zeros_like(alive))
                    first_cause[key]|=ended&v
            alive.logical_and_(~ended)
            return value
        def measured_step(inputs):
            value=original_step(inputs)
            assert last_mask is not None
            first_reward.add_(torch.where(last_mask,value[1].flatten(),0.))
            arm["steps"]+=1
            return value
        action_rng=torch.cuda.get_rng_state(self.device)
        def controlled_act(inputs):
            nonlocal action_rng
            if deterministic:
                self.actor.update_distribution(inputs["actor_obs"])
                return self.actor.act_inference(inputs)
            with torch.random.fork_rng(devices=[torch.cuda.current_device()]):
                torch.cuda.set_rng_state(action_rng,self.device)
                value=original_act(inputs)
                action_rng=torch.cuda.get_rng_state(self.device)
            return value
        self.env._check_termination=measured_check;self.env.step=measured_step;self.actor.act=controlled_act
        try:
            for r in range(ROLLOUTS):
                obs=self._rollout_step(obs)
                if not deterministic:arm["rollouts"].append(gradients(self))
                self.storage.clear()
                self.logging_helper.episode_env_tensors.mean_and_clear()
                self.logging_helper.ep_infos.clear();self.logging_helper.raw_ep_infos.clear()
                print("CAUSAL_ROLLOUT",name,r+1,"alive",int(alive.sum()),flush=True)
        finally:
            self.env._check_termination=original_check;self.env.step=original_step;self.actor.act=original_act
        arm["families"]={}
        for j,family in enumerate(FAMILIES):
            mask=cmd.family_ids==j
            n=int(mask.sum());steps=first_steps[mask].sum().clamp_min(1)
            row=dict(envs=n,first_episode_failure_or_end_fraction=float((~alive[mask]).float().mean()),
                observation_steps=float(steps),mean_first_episode_observed_s=float(first_steps[mask].mean()*.02),
                reward_per_observed_step=float(first_reward[mask].sum()/steps),
                observed_first_episode_reward_mean=float(first_reward[mask].mean()),
                termination_fraction={k:float(v[mask].float().mean()) for k,v in first_cause.items()})
            row.update({k:float(v[mask].sum()/steps) for k,v in metric_sums.items()})
            arm["families"][family]=row
        arm["phase"]={m:{k:float(v[j]/phase_sums["steps"][j].clamp_min(1)) for k,v in phase_sums.items() if k!="steps"} for j,m in enumerate(MODES)}
        result["arms"][name]=arm
        result["elapsed_s"]=time.monotonic()-started
        atomic_json(OUT/("probe_partial_"+os.environ["HMI_CAUSAL_ARM"]+".json"),result)
        print("CAUSAL_ARM_DONE",name,"elapsed",result["elapsed_s"],flush=True)
    result["passed"]=True
    result["optimizer_updates"]=0
    result["elapsed_s"]=time.monotonic()-started
    atomic_json(OUT/("probe_results_"+os.environ["HMI_CAUSAL_ARM"]+".json"),result)
    print("CAUSAL_PROBE_COMPLETE",result["elapsed_s"],flush=True)

UnifiedCarryPPO.learn=probe
sys.argv=["train_agent.py"]+sys.argv[1:]
runpy.run_path("/home/han/pyx/g1_carry_baseline_new/HMI/src/holosoma/holosoma/train_agent.py",run_name="__main__")
