"""Browser replay of measured Isaac dynamics, reference, and measured hand contact forces."""
from __future__ import annotations
import argparse
import json
import time
from pathlib import Path

import numpy as np

from common import ROBOT, SOURCE, load
from holosoma.utils.viser_helper import ViserHelper
from holosoma.utils.viser_robot import RobotAssetViser
from holosoma.utils.viser_scene import StaticUrdfViser, add_ground_grid, setup_scene_lighting


def main():
    p=argparse.ArgumentParser();p.add_argument('--evidence',type=Path,required=True);p.add_argument('--port',type=int,default=8013)
    args=p.parse_args();meta=json.loads((args.evidence/'viewer.json').read_text())
    actual=load(args.evidence/meta['actual_motion']);ref=load(meta['reference']);a=load(args.evidence/'rollout.npz');env=meta['env']
    indices=np.array(meta['sampled_physics_indices']);n=len(indices)
    v=ViserHelper(port=args.port);setup_scene_lighting(v);add_ground_grid(v)
    robot=RobotAssetViser(v,str(ROBOT),actual['body_names'].tolist(),name_prefix='/actual')
    ghost=RobotAssetViser(v,str(ROBOT),ref['body_names'].tolist(),name_prefix='/reference',color_override=(.35,.65,.9))
    box=StaticUrdfViser(v,str(SOURCE/'objects_largebox.urdf'),prefix='/actual_box',color_override=(.95,.6,.2))
    refbox=StaticUrdfViser(v,str(SOURCE/'objects_largebox.urdf'),prefix='/reference_box',color_override=(.35,.65,.9))
    scene=v.server.scene;gui=v.server.gui
    gui.add_markdown(f"**Measured Isaac Sim rollout** — {meta['status']}\n\nOrange box: actual free dynamics. Blue: reference. Contact markers/arrows: measured PhysX contacts/forces. This viewer does not run physics.")
    frame=gui.add_slider('Frame',min=0,max=n-1,step=1,initial_value=0)
    playing=gui.add_checkbox('Play',initial_value=True)
    fps=gui.add_number('Play FPS',initial_value=25.,min=1.,max=100.,step=1.)
    separate=gui.add_checkbox('Reference beside actual',initial_value=True)
    info=gui.add_text('Measured values',initial_value='',disabled=True)
    markers=[scene.add_icosphere('/contacts/'+s,radius=.009,color=c,visible=False) for s,c in [('left',(0,160,130)),('right',(220,60,90))]]
    arrows=scene.add_line_segments('/contact_forces',points=np.zeros((2,2,3),np.float32),colors=np.array([[[0,160,130]]*2,[[220,60,90]]*2],np.uint8),line_width=4.)
    last=-1;last_separate=None;clock=time.monotonic()
    print(f'Open http://localhost:{args.port}',flush=True)
    while True:
        f=int(frame.value)
        if f!=last or separate.value!=last_separate:
            j=indices[f];r=min(int(round(a.get('motion_time',a['time'])[j]*float(ref['fps'].item()))),len(ref['joint_pos'])-1)
            offset=np.array([0.,1.1 if separate.value else 0.,0.])
            robot.update(actual['body_pos_w'][f],actual['body_quat_w'][f][:,[1,2,3,0]])
            ghost.update(ref['body_pos_w'][r]+offset,ref['body_quat_w'][r][:,[1,2,3,0]])
            box.update(actual['object_pos_w'][f],actual['object_quat_w'][f,[1,2,3,0]])
            refbox.update(ref['object_pos_w'][r]+offset,ref['object_quat_w'][r,[1,2,3,0]])
            cp=a['contact_pos'][j,env];forces=-(a['normal_force_on_hand'][j,env]+a['friction_force_on_hand'][j,env]);points=np.zeros((2,2,3))
            for h,marker in enumerate(markers):
                valid=np.isfinite(cp[h]).all();marker.visible=bool(valid)
                if valid:marker.position=cp[h];points[h]=[cp[h],cp[h]+forces[h]*.003]
            arrows.points=points.astype(np.float32)
            normals=np.linalg.norm(a['normal_force_on_hand'][j,env],axis=-1)
            info.value=f"t={a['time'][j]:.2f}s | pelvis={a['root'][j,env,2]:.3f}m | box clearance={a['box_bottom'][j,env]:.3f}m | L/R normal={normals[0]:.1f}/{normals[1]:.1f}N"
            last=f
            last_separate=separate.value
        if playing.value and time.monotonic()-clock>=1/max(float(fps.value),1):
            frame.value=(f+1)%n;clock=time.monotonic()
        time.sleep(.005)


if __name__=='__main__':main()
