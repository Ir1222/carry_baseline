"""Re-export a trusted FullBody checkpoint on CPU, with no simulator/reference files."""
import argparse
from pathlib import Path
import json
import os
import tempfile
import numpy as np
import torch
from torch import nn
import yaml
import onnxruntime as ort
from holosoma.agents.modules.module_utils import setup_ppo_actor_module
from holosoma.agents.ppo.ppo import EmpiricalNormalization
from holosoma.config_types.algo import ModuleConfig,LayerConfig
from holosoma.carry.checkpoints import validate,atomic_json,digest,validate_export
from holosoma.utils.inference_helpers import export_policy_as_onnx,attach_onnx_metadata


def main():
    p=argparse.ArgumentParser();p.add_argument('--checkpoint',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--config',type=Path)
    p.add_argument('--metadata',type=Path);a=p.parse_args()
    if a.output.exists():raise FileExistsError(a.output)
    info=validate(a.checkpoint)
    state=torch.load(a.checkpoint,map_location='cpu',weights_only=True)
    if state['env_state'].get('fullbody_schema')!=1:raise ValueError('Not a FullBody checkpoint')
    config=yaml.safe_load((a.config or a.checkpoint.parent/'holosoma_config.yaml').read_text())
    actor_cfg=config['algo']['config']['module_dict']['actor']
    actor_cfg['layer_config']=LayerConfig(**actor_cfg['layer_config'])
    actor=setup_ppo_actor_module({'actor_obs':348},ModuleConfig(**actor_cfg),29,.3,'cpu',{'actor_obs':3})
    actor.load_state_dict(state['actor_model_state_dict']);actor.eval()
    norm=EmpiricalNormalization(shape=348,device='cpu');norm.load_state_dict(state['actor_obs_normalizer_state_dict']);norm.eval()
    class Wrapper(nn.Module):
        def __init__(self):super().__init__();self.actor=actor;self.norm=norm
        def forward(self,actor_obs):return self.actor.act_inference({'actor_obs':self.norm(actor_obs,update=False)})
    wrapper=Wrapper().eval()
    metadata=json.loads((a.metadata or a.checkpoint.with_suffix('.actor.json')).read_text())
    if metadata.get('fullbody_schema')!=1:raise ValueError('Fullbody action metadata required')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.'+a.output.stem,suffix='.onnx',dir=a.output.parent);os.close(fd)
    temp=Path(name)
    try:
        export_policy_as_onnx(wrapper,str(temp),{'actor_obs':torch.zeros(1,348)})
        session=ort.InferenceSession(str(temp),providers=['CPUExecutionProvider']);errors=[]
        for seed in range(32):
            x=torch.tensor(np.random.default_rng(seed).normal(size=(1,348)),dtype=torch.float32)
            with torch.no_grad():expected=wrapper(x).numpy()
            actual=session.run(['action'],{'actor_obs':x.numpy()})[0]
            np.testing.assert_allclose(expected,actual,atol=2e-5,rtol=2e-5)
            errors.append(float(abs(expected-actual).max()))
        metadata.update(checkpoint_sha256=info['sha256'],onnx_parity_max_abs_error=max(errors),
            reference_required_at_inference=False,export_device='cpu')
        attach_onnx_metadata(str(temp),metadata)
        atomic_json(temp.with_suffix('.actor.json'),metadata);validate_export(temp)
        os.replace(temp,a.output);os.replace(temp.with_suffix('.actor.json'),a.output.with_suffix('.actor.json'))
        atomic_json(a.output.with_suffix('.export.json'),dict(onnx_sha256=digest(a.output),
            metadata_sha256=digest(a.output.with_suffix('.actor.json'))))
        print(json.dumps(dict(output=str(a.output),max_abs_error=max(errors),checkpoint=info)),flush=True)
    finally:
        temp.unlink(missing_ok=True);temp.with_suffix('.actor.json').unlink(missing_ok=True)


if __name__=='__main__':main()
