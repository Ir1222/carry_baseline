"""Upstream shared PPO, verified ONNX parity and fullbody metadata."""
import json
from pathlib import Path
import numpy as np
import torch
from holosoma.carry.ppo import CarryPPO


class FullBodyCarryPPO(CarryPPO):
    def _export_actor(self,path):
        super()._export_actor(path)
        import onnxruntime as ort
        from holosoma.utils.inference_helpers import attach_onnx_metadata
        metadata_path=Path(path).with_suffix('.actor.json')
        meta=json.loads(metadata_path.read_text())
        cmd=self.env.command_manager.get_state('motion_command')
        meta.update(fullbody_schema=1,goal_limits=cmd.limits,physics=self.env.fullbody_physics,
            reference_required_at_inference=False)
        session=ort.InferenceSession(str(path),providers=['CPUExecutionProvider'])
        wrapper=self.actor_onnx_wrapper
        errors=[]
        for seed in range(8):
            # Export may move a copied module; use the actual wrapper's device.
            device=next(wrapper.parameters()).device
            x=torch.tensor(np.random.default_rng(seed).normal(size=(1,348)),dtype=torch.float32,device=device)
            with torch.no_grad(): y=wrapper(x).cpu().numpy()
            z=session.run(['action'],{'actor_obs':x.cpu().numpy()})[0]
            np.testing.assert_allclose(y,z,atol=2e-5,rtol=2e-5)
            errors.append(float(abs(y-z).max()))
        meta['onnx_parity_max_abs_error']=max(errors)
        metadata_path.write_text(json.dumps(meta,indent=2)+'\n')
        # Upstream appends metadata. Replace its earlier entries before adding
        # the extended schema, otherwise ONNX rejects duplicate property keys.
        import onnx
        model=onnx.load(path);del model.metadata_props[:];onnx.save(model,path)
        attach_onnx_metadata(path,meta)
