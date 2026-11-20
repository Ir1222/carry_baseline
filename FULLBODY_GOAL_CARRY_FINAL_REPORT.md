# FullBody Goal Carry — measured experiment report

Status: **RUNNING / STAGE1**. This file is a progress report while RUNNING. Only independent physical acceptance grants a usable policy.

Branch: `feature/fullbody-goal-carry-autotrain`. Current source commit: `b014d74413a42bcb3fa0561b2a8a5ff6bc2b63d2`. P0 preservation commit: `ed106a7`. Initial run source: `90cb7abba96283b98b059ed268e7f9c1b5f2ae40`. Additional source versions are retained as `source_*.tar`.

Run directory: `/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333`. PID, process identity and current command: {"name": "stage1_training", "pid": 367494, "identity": "163886414", "output": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/jobs/stage1_training_1795153709249524023", "started_at": 1795153709.2513907, "stage": "stage1"}

## P0 and source integrity

{
  "passed": true,
  "policy_success": false,
  "immutable_p0_sources_unchanged": true,
  "cpu_tests": "20 passed",
  "physics_evidence": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/physics_interface_gate_001.json",
  "format_fk_evidence": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/reference_v1/fresh_format_fk_validation.json",
  "fullbody_stage1_smoke": "smoke_stage1_003",
  "fullbody_stage2_resume_onnx_smoke": "smoke_stage2_002",
  "independent_evaluators": [
    "evaluator_stage1_003_data",
    "evaluator_goal_003_data"
  ],
  "forward_admitted": false,
  "forward_failures": "forward_hold_diagnosis_003_data/validation.json",
  "note": "Engineering gates passed; independent policy acceptance has NOT passed. Forward still quarantined.",
  "source_commit": "90cb7abba96283b98b059ed268e7f9c1b5f2ae40",
  "final_stage1_smoke": "final_gate_stage1_001",
  "final_stage2_resume_onnx_smoke": "final_gate_stage2_001",
  "viewer_and_lateral_acceptance_evidence": "viewer_failure_002_data/evaluation.json"
}

P0 verification is controller-only. Source NPZ checksums and motion family priors are in `../artifacts/fullbody_goal_carry/reference_v1/manifest.json`. Original P0 assets, old resets and checkpoints were preserved.

## Actual physics and controller interface

{
  "passed": true,
  "policy_success": false,
  "scope": "Physics/model/shape/legitimate high-low states",
  "physics": {
    "mass_kg": [
      1.100000023841858
    ],
    "inertia": [
      0.02200000174343586,
      0.0,
      0.0,
      0.0,
      0.02200000174343586,
      0.0,
      0.0,
      0.0,
      0.02200000174343586
    ],
    "robot_material": [
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ],
      [
        1.0,
        0.8999999761581421,
        0.0
      ]
    ],
    "object_material": [
      [
        0.6000000238418579,
        0.6000000238418579,
        0.0
      ]
    ],
    "physics_dt": 0.001,
    "policy_dt": 0.02,
    "pd_hz": 1000.0,
    "reference_fps": 50,
    "decimation": 20,
    "solver_robot": [
      16,
      8
    ],
    "torque_limits": [
      88.0,
      139.0,
      88.0,
      139.0,
      50.0,
      50.0,
      88.0,
      139.0,
      88.0,
      139.0,
      50.0,
      50.0,
      88.0,
      50.0,
      50.0,
      25.0,
      25.0,
      25.0,
      25.0,
      25.0,
      5.0,
      5.0,
      25.0,
      25.0,
      25.0,
      25.0,
      25.0,
      5.0,
      5.0
    ],
    "object_urdf": "/home/han/pyx/g1_carry_baseline_new/HMI/src/holosoma/holosoma/data/motions/g1_29dof/whole_body_tracking/objects_largebox.urdf",
    "robot_urdf": "/home/han/pyx/g1_carry_baseline_new/HMI/src/holosoma/holosoma/data/robots/g1/main_mesh_collision_halfspherehand.urdf",
    "control": "PPO joint-position offsets with PD each physics substep; no P0 feedforward or WBC",
    "p_gains": [
      160.71694946289062,
      396.3937072753906,
      160.71694946289062,
      396.3937072753906,
      250.0,
      250.0,
      160.71694946289062,
      396.3937072753906,
      160.71694946289062,
      396.3937072753906,
      250.0,
      250.0,
      160.71694946289062,
      114.0049819946289,
      114.0049819946289,
      57.00249099731445,
      57.00249099731445,
      57.00249099731445,
      57.00249099731445,
      57.00249099731445,
      67.11331176757812,
      67.11331176757812,
      57.00249099731445,
      57.00249099731445,
      57.00249099731445,
      57.00249099731445,
      57.00249099731445,
      67.11331176757812,
      67.11331176757812
    ],
    "d_gains": [
      5.115779399871826,
      12.617603302001953,
      5.115779399871826,
      12.617603302001953,
      12.0,
      12.0,
      5.115779399871826,
      12.617603302001953,
      5.115779399871826,
      12.617603302001953,
      12.0,
      12.0,
      5.115779399871826,
      3.6288914680480957,
      3.6288914680480957,
      1.8144457340240479,
      1.8144457340240479,
      1.8144457340240479,
      1.8144457340240479,
      1.8144457340240479,
      2.1362829208374023,
      2.1362829208374023,
      1.8144457340240479,
      1.8144457340240479,
      1.8144457340240479,
      1.8144457340240479,
      1.8144457340240479,
      2.1362829208374023,
      2.1362829208374023
    ],
    "action_scales": [
      0.1368866264820099,
      0.0876653715968132,
      0.1368866264820099,
      0.0876653715968132,
      0.05000000074505806,
      0.05000000074505806,
      0.1368866264820099,
      0.0876653715968132,
      0.1368866264820099,
      0.0876653715968132,
      0.05000000074505806,
      0.05000000074505806,
      0.1368866264820099,
      0.1096443235874176,
      0.1096443235874176,
      0.1096443235874176,
      0.1096443235874176,
      0.1096443235874176,
      0.1096443235874176,
      0.1096443235874176,
      0.01862521842122078,
      0.01862521842122078,
      0.1096443235874176,
      0.1096443235874176,
      0.1096443235874176,
      0.1096443235874176,
      0.1096443235874176,
      0.01862521842122078,
      0.01862521842122078
    ]
  },
  "object_flags": {
    "kinematic": false,
    "rigid_enabled": true,
    "disable_gravity": false
  },
  "states": [
    {
      "frame": 0,
      "pelvis_height": [
        0.7249915599822998,
        0.7249915599822998,
        0.7249916195869446,
        0.7249915599822998,
        0.7249915599822998,
        0.7249915599822998,
        0.7249917387962341,
        0.7249917387962341
      ],
      "box_clearance": [
        0.6519116759300232,
        0.6519116759300232,
        0.6519116759300232,
        0.6519116759300232,
        0.6519116759300232,
        0.6519116759300232,
        0.6519116759300232,
        0.6519116759300232
      ],
      "physical_failure": [
        false,
        false,
        false,
        false,
        false,
        false,
        false,
        false
      ]
    },
    {
      "frame": 175,
      "pelvis_height": [
        0.6213016510009766,
        0.6213010549545288,
        0.6212999820709229,
        0.6213006377220154,
        0.6213012933731079,
        0.621301531791687,
        0.6213006377220154,
        0.6213001012802124
      ],
      "box_clearance": [
        0.5331040620803833,
        0.5331039428710938,
        0.5331043004989624,
        0.533104419708252,
        0.5331041812896729,
        0.5331040024757385,
        0.5331037044525146,
        0.5331040024757385
      ],
      "physical_failure": [
        false,
        false,
        false,
        false,
        false,
        false,
        false,
        false
      ]
    }
  ]
}

