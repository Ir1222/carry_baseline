#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
repair_mode="${1:?Pass fixed or joint_delta}"
case "$repair_mode" in fixed|joint_delta) ;; *) exit 2 ;; esac
export HMI_CARRY_ACTION_MODE="$repair_mode"
repair_root="${HMI_STAGE1_REPAIR_OUTPUT:-../artifacts/stage1_repair_validation}"
../envs/g1_hmi_carry/bin/python scripts/carry/run_bounded.py \
  --name "train_${repair_mode}" --output-root "$repair_root" --timeout 600 \
  --require-result "$repair_root/train_${repair_mode}_data/worker/worker_result.json" -- \
  bash scripts/carry/train_stage1_joint.sh --num-envs 256 --iterations 32 --save-every 16 \
  --seed 42 --run-dir "$repair_root/train_${repair_mode}_data"
