"""Side-grasp physics and goal-compatible whole-body style, training only."""
import torch
from holosoma.carry.observations import simulator_box_state
from holosoma.carry.rewards import task_errors
from holosoma.utils.rotations import quat_apply,quat_inverse,quat_mul,quat_rotate_inverse,quat_error_magnitude,yaw_quat,quaternion_to_matrix


def box_bottom(env):
    box=simulator_box_state(env)
    # Only the z row is needed; use the actual original convex hull geometry.
    rot=quaternion_to_matrix(box[:,3:7],w_last=True)
    return box[:,2]+(rot[:,2]@env.carry_box_vertices.T).min(-1).values-env.simulator.scene.env_origins[:,2]


def relative_box(env):
    box=simulator_box_state(env); root=env.simulator.robot_root_states[:]
    q=yaw_quat(root[:,3:7],w_last=True)
    return quat_rotate_inverse(q,box[:,:3]-root[:,:3],w_last=True),quat_mul(quat_inverse(q,w_last=True),box[:,3:7],w_last=True)


def physical_metrics(env):
    sim=env.simulator
    if hasattr(sim,'carry_normal'):
        normal=sim.carry_normal; friction=sim.carry_friction
    else:
        normal,friction=sim.raw_contacts()
    mag=torch.linalg.vector_norm(normal,dim=-1)
    mass=env.carry_box_mass
    slip=[]
    box=simulator_box_state(env)
    for side in ('left','right'):
        index=sim._robot.body_names.index(side+'_sphere_hand_link')
        pos=sim._robot.data.body_pos_w[:,index]
        velocity=sim._robot.data.body_lin_vel_w[:,index]-box[:,7:10]-torch.linalg.cross(box[:,10:13],pos-box[:,:3])
        slip.append(torch.linalg.vector_norm(velocity,dim=-1))
    other=sim.scene.sensors['box_other'].data.force_matrix_w
    bottom=box_bottom(env)
    points=torch.stack([sim.scene.sensors[s+'_box_contact'].data.contact_pos_w[:,0,0] for s in ('left','right')],1)
    contact_height=points[:,:,2]-env.simulator.scene.env_origins[:,2:3]-bottom[:,None]
    contact_height=torch.nan_to_num(contact_height,nan=0.)
    vertical=(normal[:,:,2].abs()/mag.clamp_min(1e-6)).max(-1).values
    return dict(bilateral_contact=getattr(sim,'carry_bilateral',(mag>.5).all(-1).float()),
        left_hand_normal_n=mag[:,0],right_hand_normal_n=mag[:,1],
        upward_friction_weight_ratio=(-friction[:,:,2].sum(-1))/(mass*9.81),
        hand_slip_speed_m_s=torch.stack(slip,-1).max(-1).values,
        box_clearance_m=bottom,normal_vertical_fraction=vertical,
        min_contact_height_above_bottom_m=contact_height.min(-1).values,
        nonhand_box_contact_n=torch.linalg.vector_norm(other,dim=-1).sum((1,2)))


def carrying_gate(env):
    root=env.simulator.robot_root_states[:]; box=simulator_box_state(env)
    return ((box_bottom(env)>.03)&(torch.linalg.vector_norm(box[:,:3]-root[:,:3],dim=-1)<.9)).float()


def velocity_tracking(env): return torch.exp(-task_errors(env)[:,:2].square().sum(-1)/.2**2)*carrying_gate(env)
def yaw_tracking(env): return torch.exp(-task_errors(env)[:,2].square()/.3**2)*carrying_gate(env)
def height_tracking(env): return torch.exp(-task_errors(env)[:,3].square()/.05**2)*carrying_gate(env)


def grasp(env):
    m=physical_metrics(env)
    bilateral=(torch.minimum(m['left_hand_normal_n'],m['right_hand_normal_n'])/20.).clamp(0,1)
    excess=(torch.maximum(m['left_hand_normal_n'],m['right_hand_normal_n'])-45.).clamp_min(0)
    side=(m['normal_vertical_fraction']<.35)&(m['min_contact_height_above_bottom_m']>.05)
    return bilateral*side*m['upward_friction_weight_ratio'].clamp(0,1)*torch.exp(-excess.square()/30.**2)*carrying_gate(env)


