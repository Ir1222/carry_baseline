"""Independent reference synthesis utilities. NPZ quaternions are wxyz; Pinocchio is xyzw."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'

import numpy as np
import pinocchio as pin
import trimesh
from scipy.spatial.transform import Rotation

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "src/holosoma/holosoma/data"
SOURCE = DATA / "motions/g1_29dof/whole_body_tracking"
ROBOT = DATA / "robots/g1/main_mesh_collision_halfspherehand.urdf"
OUTPUT = ROOT.parent / "artifacts/carry_reference_synthesized"
SIDES = ("left", "right")


def dump(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, indent=2, allow_nan=False))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    with np.load(path, allow_pickle=False) as data:
        return {k: data[k].copy() for k in data.files}


def to_pin(q):
    q = np.asarray(q).copy()
    q[..., 3:7] = q[..., [4, 5, 6, 3]]
    return q


def from_pin(q):
    q = np.asarray(q).copy()
    q[..., 3:7] = q[..., [6, 3, 4, 5]]
    return q


def angular_velocity(q, fps):
    r = Rotation.from_quat(np.asarray(q)[..., [1, 2, 3, 0]])
    a = np.maximum(np.arange(len(q)) - 1, 0)
    b = np.minimum(np.arange(len(q)) + 1, len(q) - 1)
    return (r[b] * r[a].inv()).as_rotvec() * (fps / (b - a))[:, None]


def derivative(x, fps):
    return np.gradient(x, 1 / fps, axis=0, edge_order=2)


class Kinematics:
    def __init__(self):
        self.model = pin.buildModelFromUrdf(str(ROBOT), pin.JointModelFreeFlyer())
        self.data = self.model.createData()
        self.joint_names = list(self.model.names)[2:]
        from holosoma.config_values.wbt.g1.experiment import g1_29dof_wbt_hybrid_object as base
        self.base = base
        self.body_names = list(base.robot.body_names) + [f"{s}_sphere_hand_link" for s in SIDES]
        self.ids = {n: self.model.getFrameId(self.alias(n), pin.FrameType.BODY) for n in self.body_names}
        assert max(self.ids.values()) < self.model.nframes
        self.mesh = trimesh.load(SOURCE / "largebox.obj", force="mesh")
        self.box_vertices = np.asarray(self.mesh.convex_hull.vertices)
        self.obb, self.obb_size = trimesh.bounds.oriented_bounds(self.mesh)
        from scipy.spatial import ConvexHull
        self.hull_equations = ConvexHull(self.box_vertices).equations
        torso=trimesh.load(DATA/'robots/g1/meshes/torso_link_rev_1_0.STL',force='mesh')
        self.torso_vertices=np.asarray(torso.convex_hull.vertices)
        # Conservative OBB collision constraints for every non-hand upper-body collider.
        import xml.etree.ElementTree as ET
        self.collision_clouds=[]
        tree=ET.parse(ROBOT)
        for link in tree.findall('link'):
            name=link.get('name')
            if not any(token in name for token in ['torso_link','shoulder','elbow','wrist']): continue
            fid=self.model.getFrameId(name,pin.FrameType.BODY)
            if fid>=self.model.nframes: continue
            for collision in link.findall('collision'):
                mesh=collision.find('geometry/mesh')
                if mesh is None: continue
                path=ROBOT.parent/mesh.get('filename')
                vertices=np.asarray(trimesh.load(path,force='mesh').convex_hull.vertices)
                # Deterministic spatial extremes plus uniform vertices bound the optimization cost.
                if len(vertices)>100:
                    ids=np.unique(np.r_[np.linspace(0,len(vertices)-1,80).astype(int),vertices.argmin(0),vertices.argmax(0)])
                    vertices=vertices[ids]
                origin=collision.find('origin')
                if origin is not None:
                    rpy=np.fromstring(origin.get('rpy','0 0 0'),sep=' ');xyz=np.fromstring(origin.get('xyz','0 0 0'),sep=' ')
                    vertices=Rotation.from_euler('xyz',rpy).apply(vertices)+xyz
                self.collision_clouds.append((fid,vertices))
        self.palm = np.asarray(trimesh.load(DATA / "robots/g1/meshes/half_sphere.obj", force="mesh").vertices)

    @staticmethod
    def alias(name):
        return name

    def fk(self, q):
        pin.framesForwardKinematics(self.model, self.data, q)

    def frame(self, name):
        return self.data.oMf[self.ids[name]]

    def collision_residual(self,box,br,margin=.008):
        points=[]
        for fid,vertices in self.collision_clouds:
            f=self.data.oMf[fid]
            points.append(vertices@f.rotation.T+f.translation)
        points=br.inv().apply(np.concatenate(points)-box)
        oriented=points@self.obb[:3,:3].T+self.obb[:3,3]
        signed=(np.abs(oriented)-self.obb_size/2).max(-1)
        return np.minimum(signed-margin,0.)

    def bottom(self, pos, quat):
        r = Rotation.from_quat(np.asarray(quat)[..., [1, 2, 3, 0]])
        return np.array([np.min(rr.apply(self.box_vertices)[:, 2]) + p[2] for rr, p in zip(r, pos)])

    def export(self, path, q_pin, object_pos, object_quat, fps=50):
        q_pin = np.asarray(q_pin)
        n = len(q_pin)
        pos = np.empty((n, len(self.body_names), 3))
        quat = np.empty((n, len(self.body_names), 4))
        for t, q in enumerate(q_pin):
            self.fk(q)
            for j, name in enumerate(self.body_names):
                f = self.frame(name)
                pos[t, j] = f.translation
                quat[t, j] = Rotation.from_matrix(f.rotation).as_quat()[[3, 0, 1, 2]]
        # Sign continuity prevents artificial quaternion jumps in downstream finite differences.
        for t in range(1, n):
            flip = np.sum(quat[t] * quat[t - 1], axis=-1) < 0
            quat[t, flip] *= -1
        q = from_pin(q_pin)
        out = dict(fps=np.array([fps], dtype=np.float32), joint_names=np.array(self.joint_names),
                   body_names=np.array(self.body_names), joint_pos=q,
                   joint_vel=np.column_stack([derivative(q[:, :3], fps), angular_velocity(q[:, 3:7], fps),
                                              derivative(q[:, 7:], fps)]),
                   body_pos_w=pos, body_quat_w=quat, body_lin_vel_w=derivative(pos, fps),
                   body_ang_vel_w=np.stack([angular_velocity(quat[:, i], fps) for i in range(len(self.body_names))], axis=1),
                   object_pos_w=np.asarray(object_pos), object_quat_w=np.asarray(object_quat),
                   object_lin_vel_w=derivative(object_pos, fps), object_ang_vel_w=angular_velocity(object_quat, fps))
        for k, v in out.items():
            if v.dtype.kind == "f":
                out[k] = v.astype(np.float32)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(path, **out)
        return out

    def static_torque(self, q, mass, squeeze, hand_normals,root_wrench=None):
        """Inverse statics: gravity + force exerted on box - two foot support wrenches."""
        m, d = self.model, self.data
        g = pin.computeGeneralizedGravity(m, d, q).copy()
        for s, normal in zip(SIDES, hand_normals):
            jac = pin.computeFrameJacobian(m, d, q, self.ids[f"{s}_sphere_hand_link"], pin.LOCAL_WORLD_ALIGNED)
            g += jac.T @ np.r_[squeeze * normal + [0, 0, mass * 9.81 / 2], np.zeros(3)]
        feet = np.concatenate([pin.computeFrameJacobian(m, d, q, self.ids[f"{s}_foot_contact_point"],
                                                       pin.LOCAL_WORLD_ALIGNED).copy() for s in SIDES])
        wrench = np.linalg.lstsq(feet[:, :6].T, g[:6]+(np.zeros(6) if root_wrench is None else root_wrench), rcond=None)[0]
        return (g - feet.T @ wrench)[6:], wrench
