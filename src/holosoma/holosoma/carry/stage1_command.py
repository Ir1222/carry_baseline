"""Stage1 exclusively imitates sampled robot/object references; Gen is forbidden."""
import torch
from holosoma.carry.fullbody_command import FullBodyCommand
from holosoma.managers.command.terms.wbt import MotionCommand


class Stage1TrackCommand(FullBodyCommand):
    def _sample_motion_ids_for_reset(self,env_ids):
        rows=sorted(self.manifest['motions'],key=lambda r:r['name'])
        weights=self._weights()
        for family,parity in [('squat_stand',0),('forward_carry',1)]:
            ids=env_ids[env_ids%2==parity]
            if not ids.numel():continue
            allowed=torch.tensor([r['family']==family for r in rows],device=self.device)
            self.motion_ids[ids]=torch.multinomial(weights*allowed,len(ids),replacement=True)

    def _sample_adaptive_reset_states(self,env_ids,group_ids):
        self._sample_motion_ids_for_reset(env_ids)
        mids=self.motion_ids[env_ids].clone();bins=torch.empty_like(mids);times=torch.empty_like(mids)
        for motion in range(self.motion.num_motions):
            mask=mids==motion;n=int(mask.sum())
            if n:
                if (group_ids[mask]!=0).any():raise RuntimeError('Only Track adaptive group is allowed in Stage1')
                _,bins[mask],times[mask]=self.adaptive_timesteps_sampler.sample_from_motion_pool(
                    0,torch.tensor([motion],device=self.device),n)
        return mids,bins,times

    def setup(self):
        if self.manifest.get('schema')!='carry_track_training_v2' or {
            r.get('family') for r in self.manifest['motions']}!={'squat_stand','forward_carry'}:
            raise ValueError('Joint Stage1 requires both squat/stand and forward-carry targets')
        if self.motion_cfg.hybrid.track_ratio!=1.:
            raise ValueError('Joint Stage1 requires track_ratio=1; Gen is not part of this task')
        super().setup()
        if self.gen_env_mask.any() or not self.track_env_mask.all():
            raise ValueError('Stage1 partition must contain only Track environments')

    def sample_gen_commands(self,ids):
        if ids.numel():raise RuntimeError('Stage1 must never sample random Gen goals')

    def set_command(self,*args,**kwargs):
        raise RuntimeError('Stage1 uses reference-derived commands; external Gen goals require Stage2')

    def step(self):
        if self.motion_cfg.use_adaptive_timesteps_sampler:
            self._increment_adaptive_sampler_global_env_step()
        active=self._env.episode_length_buf>0
        self.time_steps[active]=torch.minimum(self.time_steps[active]+1,
            self.motion.motion_end_idx[self.motion_ids[active]]-1)
        self.last_clip_end_env_ids=torch.empty(0,dtype=torch.long,device=self.device)
        self._update_track_commands()
        self._update_relative_reference()

    def on_training_step(self,training_step,**kwargs):
        # Keep the original HMI adaptive sampler hooks, with no Gen curriculum.
        MotionCommand.on_training_step(self,training_step,**kwargs)

    def update_metrics(self):
        super().update_metrics()
        rows=sorted(self.manifest['motions'],key=lambda r:r['name'])
        for i,row in enumerate(rows):
            self.metrics['track/motion_fraction_'+row['name']]=(self.motion_ids==i).float()
        for family in ('squat_stand','forward_carry'):
            ids=torch.tensor([i for i,r in enumerate(rows) if r['family']==family],device=self.device)
            self.metrics['track/family_fraction_'+family]=torch.isin(self.motion_ids,ids).float()
        self.metrics['track/env_fraction']=self.track_env_mask.float()
        self.metrics['track/gen_env_fraction']=self.gen_env_mask.float()
