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
        meta.update(action_parameterization=getattr(self.env.action_manager.get_term('joint_control'),'parameterization','fixed_default_v1'),
            action_clip_value=self.env.robot_config.control.action_clip_value)
        if meta['action_parameterization']=='joint_delta_v1':
            meta['action_target_definition']='q_at_policy_step + action_scales * clipped_action; target held through PD substeps'
            meta['default_joint_pos_role']='physical observation centering only; not the PD target center'
        if getattr(cmd,'manifest',{}).get('schema')=='carry_track_training_v2':
            from holosoma.carry.checkpoints import digest
            manifest_file=Path(cmd.cfg.params['manifest_file'])
            meta.update(training_stage=1,reference_bundle_schema='carry_track_training_v2',
                reference_bundle=str(manifest_file.parent.resolve()),
                reference_manifest_sha256=digest(manifest_file),
                training_mode='Track-only joint squat/stand and forward carry')
            meta['stage1_reference_protocol']='hard_reset_post_action_v1' if hasattr(cmd,'reference_episode_step') else 'legacy_v1'
        if getattr(cmd,'manifest',{}).get('schema')=='unified_hoi_v1':
            from holosoma.carry.checkpoints import digest
            file=Path(cmd.cfg.params['manifest_file'])
            meta.update(carry_schema_version=2,unified_schema=1,actor_dim=357,critic_dim=187,
                task_modes=['pickup','carry','putdown'],task_mode_encoding='three-way one-hot appended to each physical history frame',
                reference_bundle=str(file.parent.resolve()),reference_manifest_sha256=digest(file),
                reference_bundle_schema='unified_hoi_v1',training_stage=1,reference_required_at_inference=False,
                task_mode_source_at_deployment='explicit high-level intention; no reference clock')
        session=ort.InferenceSession(str(path),providers=['CPUExecutionProvider'])
        wrapper=self.actor_onnx_wrapper
        errors=[]
        for seed in range(8):
            # Export may move a copied module; use the actual wrapper's device.
            device=next(wrapper.parameters()).device
            x=torch.tensor(np.random.default_rng(seed).normal(size=(1,getattr(self.env,'actor_dim',348))),dtype=torch.float32,device=device)
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
