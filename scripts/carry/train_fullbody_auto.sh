#!/usr/bin/env bash
set -euo pipefail
repo="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo"
fullbody_python="$repo/../envs/g1_hmi_carry/bin/python"
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV LD_LIBRARY_PATH
export PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 WANDB_MODE=disabled
export PATH="$(dirname "$fullbody_python"):$PATH"
base="$repo/../artifacts/fullbody_goal_carry"
case "${1:-status}" in
  start)
    test -f "$base/preflight.json"
    "$fullbody_python" -c 'import json,sys; assert json.load(open(sys.argv[1]))["passed"]' "$base/preflight.json"
    if systemctl --user is-active --quiet g1-fullbody-carry.service; then exit 1; fi
    root="$("$fullbody_python" scripts/carry/fullbody_auto.py init)"
    ;;
  resume)
    root="$(readlink -f "$base/current")"
    ;;
  status)
    cat "$base/current/training_status.json"
    exit 0
    ;;
  stop)
    systemctl --user stop g1-fullbody-carry.service
    exit 0
    ;;
  *) echo 'Usage: train_fullbody_auto.sh start|resume|status|stop'; exit 2 ;;
esac
systemd-run --user --unit=g1-fullbody-carry --collect \
  --property=KillMode=control-group --property=TimeoutStopSec=30 \
  --property="StandardOutput=append:$root/supervisor.log" \
  --property="StandardError=append:$root/supervisor.log" \
  --working-directory="$repo" \
  /usr/bin/env -u PYTHONPATH -u PYTHONHOME -u VIRTUAL_ENV -u LD_LIBRARY_PATH \
    PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 WANDB_MODE=disabled \
    "PATH=$PATH" "$fullbody_python" scripts/carry/fullbody_auto.py run --root "$root"
echo "$root"
