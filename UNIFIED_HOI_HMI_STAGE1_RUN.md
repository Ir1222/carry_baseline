# Unified HOI Stage1 — direct HMI launch, 8192 environments

> 本文件保留历史运行语义。2026-11-22新修复与当前执行状态以[Stage1支撑修复记录](STAGE1_SUPPORT_REPAIR_20261122.md)为准；历史full_training_ready或未训练策略成功率不作为开训门禁。

Base `38109772247c4498b93252500a79218bb52f5583`, branch `feature/unified-hoi-stage1`. This launch revision supersedes the earlier audit's decision to prohibit long training. Earlier physics failures and source validation labels remain true, preserved evidence. An untrained Actor failing reference probes is not used as a prohibition on Track-only learning.

## What changed

Removed the `iterations>32 && !full_training_ready` exception in the diagnostic launcher. No reference/manifest bytes, assets, controller, PPO optimization hyperparameters, rewards, termination or physical acceptance thresholds changed. The user subsequently changed checkpoint frequency from500 to2000; this is the only training-configuration change after capacity testing. The capacity test exposed W&B symlinks to deleted temporary ONNX paths and omitted checkpoint uploads. Unified-only save/export publishing now registers verified final files after atomic publication; a regression test reproduces the temporary-name failure, and the8192×2 test is repeated after the fix. No physics status was promoted. Added a small shell command for the original `src/holosoma/holosoma/train_agent.py`, a read-only configuration audit and a numerical/capacity verifier. The training algorithm remains the existing HMI PPO subclass with checksum checkpoints and physical-observation ONNX export.

The optional `train_unified_hmi_then_evaluate.sh` only sequences one uninterrupted15000-update HMI process and an independent10-seed evaluation after it exits successfully. It has no learning early-stop, plateau, resource-time budget, segmented resume, retry, reward edits or Stage2. Episode failures still terminate/reset individual environments and remain logged. Fatal OOM/interface/numerical exceptions are not hidden or retried. `status.txt=complete` means execution finished; physical policy success is determined separately in `final_evaluation/evaluation.json`.

## Resolved PPO comparison

Upstream column reproduces the original README Object Stage1 command, including8192/15000/Track-only/4m spacing. Unified column is the actual new run. Existing differences were retained per instruction, not tuned.

| Setting | Upstream Object Stage1 | Unified HOI actual |
|---|---:|---:|
| environments / updates |8192 /15000|8192 /15000|
| `num_mini_batches` |4|128|
| `num_learning_epochs` |5|5|
| initial action noise std |1.0|0.3|
| `num_steps_per_env` |24|24|
| actor / critic initial LR |1e-4 /1e-4|1e-4 /1e-4|
| schedule / desired KL |adaptive /0.01|adaptive /0.01|
| gamma / lambda |0.99 /0.95|0.99 /0.95|
| clip / entropy coefficient |0.2 /0.002|0.2 /0.002|
| empirical normalization |true|true|
| symmetry |false|false|
| `init_at_random_ep_len` |true|false|
| checkpoint interval |3000|2000 (latest user request)|
| latest alias interval |100|0|
| reference frame0 reset probability |0.05|0.25|
| scene spacing / Track ratio |4.0 /1.0|4.0 /1.0|

8192×24=196608 transitions/update. Unified's128 minibatches mean1536 transitions/minibatch, versus49152 upstream. Both use5 epochs; the number of optimizer steps is therefore different (640 versus20/update). This is disclosed, not claimed to be identical hyperparameter behavior. The existing std0.3 has its retained `joint_delta_v1` physical meaning. No global action-scale/gain/noise change was applied.

`init_at_random_ep_len=False` preserves exact Reset/reference episode-clock alignment; reference frame sampling still provides varied initialization. Full-sequence resets use audited task-mode-conditioned frame pools plus25% frame0; loaded clips retain adaptive sampling. All six immutable clips use family quotas30/35/35. Root/joint/object initialization remains reference-derived, with exact hard-limit-valid positions and zero initialization noise. Four reference-derived goals and intention labels remain aligned to the correct post-action reference frame. Actor357D/Critic187D, 1ms physics/PD,20ms policy and1.1kg free box remain unchanged.

