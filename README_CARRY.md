# Continuous G1 Carry — implementation in progress

**Training is not ready yet.** The original HMI Object PPO smoke passed. The new
carry interface is implemented, but a stable, freely simulated already-carrying
reset has not yet passed physical validation. `CarryCommand` intentionally refuses
to start without `verified_reset.json`. No such file has been approved/generated.
Do not interpret source availability as a working trained carrying policy.

Worktree: `/home/han/pyx/g1_carry_baseline_new/HMI`.
Branch: `carry/goal-conditioned-continuous`.
Upstream base: `c353731999b3578c41ad5a00f896415b45e6a9f5`.
User fork: https://github.com/Ir1222/carry_baseline.

## Validated runtime

```bash
source /home/han/miniconda3/etc/profile.d/conda.sh
conda activate /home/han/pyx/g1_carry_baseline_new/envs/g1_hmi_carry
export PATH="$CONDA_PREFIX/bin:$PATH"
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV LD_LIBRARY_PATH
export PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 WANDB_MODE=disabled
cd /home/han/pyx/g1_carry_baseline_new/HMI
python -c 'import torch,holosoma; print(torch.__version__, torch.version.cuda, torch.cuda.get_device_name(0), holosoma.__path__)'
python -m pip check
```

Python 3.11.15; Torch 2.7.0+cu128; Isaac Sim 5.1.0.0; Isaac Lab v2.3.0
at `3c6e67bb5c7ada942a6d1884ab69338f57596f77`. The Lab package reports
`isaaclab==0.47.2`, which is the package version shipped at that tag.
Only three upstream-documented Isaac Sim kernel metadata conflicts remain:
click, typing_extensions, and websockets. See `scripts/carry/p0_pip_check.txt`.

The dedicated environment was copied from locally available matching binaries,
then all inherited editable registrations were removed and reinstalled from this
isolated workspace. The source environment and other projects were not changed.

## Original Object smoke

This command exercises the upstream experiment with runtime assertions:

```bash
export HMI_SMOKE_REPORT="$PWD/../artifacts/original_assertions_rerun.json"
python scripts/carry/run_bounded.py --name original_smoke_rerun --timeout 900 -- \
  python scripts/carry/smoke_original.py \
  exp:g1-29dof-wbt-hybrid-object logger:disabled \
  --training.num-envs=64 --training.headless=True \
  --training.name=original_smoke --algo.config.num-learning-iterations=1 \
  --algo.config.save-interval=1 \
  --logger.base-dir="$PWD/../artifacts/training" \
  --command.setup-terms.motion-command.params.motion-config.motion-dir=holosoma/data/motions/g1_29dof/whole_body_tracking/movebox
```

Use a fresh run name/report path on each execution. The actual passed run is
`../artifacts/p1_original_attempt2`: 32 Track + 32 Gen, actor `[64,111]`, critic
`[64,316]`, 26 finite physics control steps, one PPO forward/backward update and
checkpoint/ONNX saving. Wall time 12.94 s, peak whole-GPU memory 3302 MiB,
reported training throughput 995 environment steps/s (one-iteration startup run).
There were no logged CUDA/PhysX errors. Asset importer warnings about empty visual
frames remain; dynamic box collision geometry was explicitly asserted.

## Carry data and fast interface checks

```bash
python scripts/carry/prepare_reference.py --output ../artifacts/carry_reference_fresh
python -m pytest -q tests/test_carry_interface.py
```

The crop is original frames `[95,205)` (110 frames at 50 Hz), including the
mirrored clip. It excludes pickup/place. Commands are measured reference heading
velocity, world-Z yaw angular velocity, and pelvis height, without clipping to Gen
curriculum ranges. Source hashes and command bounds are recorded in `manifest.json`.
The current fast test result is **3 passed**: actor heading-frame invariance,
independent command sampling, and smooth independent yaw/height command changes.

New actor: three 116-dimensional physical-state/command frames, oldest first,
zero-padded after reset; total 348 dimensions. No phase, clip ID, future reference,
or terminal goal appears in the actor. The four commands are
`[vx (m/s), vy (m/s), yaw_rate (rad/s), pelvis_height (m)]`.

## Current physical validation blocker

Raw carry-frame PD holds lose the box. Bounded tests are checking collision
clearance, actuator settings, and reset posture. All tests leave the box dynamic,
with gravity, no weld/attachment, and no pose-following updates after reset.
The hand sensors target the actual `*_sphere_hand_link` bodies. Total filtered
support includes PhysX tangential friction; Isaac Lab's normal-force tensor alone
does not measure side-grip support correctly.

Diagnostic example (two simulated seconds, 64 candidates; no PPO training):

```bash
python scripts/carry/run_bounded.py --name settling_fresh --timeout 240 -- \
  python scripts/carry/probe_settling.py \
  --data ../artifacts/carry_reference --output ../artifacts/settling_fresh.json
```

New-task PPO smoke, Stage 1→Stage 2 checkpoint verification, reference-free
simulation evaluation, and the 256-env/100-iteration pilot have **not yet run**.
Full training commands will be finalized only after the physical reset and these
integration checks pass. No full training has been started.
