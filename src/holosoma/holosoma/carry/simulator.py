"""Isaac Sim with separate, object-filtered hand contact force sensors."""
from isaaclab.sensors import ContactSensor, ContactSensorCfg
from holosoma.simulator.isaacsim.isaacsim import IsaacSim as UpstreamIsaacSim


class IsaacSim(UpstreamIsaacSim):
    def _setup_scene(self):
        super()._setup_scene()
        for side in ("left", "right"):
            cfg = ContactSensorCfg(
                prim_path=f"/World/envs/env_.*/Robot/{side}_sphere_hand_link",
                filter_prim_paths_expr=["/World/envs/env_.*/Object/baseLink"],
                update_period=0.0,
                history_length=3,
                max_contact_data_count_per_prim=64,
                debug_vis=False,
            )
            self.scene.sensors[f"{side}_box_contact"] = ContactSensor(cfg)

    def hand_box_forces(self):
        import torch
        # Isaac Lab's force_matrix_w contains NORMAL forces only. Side grips
        # support the box through tangential friction, which must be included.
        results = []
        for side in ("left", "right"):
            sensor = self.scene.sensors[f"{side}_box_contact"]
            normal = sensor.data.force_matrix_w[:, 0].sum(dim=1)
            friction, _, counts, starts = sensor.contact_physx_view.get_friction_data(dt=self.sim_dt)
            counts, starts = counts.long(), starts.long()
            offsets = torch.arange(64, device=friction.device)
            if (counts > 64).any():
                raise RuntimeError("Hand-box friction contact capacity exceeded")
            indices = (starts[..., None]+offsets).clamp(0, len(friction)-1)
            values = friction[indices]
            tangent = torch.where((offsets < counts[..., None])[..., None], values, 0.).sum(dim=(1, 2))
            results.append(normal+tangent)
        return torch.stack(results, dim=1)