All eight HMI Robot/Object imitation terms are preserved with HOI grasp, slip, nonhand contact and phase-specific pickup/putdown rewards. Full effective PPO, motion/reset, rewards, termination, action and gains: [machine-readable audit](experiments/unified_hoi/hmi_ppo_config_audit.json). Actual per-run `holosoma_config.yaml` is authoritative. The unchanged manifest SHA256 is `c3c5d8f41d10e3b5be339c797b90f1b723e6a1b9c8624502f1a49d0e5d26cd15`.

## Actual capacity test

Direct upstream entry,8192 environments ×2 updates, seed42, same logging/spacing/dataset as formal run. Completed normally,393216 transitions, peak GPU8702MiB on4090D24GB,114.62s including initialization/export (repeat after publication fix; first test118.38s). Collection19.049/18.679s, throughput9461/9706 env steps/s; two updates alone are not a steady-state benchmark. ONNX/PyTorch max absolute difference7.45e-7. All TensorBoard scalars and full checkpoint state were finite.106 regression tests passed.

Observed family fractions:30.0049% full sequence,34.9976% locomotion,34.9976% squat/stand. Last-rollout intention fractions:19.1391% pickup,75.3245% carry,5.5364% putdown. Short/failed episodes distort phase exposure; diagnostics preserve this. Carry success was not a capacity gate. The untrained policy's physical failures remain logged and do not prevent learning.

[Capacity evidence](experiments/unified_hoi/hmi_capacity_8192.json). Full console/GPU samples: `../artifacts/unified_hoi_hmi_stage1/capacity_8192_002/`; checkpoint/config/TensorBoard/W&B: sibling `capacity_8192_002_data/`. Retained Isaac USD warnings concern missing visuals for auxiliary foot markers; no OOM, PhysX buffer overflow or training interface exception was found.

## Actual formal command and durable execution

Run root: `../artifacts/unified_hoi_hmi_stage1/formal_8192_15000_002_save2000/`. Training starts from scratch with no checkpoint argument; capacity weights are not loaded. PID/commit/archive/manifest/status/GPU log are saved there. An independent background session, redirected stdin/stdout and file logs keep execution alive after the conversation/browser closes. There is no automatic restart.

Equivalent raw training command (choose a new output directory to avoid mixing runs):

```bash
cd /home/han/pyx/g1_carry_baseline_new/HMI
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV LD_LIBRARY_PATH
export PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
CUDA_VISIBLE_DEVICES=0 WANDB_MODE=offline \
../envs/g1_hmi_carry/bin/python -u src/holosoma/holosoma/train_agent.py \
  exp:g1-29dof-unified-hoi-stage1 logger:wandb \
  --logger.mode=offline --logger.video.enabled=False \
  --logger.base-dir=../artifacts/unified_hoi_hmi_stage1/NEW_RUN/logs \
  --training.num-envs=8192 --training.headless=True --training.seed=42 \
  --algo.config.num-learning-iterations=15000 --algo.config.save-interval=2000 \
  --simulator.config.scene.env-spacing=4.0 \
  --command.setup-terms.motion-command.params.motion-config.hybrid.track-ratio=1.0
```

`motion-dir` is deliberately not overridden: it resolves to all six Unified HOI files. Video rendering is disabled during training, matching the previous experiment; independent evaluation supports viewer/video. The HMI loop saves at indices0,2000,4000…14000 and final14999; saving/exporting does not stop or restart training. The final checkpoint is not presented as already trained or accepted. At observed short-run throughput,15000 updates could take roughly3–4 days, with no time-based cutoff.

Actual durable orchestration command:

```bash
WANDB_MODE=offline bash scripts/carry/train_unified_hmi_then_evaluate.sh \
  ../artifacts/unified_hoi_hmi_stage1/formal_8192_15000_002_save2000
```

## Monitoring and independent evaluation

