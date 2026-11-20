"""Fault injection against a real passed rollout: pose animation alone must never pass."""
import argparse
import json
from types import SimpleNamespace

import numpy as np

from common import Kinematics, dump, load
from metrics import summarize


def main():
    from pathlib import Path
    p=argparse.ArgumentParser();p.add_argument('--evidence',type=Path,required=True);p.add_argument('--motion',type=Path,required=True)
    args=p.parse_args();a=load(args.evidence/'rollout.npz');k=Kinematics();entries=json.loads((args.evidence/'candidates.json').read_text())
    dt=float(a['time'][1]-a['time'][0]);cfg=SimpleNamespace(dt=dt,motion=args.motion)
    limits=np.array(k.base.robot.dof_effort_limit_list)
    def evaluate(arr):return summarize(arr,entries,limits,k,cfg)['results'][0]
    base=evaluate(a);assert base['status']=='Physics validated',base
    cases=[]
    def case(name,mutate,expected):
        b={key:value.copy() for key,value in a.items()};mutate(b);r=evaluate(b)
        assert r['status']=='Physics validation failed' and expected in r['failures'],(name,r)
        cases.append(dict(name=name,expected_failure=expected,detected=True))
    case('Airborne box poses with no friction',lambda b:b['friction_force_on_hand'].fill(0),'insufficient_friction_support')
    def lost_hand(b):b['normal_force_on_hand'][len(a['time'])//2:len(a['time'])//2+int(.1/dt),0,0]=0
    case('Left hand detached for 100ms',lost_hand,'contact_interruption')
    case('Box touches ground',lambda b:b['box_bottom'].__setitem__((len(a['time'])//2,0),0.),'box_ground_clearance')
    case('Torso supports carton',lambda b:b['other_box_normal'].__setitem__((1000,0,0,2),5.),'max_other_box_contact_n')
    case('Foot slides 5cm',lambda b:b['foot_pos'].__setitem__((slice(len(a['time'])//2,None),0,0,0),b['foot_pos'][0,0,0,0]+.05),'max_foot_slip_m')
    case('Joint exceeds mechanical limit',lambda b:b['joint_pos'].__setitem__((1000,0,0),20.),'max_joint_limit_violation_rad')
    case('No actual squat despite reference motion',lambda b:b['root'].__setitem__((slice(None),0,2),b['root'][0,0,2]),'insufficient_squat_excursion')
    dump(args.evidence/'acceptance_fault_injection.json',dict(real_rollout_passed=True,tests=cases,passed=len(cases)))
    print(f'{len(cases)} fault injections rejected; real rollout passed')


if __name__=='__main__':main()
