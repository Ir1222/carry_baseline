from isaaclab.sensors import ContactSensor,ContactSensorCfg
from holosoma.carry.fullbody_simulator import IsaacSim as CarryIsaacSim

class IsaacSim(CarryIsaacSim):
    def _setup_scene(self):
        super()._setup_scene()
        from pxr import Usd,UsdPhysics
        self.hoi_ground_filter_paths=[str(p.GetPath()) for p in Usd.PrimRange(self.sim.stage.GetPrimAtPath('/World/ground')) if p.HasAPI(UsdPhysics.CollisionAPI)]
        if not self.hoi_ground_filter_paths:raise ValueError('No real ground collision prim found; support transfer sensor cannot be configured')
        self.scene.sensors['box_ground']=ContactSensor(ContactSensorCfg(prim_path='/World/envs/env_.*/Object/baseLink',
            filter_prim_paths_expr=self.hoi_ground_filter_paths,update_period=0.,history_length=1,max_contact_data_count_per_prim=128))
