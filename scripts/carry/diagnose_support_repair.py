"""Serial bounded old-policy physics evidence; no training or policy success gate."""
import argparse,json,subprocess,sys
from pathlib import Path
import numpy as np

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--policy",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    cases=("E_full_pick_carry_putdown","pickup_carry_boundary","carry_putdown_boundary",
           "putdown_support_probe","release_probe")
    results={}
    for case in cases:
        child=a.output/case
        argv=[sys.executable,str(Path(__file__).with_name("evaluate_unified_hoi.py")),
              "--policy",str(a.policy.resolve()),"--output",str(child.resolve()),
              "--only",case,"--seeds","2"]
        with (a.output/(case+".console.log")).open("w") as log:
            subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT,check=True)
        data=np.load(child/(case+".npz"))
        rows=[]
        for replica in range(2):
            active=data["alive"][:,replica]
            flags={}
            for key in ("legacy_loss_of_grasp","legacy_fall","legacy_body_support","legacy_drop"):
                where=np.flatnonzero(active & data[key][:,replica].astype(bool))
                flags[key]=int(data["frame"][where[0],replica]) if len(where) else None
            rows.append(dict(replica=replica,first_legacy_trigger_frames=flags,
                final_frame=int(data["frame"][np.flatnonzero(active)[-1],replica]),
                survived_after_old_trigger_is_not_physical_success=True))
        results[case]=rows
    (a.output/"diagnosis.json").write_text(json.dumps(dict(
        scope="old checkpoint diagnosis only; no initialization of repaired training",
        same_control_period_force_statistics=True,physics_dt=.001,policy_dt=.02,
        nonhand_link_order="simulator carry_other_links; per-link force vectors in rollout NPZ",
        results=results),indent=2)+"\n")

if __name__=="__main__":main()
