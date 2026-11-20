"""Physical/command invariants independent of Kit; PPO integration checked in GPU gates."""
import json
from pathlib import Path
from types import SimpleNamespace as NS
import pytest
import torch
from holosoma.carry.fullbody_sampling import transition,sample,validate_commands
from holosoma.carry.fullbody_rewards import box_bottom

LIMITS=dict(height_low=.60688,height_high=.72688,height_rate=.11247,vx_high=.6)


def test_height_transition_full_amplitude_bounded_rate():
    start=torch.tensor([[0.,0.,0.,.72688]]).repeat(501,1)
    target=start.clone();target[:,3]=.60688
    t=torch.arange(501)*.01
    out=transition(start,target,t,LIMITS['height_rate'])
    assert (out[:,1:3]==0).all()
    assert abs(float(out[-1,3]-out[0,3])+.12)<1e-6
    assert (torch.diff(out[:,3]).abs()/.01).max()<=LIMITS['height_rate']+1e-5
    assert torch.diff(out[:,3]).max()<=0


def test_forward_height_independent_mixed_modes_and_coverage():
    torch.manual_seed(42)
    value,modes=sample(100000,2,'cpu',LIMITS)
    assert set(modes.tolist())==set(range(6))
    assert value[:,0].min()>=0 and (value[:,1:3]==0).all()
    mixed=value[modes==5]
    assert abs(torch.corrcoef(mixed[:,[0,3]].T)[0,1])<.025
    assert value[:,3].max()-value[:,3].min()>.119


def test_command_range_accepts_p0_low_and_rejects_nonforward():
    validate_commands(torch.tensor([[0.,0.,0.,.60688],[.2,0.,0.,.72688]]),LIMITS)
    for bad in [[-.1,0.,0.,.7],[0.,.1,0.,.7],[0.,0.,.1,.7],[0.,0.,0.,.5],[.7,0.,0.,.7]]:
        with pytest.raises(ValueError):validate_commands(torch.tensor([bad]),LIMITS)


def test_rotated_geometry_bottom_uses_shape_not_center_threshold():
    # A legal low pose has its full box 0.4m above ground.
    vertices=torch.tensor([[-.2,-.1,-.18],[.2,.1,.18]])
    box=torch.zeros(2,13);box[:,2]=torch.tensor([.58,.19]);box[:,3]=1 # Lab wxyz
    sim=NS(_object=NS(data=NS(root_state_w=box)),scene=NS(env_origins=torch.zeros(2,3)))
    env=NS(simulator=sim,carry_box_vertices=vertices)
    torch.testing.assert_close(box_bottom(env),torch.tensor([.4,.01]),atol=1e-6,rtol=0)


def test_original_largebox_and_control_contract():
    from holosoma.carry.fullbody_presets import g1_29dof_fullbody_carry as p
    assert p.robot.asset.urdf_file.endswith('main_mesh_collision_halfspherehand.urdf')
    assert p.robot.object.object_urdf_path.endswith('objects_largebox.urdf')
    assert p.simulator.config.sim.fps==1000 and p.simulator.config.sim.control_decimation==20
    assert not p.randomization.reset_terms and not p.randomization.step_terms
    assert p.command.setup_terms['motion_command'].params['reset_pose_file'].endswith('verified_side_grasp_reset.json')


def test_physical_acceptance_rejects_false_grip_success():
    from holosoma.carry.acceptance import physical_failures
    good=dict(survived=True,contact_continuity=1.,max_hand_slip_m=.001,min_box_clearance_m=.53,
        friction_weight_ratio_mean=.96,normal_vertical_fraction_max=.04,
        contact_height_above_bottom_min_m=.12,nonhand_box_contact_max_n=0.)
    assert not physical_failures(good)
    for field,fault in [('survived',False),('contact_continuity',.98),('max_hand_slip_m',.03),
                        ('min_box_clearance_m',.0),('friction_weight_ratio_mean',0.),
                        ('normal_vertical_fraction_max',1.),('contact_height_above_bottom_min_m',0.),
                        ('nonhand_box_contact_max_n',10.)]:
        assert physical_failures({**good,field:fault}),field


def test_no_gen_clip_end_or_state_writes():
    import inspect
    from holosoma.carry.fullbody_command import FullBodyCommand
    from holosoma.carry.fullbody_deployment import FullBodyDeploymentCommand
    # Mutating goals must be usable without constructing a reference loader.
    for method in [FullBodyCommand.step,FullBodyCommand.set_command,FullBodyDeploymentCommand.step]:
        source=inspect.getsource(method)
        assert 'set_actor_states' not in source and 'write_root' not in source
        assert '.reset(' not in source


def test_gen_continues_after_clip_end_and_height_switches_in_episode():
    from holosoma.carry.fullbody_command import FullBodyCommand
    cmd=FullBodyCommand.__new__(FullBodyCommand)
    cmd.num_envs=2;cmd.device='cpu';cmd.limits=LIMITS
    cmd._env=NS(dt=.02,episode_length_buf=torch.ones(2,dtype=torch.long))
    cmd.motion_cfg=NS(use_adaptive_timesteps_sampler=False)
    cmd.motion=NS(motion_end_idx=torch.tensor([10]));cmd.motion_ids=torch.zeros(2,dtype=torch.long)
    cmd.track_env_mask=torch.tensor([True,False]);cmd.gen_env_mask=~cmd.track_env_mask
    cmd.time_steps=torch.tensor([0,5]);cmd.dwell_remaining=torch.full((2,),1000.)
    cmd.external_command=torch.ones(2,dtype=torch.bool)
    cmd.task_command=torch.tensor([[0.,0.,0.,.72688],[0.,0.,0.,.72688]])
    cmd.command_start=cmd.task_command.clone();cmd.command_target=cmd.task_command.clone()
    cmd.command_elapsed=torch.zeros(2);cmd.height_command_rate=torch.zeros(2)
    cmd._update_track_commands=lambda:None;cmd._update_relative_reference=lambda:None
    cmd.set_command([0.,0.,0.,.60688])
    for _ in range(250):cmd.step()
    assert abs(float(cmd.task_command[1,3])-.60688)<1e-6
    assert cmd.time_steps.tolist()==[9,5]
    cmd.set_command([0.,0.,0.,.72688])
    for _ in range(250):cmd.step()
    assert abs(float(cmd.task_command[1,3])-.72688)<1e-6
    assert cmd.time_steps.tolist()==[9,5] and cmd._env.episode_length_buf.tolist()==[1,1]
