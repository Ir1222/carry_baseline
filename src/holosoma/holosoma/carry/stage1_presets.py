"""One uninterrupted HMI Track PPO run, jointly learning squat/stand and walking."""
import os
from dataclasses import replace
from pathlib import Path
from holosoma.carry.fullbody_presets import g1_29dof_fullbody_carry as physical
from holosoma.config_values.wbt.g1.reward import g1_29dof_wbt_reward_w_object as hmi_tracking
from holosoma.config_types.reward import RewardTermCfg

DATA=Path(os.environ.get('HMI_STAGE1_DATA',Path(__file__).resolve().parents[4]/'datasets/fullbody_carry_track_v2'))
ACTION_MODE=os.environ.get('HMI_CARRY_ACTION_MODE','joint_delta')
if ACTION_MODE not in ('fixed','joint_delta'):raise ValueError('HMI_CARRY_ACTION_MODE must be fixed or joint_delta')
action=physical.action
if ACTION_MODE=='joint_delta':
    action=replace(action,terms={**action.terms,'joint_control':replace(action.terms['joint_control'],
        func='holosoma.carry.action:JointDeltaPositionActionTerm')})
term=physical.command.setup_terms['motion_command'];motion=term.params['motion_config']
motion=replace(motion,motion_dir=str(DATA/'motions'),motion_file='',start_at_timestep_zero_prob=.5,
    hybrid=replace(motion.hybrid,track_ratio=1.))
target='holosoma.carry.stage1_command:Stage1TrackCommand'
params={**term.params,'motion_config':motion,'reset_pose_file':str(DATA/'verified_side_grasp_reset.json'),
    'manifest_file':str(DATA/'manifest.json'),'goal_limits_file':str(DATA/'goal_limits.json')}
rewards={k:v for k,v in hmi_tracking.terms.items() if k!='undesired_contacts'}
rewards['limits_dof_pos']=replace(rewards['limits_dof_pos'],params={'soft_dof_pos_limit':1.})
rewards.update(grasp=RewardTermCfg(func='holosoma.carry.fullbody_rewards:grasp',weight=2.),
    hand_slip=RewardTermCfg(func='holosoma.carry.fullbody_rewards:hand_slip',weight=.5),
    nonhand_contact=RewardTermCfg(func='holosoma.carry.fullbody_rewards:nonhand_contact',weight=-2.))
g1_29dof_carry_stage1_joint=replace(physical,
    action=action,
    env_class='holosoma.carry.stage1_environment.Stage1CarryEnv',
    training=replace(physical.training,name='stage1_joint_squat_walk',num_envs=8192),
    algo=replace(physical.algo,config=replace(physical.algo.config,num_learning_iterations=15000,
        save_interval=2000,latest_save_interval=100,num_mini_batches=4)),
    command=replace(physical.command,setup_terms={'motion_command':replace(term,func=target,params=params)},
        reset_terms={'motion_command':replace(physical.command.reset_terms['motion_command'],func=target)},
        step_terms={'motion_command':replace(physical.command.step_terms['motion_command'],func=target)}),
    randomization=replace(physical.randomization,setup_terms={**physical.randomization.setup_terms,
        'fullbody_physics':replace(physical.randomization.setup_terms['fullbody_physics'],params={'data':str(DATA)})}),
    reward=replace(physical.reward,terms=rewards))
