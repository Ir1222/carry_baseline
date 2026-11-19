#!/usr/bin/env bash
set -euo pipefail
TASK_ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../.." && pwd)
TASK_ENV="$TASK_ROOT/envs/g1_hmi_carry"
source /home/han/miniconda3/etc/profile.d/conda.sh
conda activate "$TASK_ENV"
export PATH="$TASK_ENV/bin:$PATH"
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV
hash -r
unset LD_LIBRARY_PATH
export PYTHONNOUSERSITE=1
test "$(git -C "$TASK_ROOT/IsaacLab" rev-parse HEAD)" = 3c6e67bb5c7ada942a6d1884ab69338f57596f77
git -C "$TASK_ROOT/HMI" merge-base --is-ancestor c353731999b3578c41ad5a00f896415b45e6a9f5 HEAD
# Remove every inherited editable link inside the new environment only.
"$TASK_ENV/bin/python" - <<'PY'
import json, subprocess, sys
items=json.loads(subprocess.check_output([sys.executable,'-m','pip','list','--editable','--format=json']))
print('Removing inherited editable registrations:',items,flush=True)
if items:
    subprocess.run([sys.executable,'-m','pip','uninstall','-y',*[x['name'] for x in items]],check=True)
PY
# This is exactly the flatdict compatibility fix in HMI's pinned setup script.
"$TASK_ENV/bin/python" - "$TASK_ROOT/IsaacLab/source/isaaclab/setup.py" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]);s=p.read_text()
assert 'flatdict==4.0.1' in s or 'flatdict==4.1.0' in s
p.write_text(s.replace('flatdict==4.0.1','flatdict==4.1.0'))
PY
export PIP_CONSTRAINT="$TASK_ROOT/HMI/scripts/constraints-isaacsim-5.1.txt"
export PIP_BUILD_CONSTRAINT="$PIP_CONSTRAINT"
export CMAKE_POLICY_VERSION_MINIMUM=3.5
export OMNI_KIT_ACCEPT_EULA=1
export TERM=xterm
"$TASK_ENV/bin/python" -m pip install 'setuptools<81' 'wheel==0.45.1'
LAB_PACKAGES=()
for package in "$TASK_ROOT"/IsaacLab/source/*; do
    if [ -f "$package/setup.py" ] || [ -f "$package/pyproject.toml" ]; then
        LAB_PACKAGES+=(-e "$package")
    fi
done
# HMI owns its PPO; physical robot bridge SDK extras are not required for simulation.
"$TASK_ENV/bin/python" -m pip install "${LAB_PACKAGES[@]}" -e "$TASK_ROOT/HMI/src/holosoma" \
  'transformers==5.5.0' 'huggingface-hub==1.9.0' 'ipython==9.10.1' \
  'pytest==9.0.2' 'skrl==1.4.3' 'stable-baselines3==2.8.0' 'ray==2.52.1' \
  'typer==0.24.1' 'chardet==5.2.0' 'charset-normalizer==3.3.2' \
  'click==8.2.1' 'packaging==23.0' 'psutil==5.9.8' 'requests==2.32.3' \
  'typing-extensions==4.15.0' 'pyyaml==6.0.2' 'pyngrok==7.3.0'
"$TASK_ENV/bin/python" -m pip freeze > "$TASK_ROOT/artifacts/p0_pip_freeze.txt"
"$TASK_ENV/bin/python" -m pip check > "$TASK_ROOT/artifacts/p0_pip_check.txt" 2>&1 || true
