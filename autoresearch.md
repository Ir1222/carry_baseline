# Stage1 repair: bounded comparison

Baseline: d2281cf; unchanged NPZ/physics/rewards/termination/final acceptance.
Objective: exact hard-limit-valid Reset, post-action k+1 tracking, and better early learning for BOTH action families.

Maximum two from-scratch PPO comparisons: 256 environments, 32 updates, seed42, original init std0.3 and original effort/Kp scales. No long training or Stage2.

1. fixed: repair Reset and time alignment, retain old fixed-default action decoding.
2. joint_delta: additionally test reference-free q_at_policy_step + scale*a held during 20 PD substeps. No gain, torque-limit, action-scale, reward or dataset change.

Keep an action mode only with measured evidence; if forward remains unsuccessful report NOT READY. Preserve failed trials. Static FK found forward hemisphere axes strongly vertical, unlike validated lateral-grasp squat. Do not replace source data to hide this difference.

The first dense all-frame CPU geometry pass was deliberately stopped before completion because mesh-SDF enumeration was excessive. Use explicit stride20 samples plus all-frame joint statistics, and label sampled geometry honestly.

Artifacts: ../artifacts/stage1_repair_validation/. See STAGE1_REPAIR_VALIDATION.md for final decisions and metrics.

Final decision: keep exact Reset and post-action clock. Keep joint_delta as the default Stage1 repair candidate, with fixed still explicitly selectable; decoder metadata and checkpoint guards prevent mixed semantics. Forward contact and torque clipping improve, but physical grasp/reference compatibility remains unpassed, so do not recommend or launch 15000 updates. Both 32-update models and all failed probes remain in artifacts. No additional optimization loop was run.
