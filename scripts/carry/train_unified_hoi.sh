#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV LD_LIBRARY_PATH
export PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 WANDB_MODE=disabled OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
exec ../envs/g1_hmi_carry/bin/python scripts/carry/train_unified_hoi.py "$@"
