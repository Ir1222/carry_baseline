"""Isaac Sim with separate, object-filtered hand contact force sensors."""
from isaaclab.sensors import ContactSensor, ContactSensorCfg
from holosoma.simulator.isaacsim.isaacsim import IsaacSim


class CarryIsaacSim(IsaacSim):
    def _setup_scene(self):
        super()._setup_scene()
        for side in ("left", "right"):
            cfg = ContactSensorCfg(
                prim_path=f"/World/envs/env_.*/Robot/{side}_wrist_yaw_link",
                filter_prim_paths_expr=["/World/envs/env_.*/Object/baseLink"],
                update_period=0.0,
                history_length=3,
                debug_vis=False,
            )
            self.scene.sensors[f"{side}_box_contact"] = ContactSensor(cfg)

    def hand_box_forces(self):
        import torch
        # Each sensor has exactly one robot body and one object filter per env.
        return torch.stack([
            self.scene.sensors[f"{side}_box_contact"].data.force_matrix_w[:, 0].sum(dim=1)
            for side in ("left", "right")
        ], dim=1)
