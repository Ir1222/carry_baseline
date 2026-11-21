"""Separate unified experiment. No changes to existing squat/walk configuration."""
import os
from pathlib import Path
from dataclasses import replace
from holosoma.carry.stage1_presets import g1_29dof_carry_stage1_joint as base
from holosoma.config_types.observation import ObservationManagerCfg,ObsGroupCfg,ObsTermCfg
from holosoma.config_types.reward import RewardTermCfg
from holosoma.config_types.termination import TerminationTermCfg
DATA=Path(os.environ.get('HMI_UNIFIED_DATA',Path(__file__).resolve().parents[4]/'datasets/unified_hoi_v1'))
term=base.command.setup_terms['motion_command'];params={**term.params,
    'motion_config':replace(term.params['motion_config'],motion_dir=str(DATA/'motions'),start_at_timestep_zero_prob=.25),
    'manifest_file':str(DATA/'manifest.json'),'goal_limits_file':str(DATA/'goal_limits.json'),'reset_pose_file':str(DATA/'verified_side_grasp_reset.json')}
target='holosoma.carry.unified:UnifiedCommand'
rewards={**base.reward.terms}
for key,weight in [('grasp',2.),('hand_slip',.5),('pickup',1.),('putdown',1.)]:
    func={'grasp':'phase_grasp','hand_slip':'phase_slip','pickup':'pickup_reward','putdown':'putdown_reward'}[key]
    rewards[key]=RewardTermCfg(func='holosoma.carry.unified:'+func,weight=weight)
g1_29dof_unified_hoi_stage1=replace(base,env_class='holosoma.carry.unified.UnifiedCarryEnv',
    action=replace(base.action,terms={'joint_control':replace(base.action.terms['joint_control'],func='holosoma.carry.action:JointDeltaPositionActionTerm')}),
    training=replace(base.training,name='unified_hoi_stage1',num_envs=256),
    observation=ObservationManagerCfg(groups={'actor_obs':ObsGroupCfg(history_length=3,terms={'physical':ObsTermCfg(func='holosoma.carry.unified:actor_frame')}),
        'critic_obs':ObsGroupCfg(terms={'physical':ObsTermCfg(func='holosoma.carry.unified:actor_frame'),'reference':ObsTermCfg(func='holosoma.carry.observations:critic_reference')})}),
    simulator=replace(base.simulator,_target_='holosoma.carry.unified_simulator.IsaacSim'),
    algo=replace(base.algo,_target_='holosoma.carry.unified_ppo.UnifiedCarryPPO',config=replace(base.algo.config,save_interval=2000)),
    command=replace(base.command,setup_terms={'motion_command':replace(term,func=target,params=params)},
        reset_terms={'motion_command':replace(base.command.reset_terms['motion_command'],func=target)},
        step_terms={'motion_command':replace(base.command.step_terms['motion_command'],func=target)}),
    reward=replace(base.reward,terms=rewards),termination=replace(base.termination,terms={**base.termination.terms,
        'physical_failure':TerminationTermCfg(func='holosoma.carry.unified:UnifiedFailure')}),
    randomization=replace(base.randomization,setup_terms={**base.randomization.setup_terms,
        'fullbody_physics':replace(base.randomization.setup_terms['fullbody_physics'],params={'data':str(DATA)})}))
