#!/usr/bin/env bash
# Direct upstream entry, one continuous learn() call. No supervisor or Stage2.
set -euo pipefail
cd "$(dirname "$0")/../.."
: "${1:?Usage: train_unified_hmi_stage1.sh NEW_RUN_DIRECTORY [TOTAL_UPDATES=15000] [VERIFIED_CHECKPOINT]}"
run_dir=$(realpath -m "$1")
updates=${2:-15000}
resume=${3:-}
if [[ -e "$run_dir" ]]; then echo "Refusing to overwrite existing run: $run_dir" >&2; exit 1; fi
mkdir -p "$run_dir"
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV LD_LIBRARY_PATH
export PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
export CUDA_VISIBLE_DEVICES=0
export HMI_UNIFIED_DATA="$PWD/datasets/unified_hoi_v1"
checkpoint_args=()
remaining=$updates
if [[ -n "$resume" ]]; then
  resume=$(realpath "$resume")
  remaining=$(../envs/g1_hmi_carry/bin/python - "$resume" "$updates" "$HMI_UNIFIED_DATA" <<'PYRESUME'
import sys,json,torch
from pathlib import Path
from holosoma.carry.checkpoints import validate,digest
checkpoint,total,data=sys.argv[1],int(sys.argv[2]),Path(sys.argv[3])
info=validate(checkpoint);state=torch.load(checkpoint,map_location='cpu',weights_only=True)['env_state']
if state.get('unified_schema')!=1 or state.get('fullbody_manifest_sha256')!=digest(data/'manifest.json'):
    raise ValueError('Resume requires an identical verified Unified HOI checkpoint/dataset')
if state.get('stage1_reference_protocol')!='hard_reset_post_action_v1' or state.get('stage1_action_parameterization')!='joint_delta_v1':
    raise ValueError('Incompatible reference timing/action protocol')
remaining=total-info['completed_updates']
if remaining<=0:raise ValueError('Checkpoint already reached the requested total updates')
print(remaining)
PYRESUME
  )
  checkpoint_args=("--training.checkpoint=$resume" '--algo.config.load-optimizer=True' '--algo.config.reset-policy-std-on-resume=False')
  printf 'Resuming verified checkpoint %s; %s additional updates to total %s\n' "$resume" "$remaining" "$updates"
fi
# Override with online after valid W&B authentication. Offline preserves W&B data.
export WANDB_MODE=${WANDB_MODE:-offline}
exec ../envs/g1_hmi_carry/bin/python -u src/holosoma/holosoma/train_agent.py \
  exp:g1-29dof-unified-hoi-stage1 logger:wandb \
  --logger.mode="$WANDB_MODE" --logger.video.enabled=False \
  --logger.base-dir="$run_dir/logs" \
  --training.num-envs=8192 --training.headless=True --training.seed=42 \
  --algo.config.num-learning-iterations="$remaining" --algo.config.save-interval=2000 \
  --simulator.config.scene.env-spacing=4.0 \
  --command.setup-terms.motion-command.params.motion-config.hybrid.track-ratio=1.0 \
  "${checkpoint_args[@]}"
