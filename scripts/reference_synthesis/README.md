# Continuous side-grasp carry / squat / stand

These standalone tools generate and validate reference motions. They do not register experiments or change PPO, Actor/Critic, rewards, command sampling, or training resets.

Run from the workspace **above `HMI/`**:

```bash
cd /home/han/pyx/g1_carry_baseline_new
source /home/han/miniconda3/etc/profile.d/conda.sh
conda activate "$PWD/envs/g1_hmi_carry"
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV LD_LIBRARY_PATH
export PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
```

## Inspect existing evidence

```bash
python HMI/scripts/reference_synthesis/view.py \
  --evidence artifacts/carry_reference_synthesized/evidence/squat_12cm_001_data --port 8013
```

Open `http://localhost:8013`. Orange is the **measured free-body Isaac Sim rollout**; blue is the reference. `Frame`, `Play`, and `Play FPS` allow exact inspection. Contact markers and arrows come from measured, object-filtered PhysX contact data. The side-by-side reference can be overlaid. The viewer replays saved data; it does not itself validate physics.

For the repeated trial, substitute `evidence/repeated_12cm_001_data`. Run `review.py --evidence ... --motion ...` first when adding a new trial, to create its viewer metadata, actual-motion NPZ, CSV and PNG/SVG figures.

## Reproduce actual physics, optionally with Isaac Sim GUI

Always use a fresh evidence directory:

```bash
python HMI/scripts/reference_synthesis/physics.py \
  --output artifacts/carry_reference_synthesized/evidence/manual_single_data \
  --motion artifacts/carry_reference_synthesized/validated_motions/continuous_grasped_squat_stand.npz \
  --reset-state artifacts/carry_reference_synthesized/verified_side_grasp_reset.json \
  --gain 4 --balance 0 --dt .001 --wbc --view
```

Omit `--view` for headless execution. The 2 s pre-motion hold is part of the same uninterrupted episode. The program refuses to start the squat if that hold fails. After reset, runtime guards reject writes to robot root / object state. Only joint torques act on the robot; gravity and contacts act on the free box. Original joint effort/velocity limits apply.

## Rebuild everything into a new directory

```bash
python HMI/scripts/reference_synthesis/run_pipeline.py \
  --output artifacts/carry_reference_synthesis_reproduction_001
```

The bounded pipeline audits the immutable originals, uses full-body constrained IK for side grasp, tests a finite standing-grasp sweep, rejects failed resets, optimizes and physically tests 10/12 cm single cycles, and tests two cycles at the largest passed depth. Only passed trajectories enter `validated_motions/`. A failure is retained as evidence and never promoted. The exact child commands, source snapshots, logs and results are saved. An all-failed standing sweep stops before any squat synthesis.

## Data contract

- `source_crops/`: bit-exact crops of original frames `[95,205)`, all original arrays preserved.
- `motions_kinematic/original_forward_carry*.npz`: all original joints, root and object motion preserved; body FK/derivatives regenerated for the **original half-sphere-hand collision URDF**, including the actual `left/right_foot_contact_point` frames. These original forward clips have **not** passed this new physical controller test.
- `motions_kinematic/`: all candidates, including failures; never use this whole directory for training.
- `validated_motions/`: only physically passed references; sidecars link to the raw physical evidence and its SHA256. `motion_manifest.json` is the authoritative status inventory.
- NPZ `joint_pos=[xyz,wxyz,29 joints]`, `joint_vel=[world linear velocity,world angular velocity,29 joint velocities]`. All body and object quaternions are **wxyz**. Coordinates are world Z-up; FPS=50. Velocities are clip-safe finite differences, angular velocities are rotation-log differences. Actual rollout NPZ/CSV retain measurements at 1000 Hz; downsampled actual-motion exports use 50 Hz.
- Source meshes and original NPZ files are immutable and hashed. The actual LargeBox is kept at scale 1; its axis-aligned bounding box is not its physical side-face frame.

```bash
python HMI/scripts/reference_synthesis/verify.py
python HMI/scripts/reference_synthesis/audit_imports.py \
  --evidence artifacts/carry_reference_synthesized/evidence/repeated_12cm_001_data
python HMI/scripts/reference_synthesis/test_acceptance.py \
  --evidence artifacts/carry_reference_synthesized/evidence/squat_12cm_001_data \
  --motion artifacts/carry_reference_synthesized/motions_kinematic/continuous_grasped_squat_stand_12cm.npz
```

`verify.py` checks actual HMI `MotionLoader` loading, names, quaternion norms, finite values, derivatives, FK, original checksums, and protected training-file checksums. `test_acceptance.py` requires a real passing rollout and verifies that injected no-friction, detached-hand, ground-contact, torso-support, foot-slip, joint-limit and no-squat failures are rejected.

## Scope of the physics result

Validation applies to the recorded deterministic model, 1.1 kg free LargeBox, original geometry, fixed materials and 1 ms joint-control timestep. It is not validation of a learned PPO policy, hardware, mass randomization, or the old 5 ms/small-box/palm-support training setup. Do not point the old simplified carry task at these files without an explicitly authorized matching-model integration. No training is started by these tools.
