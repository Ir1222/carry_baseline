"""Standalone Isaac Lab free-object validation; no PPO/command/reward imports at runtime.

Box and robot state writes occur only in reset_trial(). All subsequent actuation is joint torque.
Filtered PhysX normal and friction forces are logged separately at EVERY physics step.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("OMNI_KIT_ACCEPT_EULA", "1")
os.environ.setdefault("PYTHONNOUSERSITE", "1")


def arguments():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True, help='Fresh evidence directory; never overwritten')
    p.add_argument('--candidates', type=Path)
    p.add_argument('--motion', type=Path)
    p.add_argument('--duration', type=float, default=2.)
    p.add_argument('--squeezes', type=float, nargs='+', default=[8.,16.])
    p.add_argument('--gain', type=float, default=4.)
    p.add_argument('--balance', type=float, default=.2)
    p.add_argument('--dt', type=float, default=.001)
    p.add_argument('--view', action='store_true')
    p.add_argument('--reset-state', type=Path)
    p.add_argument('--max-candidates', type=int, default=1000)
    p.add_argument('--wbc',action='store_true',help='Joint-only inverse-statics foot-wrench feedback for root tracking')
    p.add_argument('--warmup-seconds',type=float,default=2.,help='Motion trials first establish stable grasp in the SAME episode')
    return p.parse_args()


def main():
    args = arguments()
    args.output=args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=False)
    import shutil
    for source in Path(__file__).parent.glob('*.py'):
        destination=args.output/'source_snapshot'/source.name
        destination.parent.mkdir(exist_ok=True)
        shutil.copyfile(source,destination)
    # Pinocchio/eigenpy must register their C++ vector bindings before Kit loads its Boost.Python.
    from common import Kinematics
    k=Kinematics()
    from isaaclab.app import AppLauncher
    launcher = AppLauncher(headless=not args.view, device='cuda:0', enable_cameras=False)
    app = launcher.app
    try:
        run(args,k)
    except BaseException:
        import traceback
        error=traceback.format_exc()
        (args.output/'exception.txt').write_text(error)
        print(error,flush=True)
        raise
    finally:
        from isaaclab.sim import SimulationContext
        context=SimulationContext.instance()
        if context is not None:
            context._disable_app_control_on_stop_handle=True
        app.close(wait_for_replicator=False)


def run(args,k):
    import numpy as np
    import torch
    import isaaclab.sim as su
    from isaaclab.assets import Articulation, ArticulationCfg, RigidObject, RigidObjectCfg
    from isaaclab.actuators import IdealPDActuatorCfg
    from isaaclab.scene import InteractiveScene, InteractiveSceneCfg
    from isaaclab.sensors import ContactSensor, ContactSensorCfg
    from isaaclab.sim import SimulationContext, SimulationCfg, PhysxCfg
    from pxr import Usd, UsdGeom, UsdPhysics, PhysxSchema
    import pinocchio as pin
    from scipy.spatial.transform import Rotation
    from common import DATA, OUTPUT, ROBOT, SIDES, SOURCE, Kinematics, dump, from_pin, load, to_pin

    torch.manual_seed(0); np.random.seed(0)
    base=k.base.robot
    if args.candidates:
        candidates=json.loads(args.candidates.read_text())[:args.max_candidates]
        entries=[dict(**c,squeeze_n=s) for c in candidates for s in args.squeezes]
        motion=None
    elif args.motion:
        motion=load(args.motion)
        if not args.reset_state:
            raise ValueError('A squat motion requires an independently passed stable side-grasp reset state')
        reset=json.loads(args.reset_state.read_text())
        assert reset['status']=='Physics validated' and reset['validation_scope']=='standing side-grasp hold'
        meta=reset['candidate']
        entries=[dict(**meta)]
        args.duration=(len(motion['joint_pos'])-1)/float(motion['fps'].item())
    else:
        raise ValueError('Supply --candidates or --motion')
    n=len(entries); device='cuda:0'
    dt=args.dt; mass=1.1
    sim=SimulationContext(SimulationCfg(dt=dt,render_interval=4,device=device,
        physx=PhysxCfg(solver_type=1,min_position_iteration_count=8,max_position_iteration_count=16,
            min_velocity_iteration_count=4,max_velocity_iteration_count=8,gpu_max_rigid_patch_count=10*2**15),
        physics_material=su.RigidBodyMaterialCfg(static_friction=1.,dynamic_friction=.9,restitution=0.,friction_combine_mode='average')))
    scene=InteractiveScene(InteractiveSceneCfg(num_envs=n,env_spacing=3.,replicate_physics=True))
    su.GroundPlaneCfg(physics_material=su.RigidBodyMaterialCfg(static_friction=1.,dynamic_friction=.9,restitution=0.)).func('/World/ground',su.GroundPlaneCfg(physics_material=su.RigidBodyMaterialCfg(static_friction=1.,dynamic_friction=.9,restitution=0.)))
    gains=su.UrdfConverterCfg.JointDriveCfg(target_type='none',gains=su.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(stiffness=0.,damping=0.))
    acts={name:IdealPDActuatorCfg(joint_names_expr=[name],effort_limit=base.dof_effort_limit_list[i],
        velocity_limit=base.dof_vel_limit_list[i],stiffness=0.,damping=0.,armature=base.dof_armature_list[i],
        friction=base.dof_joint_friction_list[i]) for i,name in enumerate(k.joint_names)}
    robot=Articulation(ArticulationCfg(prim_path='/World/envs/env_.*/Robot',
        spawn=su.UrdfFileCfg(asset_path=str(ROBOT),usd_dir=str(args.output/'imports/robot'),fix_base=False,
            merge_fixed_joints=True,replace_cylinders_with_capsules=True,activate_contact_sensors=True,joint_drive=gains,
            rigid_props=su.RigidBodyPropertiesCfg(disable_gravity=False,linear_damping=0.,angular_damping=0.,max_depenetration_velocity=1.),
            articulation_props=su.ArticulationRootPropertiesCfg(enabled_self_collisions=True,solver_position_iteration_count=16,solver_velocity_iteration_count=8)),
        init_state=ArticulationCfg.InitialStateCfg(pos=(0.,0.,.74),joint_pos={'.*':0.},joint_vel={'.*':0.}),
        soft_joint_pos_limit_factor=1.,actuators=acts))
    scene.articulations['robot']=robot
    box=RigidObject(RigidObjectCfg(prim_path='/World/envs/env_.*/Object',
        spawn=su.UrdfFileCfg(asset_path=str(SOURCE/'objects_largebox.urdf'),usd_dir=str(args.output/'imports/box'),fix_base=False,
            activate_contact_sensors=True,joint_drive=gains,
            rigid_props=su.RigidBodyPropertiesCfg(disable_gravity=False,linear_damping=.01,angular_damping=.01,max_depenetration_velocity=1.)),
        init_state=RigidObjectCfg.InitialStateCfg(pos=(0.,0.,.8))))
    scene.rigid_objects['object']=box
    for s in SIDES:
        scene.sensors[s]=ContactSensor(ContactSensorCfg(prim_path=f'/World/envs/env_.*/Robot/{s}_sphere_hand_link',
            filter_prim_paths_expr=['/World/envs/env_.*/Object/baseLink'],update_period=0.,history_length=1,
            max_contact_data_count_per_prim=128,track_contact_points=True))
    scene.sensors['box_other']=ContactSensor(ContactSensorCfg(prim_path='/World/envs/env_.*/Object/baseLink',
        filter_prim_paths_expr=[f'/World/envs/env_.*/Robot/{name}' for name in base.body_names if 'foot_contact_point' not in name],
        update_period=0.,history_length=1,max_contact_data_count_per_prim=128))
    for s in SIDES:
        scene.sensors[s+'_foot']=ContactSensor(ContactSensorCfg(prim_path=f'/World/envs/env_.*/Robot/{s}_ankle_roll_link',
            update_period=0.,history_length=1,max_contact_data_count_per_prim=128))
    scene.clone_environments(copy_from_source=False)
    scene.filter_collisions(global_prim_paths=['/World/ground'])
    light=su.DomeLightCfg(intensity=2200.); light.func('/World/light',light)
    sim.set_camera_view(eye=(2.,2.,1.5),target=(.2,0.,.6))
    sim.reset(); scene.update(dt)
    cpuids=torch.arange(n,dtype=torch.int32,device='cpu')
    for asset,friction in [(robot,[1.,.9,0.]),(box,[.6,.6,0.])]:
        material=asset.root_physx_view.get_material_properties().clone()
        material[...,:3]=torch.tensor(friction,dtype=material.dtype,device=material.device)
        asset.root_physx_view.set_material_properties(material,cpuids)
    masses=box.root_physx_view.get_masses().clone(); imported_mass=masses.clone()
    inertia=box.root_physx_view.get_inertias().clone(); imported_inertia=inertia.clone()
    inertia *= mass/masses
    masses[:]=mass
    box.root_physx_view.set_masses(masses,cpuids)
    box.root_physx_view.set_inertias(inertia,cpuids)
    ji=torch.tensor([robot.joint_names.index(name) for name in k.joint_names],device=device)
    bi=[robot.body_names.index(f'{s}_sphere_hand_link') for s in SIDES]
    fi=[robot.body_names.index(f'{s}_ankle_roll_link') for s in SIDES]
    desired_q=np.array([e['q_pin'] for e in entries])
    initial_box=np.array([e['box_wxyz'] for e in entries])
    squeezes=np.array([e['squeeze_n'] for e in entries])
    inward=np.array([e['inward_normals'] for e in entries])
    kp=np.array([next(v for key,v in base.control.stiffness.items() if key in name) for name in k.joint_names])*args.gain
    kd=np.array([next(v for key,v in base.control.damping.items() if key in name) for name in k.joint_names])*args.gain**.5
    for i,name in enumerate(k.joint_names):
        if 'ankle' in name: kp[i]=max(kp[i],250.);kd[i]=max(kd[i],12.)
    limits=np.array(base.dof_effort_limit_list)
    tau_ff=np.array([k.static_torque(q,mass,s,hn)[0] for q,s,hn in zip(desired_q,squeezes,inward)])
    positions=np.array([q[:3] for q in desired_q])
    offsets=scene.env_origins.cpu().numpy()
    tensor=lambda a: torch.tensor(a,dtype=torch.float32,device=device)
    kpt,kdt,lt=tensor(kp),tensor(kd),tensor(limits)

    def reset_trial():
        root=robot.data.default_root_state.clone()
        root[:,:3]=tensor(positions)+scene.env_origins
        root[:,3:7]=tensor(desired_q[:,[6,3,4,5]])
        root[:,7:]=0
        qj=robot.data.default_joint_pos.clone();qj[:,ji]=tensor(desired_q[:,7:])
        robot.write_root_state_to_sim(root)
        robot.write_joint_state_to_sim(qj,torch.zeros_like(qj))
        obj=box.data.default_root_state.clone();obj[:,:3]=tensor(initial_box[:,:3])+scene.env_origins
        obj[:,3:7]=tensor(initial_box[:,3:7]);obj[:,7:]=0
        box.write_root_state_to_sim(obj)
        scene.reset();scene.update(dt)
    reset_trial()
    def forbidden_state_write(*unused,**kwargs):
        raise RuntimeError('Forbidden root/object state write after episode reset')
    for asset in [robot,box]:
        for method in ['write_root_state_to_sim','write_root_pose_to_sim','write_root_velocity_to_sim']:
            setattr(asset,method,forbidden_state_write)
    # Audit BEFORE rollout, including USD-authored flags and actual PhysX tensors.
    prims=[];rigid_prims=[]
    for p in Usd.PrimRange(sim.stage.GetPrimAtPath('/World/envs/env_0'),Usd.TraverseInstanceProxies()):
        if p.HasAPI(UsdPhysics.CollisionAPI):
            prims.append(dict(path=str(p.GetPath()),enabled=UsdPhysics.CollisionAPI(p).GetCollisionEnabledAttr().Get(),
                approximation=UsdPhysics.MeshCollisionAPI(p).GetApproximationAttr().Get() if p.HasAPI(UsdPhysics.MeshCollisionAPI) else 'primitive',
                contact_offset=PhysxSchema.PhysxCollisionAPI(p).GetContactOffsetAttr().Get(),
                rest_offset=PhysxSchema.PhysxCollisionAPI(p).GetRestOffsetAttr().Get(),
                local_extent=str(UsdGeom.Boundable(p).GetExtentAttr().Get()) if p.IsA(UsdGeom.Boundable) else None))
        if p.HasAPI(UsdPhysics.RigidBodyAPI):
            rigid_prims.append(dict(path=str(p.GetPath()),kinematic=UsdPhysics.RigidBodyAPI(p).GetKinematicEnabledAttr().Get(),
                rigid_enabled=UsdPhysics.RigidBodyAPI(p).GetRigidBodyEnabledAttr().Get(),
                disable_gravity=PhysxSchema.PhysxRigidBodyAPI(p).GetDisableGravityAttr().Get()))
    materials=[]
    for p in sim.stage.Traverse():
        if p.HasAPI(UsdPhysics.MaterialAPI):
            mat=UsdPhysics.MaterialAPI(p);px=PhysxSchema.PhysxMaterialAPI(p)
            materials.append(dict(path=str(p.GetPath()),static_friction=mat.GetStaticFrictionAttr().Get(),dynamic_friction=mat.GetDynamicFrictionAttr().Get(),
                restitution=mat.GetRestitutionAttr().Get(),friction_combine_mode=px.GetFrictionCombineModeAttr().Get(),
                compliant_stiffness=p.GetAttribute('physxMaterial:compliantContactStiffness').Get() if p.HasAttribute('physxMaterial:compliantContactStiffness') else None,
                compliant_damping=p.GetAttribute('physxMaterial:compliantContactDamping').Get() if p.HasAttribute('physxMaterial:compliantContactDamping') else None))
    object_body=sim.stage.GetPrimAtPath('/World/envs/env_0/Object/baseLink')
    object_flags=dict(kinematic=UsdPhysics.RigidBodyAPI(object_body).GetKinematicEnabledAttr().Get(),
        rigid_body_enabled=UsdPhysics.RigidBodyAPI(object_body).GetRigidBodyEnabledAttr().Get(),
        disable_gravity=PhysxSchema.PhysxRigidBodyAPI(object_body).GetDisableGravityAttr().Get())
    assert not object_flags['kinematic'] and not object_flags['disable_gravity'] and object_flags['rigid_body_enabled']
    dump(args.output/'physics_model.json',dict(dt=sim.get_physics_dt(),gravity=list(sim.cfg.gravity),num_envs=n,
        robot_urdf=str(ROBOT),object_urdf=str(SOURCE/'objects_largebox.urdf'),
        imported_box_mass_kg=imported_mass.tolist(),actual_box_mass_kg=box.root_physx_view.get_masses().tolist(),
        imported_box_inertia=imported_inertia.tolist(),actual_box_inertia=box.root_physx_view.get_inertias().tolist(),
        robot_material=robot.root_physx_view.get_material_properties()[0].tolist(),
        box_material=box.root_physx_view.get_material_properties()[0].tolist(),
        robot_body_masses=robot.root_physx_view.get_masses()[0].tolist(),body_names=robot.body_names,
        joint_names=k.joint_names,sim_joint_names=robot.joint_names,kp=kp.tolist(),kd=kd.tolist(),torque_limits=limits.tolist(),
        collider_prims=prims,rigid_body_prims=rigid_prims,usd_materials=materials,
        control='joint torque PD + inverse statics; optional inverse-statics foot-wrench root feedback; optional ankle feedback',
        no_root_or_object_writes_after_reset=True,runtime_state_write_guards=True,box_free_dynamic=True,hidden_supports=False,
        actual_object_rigid_body_flags=object_flags,wbc_enabled=args.wbc,balance_gain=args.balance,gain_scale=args.gain,
        authored_scene_joints=[str(p.GetPath()) for p in Usd.PrimRange(sim.stage.GetPrimAtPath('/World/envs/env_0')) if p.IsA(UsdPhysics.Joint)]))
    dump(args.output/'candidates.json',entries)
    warmup=args.warmup_seconds if motion is not None else 0.
    records=[]; steps=int(round((args.duration+warmup)/dt)); side_sensors=[scene.sensors[s] for s in SIDES]
    phase_idx=0
    for step in range(steps):
        elapsed=step*dt
        time=max(0.,elapsed-warmup)
        if motion is not None and warmup and step==int(round(warmup/dt)):
            recent=records[-int(round(1./dt)):]
            nf=np.array([r['normal_force_on_hand'][0] for r in recent])
            compression=-np.sum(nf*inward[0][None],axis=-1)
            drift=np.array([r['hand_local'][0]-recent[0]['hand_local'][0] for r in recent])
            upright=np.array([r['root'][0] for r in recent])
            tilt=np.linalg.norm(Rotation.from_quat(upright[:,[4,5,6,3]]).as_euler('xyz')[:,:2],axis=-1)
            gate=dict(contact_fraction=(compression>.5).mean(0).tolist(),max_hand_drift_m=float(np.linalg.norm(drift,axis=-1).max()),
                min_clearance_m=float(min(r['box_bottom'][0] for r in recent)),max_tilt_rad=float(tilt.max()),
                max_other_contact_n=float(max(np.linalg.norm(r['other_box_normal'][0],axis=-1).max() for r in recent)),
                final_box_speed_m_s=float(np.linalg.norm(recent[-1]['object'][0,7:10])),warmup_seconds=warmup)
            gate['passed']=bool(min(gate['contact_fraction'])>=.99 and gate['max_hand_drift_m']<=.025 and
                gate['min_clearance_m']>=.03 and gate['max_tilt_rad']<=.25 and gate['max_other_contact_n']<=.5 and gate['final_box_speed_m_s']<=.12)
            dump(args.output/'pre_motion_gate.json',gate)
            if not gate['passed']:
                print('Pre-motion stable grasp gate FAILED; squat not started',gate,flush=True)
                break
        if motion is not None:
            mi=min(int(round(time*float(motion['fps'].item()))),len(motion['joint_pos'])-1)
            target=to_pin(motion['joint_pos'][mi:mi+1])
            desired_q[:]=target
            target_vel=motion['joint_vel'][mi,6:][None]
            # Full-body reference torque changes with pose; the box itself receives no actuation.
            if step%4==0:
                tau_ff=np.array([k.static_torque(target[0],mass,squeezes[0],inward[0])[0]])
        else:
            target_vel=np.zeros((n,29))
        q=robot.data.joint_pos[:,ji];qd=robot.data.joint_vel[:,ji]
        tau=kpt*(tensor(desired_q[:,7:])-q)+kdt*(tensor(target_vel)-qd)+tensor(tau_ff)
        root=robot.data.root_state_w
        rpy=Rotation.from_quat(root[:,[4,5,6,3]].cpu().numpy()).as_euler('xyz')
        pos=root[:,:3].cpu().numpy()-offsets
        vel=root[:,7:10].cpu().numpy()
        omega=root[:,10:13].cpu().numpy()
        # Balance feedback acts only through ankle joints, bounded by original motor limits.
        target_pos=desired_q[:,:3]
        target_rpy=Rotation.from_quat(desired_q[:,3:7]).as_euler('xyz')
        if args.wbc:
            feedback_torques=[]
            for eidx in range(n):
                ar=Rotation.from_quat(root[eidx,[4,5,6,3]].cpu().numpy())
                rr=Rotation.from_quat(desired_q[eidx,3:7])
                target_v=motion['joint_vel'][mi,:3] if motion is not None else np.zeros(3)
                total_mass=sum(inertia.mass for inertia in k.model.inertias)+mass
                force=total_mass*(np.array([25.,25.,80.])*(target_pos[eidx]-pos[eidx])+np.array([10.,10.,15.])*(target_v-vel[eidx]))
                moment=100.*(rr*ar.inv()).as_rotvec()-12.*omega[eidx]
                feedback=np.r_[ar.inv().apply(force),ar.inv().apply(moment)]
                actual_q=np.r_[pos[eidx],ar.as_quat(),q[eidx].cpu().numpy()]
                feedback_torques.append(k.static_torque(actual_q,mass,squeezes[eidx],inward[eidx],feedback)[0])
            tau=kpt*(tensor(desired_q[:,7:])-q)+kdt*(tensor(target_vel)-qd)+tensor(np.array(feedback_torques))
        for s in SIDES:
            for axis,joint in [(0,'roll'),(1,'pitch')]:
                j=k.joint_names.index(f'{s}_ankle_{joint}_joint')
                feedback=(.9*(rpy[:,axis]-target_rpy[:,axis])+.12*omega[:,axis])
                if joint=='pitch': feedback += .5*(pos[:,0]-target_pos[:,0])+.15*vel[:,0]
                else: feedback -= .5*(pos[:,1]-target_pos[:,1])+.15*vel[:,1]
                tau[:,j]+=args.balance*kpt[j]*tensor(feedback)
        tau=torch.maximum(torch.minimum(tau,lt),-lt)
        all_tau=torch.zeros_like(robot.data.joint_pos);all_tau[:,ji]=tau
        robot.set_joint_effort_target(all_tau)
        scene.write_data_to_sim();sim.step(render=args.view);scene.update(dt)
        normal=[];friction=[];contact=[];counts_list=[]
        for sensor in side_sensors:
            sensor.update(dt,force_recompute=True)
            normal.append(sensor.data.force_matrix_w[:,0,0].clone())
            f,_,counts,starts=sensor.contact_physx_view.get_friction_data(dt=dt)
            counts=counts.long();starts=starts.long()
            if (counts>=128).any(): raise RuntimeError('Friction sensor buffer saturated')
            idx=torch.arange(128,device=device)
            if len(f):
                indices=(starts[...,None]+idx).clamp(0,len(f)-1)
                friction.append(torch.where((idx<counts[...,None])[...,None],f[indices],0.).sum(dim=(1,2)))
            else: friction.append(torch.zeros((n,3),device=device))
            contact.append(sensor.data.contact_pos_w[:,0,0].clone())
            counts_list.append(counts[:,0])
        nr=torch.stack(normal,dim=1).cpu().numpy();fr=torch.stack(friction,dim=1).cpu().numpy()
        root=robot.data.root_state_w.cpu().numpy().copy();root[:,:3]-=offsets
        obj=box.data.root_state_w.cpu().numpy().copy();obj[:,:3]-=offsets
        hp=robot.data.body_pos_w[:,bi].cpu().numpy()-offsets[:,None]
        hq=robot.data.body_quat_w[:,bi].cpu().numpy()
        foot=robot.data.body_pos_w[:,fi].cpu().numpy()-offsets[:,None]
        cp=torch.stack(contact,dim=1).cpu().numpy()-offsets[:,None]
        hand_local=np.stack([Rotation.from_quat(obj[:,[4,5,6,3]]).inv().apply(hp[:,j]-obj[:,:3]) for j in range(2)],axis=1)
        bottom=k.bottom(obj[:,:3],obj[:,3:7])
        other=scene.sensors['box_other'].data.force_matrix_w[:,0].cpu().numpy()
        foot_forces=np.stack([scene.sensors[s+'_foot'].data.net_forces_w[:,0].cpu().numpy() for s in SIDES],axis=1)
        row=dict(time=(step+1)*dt,motion_time=max(0.,(step+1)*dt-warmup),root=root,object=obj,joint_pos=robot.data.joint_pos[:,ji].cpu().numpy(),
            joint_vel=robot.data.joint_vel[:,ji].cpu().numpy(),torque=robot.data.applied_torque[:,ji].cpu().numpy(),
            commanded_torque=tau.cpu().numpy(),
            target_joint_pos=desired_q[:,7:].copy(),target_root=desired_q[:,:7].copy(),
            normal_force_on_hand=nr,friction_force_on_hand=fr,hand_pos=hp,hand_quat=hq,contact_pos=cp,
            hand_local=hand_local,box_bottom=bottom,other_box_normal=other,foot_pos=foot,foot_normal=foot_forces,
            friction_contact_count=torch.stack(counts_list,dim=1).cpu().numpy(),
            box_net_normal=scene.sensors['box_other'].data.net_forces_w[:,0].cpu().numpy())
        records.append(row)
        if step%100==0:
            print('step',step,'root min/max',float(root[:,2].min()),float(root[:,2].max()),'box min/max',float(bottom.min()),float(bottom.max()),flush=True)
    arrays={key:np.array([r[key] for r in records]) for key in records[0]}
    np.savez_compressed(args.output/'rollout.npz',**arrays)
    # Full episode raw data are retained even for failures. A small initial transient is reported separately.
    from metrics import summarize
    results=summarize(arrays,entries,limits,k,args)
    dump(args.output/'validation.json',results)
    print(json.dumps(results['summary'],indent=2),flush=True)


if __name__=='__main__':
    main()
