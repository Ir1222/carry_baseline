#!/usr/bin/env bash
set -euo pipefail
repo="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
carry_python="$repo/../envs/g1_hmi_carry/bin/python"
base="$repo/../artifacts/auto_training"
cd "$repo"
export PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 WANDB_MODE=disabled
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV LD_LIBRARY_PATH
export PATH="$(dirname "$carry_python"):$PATH"

launch_supervisor() {
  local run_root="$1"
  if systemctl --user is-active --quiet g1-carry-supervisor.service; then
    echo 'Supervisor already active. Use status.'; exit 1
  fi
  systemd-run --user --unit=g1-carry-supervisor --collect \
    --property=Restart=on-failure --property=RestartSec=30 \
    --property=KillMode=control-group --property=TimeoutStopSec=30 \
    --property="StandardOutput=append:$run_root/supervisor.log" \
    --property="StandardError=append:$run_root/supervisor.log" \
    --working-directory="$repo" \
    /usr/bin/env -u PYTHONPATH -u PYTHONHOME -u VIRTUAL_ENV -u LD_LIBRARY_PATH \
      PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 WANDB_MODE=disabled \
      "PATH=$PATH" "$carry_python" scripts/carry/auto_train.py run --root "$run_root"
}

dashboard() {
  if systemctl --user is-active --quiet g1-carry-tensorboard.service; then
    "$carry_python" -c 'import json,sys; print(json.load(open(sys.argv[1]))["url"])' "$base/dashboard.json"
    return
  fi
  local port
  port="$("$carry_python" -c 'import socket
for p in (6006,6008,6009,6010):
 s=socket.socket()
 try:
  s.bind(("127.0.0.1",p)); print(p); break
 except OSError: pass
 finally: s.close()
else: raise SystemExit("No free local dashboard port")')"
  systemd-run --user --unit=g1-carry-tensorboard --collect \
    --property=Restart=on-failure --property=RestartSec=10 \
    --working-directory="$repo" \
    /usr/bin/env -u PYTHONPATH -u PYTHONHOME -u VIRTUAL_ENV -u LD_LIBRARY_PATH \
      PYTHONNOUSERSITE=1 "$carry_python" -m tensorboard.main \
      --logdir "$base" --host 127.0.0.1 --port "$port" --reload_interval 10
  "$carry_python" - "$base/dashboard.json" "$port" <<'PY'
import sys
from holosoma.carry.checkpoints import atomic_json
atomic_json(sys.argv[1],dict(port=int(sys.argv[2]),url=f'http://127.0.0.1:{sys.argv[2]}',unit='g1-carry-tensorboard.service'))
print(f'http://127.0.0.1:{sys.argv[2]}')
PY
}

case "${1:-status}" in
  start)
    test -f "$base/validation_success.json" || { echo 'Bounded engineering validation has not passed.'; exit 1; }
    root="$("$carry_python" scripts/carry/auto_train.py init "${@:2}")"
    dashboard
    launch_supervisor "$root"
    ;;
  resume)
    test -f "$base/validation_success.json"
    launch_supervisor "$(readlink -f "$base/current")"
    dashboard
    ;;
  stop)
    systemctl --user stop g1-carry-supervisor.service
    ;;
  status|monitor)
    "$carry_python" scripts/carry/status.py "${@:2}"
    ;;
  dashboard)
    dashboard
    ;;
  *) echo 'Usage: carryctl.sh start [--config FILE] | stop | resume | status [--watch|--json] | dashboard'; exit 2 ;;
esac
