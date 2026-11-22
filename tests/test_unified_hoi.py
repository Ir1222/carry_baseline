import json
from pathlib import Path
from types import SimpleNamespace as NS
import pytest
import torch
from holosoma.carry.unified import family_assignment,UnifiedFailure
from holosoma.carry.unified_presets import g1_29dof_unified_hoi_stage1 as cfg,DATA

def test_dataset_provenance_phase_coverage_and_immutable_squats():
    import hashlib
    m=json.loads((DATA/'manifest.json').read_text())
    assert m['schema']=='unified_hoi_v1' and len(m['motions'])==6 and not m['full_training_ready']
    for a in m['source_audits']:
        assert a['upstream_byte_identical'] and a['release_candidate_frame'] is not None
    for r in m['motions']:
        assert hashlib.sha256((DATA/r['path']).read_bytes()).hexdigest()==r['sha256']
        if r['family']=='full_sequence':assert set(r['task_modes'])=={0,1,2} and r['physics_validation']=='unvalidated'
    weights=[m['family_weights'][k] for k in ['full_sequence','loaded_locomotion','loaded_squat_stand']]
    for n in [256,1024,4096,8192]:
        ids=family_assignment(n,weights,'cpu');frac=torch.bincount(ids,minlength=3)/n
        torch.testing.assert_close(frac,torch.tensor(weights),atol=1/n,rtol=0)
    assert len(family_assignment(1,weights,'cpu'))==1
    assert cfg.command.setup_terms['motion_command'].params['motion_config'].hybrid.track_ratio==1
    assert not any('goal_compatible' in r for r in cfg.reward.terms)

def test_explicit_mode_observation_keeps_goal_and_history_without_reset():
    from holosoma.carry.unified_inference import UnifiedActor
    import numpy as np
    actor=UnifiedActor.__new__(UnifiedActor);actor.default_joint_pos=torch.zeros(29)
    actor.previous_action=torch.zeros(1,29);actor.history=torch.zeros(1,3,119)
    class Session:
        def run(self,names,inputs):
            assert inputs['actor_obs'].shape==(1,357)
            return [np.zeros((1,29),dtype=np.float32)]
    actor.session=Session();root=torch.zeros(1,13);root[:,6]=1;box=root.clone();q=torch.zeros(1,29);goal=torch.tensor([[.1,0,0,.7]])
    actor.act(root,q,q,box,goal,torch.zeros(1),0)
    actor.act(root,q,q,box,goal,torch.zeros(1),2)
    assert actor.history[0,-2,-3:].tolist()==[1.,0.,0.]
    assert actor.history[0,-1,-3:].tolist()==[0.,0.,1.]
    torch.testing.assert_close(actor.history[0,-1,-7:-3],goal[0])
    with pytest.raises(ValueError):actor.act(root,q,q,box,goal,torch.zeros(1),3)


def test_wandb_receives_only_published_verified_export_files(tmp_path,monkeypatch):
    import onnx
    from onnx import helper,TensorProto
    from holosoma.carry.unified_ppo import UnifiedCarryPPO
    from holosoma.carry.fullbody_ppo import FullBodyCarryPPO
    from holosoma.carry.checkpoints import validate_export
    files=[]
    def upload(path):
        p=Path(path);assert p.exists() and not p.name.startswith('.')
        files.append(p.name)
    algo=UnifiedCarryPPO.__new__(UnifiedCarryPPO);algo.logging_helper=NS(save_to_wandb=upload)
    def export_temporary(self,path):
        graph=helper.make_graph([helper.make_node('Constant',[],['action'],value=helper.make_tensor('zeros',TensorProto.FLOAT,[1,29],[0.]*29))],
            'test-export',[helper.make_tensor_value_info('actor_obs',TensorProto.FLOAT,[1,357])],
            [helper.make_tensor_value_info('action',TensorProto.FLOAT,[1,29])])
        onnx.save(helper.make_model(graph),path)
        Path(path).with_suffix('.actor.json').write_text(json.dumps(dict(carry_schema_version=2,unified_schema=1,frame_dim=119,history_length=3,
            commands=['vx','vy','yaw_rate','pelvis_height'],actor_dim=357,critic_dim=187,
            task_modes=['pickup','carry','putdown'],action_parameterization='joint_delta_v1')))
        self.logging_helper.save_to_wandb(path)  # reproduces the old early/temp upload
    monkeypatch.setattr(FullBodyCarryPPO,'_export_actor',export_temporary)
    path=tmp_path/'model_00001.onnx';algo.export(path);validate_export(path)
    assert files==['model_00001.onnx','model_00001.actor.json','model_00001.export.json']
