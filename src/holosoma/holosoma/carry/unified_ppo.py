"""HMI PPO unchanged; publish only complete, stable checkpoint/export files."""
import os,signal,random
import numpy as np
import torch
from pathlib import Path
from holosoma.carry.fullbody_ppo import FullBodyCarryPPO


class UnifiedCarryPPO(FullBodyCarryPPO):
    def _checkpoint_metadata(self,iteration=None):
        value=super()._checkpoint_metadata(iteration)
        value.update(completed_updates=self.current_learning_iteration+1,
            training_status=getattr(self,'training_status','running'),
            optimizer_steps=getattr(self,'optimizer_steps',{}),
            rng_state=dict(torch=torch.get_rng_state(),cuda=torch.cuda.get_rng_state_all(),
                python=random.getstate(),numpy=(np.random.get_state()[0],
                    np.random.get_state()[1].tolist(),*np.random.get_state()[2:])))
        return value

    def load(self,ckpt_path):
        if ckpt_path:
            from holosoma.carry.checkpoints import validate
            validate(ckpt_path)
            saved=torch.load(ckpt_path,map_location='cpu',weights_only=True)
            state=saved['env_state']
            if state.get('unified_schema')!=2 or state.get('task_contract')!=self.env.task_contract():
                raise ValueError('Repaired Unified training requires a matching v2 task contract')
        result=super().load(ckpt_path)
        if ckpt_path:
            rng=saved['rng_state']
            torch.set_rng_state(rng['torch']);torch.cuda.set_rng_state_all(rng['cuda'])
            random.setstate(rng['python'])
            n=rng['numpy'];np.random.set_state((n[0],np.array(n[1],dtype=np.uint32),*n[2:]))
            self.optimizer_steps=saved['optimizer_steps']
        return result

    def load_for_evaluation(self, ckpt_path):
        # Evaluation can change reset sampling, episode limits and termination
        # display settings. It must keep the actor/control/data protocol.
        from holosoma.carry.checkpoints import validate
        validate(ckpt_path)
        saved=torch.load(ckpt_path,map_location=self.device,weights_only=True)
        state=saved['env_state'];current=self.env.get_checkpoint_state()
        if state.get('unified_schema')!=2:
            raise ValueError('Native Unified playback requires v2 checkpoint')
        for key in ('actor_dim','critic_dim','fullbody_manifest_sha256','fullbody_limits',
                    'stage1_reference_protocol','stage1_action_parameterization'):
            if state.get(key)!=current.get(key):
                raise ValueError('Playback protocol mismatch: '+key)
        control_keys=('protocol','actor_dim','critic_dim','physics','p_gains','d_gains','action_scales','action')
        for key in control_keys:
            if state['task_contract'].get(key)!=current['task_contract'].get(key):
                raise ValueError('Playback control mismatch: '+key)
        self.actor.load_state_dict(saved['actor_model_state_dict'])
        self.critic.load_state_dict(saved['critic_model_state_dict'])
        if self.empirical_normalization:
            self.actor_obs_normalizer.load_state_dict(saved['actor_obs_normalizer_state_dict'])
            self.critic_obs_normalizer.load_state_dict(saved['critic_obs_normalizer_state_dict'])
        self.current_learning_iteration=saved['iter']
        self._evaluation_only_loaded=True
        self._eval_mode()
        return saved.get('infos')

    def learn(self):
        if getattr(self,'_evaluation_only_loaded',False):
            raise ValueError('Evaluation-only load cannot resume PPO; use strict training load')
        # Only orchestration differs from PPO.learn(). Rollout, GAE, losses,
        # minibatch ordering, KL adaptation and optimizer operations are inherited.
        from holosoma.carry.checkpoints import atomic_json
        self.stop_requested=False
        def request_stop(signum,frame):
            self.stop_requested=True
        previous={sig:signal.signal(sig,request_stop) for sig in (signal.SIGINT,signal.SIGTERM)}
        self.optimizer_steps=getattr(self,'optimizer_steps',dict(actor=0,critic=0))
        originals={}
        for name in ('actor','critic'):
            optimizer=getattr(self,name+'_optimizer')
            originals[name]=optimizer.step
            def counted(*args,_name=name,**kwargs):
                result=originals[_name](*args,**kwargs)
                self.optimizer_steps[_name]+=1
                return result
            optimizer.step=counted
        self.training_status='running'
        def status():
            atomic_json(Path(self.log_dir)/'training_status.json',dict(
                status=self.training_status,completed_updates=self.current_learning_iteration+1,
                optimizer_steps=self.optimizer_steps,
                gpu_peak_allocated_bytes=torch.cuda.max_memory_allocated(),
                gpu_peak_reserved_bytes=torch.cuda.max_memory_reserved()))
        try:
            self._train_mode()
            obs_dict=self.env.reset_all()
            if self.config.init_at_random_ep_len:
                self.env.episode_length_buf=torch.randint_like(self.env.episode_length_buf,high=int(self.env.max_episode_length))
            obs_dict={k:v.to(self.device) for k,v in obs_dict.items()}
            self.logging_helper.set_run_start_learning_iteration(self.current_learning_iteration)
            first=self.current_learning_iteration
            end=first+self.config.num_learning_iterations
            for it in range(first,end):
                self.current_learning_iteration=it
                self._notify_training_step(it)
                if self.is_multi_gpu:self._synchronize_curriculum_metrics()
                with self.logging_helper.record_collection_time():
                    obs_dict=self._rollout_step(obs_dict)
                self._notify_rollout_end(it)
                with self.logging_helper.record_learn_time():
                    loss_dict=self._training_step()
                # The index becomes completed only after both optimizers finish.
                completed=it+1
                self.training_status='interrupted' if self.stop_requested else ('complete' if completed==end else 'running')
                if self.is_main_process:
                    latest=self.config.latest_save_interval>0 and completed%self.config.latest_save_interval==0
                    archive=completed%self.config.save_interval==0 or completed==end
                    if latest or archive or self.stop_requested:self.save(Path(self.log_dir)/'model.pt')
                    if archive and not self.stop_requested:
                        path=Path(self.log_dir)/f'model_{it:05d}.pt'
                        self.save(path);self.export(path.with_suffix('.onnx'))
                    # Durable completion / scheduled snapshots precede external
                    # logging so a logger cannot hide a completed optimizer update.
                    status()
                    self._post_epoch_logging(it,loss_dict)
                if self.stop_requested:
                    self.training_status='interrupted'
                    if self.is_main_process:
                        self.save(Path(self.log_dir)/'model.pt');status()
                    # A distinct exit status prevents shell evaluation after interruption.
                    raise SystemExit(130)
        finally:
            for name,step in originals.items():getattr(self,name+'_optimizer').step=step
            for sig,handler in previous.items():signal.signal(sig,handler)

    def save(self,path,infos=None):
        super().save(path,infos)
        for file in (Path(path),Path(path).with_suffix('.ready.json')):
            self.logging_helper.save_to_wandb(str(file))

    def _export_actor(self,path):
        # CarryPPO exports to a temporary name. W&B must see the final names,
        # after parity/checksums/atomic publication, rather than broken symlinks.
        upload=self.logging_helper.save_to_wandb
        self.logging_helper.save_to_wandb=lambda _:None
        try:
            super()._export_actor(path)
        finally:
            self.logging_helper.save_to_wandb=upload

    def export(self,onnx_file_path):
        super().export(onnx_file_path)
        path=Path(onnx_file_path)
        for file in (path,path.with_suffix('.actor.json'),path.with_suffix('.export.json')):
            self.logging_helper.save_to_wandb(str(file))
