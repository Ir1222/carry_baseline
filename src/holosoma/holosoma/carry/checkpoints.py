"""Atomic, checksum-verified carry checkpoints. No simulator imports."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
from holosoma.carry.support import PRIVILEGED_FIELDS
UNIFIED_CRITIC_DIM=119+68+len(PRIVILEGED_FIELDS)


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.' + path.name, dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(value, f, indent=2, allow_nan=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
        dfd = os.open(path.parent, os.O_DIRECTORY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for data in iter(lambda: f.read(1024 * 1024), b''):
            h.update(data)
    return h.hexdigest()


def finite_tree(value):
    import math
    import torch
    if isinstance(value, torch.Tensor):
        return bool(torch.isfinite(value).all())
    if isinstance(value, dict):
        return all(finite_tree(v) for v in value.values())
    if isinstance(value, (tuple, list)):
        return all(finite_tree(v) for v in value)
    return not isinstance(value, float) or math.isfinite(value)


def validate(path, require_manifest=True):
    """Load trusted local weights on CPU and reject incomplete/nonfinite PPO state."""
    import torch
    path = Path(path)
    stat = path.stat()
    checksum = digest(path)
    sidecar = path.with_suffix('.ready.json')
    if require_manifest:
        manifest = json.loads(sidecar.read_text())
        if manifest['sha256'] != checksum or manifest['bytes'] != stat.st_size:
            raise ValueError(f'Checkpoint checksum mismatch: {path}')
    state = torch.load(path, map_location='cpu', weights_only=True)
    for key in ('actor_model_state_dict', 'critic_model_state_dict',
                'actor_optimizer_state_dict', 'critic_optimizer_state_dict'):
        if not state.get(key):
            raise ValueError(f'Missing full PPO state {key}: {path}')
    for key in ('actor_optimizer_state_dict', 'critic_optimizer_state_dict'):
        if not state[key].get('state') or not state[key].get('param_groups'):
            raise ValueError(f'Empty optimizer: {path}')
    for key in ('actor_obs_normalizer_state_dict', 'critic_obs_normalizer_state_dict'):
        if not state.get(key):
            raise ValueError(f'Missing normalization: {path}')
    if state.get('env_state', {}).get('carry_schema_version') != 1:
        raise ValueError(f'Incompatible carry schema: {path}')
    if not isinstance(state.get('iter'), int) or state['iter'] < 0 or not finite_tree(state):
        raise ValueError(f'Invalid iteration or nonfinite checkpoint: {path}')
    matrices = [v for v in state['actor_model_state_dict'].values()
                if isinstance(v, torch.Tensor) and v.ndim == 2]
    expected=357 if state.get('env_state',{}).get('unified_schema') in (1,2) else 348
    if not matrices or matrices[0].shape[1] != expected or matrices[-1].shape[0] != 29:
        raise ValueError(f'Actor must be {expected}D -> 29D: {path}')
    schema=state.get('env_state',{}).get('unified_schema')
    if schema:
        expected_critic=187 if schema==1 else UNIFIED_CRITIC_DIM if schema==2 else None
        matrices=[v for v in state['critic_model_state_dict'].values() if isinstance(v,torch.Tensor) and v.ndim==2]
        if not matrices or matrices[0].shape[1]!=expected_critic:
            raise ValueError('Incompatible privileged critic schema')
        if schema==2 and state.get('completed_updates')!=state['iter']+1:
            raise ValueError('Incomplete completed-update accounting')
        if schema==2 and not state['env_state'].get('task_contract'):
            raise ValueError('Missing repaired task contract')
    if path.stat().st_mtime_ns != stat.st_mtime_ns or path.stat().st_size != stat.st_size:
        raise ValueError(f'Checkpoint changed during validation: {path}')
    return dict(path=str(path.resolve()), sha256=checksum, bytes=stat.st_size,
                iteration=state['iter'], completed_updates=state['iter'] + 1,
                curriculum_level=state['env_state']['carry_level'])


def atomic_save(state, path):
    import torch
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.' + path.name, suffix='.partial', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            torch.save(state, f)
            f.flush()
            os.fsync(f.fileno())
        # Validate before publishing; a sidecar is the commit record.
        info = validate(tmp, require_manifest=False)
        os.replace(tmp, path)
        info['path'] = str(path.resolve())
        atomic_json(path.with_suffix('.ready.json'), info)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def validate_export(path):
    import onnx
    path = Path(path)
    metadata = json.loads(path.with_suffix('.actor.json').read_text())
    if metadata.get('unified_schema') not in (None,1,2):raise ValueError('Unknown unified export schema')
    if metadata.get('unified_schema')==2 and metadata.get('support_protocol')!='measured_support_v2':raise ValueError('Missing measured support protocol')
    expected=119 if metadata.get('unified_schema') in (1,2) else 116
    if metadata.get('frame_dim') != expected or metadata.get('history_length') != 3 or metadata.get('commands') != ['vx','vy','yaw_rate','pelvis_height']:
        raise ValueError('Incompatible Actor metadata')
    if metadata.get('unified_schema') in (1,2) and (metadata.get('carry_schema_version')!=2 or metadata.get('actor_dim')!=357
        or metadata.get('critic_dim')!=(187 if metadata.get('unified_schema')==1 else UNIFIED_CRITIC_DIM) or metadata.get('task_modes')!=['pickup','carry','putdown']
        or metadata.get('action_parameterization')!='joint_delta_v1'):
        raise ValueError('Incompatible unified task-mode/action metadata')
    onnx.checker.check_model(str(path))
    manifest = path.with_suffix('.export.json')
    if manifest.exists():
        commit = json.loads(manifest.read_text())
        if commit['onnx_sha256'] != digest(path) or commit['metadata_sha256'] != digest(path.with_suffix('.actor.json')):
            raise ValueError('Export checksum mismatch')


def newest_valid(root, require_export=False):
    candidates = set(Path(root).rglob('model_*.pt')) | set(Path(root).rglob('model.pt'))
    rejected = []
    valid = []
    for path in candidates:
        try:
            info=validate(path)
            if require_export:
                validate_export(path.with_suffix('.onnx'))
            valid.append(info)
        except Exception as error:
            rejected.append(dict(path=str(path), error=str(error)))
    if valid:
        # The verified internal completed count is authoritative. Latest wins ties.
        return max(valid,key=lambda x:(x['completed_updates'],Path(x['path']).name=='model.pt')),rejected
    raise ValueError(f'No valid full checkpoint in {root}; rejected={rejected}')
