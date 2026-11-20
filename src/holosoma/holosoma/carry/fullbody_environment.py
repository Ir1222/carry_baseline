"""Carry PPO lifecycle with an explicit source/configuration resume contract."""
import json
from pathlib import Path
import torch
from holosoma.carry.environment import CarryEnv
from holosoma.carry.checkpoints import digest


class FullBodyCarryEnv(CarryEnv):
    def get_checkpoint_state(self):
        state=super().get_checkpoint_state()
        cmd=self.command_manager.get_state('motion_command')
        state['fullbody_schema']=1
        state['fullbody_limits']=cmd.limits
        state['fullbody_manifest_sha256']=digest(cmd.cfg.params['manifest_file'])
        return state

    def load_checkpoint_state(self,state):
        if not state:return
        if state.get('fullbody_schema') != 1:
            raise ValueError('Refusing a legacy palm-support checkpoint in FullBody experiment')
        cmd=self.command_manager.get_state('motion_command')
        if state['fullbody_manifest_sha256'] != digest(cmd.cfg.params['manifest_file']):
            raise ValueError('Checkpoint reference manifest differs')
        if state['fullbody_limits'] != cmd.limits:raise ValueError('Checkpoint goal curriculum configuration differs')
        super().load_checkpoint_state(state)

    def _check_termination(self):
        super()._check_termination()
        # Aggregate failures BEFORE automatic reset, not from freshly reset states.
        for name,term in self.termination_manager.last_term_results.items():
            self.log_dict['fullbody/termination_'+name]=term.float().mean()

