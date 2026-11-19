# Implementation and bounded validation report

Date: 2026-11-19. Hardware: RTX 4090 D 24 GB, Ubuntu, driver 580.178.04.
Repository: `Ir1222/carry_baseline`, branch `carry/goal-conditioned-continuous`.
Audited base: `c353731999b3578c41ad5a00f896415b45e6a9f5`.

## Outcome and readiness

`exp:g1-29dof-wbt-hybrid-carry` runs through physics, PPO, checkpoint resume,
policy-only ONNX export, reference-free simulation and GUI viewing. Both stages
share a 348D Actor and 184D Critic. The 256-env/100-update pilot completed.
Full Stage 1/2 was not started. Existing projects, environments and original weights
were unchanged; all work is isolated. Commits were pushed after user authorization.

**Ready for training experiments; not a demonstrated stable carrying policy.**
Initial support passed a narrow 0.2 s settling check. Sustained free-box carrying
and dynamic feasibility of moving retargeted references remain unverified. The
pilot stayed at curriculum level 0 with mean episode length 46.79 control steps
(0.936 s). This is not evidence of successful command following.

## Files

All `carry/*` paths below are under `src/holosoma/holosoma/`.

| Files | Purpose |
|---|---|
| `carry/presets.py`, `config_values/experiment.py` | New experiment, control gains, observations, rewards and termination |
| `carry/command.py`, `sampling.py` | Four commands, Track extraction, Gen sampling/smoothing/curriculum, no Gen clip reset |
| `carry/observations.py` | Physical 116D frame × 3 history; privileged reference only in Track Critic |
| `carry/rewards.py`, `termination.py` | Task/support rewards; exactly zero Gen imitation; physical failures and Track-only reference failure |
| `carry/simulator.py` | Actual hand–box normal/friction force sensing each physics substep |
| `carry/environment.py`, `ppo.py` | Failure/timeout semantics, curriculum checkpoint state, policy-only export, physical viewer overlay |
| `carry/inference.py`, `deployment.py` | Physical-state ONNX Actor; static-reset deployment without motion loaders |
| `scripts/carry/prepare_reference.py`, `finalize_reference.py` | Crop, measured-reset assertions, carton/posture retargeting and FK |
| `scripts/carry/probe_settling.py` | Bounded diagnostics/replay; diagnostic feedback never enters RL |
| `scripts/carry/smoke_original.py`, `smoke_carry.py`, `run_bounded.py` | Real PPO/runtime assertions, bounded execution and GPU measurement |
| `scripts/carry/evaluate.py`, `verify_runtime.py` | Scripted/interactive/viewer evaluation and dedicated-runtime checks |
| `assets/carry/*`, `tests/test_carry_interface.py` | Static reset, compressed actual evidence, three physical-interface tests |

The only change to original HMI source outside the new package is experiment
import/registration. Original experiment definitions and Actor schemas remain.

## Actual tests

Exact argv/logs/measurement JSON are in
`/home/han/pyx/g1_carry_baseline_new/artifacts/<run>/`.
Smoke reports are adjacent `*_assertions.json`. A portable summary is
`scripts/carry/validation_results.json`.

| Test/run | Result |
|---|---|
| Runtime verifier | Python/Torch/CUDA versions, finite GPU matmul, isolated import paths, Isaac package/tag passed; only 3 acknowledged pip metadata conflicts |
| `p1_original_attempt2` | 64 env, 32/32 Track/Gen; gravity/free-base/collision box checks; actor 111/critic 316; 26 finite steps, 1 real PPO update; checkpoint/ONNX saved |
| CPU interface tests | 3 passed: heading/translation invariance and dimensions, independent command distribution, smooth independent yaw/height |
| `p2_reset_replay1` | 64 identical resets, first 0.2 s: max drop 1.44 cm, min root 0.758 m, min hand force 1.44 N, min support/weight 0.684 |
| Reference regeneration | Every array in all 3 output NPZs reproduced exactly from committed compressed evidence in a fresh directory |
| `p3_stage1_attempt1` | 64 Track, actor `[64,348]`, critic `[64,184]`; 26 finite steps, 1 update |
| `p3_stage2_attempt2` | Stage 1 checkpoint loaded into 32/32 Track/Gen; update, reward masks, no command reset, Gen clip independence, ONNX equivalence passed |
| `p3_stage2_attempt3` | Real timeout and simultaneous fall/time limit injected; stored PPO bootstrap matched final Critic values; failure did not bootstrap; reset history cleared; ONNX max error 1.32e-6 |
| `p3_deploy_attempt1` | 1500 steps, all 10 scripted command phases, motion-loader constructors forbidden; finite outputs; 21 physical resets: interface passed, behavior did not |
| `p3_pilot256_100` | 256 env (128/128), 100 updates, 614,400 transitions; finite saved weights/checkpoints/ONNX; no logged CUDA/PhysX error or traceback |
| `p3_view_attempt1` | Local GUI, 60 rendered physics steps, no motion loading; completed without traceback or logged error |