```bash
tail -f ../artifacts/unified_hoi_hmi_stage1/formal_8192_15000_002_save2000/training.console.log
../envs/g1_hmi_carry/bin/python -m tensorboard.main \
  --logdir ../artifacts/unified_hoi_hmi_stage1 --host 127.0.0.1 --port 6015
```

TensorBoard: http://127.0.0.1:6015 . Scalars include PPO losses/noise/LR/FPS, episode rewards/length, per-family and per-phase tracking/contact/slip/friction/clearance/support/torque/foot metrics, motion coverage and all termination causes. Checkpoints/config/events are in `formal_8192_15000_002_save2000/training/logs/WholeBodyTracking/<timestamp>-unified_hoi_stage1-locomotion/`; exact path is also in the HMI console and `runtime_paths.json` after startup.

TensorBoard is the primary dashboard, as requested. W&B uses `logger:wandb --logger.mode=offline`: online credential verification returned HTTP403 before training. W&B availability is not a training/capacity gate; no further online repair is attempted. Local `.wandb/wandb/offline-run-*` files contain W&B data; no working cloud dashboard URL is claimed. After authentication/network access is restored, run:

```bash
../envs/g1_hmi_carry/bin/wandb sync /absolute/path/to/the/offline-run-directory
```

Training exit success is followed by full-checkpoint/ONNX/numerical validation and then independent A–E plus boundary/support/release evaluation,10 seeds each. No second Isaac process runs while training owns the GPU. Manual evaluation (run after training):

```bash
POLICY=/absolute/path/to/model_14999.onnx
../envs/g1_hmi_carry/bin/python scripts/carry/evaluate_unified_hoi.py \
  --policy "$POLICY" --seeds 10 --output ../artifacts/unified_hoi_hmi_stage1/NEW_EVALUATION
```

Outputs: `final_evaluation/evaluation.json`, per-case logs and rollout NPZ. Original physical acceptance is unchanged. Tests distinguish isolated pickup, loaded walking, validated single/repeated squat, full pickup→carry→putdown, and explicit putdown-support/release probes. Continuous walk→squat→walk remains missing from the data and is not fabricated or teleported. No Stage2 is started.

## Save-frequency correction

The first formal attempt (source7d456e6, learner3413459) was stopped very early at the user's request to change checkpoint interval500→2000. Its outputs remain in `formal_8192_15000_001/`, with `stop_reason.json`; no physical performance gate caused this stop. The replacement starts from scratch in `formal_8192_15000_002_save2000/` and runs one continuous15000-update invocation. There are no2000-update training segments or automatic resumes. Source/actual PID/config paths are recorded in that directory.

## 2026-11-22 reboot recovery

Host reboot interrupted the old run after its last logged iteration3782. Latest verified complete state is `model_02000.pt`, SHA256 `f8a5447bb85dbca02e0fc8623dcd14c5d7e888c7d6c13b669b8b0a07323b9451`. At the user's explicit latest instruction, recover this checkpoint rather than starting from scratch. Its2001 completed updates leave12999 additional updates to the total15000 target. The first resumed iteration must be2001; final must be14999. The unsaved1782 updates are not recovered or counted as retained learning.

Only launch/recovery accounting changed: optional explicit checkpoint argument, checksum/schema/manifest/protocol checks, optimizer/noise preservation, and resumed completion verification. PPO, action, data, physics, rewards and physical acceptance remain unchanged. The new output is `formal_8192_15000_003_resume02000_20261122/`. The training controller and TensorBoard run as user-level systemd units independent of the chat. No automatic retry/Stage2 is enabled; a future host reboot still interrupts the running simulator and requires a new explicit recovery.

At the user's request, TensorBoard now displays retained step0–2000 and resumed step2001 onward as one `stage1_continued` Run at port6015. Separate view directory: `tensorboard_continuation_20261122/`; source events are immutable.1,314,658 historical event records were retained,1,170,774 records on the old unsaved branch excluded from this view. A direct raw-event check verified reward steps0–2012 without gaps or duplicates; live events continue to append. The website's default reservoir displays a sample of the source points, not a new metric calculation. This view does not imply recovery of unsaved policy/simulator state.
