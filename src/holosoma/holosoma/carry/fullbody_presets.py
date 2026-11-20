"""Separate original-LargeBox experiment. No changes to accepted legacy carry."""
import json
import os
from pathlib import Path
from dataclasses import replace
from holosoma.carry.presets import g1_29dof_wbt_hybrid_carry as legacy
from holosoma.config_values.wbt.g1.experiment import g1_29dof_wbt_hybrid_object as original
from holosoma.config_types.command import CommandTermCfg, CommandManagerCfg
from holosoma.config_types.randomization import RandomizationManagerCfg, RandomizationTermCfg
from holosoma.config_types.reward import RewardTermCfg
from holosoma.config_types.termination import TerminationTermCfg

DATA=Path(os.environ.get('HMI_FULLBODY_DATA',Path(__file__).resolve().parents[5]/'artifacts/fullbody_goal_carry/reference_v1'))
motion=legacy.command.setup_terms['motion_command'].params['motion_config']
motion=replace(motion,motion_dir=str(DATA/'motions'),motion_file='',
    hybrid=replace(motion.hybrid,track_ratio=1.))
target='holosoma.carry.fullbody_command:FullBodyCommand'
params=dict(motion_config=motion,hold_frame=0,curriculum_level=0,
    reset_pose_file=str(DATA/'verified_side_grasp_reset.json'),
    goal_limits_file=str(DATA/'goal_limits.json'),manifest_file=str(DATA/'manifest.json'))
stiffness={k:4*v for k,v in original.robot.control.stiffness.items()}
damping={k:2*v for k,v in original.robot.control.damping.items()}
for key in ('ankle_pitch','ankle_roll'):
    stiffness[key]=max(stiffness[key],250.); damping[key]=max(damping[key],12.)
terms={k:v for k,v in legacy.reward.terms.items() if k not in
    ('velocity_tracking','yaw_tracking','height_tracking','stable_carry','hand_support','box_orientation','undesired_contacts')}
for name,weight in dict(velocity_tracking=3.,yaw_tracking=1.,height_tracking=3.,
    grasp=3.,stable_carry=1.,box_orientation=1.,hand_slip=1.,goal_compatible_style_reward=.5).items():
    terms[name]=RewardTermCfg(func='holosoma.carry.fullbody_rewards:'+name,weight=weight)
terms['nonhand_contact']=RewardTermCfg(func='holosoma.carry.fullbody_rewards:nonhand_contact',weight=-2.)
# P0 references legitimately reach waist/wrist URDF limits. Penalize actual
# limit violations rather than requiring an incompatible 10% inner margin.
terms['limits_dof_pos']=replace(terms['limits_dof_pos'],params={'soft_dof_pos_limit':1.})
termination=dict(legacy.termination.terms)
termination['physical_failure']=TerminationTermCfg(func='holosoma.carry.fullbody_termination:FullBodyFailure')
g1_29dof_fullbody_carry=replace(legacy,
    env_class='holosoma.carry.fullbody_environment.FullBodyCarryEnv',
    algo=replace(legacy.algo,_target_='holosoma.carry.fullbody_ppo.FullBodyCarryPPO'),
    training=replace(legacy.training,name='g1_fullbody_carry',num_envs=4096),
    simulator=replace(legacy.simulator,_target_='holosoma.carry.fullbody_simulator.IsaacSim',
        config=replace(legacy.simulator.config,sim=replace(legacy.simulator.config.sim,
            fps=1000,control_decimation=20,render_interval=20,max_episode_length_s=30.,
            physx=replace(legacy.simulator.config.sim.physx,num_position_iterations=16,num_velocity_iterations=8,
                min_position_iterations=8,min_velocity_iterations=4)))),
    robot=replace(original.robot,asset=replace(original.robot.asset,solver_position_iterations=16,solver_velocity_iterations=8),
        control=replace(original.robot.control,stiffness=stiffness,damping=damping)),
    command=CommandManagerCfg(setup_terms={'motion_command':CommandTermCfg(func=target,params=params)},
        reset_terms={'motion_command':CommandTermCfg(func=target)},step_terms={'motion_command':CommandTermCfg(func=target)}),
    randomization=RandomizationManagerCfg(setup_terms={
        'actuator_randomizer_state':legacy.randomization.setup_terms['actuator_randomizer_state'],
        'setup_action_delay_buffers':legacy.randomization.setup_terms['setup_action_delay_buffers'],
        'fullbody_physics':RandomizationTermCfg(func='holosoma.carry.fullbody_simulator:fixed_physics',params={'data':str(DATA)})}),
    reward=replace(legacy.reward,terms=terms),termination=replace(legacy.termination,terms=termination))