The PPO actor supplies position offsets at 50Hz. PD runs at 1000Hz within the original torque limits. There is no P0 WBC/static-force feedforward, object attachment, gantry support or post-reset object pose write.

## Reference admission and unresolved forward capability

The direct forward trial failed its pre-motion grip gate. A separate 3-pose × 3-force diagnostic passed 0/9 cases. Static pose diagnostics are not a certification of continuous forward locomotion. No forward motion is admitted; vx remains 0 rather than mixing a failed clip into training.

Failure evidence: `forward_probe_001_data/rollout.npz`, `forward_probe_001_data/pre_motion_gate.json`, `forward_hold_diagnosis_003_data/validation.json`. Additional failed engineering runs are also retained.

## Goal distribution and style

{
  "height_low": 0.6068800687789917,
  "height_high": 0.7268800735473633,
  "height_rate": 0.11247000098228455,
  "vx_high": 0.0,
  "forward_admitted": false,
  "reference_fps": 50,
  "episode_seconds": 30.0
}

Four-dimensional interface [vx,vy,yaw_rate,pelvis_height], 348D Actor and 184D Critic. Gen vy/yaw are zero. Six conditional modes sample vx/h independently in mixed mode; half the environments execute a continuous standing→squat→low hold→stand cycle. Height transitions use reference-derived bounded smoothstep rates. Style matches full-body posture and hand-box geometry using height, ascent/descent direction, vx and temporal continuity. Compatibility reduces its influence outside the reference distribution. Deployment does not load references.

