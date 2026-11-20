"""Atomic, checksum-verified carry checkpoints. No simulator imports."""
import hashlib
import json
import os
from pathlib import Path
import tempfile


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
    if not matrices or matrices[0].shape[1] != 348 or matrices[-1].shape[0] != 29:
        raise ValueError(f'Actor must be 348D -> 29D: {path}')
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
    if metadata.get('frame_dim') != 116 or metadata.get('history_length') != 3 or metadata.get('commands') != ['vx','vy','yaw_rate','pelvis_height']:
        raise ValueError('Incompatible Actor metadata')
    onnx.checker.check_model(str(path))
    manifest = path.with_suffix('.export.json')
    if manifest.exists():
        commit = json.loads(manifest.read_text())
        if commit['onnx_sha256'] != digest(path) or commit['metadata_sha256'] != digest(path.with_suffix('.actor.json')):
            raise ValueError('Export checksum mismatch')


def newest_valid(root, require_export=False):
    candidates = list(Path(root).rglob('model_*.pt'))
    candidates.sort(key=lambda p: (int(p.stem.split('_')[-1]), p.stat().st_mtime_ns), reverse=True)
    rejected = []
    for path in candidates:
        try:
            if require_export and not all(path.with_suffix(ext).is_file() for ext in ('.onnx', '.actor.json')):
                raise ValueError('Adjacent ONNX/metadata missing')
            if require_export:
                validate_export(path.with_suffix('.onnx'))
            return validate(path), rejected
        except Exception as error:
            rejected.append(dict(path=str(path), error=str(error)))
    raise ValueError(f'No valid full checkpoint in {root}; rejected={rejected}')
