#!/usr/bin/env bash
set -euo pipefail
repo="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo"
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV LD_LIBRARY_PATH
export PYTHONNOUSERSITE=1
exec "$repo/../envs/g1_hmi_carry/bin/python" -m tensorboard.main \
  --logdir "$repo/../artifacts/fullbody_stage1_joint" --host 127.0.0.1 --port 6012 "$@"
