"""Run a bounded validation command and preserve output plus GPU measurements."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import threading
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--timeout', type=float, required=True)
    parser.add_argument('--output-root', type=Path, default=Path(__file__).resolve().parents[1] / 'artifacts')
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        parser.error('a command is required')
    output = args.output_root / args.name
    output.mkdir(parents=True, exist_ok=False)
    (output / 'command.json').write_text(json.dumps({'cwd': os.getcwd(), 'argv': command}, indent=2))
    start = time.monotonic()
    stop = threading.Event()
    samples = []

    def sample_gpu():
        while not stop.is_set():
            result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,utilization.gpu', '--format=csv,noheader,nounits'], capture_output=True, text=True)
            if result.returncode == 0:
                values = result.stdout.strip().splitlines()[0].split(',')
                samples.append({'seconds': time.monotonic() - start, 'gpu_memory_mib': int(values[0]), 'gpu_utilization_pct': int(values[1])})
            stop.wait(1)

    monitor = threading.Thread(target=sample_gpu, daemon=True)
    monitor.start()
    timed_out = False
    with (output / 'console.log').open('w') as logfile:
        process = subprocess.Popen(command, stdout=logfile, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            code = process.wait(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            code = 124
        finally:
            stop.set()
            monitor.join(timeout=10)
    summary = {'exit_code': code, 'timed_out': timed_out, 'wall_seconds': time.monotonic() - start,
               'peak_gpu_memory_mib': max((x['gpu_memory_mib'] for x in samples), default=None),
               'gpu_samples': samples}
    (output / 'result.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps({k: v for k, v in summary.items() if k != 'gpu_samples'}), flush=True)
    print('Full log:', output / 'console.log', flush=True)
    raise SystemExit(code)


if __name__ == '__main__':
    main()