The viewer was exercised programmatically; no human visual assessment of a
successful trajectory is claimed. Empty foot visual-reference and non-articulation
box importer warnings remain; collisions were separately checked.

## Resource measurements

| Run | Wall seconds | Peak whole-GPU MiB | Throughput |
|---|---:|---:|---|
| Original 64-env/1-update | 12.94 | 3302 | 995 env steps/s, startup iteration |
| Carry Track 64-env/1-update | 12.29 | 3300 | 1259 env steps/s, startup iteration |
| Carry corrected mixed 64-env/1-update | 12.69 | 3326 | Startup smoke |
| Carry 256-env/100-update | 156.33 | 3448 | Median 4333, last-20 median 4421 env steps/s |
| GUI 1-env/60-step | 80.32 | 6238 | First viewer startup included |

Whole-GPU samples include about 388 MiB idle desktop use. The final bootstrap smoke
and first deployment overlapped; their ~6.1 GiB peaks are not per-run capacity
estimates. Pilot/GUI measurements above were separate. No 8192-env assumption was
used. GPU memory is sampled every second, not an exact instantaneous maximum.

Pilot final aggregate metrics (Track and Gen mixed): vx error 0.177 m/s, vy error
0.117 m/s, yaw error 0.659 rad/s, height error 0.0180 m, contact quality 0.711,
curriculum level 0. These are training aggregates, not behavioral success rates.
The pilot resumed a **one-update** Stage 1 checkpoint to exercise the lifecycle;
it did not follow a converged two-stage training recipe.

## Failures diagnosed and remaining limitations

Raw carry-frame PD holds and several grip/under-support variants dropped the box.
Wrong diagnostic wrist-body sensor selection, missing tangential friction, an IK
float32 finite-difference issue and hidden Isaac shutdown exceptions were fixed.
Sensors now target sphere-hand bodies. The runner requires result artifacts and
rejects tracebacks. Integration also exposed upstream Gen imitation constants;
these were removed from the new experiment.

The MVP is a 0.5 kg, 0.28×0.40×0.30 m cuboid with upward palm support and modified
PD gains, retaining original torque limits. It is not the original large-box
setup. Carry-only root/legs are preserved and upper-body/object targets regenerated
through FK. **Full dynamic replay of moving references is not validated.** Static
targets also do not prove sustained balance. Initial settling passed only the
stated 0.2 s window; at 0.5 s some fixed-PD resets dropped 10.1 cm. Longer diagnostic
holds used ankle feedback, absent from RL and not counted as policy success.

No attachment, weld, box pose-following, terminal destination reward, World Model,
AMP, human-force controller or pickup/place extension was added. Terrain is flat;
mass/friction are fixed. Payload/friction/terrain generalization, external-force
robustness and hardware are untested.

## Next manual work

Exact activation, full Stage 1/2, evaluation, viewer and metrics commands are in
`README_CARRY.md`. Train Stage 1 from scratch and inspect holding/tracking before
resuming mixed Stage 2. Require repeated ≥20 s episodes with bilateral support and
independent command changes before claiming usability. If Stage 1 cannot learn
stable support/balance, inspect reference/contact/termination metrics and revise
the reset/control/reference fit before spending on Stage 2. No further training
process is left running by this implementation task.
