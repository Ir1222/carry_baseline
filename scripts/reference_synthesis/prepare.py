"""Audit immutable HMI sources; optimize whole-body side-grasp standing candidates."""
from __future__ import annotations

import argparse
import itertools
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pinocchio as pin
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation

from common import DATA, OUTPUT, ROBOT, ROOT, SIDES, SOURCE, Kinematics, dump, from_pin, load, sha, to_pin


def audit(k, output):
    paths = [SOURCE / "movebox" / f"sub3_largebox_003_mj_w_obj_reframed{s}.npz" for s in ("", "_mirrored")]
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in paths + [ROBOT, SOURCE / "objects_largebox.urdf", SOURCE / "largebox.obj",
                                                               DATA / "robots/g1/meshes/half_sphere.obj"]}
    protected = [ROOT / "src/holosoma/holosoma" / s for s in
                 ("carry/ppo.py", "carry/command.py", "carry/environment.py", "carry/presets.py", "carry/rewards.py",
                  "config_values/wbt/g1/experiment.py", "config_values/wbt/g1/randomization.py")]
    dump(output / "immutable_sources.json", hashes)
    dump(output / "protected_training_files.json", {str(p.relative_to(ROOT)): sha(p) for p in protected})
    summaries = []
    for path in paths:
        d = load(path); n = len(d["joint_pos"]); names = d["body_names"].tolist()
        hp = np.zeros((n, 2, 3)); handbox = np.zeros_like(hp); fkerr = []
        for i, qp in enumerate(to_pin(d["joint_pos"])):
            k.fk(qp)
            br = Rotation.from_quat(d["object_quat_w"][i, [1, 2, 3, 0]])
            for h, s in enumerate(SIDES):
                hp[i, h] = k.frame(f"{s}_sphere_hand_link").translation
                handbox[i, h] = br.inv().apply(hp[i, h] - d["object_pos_w"][i])
            fkerr.append(max(np.linalg.norm(k.frame(name).translation - d["body_pos_w"][i, names.index(name)])
                             for name in k.body_names if name in names))
        bottom = k.bottom(d["object_pos_w"], d["object_quat_w"])
        pelvis = d["body_pos_w"][:, names.index("pelvis"), 2]
        np.savez_compressed(output / f"audit_{path.stem}.npz", pelvis_z=pelvis, box_bottom=bottom,
                            palm_pos_w=hp, palm_pos_box=handbox, original_common_body_fk_error=fkerr)
        summary = dict(source=str(path.relative_to(ROOT)), frames=n, fps=float(d["fps"].item()),
                       common_body_fk_error_max_m=float(max(fkerr)), ranges=[])
        for start, stop in [(54, 96), (95, 205), (205, 255)]:
            summary["ranges"].append(dict(frames_inclusive=[start, stop-1], pelvis_height_m=[float(pelvis[start:stop].min()), float(pelvis[start:stop].max())],
                box_bottom_m=[float(bottom[start:stop].min()), float(bottom[start:stop].max())],
                palm_in_box_min=handbox[start:stop].min(0).tolist(), palm_in_box_max=handbox[start:stop].max(0).tolist()))
        summaries.append(summary)
        # Exact original crop. Preserve every original robot/object field; append only missing FK body aliases.
        crop = {key: value[95:205].copy() if value.ndim and value.shape[0] == n else value.copy() for key, value in d.items()}
        source_crop=output/'source_crops'
        source_crop.mkdir(exist_ok=True)
        np.savez_compressed(source_crop/path.name,**crop)
        fps = float(d["fps"].item())
        filename = "original_forward_carry" + ("_mirrored" if "mirrored" in path.name else "") + ".npz"
        # Retain the full original q/object trajectory; regenerate collision-model body FK and derivatives.
        # The bit-exact original crop is saved separately above for provenance.
        k.export(output/'motions_kinematic'/filename,to_pin(d['joint_pos'][95:205]),
                 d['object_pos_w'][95:205],d['object_quat_w'][95:205],fps)
    dump(output / "source_audit.json", dict(sources=summaries, box_bounds=k.mesh.bounds.tolist(),
        palm_bounds=[k.palm.min(0).tolist(), k.palm.max(0).tolist()],
        urdf_box_mass_kg=0.1, upstream_mass_randomization=dict(operation="add",range_kg=[1,4],actual_range_kg=[1.1,4.1]),
        fixed_parameters=dict(mass_kg=1.1, inertia_scale_from_urdf=11, robot_friction=[1.0,0.9],box_friction=[0.6,0.6], restitution=0.0),
        oriented_box_size_m=k.obb_size.tolist(),
        note="The original mesh has rotated/slanted side faces. AABB overlap is not a valid contact test. Raw source body transforms differ from the collision URDF by up to the reported FK error; canonical exports regenerate body FK while retaining full source joints/root/object motion. Raw crops are bit-exact in source_crops/."))