## Training configuration, resource benchmark and budgets

{
  "candidates": [
    4096,
    8192
  ],
  "fixed_num_envs": null,
  "warmup_updates": 4,
  "benchmark_updates": 12,
  "benchmark_timeout_s": 1800,
  "stage1_gpu_hours": 24.0,
  "stage2_gpu_hours": 24.0,
  "eval_every": 500,
  "first_eval_updates": 500,
  "checkpoint_every": 500,
  "evaluation_seeds": 10,
  "final_seeds": 10,
  "evaluation_timeout_s": 1800,
  "minimum_free_gib": 15.0,
  "headroom_mib": 4096,
  "stage1_max_updates": 15000,
  "stage2_max_updates": 20000,
  "stagnation_windows": 3,
  "minimum_improvement": 0.01,
  "poll_seconds": 10,
  "report_seconds": 60,
  "max_corrections": 3,
  "source_commit": "90cb7abba96283b98b059ed268e7f9c1b5f2ae40"
}

[
  {
    "num_envs": 4096,
    "stable": true,
    "samples_per_iteration": 98304,
    "minibatches": 64,
    "epochs": 5,
    "steps_per_s": 8947.531230301614,
    "rollout_s": 10.339841171517037,
    "simulation_s": 9.659425499849021,
    "update_s": 0.6445119869895279,
    "iterations_per_s": 0.09103858785035279,
    "peak_gpu_memory_mib": 5860,
    "evidence": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/jobs/benchmark_4096_1795152814934836057",
    "physx_errors": 0,
    "nan_errors": 0,
    "crash_exit_code": 0
  },
  {
    "num_envs": 8192,
    "stable": true,
    "samples_per_iteration": 196608,
    "minibatches": 128,
    "epochs": 5,
    "steps_per_s": 12431.143144491927,
    "rollout_s": 14.525944530614652,
    "simulation_s": 13.680859697167762,
    "update_s": 1.2975117255700752,
    "iterations_per_s": 0.06319731819710007,
    "peak_gpu_memory_mib": 8302,
    "evidence": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/jobs/benchmark_8192_1795153185087080876",
    "physx_errors": 0,
    "nan_errors": 0,
    "crash_exit_code": 0
  }
]

Every job retains its exact command, source version, console, per-iteration timing and GPU samples. See `dashboard/` for TensorBoard and `jobs/*/iterations.jsonl` for simulation/learner timings. Training and evaluation use the GPU serially. Stage 1 starts from scratch; Stage 2 requires the physical Stage 1 gate.

## Stage 1 measured evaluations

[]

## Stage 2 measured evaluations

[]

## Style ablation

"Not executed; cannot claim an improvement"

## Motion-quality analysis

{}

## Best checkpoints, acceptance and inference artifacts

{
  "best_stage1": null,
  "best_stage2": null,
  "valid_stage1": null,
  "valid_stage2": null,
  "final_checkpoint": null
}

Unaccepted models stay in best_stage*/ and must not be presented as usable final policies. Accepted models, full config and ONNX metadata are copied into deliverables/. ONNX parity is tested at training export and the CPU exporter; per-model errors are in .actor.json. Viewer/interactive/evaluation/export commands are in README_FULLBODY_CARRY.md.

## Stop reason, failures and remaining work

{
  "blocker": null,
  "gpu_seconds": {
    "stage1": 31.492636112961918
  },
  "stage1_corrections": null,
  "stage2_corrections": null,
  "last_job": {
    "output": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/jobs/stage1_training_1795153506526842935",
    "exit_code": 0,
    "wall_seconds": 31.492636112961918,
    "peak_gpu_memory_mib": 1116,
    "error": "Stop requested; valid checkpoints retained",
    "failure_evidence": [],
    "worker": {}
  }
}

Unimplemented or unverified capabilities must be read from the measured acceptance tables, not inferred from finite PPO losses or rising rewards. Forward reference contact consistency is a known blocker. No unseen forward+height combinations, lateral motion or turning are certified. For vy/yaw extension, first admit compatible dynamic references and separately benchmark each command family. Failed policies and failed references are retained rather than hidden.

## Reproduction

See README_FULLBODY_CARRY.md for environment activation, validation, Stage 1/2, resume, automatic controller, TensorBoard, checkpoint evaluation, ONNX export, Viewer, interactive four-dimensional commands and goal grid. TensorBoard for this workspace: http://127.0.0.1:6011 .
