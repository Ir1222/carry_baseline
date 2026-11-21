"""Immutable-reference FK comparison using the actual hemisphere and LargeBox mesh."""
import argparse
import json
from pathlib import Path
import sys
import numpy as np
from scipy.spatial.transform import Rotation


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    p.add_argument('--stride',type=int,default=20);a=p.parse_args()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    if a.output.exists():raise FileExistsError(a.output)
    repo=Path(__file__).resolve().parents[2]
    sys.path.insert(0,str(repo/'scripts/reference_synthesis'))
    from common import Kinematics,to_pin,sha
    k=Kinematics();source=repo/'src/holosoma/holosoma/data/motions/g1_29dof/whole_body_tracking'
    paths=list(sorted((repo/'datasets/fullbody_carry_track_v2/motions').glob('*.npz')))+[
        source/'movebox/sub3_largebox_003_mj_w_obj_reframed.npz',source/'sub3_largebox_003_mj_w_obj.npz']
    output=[]
    for path in paths:
        with np.load(path,allow_pickle=False) as d:
            rows=[]
            frames=sorted(set(range(0,len(d['joint_pos']),a.stride))|{len(d['joint_pos'])-1})
            for i in frames:
                q=to_pin(d['joint_pos'][i])
                k.fk(q);br=Rotation.from_quat(d['object_quat_w'][i,[1,2,3,0]])
                pos=[];axis=[];gaps=[];vertical=[]
                for side in ('left','right'):
                    hand=k.frame(side+'_sphere_hand_link')
                    local=br.inv().apply(hand.translation-d['object_pos_w'][i])
                    center=k.obb[:3,:3]@local+k.obb[:3,3]
                    tip=hand.rotation[:,2]  # Actual mesh spans local z=0..0.062m.
                    tip_obb=k.obb[:3,:3]@br.inv().apply(tip)
                    cloud=br.inv().apply(k.palm@hand.rotation.T+hand.translation-d['object_pos_w'][i])
                    sdf=(cloud@k.hull_equations[:,:3].T+k.hull_equations[:,3]).max(-1)
                    pos.append(center);axis.append(tip_obb);gaps.append(sdf.min());vertical.append(abs(tip[2]))
                rows.append(dict(center=pos,axis=axis,gap=gaps,vertical=vertical))
            center=np.array([r['center'] for r in rows]);axis=np.array([r['axis'] for r in rows])
            gap=np.array([r['gap'] for r in rows]);vertical=np.array([r['vertical'] for r in rows])
            inward=-np.sign(center[:,:,0])*axis[:,:,0]
            q=d['joint_pos'][:,7:];names=d['joint_names'].tolist()
            output.append(dict(file=str(path.relative_to(repo)),sha256=sha(path),sampled_frames=frames,
                interpretation='FK hemisphere +z geometry, not measured contact normals; convex mesh signed gap negative means penetration',
                arm_wrist_ranges={n:[float(q[:,j].min()),float(q[:,j].max())] for j,n in enumerate(names) if j>=15},
                hand_center_obb_min=center.min(0).tolist(),hand_center_obb_max=center.max(0).tolist(),
                inward_alignment_mean=inward.mean(0).tolist(),inward_alignment_min=inward.min(0).tolist(),
                palm_axis_abs_vertical_mean=vertical.mean(0).tolist(),
                hemisphere_mesh_signed_gap_min_m=gap.min(0).tolist(),hemisphere_mesh_signed_gap_max_m=gap.max(0).tolist(),
                hand_axis_opposition_dot_mean=float((axis[:,0]*axis[:,1]).sum(-1).mean())))
    a.output.write_text(json.dumps(dict(obb_size=k.obb_size.tolist(),hemisphere_bounds=[k.palm.min(0).tolist(),k.palm.max(0).tolist()],clips=output),indent=2)+'\n')
    for row in output:print(json.dumps({key:row[key] for key in ['file','inward_alignment_mean','palm_axis_abs_vertical_mean','hemisphere_mesh_signed_gap_max_m']}))


if __name__=='__main__':main()