def solve_hold(k, frame=140, box_x=.36, box_z=.80, squeeze_depth=.001, yaw=np.pi/2, stance=.13):
    d = load(SOURCE / "movebox/sub3_largebox_003_mj_w_obj_reframed.npz")
    source = to_pin(d["joint_pos"][frame]); seed = source[7:].copy()
    height = float(source[2])
    # Root and all 29 joints are optimized. Feet have fixed poses; palms face opposing box side faces.
    box = np.array([box_x, 0., box_z])
    # The raw mesh's principal side faces are rotated relative to its local XYZ.
    # Level the actual carton, retaining its exact vertices/scale, not its axis-aligned bounds.
    br = Rotation.from_matrix(Rotation.from_euler('z',yaw).as_matrix()@k.obb[:3,:3])
    targets = []
    inward = []
    for side, sign in zip(SIDES, [1.,-1.]):
        outward_local=sign*k.obb[0,:3]
        outward = br.apply(outward_local); inward.append(-outward)
        zaxis = -outward
        xaxis = np.array([1.,0.,0.]); yaxis = np.cross(zaxis, xaxis)
        hr = np.column_stack([xaxis, yaxis, zaxis])
        # Use exact mesh support and hemisphere tip; hand contact stays on the side, above the bottom.
        center=np.linalg.inv(k.obb)@np.array([0.,0.,-.06,1.])
        eq=k.hull_equations
        den=eq[:,:3]@outward_local
        intersections=-(eq[:,:3]@center[:3]+eq[:,3])/np.where(abs(den)>1e-9,den,np.nan)
        distance=np.nanmin(intersections[den>1e-9])
        face = box + br.apply(center[:3]+distance*outward_local)
        base = face + outward * (np.max(k.palm @ hr.T @ (-outward)) - squeeze_depth)
        targets.append(pin.SE3(hr, base))
    foot_targets = [pin.SE3(np.eye(3), np.array([0., sign * stance, .037])) for sign in [1,-1]]
    x0 = np.r_[0.,0.,0.,0.,0.,seed]
    x0[5:17] = np.array([-.25,.05,0.,.55,-.3,-.05,-.25,-.05,0.,.55,-.3,.05])
    lower = np.r_[-.15,-.10,-.08,-.12,-.08,k.model.lowerPositionLimit[7:]+1e-4]
    upper = np.r_[.15,.10,.08,.12,.08,k.model.upperPositionLimit[7:]-1e-4]
    def unpack(x):
        return np.r_[x[:2],height,Rotation.from_euler("xyz",x[2:5]).as_quat(),x[5:]]
    def residual(x):
        q = unpack(x); k.fk(q); res=[]
        for s,t in zip(SIDES,foot_targets):
            f=k.frame(f"{s}_ankle_roll_link")
            res.extend(100*(f.translation-t.translation)); res.extend(15*pin.log3(t.rotation.T@f.rotation))
        for s,t in zip(SIDES,targets):
            f=k.frame(f"{s}_sphere_hand_link")
            res.extend(100*(f.translation-t.translation)); res.extend(8*pin.log3(t.rotation.T@f.rotation))
        com=pin.centerOfMass(k.model,k.data,q); total=sum(i.mass for i in k.model.inertias)
        combined=(total*com+1.1*box)/(total+1.1)
        res.extend(20*(combined[:2]-np.array([.025,0.])))
        res.extend(150*k.collision_residual(box,br))
        res.extend(.12*(x[5:]-seed)); res.extend(3.*x[2:5])
        return np.array(res)
    fit=least_squares(residual,np.clip(x0,lower+1e-6,upper-1e-6),bounds=(lower,upper),max_nfev=180,ftol=1e-9,xtol=1e-9,gtol=1e-7)
    q=unpack(fit.x); k.fk(q)
    errors={s:float(np.linalg.norm(k.frame(f"{s}_sphere_hand_link").translation-t.translation)) for s,t in zip(SIDES,targets)}
    return q,box,br.as_quat()[[3,0,1,2]],dict(source_frame=frame,box_x=box_x,box_z=box_z,yaw=yaw,stance=stance,
        squeeze_depth_m=squeeze_depth,optimizer_cost=float(fit.cost),optimizer_success=bool(fit.success),palm_error_m=errors,
        inward_normals=np.array(inward).tolist(),foot_targets=[t.translation.tolist() for t in foot_targets])


def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,default=OUTPUT)
    p.add_argument('--frames',type=int,nargs='+',default=[95,140]);p.add_argument('--box-x',type=float,nargs='+',default=[.32,.38])
    p.add_argument('--box-z',type=float,nargs='+',default=[.78,.84]);p.add_argument('--penetrations',type=float,nargs='+',default=[.001,.004])
    args=p.parse_args();args.output=args.output.resolve()
    args.output.mkdir(parents=True,exist_ok=False)
    for name in ['motions_kinematic','candidates','evidence','figures','assets','validated_motions']:
        (args.output/name).mkdir()
    k=Kinematics(); audit(k,args.output)
    entries=[]
    for i,(frame,x,z,penetration) in enumerate(itertools.product(args.frames,args.box_x,args.box_z,args.penetrations)):
        q,box,bq,meta=solve_hold(k,frame,x,z,penetration)
        meta['id']=f'hold_{i:03d}'; meta['q_pin']=q.tolist(); meta['box_wxyz']=np.r_[box,bq].tolist()
        entries.append(meta)
        k.export(args.output/'candidates'/f"{meta['id']}.npz",np.tile(q,(101,1)),np.tile(box,(101,1)),np.tile(bq,(101,1)))
        print(meta['id'],meta['optimizer_cost'],meta['palm_error_m'],flush=True)
    dump(args.output/'hold_candidates.json',entries)
    print('Prepared',args.output,flush=True)


if __name__ == '__main__':
    main()
