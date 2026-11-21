# Unified Full-body HOI Stage1 implementation and validation

Base: `6c3eed6462ddbcc9a4d4870c1bc06146d54b3dae`; new branch `feature/unified-hoi-stage1`. Date2026-11-21. The final implementation commit is available via `git log -1`.

## Outcome and recommendation

**The independent unified experiment and end-to-end training/evaluation infrastructure are implemented. Full unified HOI physics success is NOT established. Do not start15000 updates yet.** No usable pickup/carry/squat/putdown policy is claimed.

One shared HMI PPO, Track-only, unchanged four continuous Carry goals, an explicit three-way intention observation, six motion clips, exact hard-limit Reset, corrected post-action timing, retained reference-free delta action, phase-aware physical supervision, measured ground support, checkpoint integrity, resume, ONNX and no-reference inference are working. Original data, existing squat/walk experiment and historical results remain intact.

The minimal implementation plan was: (1) pin upstream and audit all frames; (2) create canonical FK/phase dataset without pretending to retarget grasp; (3) add isolated phase/observation/physics modules; (4) run unit, real contact, smoke, resume and inference/evaluation checks; (5) withhold exploratory/long training when physical gates fail. These steps were executed. A grasp retargeting solution and walk–squat–walk transition remain outstanding.

## Source restoration and complete motion audit

Contrary to the concern that the local original had been altered, all three full motion files are **byte-identical** to upstream HEAD `c353731999b3578c41ad5a00f896415b45e6a9f5` (remote HEAD was checked). Independent Git blob exports were retained in `../artifacts/unified_hoi_stage1/upstream_c353731/`; no existing source was overwritten.

| Upstream source | SHA256 |
|---|---|
| original full NPZ | `76077a5035726aabe25b084de5414f3113646c43ac1bfa6ccc0742e46b1a4cea` |
| full reframed | `827aced06e4111ade1bd38c9880cb76e870727438cc75fbcc2aee5b636edc5c9` |
| full reframed mirrored | `9b8fa055065e9df0892a2fbdd1aa6357b524b0cc0d851fc2ece3da954e26ab39` |

All325 frames were inspected: root/joint/object poses and velocities, wxyz quaternion conventions, collision-URDF FK, object convex-hull bottom, speed and hand vertex-to-hull gap proxy. The source has pickup/lowering/release **kinematic candidates**, not just the old110-frame crop.

| Candidate interval | Frames [start,end) | Evidence |
|---|---|---|
| reach/crouch | 0–25 (mirror0–27) | box remains near floor; hands approach |
| acquire-contact candidate | 25–55 (mirror27–55) | hand gap proxy falls below3cm; not a measured force assertion |
| lift candidate | 55–95 | convex bottom rises above3cm and then to carrying height |
| conservative loaded plateau | 95–205 | prior audited crop; bottom roughly0.57–0.61m and forward displacement |
| lower candidate | 205–271 | object descends back to floor |
| support-transfer candidate | 271–285 (mirror271–287) | low reference object speed, bottom near floor |
| release candidate | 285–325 (mirror287–325) | hands move away while object remains near stationary |

The full duration is6.48s. This is initially a within-reach floor pickup, not a demonstrated long-distance walking approach. The conservative95/205 boundaries are retained annotation choices, not exact measured contact events. Contact/liftoff/settle/release detectors and their thresholds are in the preparation code; labels remain explicitly kinematic until physical evidence supports them.

Machine-readable [phase audit](datasets/unified_hoi_v1/audit/phase_annotations.json), [manifest](datasets/unified_hoi_v1/manifest.json), [timeline](datasets/unified_hoi_v1/audit/MOTION_TIMELINE.md) and [plot](datasets/unified_hoi_v1/audit/motion_timeline.png) preserve boundaries, sampled values and provenance. Original reference bottom slightly penetrates the collision floor (millimetres, up to roughly9mm in mirrored lowering); this warning is not hidden or corrected by object teleports.

## Compatibility and derivation

Original body transforms differ from the current collision URDF FK by up to **10.16mm**. The new full/reframed/mirrored and loaded crop artifacts preserve all root/joint/object poses to float32, recompute body FK and all linear/angular velocities, and add actual hand frames. They do **not** silently replace wrist/arm grasp poses. Rechecked FK errors across all six clips are at most1.38e-7m. Both P0 12cm NPZs are exact copies with unchanged SHA and keep their independent P0-controller physics validation; failure of this task's simple position probe does not invalidate P0's different validated controller.

