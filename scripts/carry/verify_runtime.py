"""Read-only verification of the dedicated runtime; no package changes."""
import importlib.metadata as metadata
import json
from pathlib import Path
import subprocess
import sys
import torch
import holosoma

root = Path(__file__).resolve().parents[2]
assert sys.version_info[:2] == (3,11)
assert Path(sys.prefix).resolve() == (root.parent/'envs/g1_hmi_carry').resolve()
assert torch.__version__ == '2.7.0+cu128' and torch.version.cuda == '12.8'
assert torch.cuda.is_available()
assert Path(next(iter(holosoma.__path__))).resolve().is_relative_to(root)
for package, version in {'isaacsim':'5.1.0.0','isaaclab':'0.47.2','warp-lang':'1.10.0','tyro':'1.0.12'}.items():
    assert metadata.version(package) == version, (package,metadata.version(package))
commit = subprocess.check_output(['git','-C',str(root.parent/'IsaacLab'),'rev-parse','HEAD'],text=True).strip()
assert commit == '3c6e67bb5c7ada942a6d1884ab69338f57596f77'
result = subprocess.run([sys.executable,'-m','pip','check'],text=True,capture_output=True)
allowed = set((root/'scripts/carry/p0_pip_check.txt').read_text().strip().splitlines())
conflicts = set(result.stdout.strip().splitlines()) if result.returncode else set()
assert not conflicts-allowed, result.stdout+result.stderr
x = torch.randn(128,128,device='cuda'); assert torch.isfinite(x@x).all()
print(json.dumps(dict(passed=True,python=sys.version,environment=sys.prefix,torch=torch.__version__,
    cuda=torch.version.cuda,gpu=torch.cuda.get_device_name(),isaaclab_commit=commit,
    acknowledged_upstream_metadata_conflicts=sorted(conflicts)),indent=2))
