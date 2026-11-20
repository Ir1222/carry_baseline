"""Read the actual imported USD geometry and MeshCollisionAPI, including Xform colliders."""
import argparse
import json
from pathlib import Path


def main():
    p=argparse.ArgumentParser();p.add_argument('--evidence',type=Path,required=True);args=p.parse_args()
    from isaaclab.app import AppLauncher
    app=AppLauncher(headless=True,device='cuda:0').app
    try:
        from pxr import Usd,UsdGeom,UsdPhysics
        import numpy as np
        result={}
        for kind,file in [('box','box/objects_largebox.usd'),('robot','robot/main_mesh_collision_halfspherehand.usd')]:
            stage=Usd.Stage.Open(str((args.evidence/'imports'/file).resolve()));items=[]
            for prim in Usd.PrimRange(stage.GetPseudoRoot(),Usd.TraverseInstanceProxies()):
                rec=dict(path=str(prim.GetPath()),type=prim.GetTypeName(),collision_api=prim.HasAPI(UsdPhysics.CollisionAPI))
                if prim.GetTypeName()=='Mesh':
                    points=np.array(UsdGeom.Mesh(prim).GetPointsAttr().Get())
                    rec.update(points=len(points),bounds=[points.min(0).tolist(),points.max(0).tolist()],
                        asset_transform=np.array(UsdGeom.Xformable(prim).ComputeLocalToWorldTransform(Usd.TimeCode.Default())).tolist())
                if rec['collision_api']:
                    rec.update(approximation=UsdPhysics.MeshCollisionAPI(prim).GetApproximationAttr().Get() if prim.HasAPI(UsdPhysics.MeshCollisionAPI) else None,
                        collision_enabled=UsdPhysics.CollisionAPI(prim).GetCollisionEnabledAttr().Get())
                if rec['type']=='Mesh' or rec['collision_api']:items.append(rec)
            result[kind]=items
        (args.evidence/'import_geometry_audit.json').write_text(json.dumps(result,indent=2))
        print('Saved',args.evidence/'import_geometry_audit.json',flush=True)
    except BaseException:
        import traceback
        print(traceback.format_exc(),flush=True)
        raise
    finally:
        app.close(wait_for_replicator=False)


if __name__=='__main__':main()