The original Forward wrist yaw near±0.05rad and wrist pitch about+0.2～0.3rad differ from P0 yaw near±1.614rad/pitch near-1.05rad. Earlier and current free-box probes cannot establish continuous bilateral grasp in the original loaded crop. This supports an unresolved physical/retargeting problem, **not proof that no controller or alternative grasp could ever execute the source motion**. Actual contact forces, not merely palm axes, determine grasp validity.

A bounded diagnostic arm-only IK study used five loaded source frames95/125/155/185/204 and two initial guesses per frame, preserving root/legs/waist/box. P0-relative hand SE3 targets still had best position residuals about3.5～6.5cm and orientation residuals about0.77～1.30rad. Solver termination did not mean accurate feasibility. Neither this local-search failure nor one P0 grasp target proves global infeasibility; it does show that simply copying P0 arm angles or forcing a common grasp pose is not a validated repair. Candidate poses are stored separately, marked non-motion/non-admitted/non-physics-validated, and were never inserted into training data.

Classification: body/FK alignment inconsistency is confirmed and canonicalized; a different feasible original grasp is **unverified**; current literal reference-position/contact probes **fail**, while universal contact infeasibility is not established. No physical compatibility success is claimed.

Measured PhysX contract: box mass1.100000024kg, diagonal inertia0.022000002kg·m²; robot material(static,dynamic,restitution)=(1.0,0.9,0), box=(0.6,0.6,0). Physics/PD1ms, policy20ms, decimation20, reference50Hz, robot solver16/8. Torque limits stay5–139Nm by joint, with exact vector retained in the audit; gains/scales remain those from the base `joint_delta_v1`. The inherited physics-report string says position offsets generically; decoder metadata and executed action term explicitly specify measured-current-joint delta, not fixed-default targets.

## Dataset and one-policy interface

The separate `datasets/unified_hoi_v1/` contains two full sequences, two loaded crops and two P0 squat clips. Families are not policies. Fixed environment quotas ensure family control-step coverage is near30%/35%/35% despite short clips and early failures. Within full-sequence random resets, mode-balanced starts and25% clip-first-frame starts provide acquisition/release exposure; loaded families retain HMI adaptive timestep bins. Eligible frames exclude terminal-only frames and are kinematic/hard-limit eligibility, not certified stable physical resets.

Actor frame119 = prior116 physical/4D-goal +3 intention one-hot; history3 → **357D**. Critic **187D** =119+68 reference-only privileged features. Pickup/carry/putdown come from phase annotations only during Stage1; deployed `UnifiedActor` requires explicit mode, supports symbolic mode names and never loads a Reference Loader. Walking/squatting share mode=carry. No motion ID, phase scalar, future pose or expert action is fed to Actor.

This intentionally starts from scratch; legacy348D Actor and mismatched manifests cannot resume. Metadata schema2 records dimensions, mode encoding, physical delta decoder, source fingerprint and parity. Stage2 must keep this new interface; the old Stage2 interface cannot be used unchanged. No Gen, AMP, world model, teacher/student, separate skill checkpoint or deployed trajectory playback was added.

## Physical phase supervision and temporal continuity

Original eight Robot/Object imitation terms and regularization are retained. Added physical pickup/putdown rewards use real forces, clearance and measured support. Grasp/slip terms are phase-masked so deliberate release is not rewarded as continued squeezing. Loaded carry keeps the prior physical gates and final acceptance functions unchanged.

- Pickup allows pre-contact hands. Physical acquisition requires bilateral contact, friction load fraction≥0.8, real clearance>3cm and no nonhand support. Acquisition is latched within an episode; dropping after acquisition remains a failure.
- Carry retains loss-of-grasp20ms-window logic,0.1s Reset grace,3cm floor clearance,0.5N undesired support detection, falls/separation/nonfinite safety and existing final side-grasp/slip thresholds.
- Putdown permits actual weight transfer to real ground and subsequent release. A support sample requires measured upward ground normal≥0.8 weight, bottom<3cm, speed<0.08m/s and angular speed<0.3rad/s. Stable support requires0.2s; final putdown success additionally requires0.5s stable released state, with nonhand box contact≤0.5N (a torso/knee pressing the box cannot qualify as release). Intent alone never establishes support.
- Noncarry deep forward lean is permitted only with positive body up-axis, pelvis≥0.45m and actual bilateral foot support (>5N each) when up-axis falls below0.5. This replaces a confirmed false fall classification for source root pitches exceeding60°. Carry retains its original absolute fall gate.
- Incidental nonhand contact on an actually stable supported box stays logged/penalized but is not treated as load-bearing body support in pickup/putdown. Loaded carry remains strict. Severe floor intrusion below-2cm remains a failure in every mode.

