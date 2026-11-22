"""Guard shell evaluation using durable PPO status, even if Kit changes exit code."""
import json
from pathlib import Path
import sys


def training_exit_code(root, process_exit):
    files=[p for p in Path(root).rglob("training_status.json") if ".wandb" not in p.parts]
    status=json.loads(files[0].read_text()) if len(files)==1 else {}
    if status.get("status")=="interrupted" or process_exit in (130,143):
        return 130
    if process_exit:
        return process_exit
    return 0 if status.get("status")=="complete" else 1


if __name__=="__main__":
    raise SystemExit(training_exit_code(sys.argv[1],int(sys.argv[2])))