def stable_carry(env):
    root=env.simulator.robot_root_states[:];box=simulator_box_state(env)
    v=box[:,7:10]-root[:,7:10]-torch.linalg.cross(root[:,10:13],box[:,:3]-root[:,:3])
    return torch.exp(-v.square().sum(-1)/.3**2)*carrying_gate(env)


def box_orientation(env):
    cmd=env.command_manager.get_state('motion_command'); pose=cmd.reset_pose
    root=torch.tensor(pose['root_xyzw'][3:7],device=env.device).expand(env.num_envs,-1)
    box=torch.tensor(pose['box_xyzw'][3:7],device=env.device).expand(env.num_envs,-1)
    desired=quat_mul(quat_inverse(yaw_quat(root,w_last=True),w_last=True),box,w_last=True)
    _,actual=relative_box(env)
    return torch.exp(-quat_error_magnitude(actual,desired,w_last=True).square()/.25**2)*carrying_gate(env)


def hand_slip(env): return torch.exp(-physical_metrics(env)['hand_slip_speed_m_s'].square()/.1**2)*carrying_gate(env)
def nonhand_contact(env): return (physical_metrics(env)['nonhand_box_contact_n']>.5).float()


def goal_compatible_style_reward(env):
    cmd=env.command_manager.get_state('motion_command')
    if not cmd.gen_env_mask.any():return torch.zeros(env.num_envs,device=env.device)
    if not hasattr(cmd,'style_bank'):
        motion=cmd.motion
        idx=torch.arange(0,motion.time_step_total,3,device=env.device)
        rootp=motion.body_pos_w[idx,0]; rootq=motion.body_quat_w[idx,0]
        v=quat_rotate_inverse(yaw_quat(rootq,w_last=True),motion.body_lin_vel_w[idx,0],w_last=True)
        cmd.style_bank=dict(idx=idx,height=rootp[:,2],vz=motion.body_lin_vel_w[idx,0,2],vx=v[:,0],
            q=motion.joint_pos[idx],qd=motion.joint_vel[idx],
            box=quat_rotate_inverse(yaw_quat(rootq,w_last=True),motion.object_pos_w[idx]-rootp,w_last=True))
        cmd.style_previous=torch.full((env.num_envs,),-1,device=env.device,dtype=torch.long)
    b=cmd.style_bank; goal=cmd.task_command; trend=cmd.height_command_rate
    h=goal[:,3]
    cost=((h[:,None]-b['height'])/.04).square()+((goal[:,0,None]-b['vx'])/.15).square()
    cost+=((trend[:,None]-b['vz'])/.06).square()
    # Same height, opposite movement direction is incompatible.
    cost+=5*((trend[:,None]*b['vz'])<-.0002).float()
    previous=cmd.style_previous
    continuity=(b['idx'][None]-(previous[:,None]+1)).abs().float().clamp_max(50)/50.
    continuity[env.episode_length_buf<=1]=0
    match=(cost+.1*continuity).argmin(-1)
    compatibility=torch.exp(-.25*cost.gather(1,match[:,None]).squeeze(1))
    qerror=(env.simulator.dof_pos-b['q'][match]).square().mean(-1)
    qd=(env.simulator.dof_vel-b['qd'][match]).square().mean(-1)
    rel,_=relative_box(env)
    boxerror=(rel-b['box'][match]).square().sum(-1)
    static=torch.exp(-qerror/.3**2-boxerror/.08**2)
    dynamic=torch.exp(-qd/2.**2)
    value=compatibility*(.8*static+.2*dynamic)*carrying_gate(env)*cmd.gen_env_mask
    cmd.style_previous=b['idx'][match]
    cmd.metrics['style/compatibility']=compatibility
    cmd.metrics['style/joint_pose_error_rad']=qerror.sqrt()
    cmd.metrics['style/matching_cost']=cost.gather(1,match[:,None]).squeeze(1)
    cmd.metrics['style/reward']=value
    return value