These are explicit **new experiment phase semantics**, not changes to the old experiment or its final Carry acceptance. Safety causes and raw undesired contacts remain logged. No groundless success, mass/gravity change, invisible support, weld, gantry or object state write was introduced.

Post-action reference k+1 timing and exact hard-limit Reset are inherited. A full source clip progresses continuously with no physical reset on task-mode change. Independent clip episodes Reset normally; clips are never stitched by teleportation. Real policy boundary probes recorded modes[0,1] and[1,2] before failing; they validate interface/timing, **not learned transition success**. No walk→squat→walk reference exists; caseF is explicitly unavailable.

## Tests and actual experiments

Local evidence root: `../artifacts/unified_hoi_stage1/`.

1. Carry/Unified and upstream command/termination/WBT tests: **105 passed**. Includes phase-specific failures, unchanged loaded Carry causes, family coverage, one-hot history switching and old interfaces.
2. Real source probes with3 exact Reset replicas: original source pickup/full sequence fail around0.16s from body-support contact; loaded crop fails around0.12s from loss of grasp; P0 simple-position probes fail around0.26s. This is not P0's validated controller and is not a learned Actor.
3. Confirmed implementation corrections: resolved actual ground collider `/World/ground/terrain/GroundPlane/CollisionPlane` after a wildcard sensor returned zero; corrected legitimate deep-lean classification in noncarry; corrected Python-float diagnostic counters to tensors for HMI's logging meters; replaced a single-environment Reset mode bias with independent random mode starts (regression tested and smoke rerun). The failed first smoke and first probes are retained.
4. Ground support sensor is physically verified. Some putdown resets produce large impact/support impulses; these do not imply stable release. Remaining local probes fail from nonhand contact, missing grasp or missing foot support.
5. Final smoke: **256 envs,4 updates, seed42**,48.85s including startup/export,3520MiB peak GPU. PPO/finite-value/357D/187D checks passed; all checkpoint and ONNX sidecars were produced. This is a chain test only.
6. Manual resume: model00003→total5 performed **one** update; model, optimizer, normalizers, sampler and environment config restoration verified;23.56s,3424MiB peak GPU. Physical episodes restart, not bit-exact simulator state.
7. ONNX/PyTorch maximum raw-action error **1.31e-6**. Independent process forbidding command/MotionLoader imports loaded the policy and inferred pickup/carry/putdown explicitly. Legacy CarryActor rejects this schema.
8. All available A–E and local boundary/support/release cases evaluated with3 seeded policy initial-velocity perturbations, std0.001rad/s. **All cases0/3; final passed=false**. No successful usable policy claimed.
9. TensorBoard endpoint6014 returned HTTP200. GUI/video entry is provided, but GUI playback was not visually verified here.

| Family | Observed steps | Completed-episode steps | Observed fraction | Smoke mean episode s | Bilateral contact | Robot/Object error m |
|---|---:|---:|---:|---:|---:|---:|
| Full sequence |7392|7031|30.078%|0.16485|3.228%|0.03907 /0.02057|
| Loaded locomotion |8640|8383|35.156%|0.12105|7.086%|0.01855 /0.02907|
| Loaded squat/stand |8544|8271|34.766%|0.12317|15.775%|0.01563 /0.02995|

Observed intention steps: pickup4527, carry18664, putdown1385 of24576. Thus putdown gets only5.64% of actual steps despite balanced phase Reset attempts: early failure still distorts **phase** coverage, and is reported rather than hidden. Family quotas prevent the corresponding family-step distortion.

