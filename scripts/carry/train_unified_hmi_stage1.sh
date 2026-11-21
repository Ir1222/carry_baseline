#!/usr/bin/env bash
# Direct upstream entry, one continuous learn() call. No supervisor or Stage2.
set -euo pipefail
cd "$(dirname "$0")/../.."
: "${1:?Usage: train_unified_hmi_stage1.sh NEW_RUN_DIRECTORY [UPDATES=15000]}"
run_dir=$(realpath -m "$1")
updates=${2:-15000}
if [[ -e "$run_dir" ]]; then echo "Refusing to overwrite existing run: $run_dir" >&2; exit 1; fi
mkdir -p "$run_dir"
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV LD_LIBRARY_PATH
export PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
export CUDA_VISIBLE_DEVICES=0
export HMI_UNIFIED_DATA="$PWD/datasets/unified_hoi_v1"
# Override with online after valid W&B authentication. Offline preserves W&B data.
export WANDB_MODE=${WANDB_MODE:-offline}
exec ../envs/g1_hmi_carry/bin/python -u src/holosoma/holosoma/train_agent.py \
  exp:g1-29dof-unified-hoi-stage1 logger:wandb \
  --logger.mode="$WANDB_MODE" --logger.video.enabled=False \
  --logger.base-dir="$run_dir/logs" \
  --training.num-envs=8192 --training.headless=True --training.seed=42 \
  --algo.config.num-learning-iterations="$updates" --algo.config.save-interval=2000 \
  --simulator.config.scene.env-spacing=4.0 \
  --command.setup-terms.motion-command.params.motion-config.hybrid.track-ratio=1.0
