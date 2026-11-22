#!/usr/bin/env bash
# Durable shell sequencing only: one HMI training process, then offline evaluation.
# No plateau/time budget/retry/reward editing/Stage2, no concurrent Isaac jobs.
set -euo pipefail
cd "$(dirname "$0")/../.."
: "${1:?Usage: train_unified_hmi_then_evaluate.sh NEW_OUTPUT_DIRECTORY [VERIFIED_CHECKPOINT]}"
run_dir=$(realpath -m "$1")
resume=${2:-}
if [[ -e "$run_dir" ]]; then echo "Refusing existing output: $run_dir" >&2; exit 1; fi
mkdir -p "$run_dir"
exec 9>/tmp/g1-carry-gpu0.lock
flock -n 9 || { echo 'GPU0 is owned by another carry job' >&2; exit 1; }
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV LD_LIBRARY_PATH
export PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
export WANDB_MODE=${WANDB_MODE:-offline}
python_bin="$PWD/../envs/g1_hmi_carry/bin/python"
echo "$$" > "$run_dir/controller.pid"
git rev-parse HEAD > "$run_dir/source_commit.txt"
git archive HEAD > "$run_dir/source.tar"
git diff HEAD > "$run_dir/source.patch"
git ls-files --cached --others --exclude-standard -z | tar --null -T - -czf "$run_dir/source_worktree.tar.gz"
cp datasets/unified_hoi_v1/manifest.json "$run_dir/dataset_manifest.json"
printf 'running\n' > "$run_dir/status.txt"
nvidia-smi --query-gpu=timestamp,memory.used,utilization.gpu --format=csv -l 10 > "$run_dir/gpu.csv" &
gpu_pid=$!
trap 'kill "$gpu_pid" 2>/dev/null || true; if [[ $(cat "$run_dir/status.txt") == running ]]; then printf "stopped_or_failed\n" > "$run_dir/status.txt"; fi' EXIT
bash scripts/carry/train_unified_hmi_stage1.sh "$run_dir/training" 15000 "$resume" > "$run_dir/training.console.log" 2>&1 &
training_pid=$!
echo "$training_pid" > "$run_dir/training.pid"
set +e
wait "$training_pid"
training_exit=$?
set -e
if [[ $training_exit -eq 130 || $training_exit -eq 143 ]]; then
  printf 'interrupted\n' > "$run_dir/status.txt"
  exit "$training_exit"
fi
if [[ $training_exit -ne 0 ]]; then
  printf 'failed\n' > "$run_dir/status.txt"
  exit "$training_exit"
fi
"$python_bin" scripts/carry/validate_unified_hmi_run.py --run "$run_dir/training" --updates 15000 --output "$run_dir/training_completion.json" > "$run_dir/completion_validation.log" 2>&1
policy=$("$python_bin" -c 'import json,sys; from pathlib import Path; print(Path(json.load(open(sys.argv[1]))["checkpoint"]["path"]).with_suffix(".onnx"))' "$run_dir/training_completion.json")
printf 'evaluating\n' > "$run_dir/status.txt"
"$python_bin" -u scripts/carry/evaluate_unified_hoi.py --policy "$policy" --seeds 10 --output "$run_dir/final_evaluation" > "$run_dir/evaluation.console.log" 2>&1
printf 'complete\n' > "$run_dir/status.txt"