| Policy case | Example first-seed survival | Main failure |
|---|---:|---|
| A pickup |0.32s|reference orientation tracking failure|
| B loaded walk |0.24s|loss of grasp, contact/slip/friction failures|
| C single squat |0.16s|nonhand support, insufficient friction/contact|
| D repeated squat |0.16s|same|
| E complete sequence |0.32s|orientation tracking failure during pickup|
| pickup→carry boundary |0.12s|loss of grasp after mode transition|
| carry→putdown boundary |0.12s|loss of grasp|
| release tail |0.28s|reference orientation tracking failure|

Evaluation originally reused one scene across cases; identical A/E first states produced inconsistent initial impacts. Reset state equality did not rule out PhysX history. The evaluator now launches each case in its own process, serially, with no concurrent GPU evaluation. Two full isolated suites confirmed the same failures; final suite took147.65s, peak3234MiB. Every case Reset matched joint/root/box reference exactly before physics; arbitrary-frame contact equilibrium remains unverified.

Every seed, terminal state, orientation/force/slip/clearance/support metric and cause is in `independent_eval_002/evaluation.json` and NPZ rollouts; the table is not a selected-success presentation. The available2.18s walking clip is not a20s carrying robustness test. Isolated source-phase Reset probes do not prove complete task continuity.

Family smoke torque-clip fractions (completed episodes) were0.0310% full-family,0.00221% locomotion,0.3542% squat. Low clipping does not imply enough contact force. First-seed isolated loaded-walk evaluation had46.25% bilateral-contact samples, only0.0588 upward friction/weight mean and0.0835m object tracking error before failure. Squat had82.50% bilateral contact,0.2357 friction/weight and0.0471m object error; neither meets acceptance. Full per-phase force, slip, ground support, torque clipping, hard-limit violations, acceleration and foot sliding are in the tracked JSON summaries. No full-run motion quality or grasp-transition success is claimed.

## Files and reproduction

New modules: `carry/unified.py`, `unified_presets.py`, `unified_simulator.py`, `unified_ppo.py`, `unified_inference.py`; new preparation, training, evaluation and grasp-diagnosis scripts; new dataset/audits and tests. Shared export/checkpoint/worker code gained explicit schema-gated dimensions; PPO algorithm, old motion files, old Stage1 classes/config, Carry termination and final acceptance remain unchanged.

Copyable tested commands, resume, TensorBoard, viewer and schema details: [README_UNIFIED_HOI_STAGE1.md](README_UNIFIED_HOI_STAGE1.md).

Smoke model (NOT final): `../artifacts/unified_hoi_stage1/smoke_003_data/tensorboard/WholeBodyTracking/20261121_100537-unified_hoi_stage1-locomotion/model_00003.pt` and `.onnx`. Full logs/config/manifest accompany it. These development runs record base6c3eed6 plus dirty status/patch; the new files are versioned in this delivery commit. Future launches also archive hashed tracked/untracked worktree text, rather than relying on HEAD-only snapshots. Large checkpoints remain local, not pushed into Git. Compact measured evidence is committed under `datasets/unified_hoi_v1/audit/`: `bounded_policy_evaluation.json`, `reference_probe_evaluation.json`, `training_smoke_summary.json`, `fk_validation.json` and `standalone_inference.json`; full NPZ rollouts, TensorBoard and console logs remain in the local evidence root.

## Blocking work and minimal resolution path

Do not consume the15000-update budget. The original HMI full trajectory is present, but physical grasp/support/balance compatibility with current collision geometry is not established; the canonical FK export alone does not fix it. Exploratory long PPO was deliberately skipped after failing physical probes; two successful 4-update smoke tests plus one recovery update ran (one earlier smoke failed before any update). No exploratory learning experiment beyond those chain checks ran.

The next minimal work is a separately versioned, contact-constrained retargeting/validation experiment: search for a feasible actual-hemisphere grasp (it need not copy P0 joint angles or exact hand orientation); preserve source root/locomotion/lift/place semantics where physically possible; adjust only necessary upper body/waist/foot balance with logged residuals, velocities, torque and collision checks; validate free-box contact acquisition, support transfer and release. Do not insert the unsuccessful arm-only candidates into training. Keep both validated squat references intact. Add a genuine physically checked loaded walk–squat–walk transition before claiming F.

After those issues are resolved, repeat bounded policy experiments and environment scaling benchmarks, then independently evaluate all task families and true full episodes. A boolean admission flag or reward increase is not evidence. No reference was relabeled physics-validated, no thresholds were secretly relaxed to obtain a pass, and no untrained model was marked final.
