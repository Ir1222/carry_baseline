"""Free original LargeBox, fixed P0 physics and unsmoothed contact evidence."""
import json
from pathlib import Path
import torch
from isaaclab.sensors import ContactSensor, ContactSensorCfg
from holosoma.simulator.isaacsim.isaacsim import IsaacSim as UpstreamIsaacSim


class IsaacSim(UpstreamIsaacSim):
    def _setup_scene(self):
        super()._setup_scene()
        for side in ('left','right'):
            self.scene.sensors[side+'_box_contact']=ContactSensor(ContactSensorCfg(
                prim_path=f'/World/envs/env_.*/Robot/{side}_sphere_hand_link',
                filter_prim_paths_expr=['/World/envs/env_.*/Object/baseLink'],
                update_period=0.,history_length=1,track_contact_points=True,max_contact_data_count_per_prim=64))
        others=[name for name in self.robot_config.body_names if
                'sphere_hand' not in name and 'foot_contact_point' not in name]
        self.scene.sensors['box_other']=ContactSensor(ContactSensorCfg(
            prim_path='/World/envs/env_.*/Object/baseLink',
            filter_prim_paths_expr=[f'/World/envs/env_.*/Robot/{name}' for name in others],
            update_period=0.,history_length=1,max_contact_data_count_per_prim=128))

    def raw_contacts(self):
        normals=[]; tangents=[]
        for side in ('left','right'):
            sensor=self.scene.sensors[side+'_box_contact']
            normal=sensor.data.force_matrix_w[:,0].sum(1)
            f,_,counts,starts=sensor.contact_physx_view.get_friction_data(dt=self.sim_dt)
            if (counts >= 64).any(): raise RuntimeError('Friction contact buffer saturated')
            if len(f):
                offsets=torch.arange(64,device=f.device)
                idx=(starts.long()[...,None]+offsets).clamp(0,len(f)-1)
                tangent=torch.where((offsets<counts[...,None])[...,None],f[idx],0.).sum((1,2))
            else: tangent=torch.zeros_like(normal)
            normals.append(normal); tangents.append(tangent)
        return torch.stack(normals,1),torch.stack(tangents,1)

    def simulate_at_each_physics_step(self):
        if getattr(self,'virtual_gantry',None) and self.virtual_gantry.enabled:
            raise RuntimeError('Virtual gantry is forbidden in the free-box FullBody experiment')
        super().simulate_at_each_physics_step()
        normal,friction=self.raw_contacts()
        both=(torch.linalg.vector_norm(normal,dim=-1)>.5).all(-1).float()
        if not hasattr(self,'carry_normal'):
            self.carry_normal=torch.zeros_like(normal); self.carry_friction=torch.zeros_like(friction)
            self.carry_bilateral=torch.zeros_like(both); self.carry_substep=0
        if self.carry_substep % self.simulator_config.sim.control_decimation == 0:
            self.carry_normal.zero_(); self.carry_friction.zero_(); self.carry_bilateral.zero_()
        decimation=self.simulator_config.sim.control_decimation
        self.carry_normal+=normal/decimation; self.carry_friction+=friction/decimation
        self.carry_bilateral+=both/decimation
        self.carry_substep+=1

    def hand_box_forces(self):
        if hasattr(self,'carry_normal'): return self.carry_normal+self.carry_friction
        n,f=self.raw_contacts(); return n+f

    def clear_carry_contacts(self, ids):
        if hasattr(self,'carry_normal'):
            self.carry_normal[ids]=0; self.carry_friction[ids]=0; self.carry_bilateral[ids]=0


def fixed_physics(env, data, **_):
    import numpy as np
    from scipy.spatial import ConvexHull
    from holosoma.carry.checkpoints import atomic_json
    from holosoma.utils.path import resolve_data_file_path
    sim=env.simulator; contract=json.loads((Path(data)/'model_contract.json').read_text())
    ids=torch.arange(env.num_envs,dtype=torch.int32,device='cpu')
    for asset,material in [(sim._robot,[1.,.9,0.]),(sim._object,[.6,.6,0.])]:
        props=asset.root_physx_view.get_material_properties().clone()
        props[...,:3]=torch.tensor(material,device=props.device)
        asset.root_physx_view.set_material_properties(props,ids)
    view=sim._object.root_physx_view
    masses=view.get_masses().clone(); inertia=view.get_inertias().clone()
    inertia*=1.1/masses.reshape(-1,1); masses[:]=1.1
    view.set_masses(masses,ids); view.set_inertias(inertia,ids)
    env.carry_box_mass=masses.to(env.device).flatten()
    assert torch.allclose(env.carry_box_mass,torch.full_like(env.carry_box_mass,1.1),atol=1e-6)
    mesh=Path(resolve_data_file_path(contract['object_urdf'])).parent/'largebox.obj'
    vertices=np.array([list(map(float,line.split()[1:4])) for line in mesh.read_text().splitlines() if line.startswith('v ')])
    vertices=vertices[ConvexHull(vertices).vertices]
    env.carry_box_vertices=torch.tensor(vertices,device=env.device,dtype=torch.float32)
    env.fullbody_physics=dict(mass_kg=masses[0].tolist(),inertia=inertia[0].tolist(),
        robot_material=sim._robot.root_physx_view.get_material_properties()[0].tolist(),
        object_material=view.get_material_properties()[0].tolist(),physics_dt=env.sim_dt,policy_dt=env.dt,
        pd_hz=1/env.sim_dt,reference_fps=50,decimation=sim.simulator_config.sim.control_decimation,
        solver_robot=[16,8],torque_limits=env.torque_limits.tolist(),
        object_urdf=contract['object_urdf'],robot_urdf=contract['robot_urdf'],
        control='PPO joint-position offsets with PD each physics substep; no P0 feedforward or WBC')
