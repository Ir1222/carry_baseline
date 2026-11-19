"""New carry experiment. Both stages differ only in the Track/Gen partition."""
import os
from dataclasses import replace
from pathlib import Path
from holosoma.config_values.wbt.g1.experiment import g1_29dof_wbt_hybrid_object as base
from holosoma.config_values.wbt.g1.curriculum import g1_29dof_wbt_curriculum
from holosoma.config_values.wbt.g1.randomization import base_setup_terms, robot_state_dr_at_setup, object_state_dr_at_setup
from holosoma.config_values.wbt.g1.termination import g1_29dof_wbt_termination
from holosoma.config_types.command import CommandTermCfg, CommandManagerCfg, NoiseToInitialPoseConfig, StepZeroRootNoiseConfig
from holosoma.config_types.observation import ObservationManagerCfg, ObsGroupCfg, ObsTermCfg
from holosoma.config_types.reward import RewardTermCfg
from holosoma.config_types.randomization import RandomizationManagerCfg
from holosoma.config_types.termination import TerminationManagerCfg, TerminationTermCfg
from holosoma.config_types.logger import DisabledLoggerConfig

DATA = Path(os.environ.get("HMI_CARRY_DATA", Path(__file__).resolve().parents[5] / "artifacts/carry_reference_ready"))
_stiffness = {k: v*4 for k,v in base.robot.control.stiffness.items()}
_damping = {k: v*2 for k,v in base.robot.control.damping.items()}
for _joint in ("ankle_pitch", "ankle_roll"):
    _stiffness[_joint], _damping[_joint] = 300., 15.
_motion = base.command.setup_terms["motion_command"].params["motion_config"]
_motion = replace(_motion, motion_dir=str(DATA / "motions"), motion_file="",
    noise_to_initial_pose=NoiseToInitialPoseConfig(), enable_terminal_pose_hold=False,
    load_fixed_scene_from_motion=False, freeze_at_timestep_zero_prob=0.,
    hybrid=replace(_motion.hybrid, gen_start_at_timestep_zero_prob=0.,
                   gen_step_zero_root_noise=StepZeroRootNoiseConfig()))
_command = "holosoma.carry.command:CarryCommand"
_materials = {"setup_action_delay_buffers": base_setup_terms["setup_action_delay_buffers"],
              "actuator_randomizer_state": base_setup_terms["actuator_randomizer_state"]}
for _name, _term in {**robot_state_dr_at_setup, **object_state_dr_at_setup}.items():
    if "material" in _name:
        _materials[_name] = replace(_term, params={"enabled": True,
            "static_friction_range": [0.9, 0.9], "dynamic_friction_range": [0.8, 0.8], "restitution_range": [0., 0.]})
_rewards = {k: v for k, v in base.reward.terms.items() if "reached_once" not in k}
for _name, _term in list(_rewards.items()):
    if "hybrid_" in str(_term.func):
        _rewards[_name] = replace(_term, func="holosoma.carry.rewards:track_imitation",
            params={"reward_function": _term.func, **_term.params})
for _name, _weight in {"velocity_tracking": 3., "yaw_tracking": 1., "height_tracking": 1.,
                       "stable_carry": 1., "hand_support": 2., "box_orientation": .5}.items():
    _rewards[_name] = RewardTermCfg(func=f"holosoma.carry.rewards:{_name}", weight=_weight)

g1_29dof_wbt_hybrid_carry = replace(base,
    training=replace(base.training, name="g1_hybrid_carry", num_envs=256),
    logger=DisabledLoggerConfig(base_dir=str(DATA.parent / "training")),
    env_class="holosoma.carry.environment.CarryEnv",
    algo=replace(base.algo, _target_="holosoma.carry.ppo.CarryPPO",
        config=replace(base.algo.config, init_at_random_ep_len=False, save_interval=500, init_noise_std=.3)),
    simulator=replace(base.simulator, _target_="holosoma.carry.simulator.IsaacSim",
        config=replace(base.simulator.config, sim=replace(base.simulator.config.sim, max_episode_length_s=20.))),
    robot=replace(base.robot, object=replace(base.robot.object, object_urdf_path=str(DATA / "carry_box.urdf")),
        control=replace(base.robot.control, stiffness=_stiffness, damping=_damping)),
    command=CommandManagerCfg(setup_terms={"motion_command": CommandTermCfg(func=_command,
        params={"motion_config": _motion, "hold_frame": 5, "curriculum_level": 0,
                "reset_pose_file": str(DATA / "verified_reset.json")})},
        reset_terms={"motion_command": CommandTermCfg(func=_command)},
        step_terms={"motion_command": CommandTermCfg(func=_command)}),
    observation=ObservationManagerCfg(groups={
        "actor_obs": ObsGroupCfg(history_length=3, terms={"physical": ObsTermCfg(func="holosoma.carry.observations:actor_frame")}),
        "critic_obs": ObsGroupCfg(terms={"physical": ObsTermCfg(func="holosoma.carry.observations:actor_frame"),
            "reference": ObsTermCfg(func="holosoma.carry.observations:critic_reference")})}),
    reward=replace(base.reward, terms=_rewards),
    termination=TerminationManagerCfg(terms={
        "timeout": g1_29dof_wbt_termination.terms["timeout"],
        "clip_timeout": TerminationTermCfg(func="holosoma.carry.termination:clip_timeout", is_timeout=True),
        "physical_failure": TerminationTermCfg(func="holosoma.carry.termination:CarryFailure"),
        "track_failure": replace(g1_29dof_wbt_termination.terms["bad_tracking"], func="holosoma.carry.termination:TrackFailure"),
        "body_proximity": g1_29dof_wbt_termination.terms["body_proximity"]}),
    randomization=RandomizationManagerCfg(setup_terms=_materials),
    curriculum=g1_29dof_wbt_curriculum)
