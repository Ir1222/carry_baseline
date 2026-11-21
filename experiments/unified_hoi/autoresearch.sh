#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
# One bounded diagnostic command only. No restart/optimization/Stage2 loop.
exec bash scripts/carry/train_unified_hoi.sh --num-envs 256 --iterations 4 --save-every 2 "$@"
