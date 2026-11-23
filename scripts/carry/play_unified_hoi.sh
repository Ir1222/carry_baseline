#!/usr/bin/env bash
# Native checkpoint playback; share the carry GPU lock and use the saved experiment.
set -euo pipefail
cd "$(dirname "$0")/../.."
: "${1:?Usage: play_unified_hoi.sh CHECKPOINT.pt [eval_agent overrides]}"
checkpoint=$(realpath "$1")
shift
[[ -f "$checkpoint" ]] || { echo "Checkpoint missing: $checkpoint" >&2; exit 1; }
exec 9>/tmp/g1-carry-gpu0.lock
flock -n 9 || { echo 'GPU0 is owned by training/evaluation; stop it safely before native play' >&2; exit 1; }
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV LD_LIBRARY_PATH
export PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 WANDB_MODE=offline
exec ../envs/g1_hmi_carry/bin/python -u src/holosoma/holosoma/eval_agent.py \
  --checkpoint="$checkpoint" --viser.config.enabled --viser.config.port="${HMI_PLAY_PORT:-8012}" \
  --training.num-envs=2 --training.headless=True --training.export-onnx=False "$@"
