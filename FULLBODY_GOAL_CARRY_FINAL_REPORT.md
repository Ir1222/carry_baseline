# FullBody Goal Carry — measured experiment report

Status: **BLOCKED / BLOCKED**. This file is a progress report while RUNNING. Only independent physical acceptance grants a usable policy.

Branch: `feature/fullbody-goal-carry-autotrain`. Current source commit: `280dc9ae960614fffdb9f1ec798678635a6a6506`. P0 preservation commit: `ed106a7`. Initial run source: `90cb7abba96283b98b059ed268e7f9c1b5f2ae40`. Additional source versions are retained as `source_*.tar`.

Run directory: `/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333`. PID, process identity and current command: null

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

[
  {
    "passed": false,
    "score": 0.0,
    "suite": "stage1",
    "groups": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "trials": [
      {
        "scenario": "clip_0",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.033845189958810806,
          0.08077344298362732,
          0.4894789159297943,
          0.00947879534214735
        ],
        "steady_command_mae": [
          0.033845189958810806,
          0.08077344298362732,
          0.4894789159297943,
          0.00947879534214735
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.10679884254932404,
        "min_box_clearance_m": 0.5826303958892822,
        "pelvis_amplitude_m": 0.00749659538269043,
        "normal_forces_mean_n": [
          8.886578559875488,
          8.587066650390625
        ],
        "friction_weight_ratio_mean": 0.6134033799171448,
        "normal_vertical_fraction_max": 0.008729996159672737,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.501971244812012,
        "foot_slip_speed_mean_m_s": 0.03288116306066513,
        "joint_speed_rms": 1.2705327272415161,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.028294742107391357,
        "object_tracking_error_m": 0.03177409619092941,
        "object_tracking_error_rad_max": 0.0638560801744461,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.0344049409031868,
          0.07948581874370575,
          0.5124813318252563,
          0.009492218494415283
        ],
        "steady_command_mae": [
          0.0344049409031868,
          0.07948581874370575,
          0.5124813318252563,
          0.009492218494415283
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.10750260949134827,
        "min_box_clearance_m": 0.5826383829116821,
        "pelvis_amplitude_m": 0.007484257221221924,
        "normal_forces_mean_n": [
          8.893798828125,
          8.5518217086792
        ],
        "friction_weight_ratio_mean": 0.6080009937286377,
        "normal_vertical_fraction_max": 0.007253007031977177,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.800935745239258,
        "foot_slip_speed_mean_m_s": 0.03283294290304184,
        "joint_speed_rms": 1.268882393836975,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02841448225080967,
        "object_tracking_error_m": 0.03195952624082565,
        "object_tracking_error_rad_max": 0.06210789829492569,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03555429354310036,
          0.08205439150333405,
          0.49888482689857483,
          0.009559405036270618
        ],
        "steady_command_mae": [
          0.03555429354310036,
          0.08205439150333405,
          0.49888482689857483,
          0.009559405036270618
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.10652169585227966,
        "min_box_clearance_m": 0.5825777053833008,
        "pelvis_amplitude_m": 0.007375240325927734,
        "normal_forces_mean_n": [
          9.246617317199707,
          8.500967979431152
        ],
        "friction_weight_ratio_mean": 0.6130994558334351,
        "normal_vertical_fraction_max": 0.007661697920411825,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.34227466583252,
        "foot_slip_speed_mean_m_s": 0.03269874304533005,
        "joint_speed_rms": 1.2721412181854248,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02856130339205265,
        "object_tracking_error_m": 0.03199416771531105,
        "object_tracking_error_rad_max": 0.06374278664588928,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03375326469540596,
          0.0832815021276474,
          0.5053992867469788,
          0.009562778286635876
        ],
        "steady_command_mae": [
          0.03375326469540596,
          0.0832815021276474,
          0.5053992867469788,
          0.009562778286635876
        ],
        "contact_continuity": 0.14000001549720764,
        "max_hand_slip_m": 0.10719271749258041,
        "min_box_clearance_m": 0.5820483565330505,
        "pelvis_amplitude_m": 0.007452487945556641,
        "normal_forces_mean_n": [
          9.903156280517578,
          8.47801685333252
        ],
        "friction_weight_ratio_mean": 0.721723735332489,
        "normal_vertical_fraction_max": 0.002586039947345853,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.246953010559082,
        "foot_slip_speed_mean_m_s": 0.03321836143732071,
        "joint_speed_rms": 1.2897313833236694,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02888673171401024,
        "object_tracking_error_m": 0.033613190054893494,
        "object_tracking_error_rad_max": 0.05947696790099144,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03434082493185997,
          0.0815795511007309,
          0.5169883370399475,
          0.009536015801131725
        ],
        "steady_command_mae": [
          0.03434082493185997,
          0.0815795511007309,
          0.5169883370399475,
          0.009536015801131725
        ],
        "contact_continuity": 0.15000002086162567,
        "max_hand_slip_m": 0.10796065628528595,
        "min_box_clearance_m": 0.5815376043319702,
        "pelvis_amplitude_m": 0.007485806941986084,
        "normal_forces_mean_n": [
          9.608985900878906,
          8.620111465454102
        ],
        "friction_weight_ratio_mean": 0.6720105409622192,
        "normal_vertical_fraction_max": 0.0017198092537000775,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.530997276306152,
        "foot_slip_speed_mean_m_s": 0.0334048792719841,
        "joint_speed_rms": 1.2865872383117676,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.028775956481695175,
        "object_tracking_error_m": 0.03368593007326126,
        "object_tracking_error_rad_max": 0.06037409231066704,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03297266364097595,
          0.07977794110774994,
          0.5018573999404907,
          0.009411633014678955
        ],
        "steady_command_mae": [
          0.03297266364097595,
          0.07977794110774994,
          0.5018573999404907,
          0.009411633014678955
        ],
        "contact_continuity": 0.14000001549720764,
        "max_hand_slip_m": 0.10713078081607819,
        "min_box_clearance_m": 0.5819868445396423,
        "pelvis_amplitude_m": 0.007451295852661133,
        "normal_forces_mean_n": [
          9.617790222167969,
          8.583746910095215
        ],
        "friction_weight_ratio_mean": 0.6663500666618347,
        "normal_vertical_fraction_max": 0.0007963133975863457,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.333730697631836,
        "foot_slip_speed_mean_m_s": 0.033502284437417984,
        "joint_speed_rms": 1.282110333442688,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.028567185625433922,
        "object_tracking_error_m": 0.03314030170440674,
        "object_tracking_error_rad_max": 0.061335284262895584,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.034014992415905,
          0.08320768922567368,
          0.5133852958679199,
          0.009444355964660645
        ],
        "steady_command_mae": [
          0.034014992415905,
          0.08320768922567368,
          0.5133852958679199,
          0.009444355964660645
        ],
        "contact_continuity": 0.14000001549720764,
        "max_hand_slip_m": 0.10801367461681366,
        "min_box_clearance_m": 0.5815356969833374,
        "pelvis_amplitude_m": 0.007594585418701172,
        "normal_forces_mean_n": [
          9.599678993225098,
          8.425755500793457
        ],
        "friction_weight_ratio_mean": 0.7433089017868042,
        "normal_vertical_fraction_max": 0.002980461809784174,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.694323539733887,
        "foot_slip_speed_mean_m_s": 0.0331135019659996,
        "joint_speed_rms": 1.2878273725509644,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02884938381612301,
        "object_tracking_error_m": 0.03388423100113869,
        "object_tracking_error_rad_max": 0.05821932852268219,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.0340946763753891,
          0.08158843219280243,
          0.486645370721817,
          0.009454691782593727
        ],
        "steady_command_mae": [
          0.0340946763753891,
          0.08158843219280243,
          0.486645370721817,
          0.009454691782593727
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.10650632530450821,
        "min_box_clearance_m": 0.582990288734436,
        "pelvis_amplitude_m": 0.007361948490142822,
        "normal_forces_mean_n": [
          9.193550109863281,
          8.481197357177734
        ],
        "friction_weight_ratio_mean": 0.623384416103363,
        "normal_vertical_fraction_max": 0.0072829946875572205,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 13.97717571258545,
        "foot_slip_speed_mean_m_s": 0.032626014202833176,
        "joint_speed_rms": 1.270796298980713,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.028395509347319603,
        "object_tracking_error_m": 0.03177490830421448,
        "object_tracking_error_rad_max": 0.06363555043935776,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03352691978216171,
          0.08323561400175095,
          0.49731341004371643,
          0.009593379683792591
        ],
        "steady_command_mae": [
          0.03352691978216171,
          0.08323561400175095,
          0.49731341004371643,
          0.009593379683792591
        ],
        "contact_continuity": 0.15000002086162567,
        "max_hand_slip_m": 0.10657531023025513,
        "min_box_clearance_m": 0.5822458267211914,
        "pelvis_amplitude_m": 0.0074610114097595215,
        "normal_forces_mean_n": [
          9.9480619430542,
          8.646636962890625
        ],
        "friction_weight_ratio_mean": 0.7507079243659973,
        "normal_vertical_fraction_max": 0.0014593320665881038,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.157182693481445,
        "foot_slip_speed_mean_m_s": 0.032321929931640625,
        "joint_speed_rms": 1.2838066816329956,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02870357409119606,
        "object_tracking_error_m": 0.03330067917704582,
        "object_tracking_error_rad_max": 0.06141554191708565,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.034418120980262756,
          0.08344954252243042,
          0.48190632462501526,
          0.009500646963715553
        ],
        "steady_command_mae": [
          0.034418120980262756,
          0.08344954252243042,
          0.48190632462501526,
          0.009500646963715553
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.10795708000659943,
        "min_box_clearance_m": 0.582187294960022,
        "pelvis_amplitude_m": 0.007555484771728516,
        "normal_forces_mean_n": [
          9.376696586608887,
          8.572287559509277
        ],
        "friction_weight_ratio_mean": 0.6593832969665527,
        "normal_vertical_fraction_max": 0.0014368114061653614,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 15.257538795471191,
        "foot_slip_speed_mean_m_s": 0.03357294201850891,
        "joint_speed_rms": 1.2884156703948975,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.028872977942228317,
        "object_tracking_error_m": 0.03320237994194031,
        "object_tracking_error_rad_max": 0.057587772607803345,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03362743929028511,
          0.08078941702842712,
          0.49038806557655334,
          0.009467649273574352
        ],
        "steady_command_mae": [
          0.03362743929028511,
          0.08078941702842712,
          0.49038806557655334,
          0.009467649273574352
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.10670668631792068,
        "min_box_clearance_m": 0.5825862288475037,
        "pelvis_amplitude_m": 0.007481694221496582,
        "normal_forces_mean_n": [
          8.927607536315918,
          8.56013011932373
        ],
        "friction_weight_ratio_mean": 0.6051949858665466,
        "normal_vertical_fraction_max": 0.008699190802872181,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.406928062438965,
        "foot_slip_speed_mean_m_s": 0.032811105251312256,
        "joint_speed_rms": 1.2703241109848022,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.028289686888456345,
        "object_tracking_error_m": 0.031772103160619736,
        "object_tracking_error_rad_max": 0.0641220286488533,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03426390141248703,
          0.07951836287975311,
          0.5124646425247192,
          0.009485972113907337
        ],
        "steady_command_mae": [
          0.03426390141248703,
          0.07951836287975311,
          0.5124646425247192,
          0.009485972113907337
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.10728055983781815,
        "min_box_clearance_m": 0.5826433897018433,
        "pelvis_amplitude_m": 0.007484734058380127,
        "normal_forces_mean_n": [
          8.923307418823242,
          8.521674156188965
        ],
        "friction_weight_ratio_mean": 0.6025532484054565,
        "normal_vertical_fraction_max": 0.007301251869648695,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.760019302368164,
        "foot_slip_speed_mean_m_s": 0.03278069198131561,
        "joint_speed_rms": 1.2687400579452515,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02840641513466835,
        "object_tracking_error_m": 0.03195567429065704,
        "object_tracking_error_rad_max": 0.06222766637802124,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03553412854671478,
          0.08219790458679199,
          0.4982890188694,
          0.009568440727889538
        ],
        "steady_command_mae": [
          0.03553412854671478,
          0.08219790458679199,
          0.4982890188694,
          0.009568440727889538
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.10647901892662048,
        "min_box_clearance_m": 0.5826007127761841,
        "pelvis_amplitude_m": 0.007405102252960205,
        "normal_forces_mean_n": [
          9.171917915344238,
          8.482504844665527
        ],
        "friction_weight_ratio_mean": 0.6236129999160767,
        "normal_vertical_fraction_max": 0.007854328490793705,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.083733558654785,
        "foot_slip_speed_mean_m_s": 0.032863397151231766,
        "joint_speed_rms": 1.2723878622055054,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.028564974665641785,
        "object_tracking_error_m": 0.031982336193323135,
        "object_tracking_error_rad_max": 0.06387509405612946,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03377525880932808,
          0.08327960968017578,
          0.5044549703598022,
          0.009574055671691895
        ],
        "steady_command_mae": [
          0.03377525880932808,
          0.08327960968017578,
          0.5044549703598022,
          0.009574055671691895
        ],
        "contact_continuity": 0.14000001549720764,
        "max_hand_slip_m": 0.10734272003173828,
        "min_box_clearance_m": 0.5820752382278442,
        "pelvis_amplitude_m": 0.007484912872314453,
        "normal_forces_mean_n": [
          9.870349884033203,
          8.395438194274902
        ],
        "friction_weight_ratio_mean": 0.7373223304748535,
        "normal_vertical_fraction_max": 0.0030953020323067904,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.000049591064453,
        "foot_slip_speed_mean_m_s": 0.03332560509443283,
        "joint_speed_rms": 1.2894519567489624,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.028893211856484413,
        "object_tracking_error_m": 0.03360484167933464,
        "object_tracking_error_rad_max": 0.05956459790468216,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03447329252958298,
          0.08166949450969696,
          0.5180256962776184,
          0.009520458988845348
        ],
        "steady_command_mae": [
          0.03447329252958298,
          0.08166949450969696,
          0.5180256962776184,
          0.009520458988845348
        ],
        "contact_continuity": 0.15000002086162567,
        "max_hand_slip_m": 0.10753867030143738,
        "min_box_clearance_m": 0.5817221999168396,
        "pelvis_amplitude_m": 0.0074274539947509766,
        "normal_forces_mean_n": [
          9.788168907165527,
          8.659296989440918
        ],
        "friction_weight_ratio_mean": 0.6949347853660583,
        "normal_vertical_fraction_max": 0.0022893636487424374,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.583330154418945,
        "foot_slip_speed_mean_m_s": 0.03303912281990051,
        "joint_speed_rms": 1.2864488363265991,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.028764644637703896,
        "object_tracking_error_m": 0.0336378738284111,
        "object_tracking_error_rad_max": 0.060556862503290176,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.033164042979478836,
          0.07957880198955536,
          0.5028305053710938,
          0.009412753395736217
        ],
        "steady_command_mae": [
          0.033164042979478836,
          0.07957880198955536,
          0.5028305053710938,
          0.009412753395736217
        ],
        "contact_continuity": 0.14000001549720764,
        "max_hand_slip_m": 0.10711780190467834,
        "min_box_clearance_m": 0.5819648504257202,
        "pelvis_amplitude_m": 0.0074457526206970215,
        "normal_forces_mean_n": [
          9.691263198852539,
          8.606488227844238
        ],
        "friction_weight_ratio_mean": 0.6609662175178528,
        "normal_vertical_fraction_max": 0.0011417242931202054,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.372076988220215,
        "foot_slip_speed_mean_m_s": 0.03348037973046303,
        "joint_speed_rms": 1.281966209411621,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.0285646915435791,
        "object_tracking_error_m": 0.033136747777462006,
        "object_tracking_error_rad_max": 0.06151336431503296,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.0340258851647377,
          0.08334667235612869,
          0.5113513469696045,
          0.009434998035430908
        ],
        "steady_command_mae": [
          0.0340258851647377,
          0.08334667235612869,
          0.5113513469696045,
          0.009434998035430908
        ],
        "contact_continuity": 0.14000001549720764,
        "max_hand_slip_m": 0.1080099418759346,
        "min_box_clearance_m": 0.5814160108566284,
        "pelvis_amplitude_m": 0.007562398910522461,
        "normal_forces_mean_n": [
          9.550333976745605,
          8.55282211303711
        ],
        "friction_weight_ratio_mean": 0.7191873788833618,
        "normal_vertical_fraction_max": 0.0019302384462207556,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 15.327128410339355,
        "foot_slip_speed_mean_m_s": 0.03317009285092354,
        "joint_speed_rms": 1.2875250577926636,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.028844375163316727,
        "object_tracking_error_m": 0.03392700105905533,
        "object_tracking_error_rad_max": 0.05777613818645477,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03409365192055702,
          0.0815642848610878,
          0.4862632751464844,
          0.009454024024307728
        ],
        "steady_command_mae": [
          0.03409365192055702,
          0.0815642848610878,
          0.4862632751464844,
          0.009454024024307728
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.10648342221975327,
        "min_box_clearance_m": 0.5829933881759644,
        "pelvis_amplitude_m": 0.007362544536590576,
        "normal_forces_mean_n": [
          9.20401668548584,
          8.495080947875977
        ],
        "friction_weight_ratio_mean": 0.6231611967086792,
        "normal_vertical_fraction_max": 0.0073128025978803635,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.0045747756958,
        "foot_slip_speed_mean_m_s": 0.03255906701087952,
        "joint_speed_rms": 1.2706190347671509,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.028392497450113297,
        "object_tracking_error_m": 0.031775373965501785,
        "object_tracking_error_rad_max": 0.06361057609319687,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.033642254769802094,
          0.08312031626701355,
          0.4959377348423004,
          0.009600937366485596
        ],
        "steady_command_mae": [
          0.033642254769802094,
          0.08312031626701355,
          0.4959377348423004,
          0.009600937366485596
        ],
        "contact_continuity": 0.15000002086162567,
        "max_hand_slip_m": 0.10670416057109833,
        "min_box_clearance_m": 0.5822412967681885,
        "pelvis_amplitude_m": 0.007490575313568115,
        "normal_forces_mean_n": [
          9.886308670043945,
          8.633805274963379
        ],
        "friction_weight_ratio_mean": 0.7470043301582336,
        "normal_vertical_fraction_max": 0.0015227266121655703,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 13.978760719299316,
        "foot_slip_speed_mean_m_s": 0.03236481547355652,
        "joint_speed_rms": 1.2837018966674805,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02870955504477024,
        "object_tracking_error_m": 0.03330110386013985,
        "object_tracking_error_rad_max": 0.061391524970531464,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03438316658139229,
          0.08353009074926376,
          0.4827329218387604,
          0.009510385803878307
        ],
        "steady_command_mae": [
          0.03438316658139229,
          0.08353009074926376,
          0.4827329218387604,
          0.009510385803878307
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.10786791145801544,
        "min_box_clearance_m": 0.5822248458862305,
        "pelvis_amplitude_m": 0.007557988166809082,
        "normal_forces_mean_n": [
          9.446096420288086,
          8.601734161376953
        ],
        "friction_weight_ratio_mean": 0.6603702306747437,
        "normal_vertical_fraction_max": 0.0018978803418576717,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.9151611328125,
        "foot_slip_speed_mean_m_s": 0.033473603427410126,
        "joint_speed_rms": 1.2889864444732666,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.028875350952148438,
        "object_tracking_error_m": 0.03319215402007103,
        "object_tracking_error_rad_max": 0.05764760822057724,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      }
    ],
    "goal_limits": {
      "height_low": 0.6068800687789917,
      "height_high": 0.7268800735473633,
      "height_rate": 0.11247000098228455,
      "vx_high": 0.0,
      "forward_admitted": false,
      "reference_fps": 50,
      "episode_seconds": 30.0
    },
    "reference_free": false,
    "terminal_state_before_reset": true,
    "physical_model": {
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
      "control": "PPO joint-position offsets with PD each physics substep; no P0 feedforward or WBC"
    },
    "accepted_policy": false,
    "motion_quality": {
      "clip_0_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.1011236310005188,
          "lower_body_style_rmse_rad": 0.07091598957777023,
          "reference_compatibility_mean": 0.8916152402312975,
          "joint_acceleration_rms_rad_s2": 35.44654846191406,
          "box_relative_translation_drift_max_m": 0.055032013139381546,
          "box_relative_rotation_drift_max_rad": 0.0577934280140449
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.10118065774440765,
          "lower_body_style_rmse_rad": 0.06938589364290237,
          "reference_compatibility_mean": 0.8978695632190753,
          "joint_acceleration_rms_rad_s2": 35.460506439208984,
          "box_relative_translation_drift_max_m": 0.05526999823395054,
          "box_relative_rotation_drift_max_rad": 0.0576396737830099
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.10127242654561996,
          "lower_body_style_rmse_rad": 0.07040072977542877,
          "reference_compatibility_mean": 0.8913868134977714,
          "joint_acceleration_rms_rad_s2": 35.46141052246094,
          "box_relative_translation_drift_max_m": 0.055387622526558204,
          "box_relative_rotation_drift_max_rad": 0.057702098532900384
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.1026809960603714,
          "lower_body_style_rmse_rad": 0.06993930041790009,
          "reference_compatibility_mean": 0.8947683870789792,
          "joint_acceleration_rms_rad_s2": 35.41193389892578,
          "box_relative_translation_drift_max_m": 0.05582342089336574,
          "box_relative_rotation_drift_max_rad": 0.056288578996422096
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.10239977389574051,
          "lower_body_style_rmse_rad": 0.06987731158733368,
          "reference_compatibility_mean": 0.8960112054653229,
          "joint_acceleration_rms_rad_s2": 35.404476165771484,
          "box_relative_translation_drift_max_m": 0.05630313691592539,
          "box_relative_rotation_drift_max_rad": 0.056402919599480336
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.10195469111204147,
          "lower_body_style_rmse_rad": 0.06963054090738297,
          "reference_compatibility_mean": 0.8968813848439755,
          "joint_acceleration_rms_rad_s2": 35.16630554199219,
          "box_relative_translation_drift_max_m": 0.05567731253626865,
          "box_relative_rotation_drift_max_rad": 0.055434688010912815
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.10267283767461777,
          "lower_body_style_rmse_rad": 0.07017690688371658,
          "reference_compatibility_mean": 0.8968996933592539,
          "joint_acceleration_rms_rad_s2": 35.494327545166016,
          "box_relative_translation_drift_max_m": 0.05606714325953691,
          "box_relative_rotation_drift_max_rad": 0.05586839788136181
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.10106883943080902,
          "lower_body_style_rmse_rad": 0.06888579577207565,
          "reference_compatibility_mean": 0.8945554656795061,
          "joint_acceleration_rms_rad_s2": 35.451602935791016,
          "box_relative_translation_drift_max_m": 0.055003584079820984,
          "box_relative_rotation_drift_max_rad": 0.058193806118581604
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.10212024301290512,
          "lower_body_style_rmse_rad": 0.06975320726633072,
          "reference_compatibility_mean": 0.8929567264311775,
          "joint_acceleration_rms_rad_s2": 35.37553405761719,
          "box_relative_translation_drift_max_m": 0.05554324268456987,
          "box_relative_rotation_drift_max_rad": 0.05577375390653555
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.1025315672159195,
          "lower_body_style_rmse_rad": 0.07125764340162277,
          "reference_compatibility_mean": 0.8893355464147215,
          "joint_acceleration_rms_rad_s2": 35.46196365356445,
          "box_relative_translation_drift_max_m": 0.056141880787567815,
          "box_relative_rotation_drift_max_rad": 0.05334515468737263
        }
      ],
      "clip_1_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.10112810134887695,
          "lower_body_style_rmse_rad": 0.07078329473733902,
          "reference_compatibility_mean": 0.8922674070849499,
          "joint_acceleration_rms_rad_s2": 35.4002799987793,
          "box_relative_translation_drift_max_m": 0.05500582950432958,
          "box_relative_rotation_drift_max_rad": 0.057817870604326756
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.10116524249315262,
          "lower_body_style_rmse_rad": 0.06936813145875931,
          "reference_compatibility_mean": 0.8983877347516275,
          "joint_acceleration_rms_rad_s2": 35.437095642089844,
          "box_relative_translation_drift_max_m": 0.05521471095620653,
          "box_relative_rotation_drift_max_rad": 0.05741072127008877
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.10128884762525558,
          "lower_body_style_rmse_rad": 0.07042166590690613,
          "reference_compatibility_mean": 0.8913291012966844,
          "joint_acceleration_rms_rad_s2": 35.418277740478516,
          "box_relative_translation_drift_max_m": 0.055345358991513806,
          "box_relative_rotation_drift_max_rad": 0.05769765779039082
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.10268091410398483,
          "lower_body_style_rmse_rad": 0.06997094303369522,
          "reference_compatibility_mean": 0.8945481717540271,
          "joint_acceleration_rms_rad_s2": 35.24541473388672,
          "box_relative_translation_drift_max_m": 0.05575785314101226,
          "box_relative_rotation_drift_max_rad": 0.056331909176344244
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.1024090051651001,
          "lower_body_style_rmse_rad": 0.06996136158704758,
          "reference_compatibility_mean": 0.8958861527228066,
          "joint_acceleration_rms_rad_s2": 35.47512435913086,
          "box_relative_translation_drift_max_m": 0.05604262115962388,
          "box_relative_rotation_drift_max_rad": 0.0570354416449782
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.10193710774183273,
          "lower_body_style_rmse_rad": 0.06974803656339645,
          "reference_compatibility_mean": 0.8966164223177925,
          "joint_acceleration_rms_rad_s2": 35.24787902832031,
          "box_relative_translation_drift_max_m": 0.055672686363275804,
          "box_relative_rotation_drift_max_rad": 0.0556883922628906
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.10267023742198944,
          "lower_body_style_rmse_rad": 0.07015026360750198,
          "reference_compatibility_mean": 0.8969182810504648,
          "joint_acceleration_rms_rad_s2": 35.54161071777344,
          "box_relative_translation_drift_max_m": 0.05630709631957172,
          "box_relative_rotation_drift_max_rad": 0.055799864114629956
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.10104888677597046,
          "lower_body_style_rmse_rad": 0.06887713074684143,
          "reference_compatibility_mean": 0.8946126843867749,
          "joint_acceleration_rms_rad_s2": 35.441864013671875,
          "box_relative_translation_drift_max_m": 0.0549970878861285,
          "box_relative_rotation_drift_max_rad": 0.05811983593503357
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.10213208198547363,
          "lower_body_style_rmse_rad": 0.0695912092924118,
          "reference_compatibility_mean": 0.89304133280671,
          "joint_acceleration_rms_rad_s2": 35.367801666259766,
          "box_relative_translation_drift_max_m": 0.05554431753064702,
          "box_relative_rotation_drift_max_rad": 0.05594884957510276
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.10254174470901489,
          "lower_body_style_rmse_rad": 0.07136812806129456,
          "reference_compatibility_mean": 0.8885135512515283,
          "joint_acceleration_rms_rad_s2": 35.5484733581543,
          "box_relative_translation_drift_max_m": 0.05612691031137436,
          "box_relative_rotation_drift_max_rad": 0.05343115292379399
        }
      ]
    },
    "directory": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795161406155359032",
    "checkpoint": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/dashboard/stage1/WholeBodyTracking/20261120_054835-stage1-locomotion/model_00499.pt",
    "final": false,
    "selection_score": 0.014638463350442742,
    "failure_counts": {
      "physical_failure/body_support": 20,
      "physical_failure/loss_of_grasp": 20,
      "incomplete_episode": 20,
      "contact_interruption": 20,
      "hand_slip": 20,
      "insufficient_friction_support": 20,
      "contact_near_box_bottom": 20,
      "nonhand_support": 20
    },
    "scenarios": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "completed_updates": 500
  },
  {
    "passed": false,
    "score": 0.0,
    "suite": "stage1",
    "groups": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "trials": [
      {
        "scenario": "clip_0",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.016986776143312454,
          0.028204521164298058,
          0.4604395925998688,
          0.011333453468978405
        ],
        "steady_command_mae": [
          0.016986776143312454,
          0.028204521164298058,
          0.4604395925998688,
          0.011333453468978405
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.12469954043626785,
        "min_box_clearance_m": 0.5825552344322205,
        "pelvis_amplitude_m": 0.008217096328735352,
        "normal_forces_mean_n": [
          8.421712875366211,
          10.109477996826172
        ],
        "friction_weight_ratio_mean": 0.594089150428772,
        "normal_vertical_fraction_max": 0.00984997022897005,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 11.393763542175293,
        "foot_slip_speed_mean_m_s": 0.1429654359817505,
        "joint_speed_rms": 1.4512898921966553,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03150321543216705,
        "object_tracking_error_m": 0.03204978629946709,
        "object_tracking_error_rad_max": 0.058763086795806885,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.015418198890984058,
          0.02778054215013981,
          0.45594701170921326,
          0.011335253715515137
        ],
        "steady_command_mae": [
          0.015418198890984058,
          0.02778054215013981,
          0.45594701170921326,
          0.011335253715515137
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.12460148334503174,
        "min_box_clearance_m": 0.5826178789138794,
        "pelvis_amplitude_m": 0.008293986320495605,
        "normal_forces_mean_n": [
          8.598470687866211,
          9.96306037902832
        ],
        "friction_weight_ratio_mean": 0.5780686736106873,
        "normal_vertical_fraction_max": 0.009060448966920376,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.367022514343262,
        "foot_slip_speed_mean_m_s": 0.152335062623024,
        "joint_speed_rms": 1.4491950273513794,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03156014531850815,
        "object_tracking_error_m": 0.032218463718891144,
        "object_tracking_error_rad_max": 0.0575106143951416,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.01735049858689308,
          0.028234511613845825,
          0.47207579016685486,
          0.011536657810211182
        ],
        "steady_command_mae": [
          0.01735049858689308,
          0.028234511613845825,
          0.47207579016685486,
          0.011536657810211182
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.12490109354257584,
        "min_box_clearance_m": 0.5829389691352844,
        "pelvis_amplitude_m": 0.00822150707244873,
        "normal_forces_mean_n": [
          8.555351257324219,
          10.111944198608398
        ],
        "friction_weight_ratio_mean": 0.6126991510391235,
        "normal_vertical_fraction_max": 0.008790257386863232,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 12.890130996704102,
        "foot_slip_speed_mean_m_s": 0.13238787651062012,
        "joint_speed_rms": 1.452469825744629,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03176501393318176,
        "object_tracking_error_m": 0.032299309968948364,
        "object_tracking_error_rad_max": 0.05582369491457939,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.015564578585326672,
          0.029636073857545853,
          0.4573265016078949,
          0.011475455947220325
        ],
        "steady_command_mae": [
          0.015564578585326672,
          0.029636073857545853,
          0.4573265016078949,
          0.011475455947220325
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.12577186524868011,
        "min_box_clearance_m": 0.5827304720878601,
        "pelvis_amplitude_m": 0.008180558681488037,
        "normal_forces_mean_n": [
          9.58674144744873,
          9.951543807983398
        ],
        "friction_weight_ratio_mean": 0.6644179224967957,
        "normal_vertical_fraction_max": 0.003940467722713947,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 3.5175373554229736,
        "foot_slip_speed_mean_m_s": 0.14651969075202942,
        "joint_speed_rms": 1.469120979309082,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03198358044028282,
        "object_tracking_error_m": 0.03389151021838188,
        "object_tracking_error_rad_max": 0.0501495860517025,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.015118137001991272,
          0.030322039499878883,
          0.4484303593635559,
          0.011507714167237282
        ],
        "steady_command_mae": [
          0.015118137001991272,
          0.030322039499878883,
          0.4484303593635559,
          0.011507714167237282
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.1263730525970459,
        "min_box_clearance_m": 0.5831865072250366,
        "pelvis_amplitude_m": 0.008280515670776367,
        "normal_forces_mean_n": [
          9.363539695739746,
          10.112565040588379
        ],
        "friction_weight_ratio_mean": 0.701673150062561,
        "normal_vertical_fraction_max": 0.027436036616563797,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 13.411919593811035,
        "foot_slip_speed_mean_m_s": 0.1583976447582245,
        "joint_speed_rms": 1.4734517335891724,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03198549896478653,
        "object_tracking_error_m": 0.03382530063390732,
        "object_tracking_error_rad_max": 0.048797495663166046,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.016305293887853622,
          0.027979101985692978,
          0.452131450176239,
          0.011270237155258656
        ],
        "steady_command_mae": [
          0.016305293887853622,
          0.027979101985692978,
          0.452131450176239,
          0.011270237155258656
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.12588976323604584,
        "min_box_clearance_m": 0.5832859873771667,
        "pelvis_amplitude_m": 0.008125543594360352,
        "normal_forces_mean_n": [
          9.209129333496094,
          10.196756362915039
        ],
        "friction_weight_ratio_mean": 0.6699625253677368,
        "normal_vertical_fraction_max": 0.0019974696915596724,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 13.162283897399902,
        "foot_slip_speed_mean_m_s": 0.14989420771598816,
        "joint_speed_rms": 1.4675921201705933,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03177671879529953,
        "object_tracking_error_m": 0.03338878974318504,
        "object_tracking_error_rad_max": 0.04976482316851616,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.012249094434082508,
          0.029254715889692307,
          0.454216867685318,
          0.01122194528579712
        ],
        "steady_command_mae": [
          0.012249094434082508,
          0.029254715889692307,
          0.454216867685318,
          0.01122194528579712
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.12610459327697754,
        "min_box_clearance_m": 0.5825072526931763,
        "pelvis_amplitude_m": 0.00839322805404663,
        "normal_forces_mean_n": [
          9.2593412399292,
          9.903505325317383
        ],
        "friction_weight_ratio_mean": 0.6691619157791138,
        "normal_vertical_fraction_max": 0.00479769054800272,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 13.319085121154785,
        "foot_slip_speed_mean_m_s": 0.1783316433429718,
        "joint_speed_rms": 1.4708716869354248,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03195519745349884,
        "object_tracking_error_m": 0.0341094546020031,
        "object_tracking_error_rad_max": 0.048752330243587494,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.015772301703691483,
          0.028824960812926292,
          0.45341283082962036,
          0.011384809389710426
        ],
        "steady_command_mae": [
          0.015772301703691483,
          0.028824960812926292,
          0.45341283082962036,
          0.011384809389710426
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.12449683248996735,
        "min_box_clearance_m": 0.5825964212417603,
        "pelvis_amplitude_m": 0.00818556547164917,
        "normal_forces_mean_n": [
          8.3523530960083,
          9.986627578735352
        ],
        "friction_weight_ratio_mean": 0.5866504311561584,
        "normal_vertical_fraction_max": 0.00835437886416912,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 11.706250190734863,
        "foot_slip_speed_mean_m_s": 0.14289693534374237,
        "joint_speed_rms": 1.4505615234375,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03161744773387909,
        "object_tracking_error_m": 0.03214830160140991,
        "object_tracking_error_rad_max": 0.058096952736377716,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.016658183187246323,
          0.031664393842220306,
          0.446061909198761,
          0.011655116453766823
        ],
        "steady_command_mae": [
          0.016658183187246323,
          0.031664393842220306,
          0.446061909198761,
          0.011655116453766823
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.1265198141336441,
        "min_box_clearance_m": 0.5822893977165222,
        "pelvis_amplitude_m": 0.0084303617477417,
        "normal_forces_mean_n": [
          9.122712135314941,
          10.127551078796387
        ],
        "friction_weight_ratio_mean": 0.6551491618156433,
        "normal_vertical_fraction_max": 0.0012301082024350762,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 13.143681526184082,
        "foot_slip_speed_mean_m_s": 0.1487768292427063,
        "joint_speed_rms": 1.469330072402954,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03194065019488335,
        "object_tracking_error_m": 0.033756088465452194,
        "object_tracking_error_rad_max": 0.05154167115688324,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.015994708985090256,
          0.02808796428143978,
          0.4615944027900696,
          0.011335683055222034
        ],
        "steady_command_mae": [
          0.015994708985090256,
          0.02808796428143978,
          0.4615944027900696,
          0.011335683055222034
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.12594136595726013,
        "min_box_clearance_m": 0.5840016007423401,
        "pelvis_amplitude_m": 0.008232414722442627,
        "normal_forces_mean_n": [
          9.039449691772461,
          10.358867645263672
        ],
        "friction_weight_ratio_mean": 0.6841601729393005,
        "normal_vertical_fraction_max": 0.003509234171360731,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 12.972436904907227,
        "foot_slip_speed_mean_m_s": 0.1415826976299286,
        "joint_speed_rms": 1.4689462184906006,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.032020702958106995,
        "object_tracking_error_m": 0.03330864757299423,
        "object_tracking_error_rad_max": 0.04718143492937088,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.017135951668024063,
          0.028079066425561905,
          0.4590982496738434,
          0.011325657367706299
        ],
        "steady_command_mae": [
          0.017135951668024063,
          0.028079066425561905,
          0.4590982496738434,
          0.011325657367706299
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.1245834231376648,
        "min_box_clearance_m": 0.5826462507247925,
        "pelvis_amplitude_m": 0.008215606212615967,
        "normal_forces_mean_n": [
          8.483536720275879,
          10.096940040588379
        ],
        "friction_weight_ratio_mean": 0.5965107679367065,
        "normal_vertical_fraction_max": 0.00968057569116354,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 11.921260833740234,
        "foot_slip_speed_mean_m_s": 0.1428745985031128,
        "joint_speed_rms": 1.4510892629623413,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03150186315178871,
        "object_tracking_error_m": 0.0320386067032814,
        "object_tracking_error_rad_max": 0.05854093283414841,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.015469846315681934,
          0.027441153302788734,
          0.4551205635070801,
          0.011330986395478249
        ],
        "steady_command_mae": [
          0.015469846315681934,
          0.027441153302788734,
          0.4551205635070801,
          0.011330986395478249
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.12466734647750854,
        "min_box_clearance_m": 0.5827789902687073,
        "pelvis_amplitude_m": 0.008290648460388184,
        "normal_forces_mean_n": [
          8.688182830810547,
          10.08541488647461
        ],
        "friction_weight_ratio_mean": 0.5871327519416809,
        "normal_vertical_fraction_max": 0.00895237922668457,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 12.00477409362793,
        "foot_slip_speed_mean_m_s": 0.15226709842681885,
        "joint_speed_rms": 1.449413776397705,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03156084939837456,
        "object_tracking_error_m": 0.03219851851463318,
        "object_tracking_error_rad_max": 0.057182230055332184,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.01745123229920864,
          0.027896638959646225,
          0.46944111585617065,
          0.011531638912856579
        ],
        "steady_command_mae": [
          0.01745123229920864,
          0.027896638959646225,
          0.46944111585617065,
          0.011531638912856579
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.12488750368356705,
        "min_box_clearance_m": 0.5829470157623291,
        "pelvis_amplitude_m": 0.008225321769714355,
        "normal_forces_mean_n": [
          8.66073989868164,
          10.158782958984375
        ],
        "friction_weight_ratio_mean": 0.6099886894226074,
        "normal_vertical_fraction_max": 0.008714091032743454,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 13.112257957458496,
        "foot_slip_speed_mean_m_s": 0.13225293159484863,
        "joint_speed_rms": 1.4524534940719604,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03176451846957207,
        "object_tracking_error_m": 0.03229803964495659,
        "object_tracking_error_rad_max": 0.05579080805182457,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.01570909656584263,
          0.02936185896396637,
          0.45648193359375,
          0.01147682685405016
        ],
        "steady_command_mae": [
          0.01570909656584263,
          0.02936185896396637,
          0.45648193359375,
          0.01147682685405016
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.1257983148097992,
        "min_box_clearance_m": 0.5827520489692688,
        "pelvis_amplitude_m": 0.008191943168640137,
        "normal_forces_mean_n": [
          9.597452163696289,
          9.935532569885254
        ],
        "friction_weight_ratio_mean": 0.6699884533882141,
        "normal_vertical_fraction_max": 0.003998110070824623,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 4.291215419769287,
        "foot_slip_speed_mean_m_s": 0.14650273323059082,
        "joint_speed_rms": 1.4686124324798584,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.031984467059373856,
        "object_tracking_error_m": 0.03389272838830948,
        "object_tracking_error_rad_max": 0.05001245066523552,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.015166317112743855,
          0.030161812901496887,
          0.4454754889011383,
          0.011506604962050915
        ],
        "steady_command_mae": [
          0.015166317112743855,
          0.030161812901496887,
          0.4454754889011383,
          0.011506604962050915
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.1263945996761322,
        "min_box_clearance_m": 0.5832996964454651,
        "pelvis_amplitude_m": 0.008291065692901611,
        "normal_forces_mean_n": [
          9.452764511108398,
          10.191161155700684
        ],
        "friction_weight_ratio_mean": 0.6988519430160522,
        "normal_vertical_fraction_max": 0.027436036616563797,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 13.768301010131836,
        "foot_slip_speed_mean_m_s": 0.15833956003189087,
        "joint_speed_rms": 1.4734022617340088,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03198753669857979,
        "object_tracking_error_m": 0.03381779044866562,
        "object_tracking_error_rad_max": 0.04845985397696495,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.016228502616286278,
          0.028189554810523987,
          0.4534231126308441,
          0.011271392926573753
        ],
        "steady_command_mae": [
          0.016228502616286278,
          0.028189554810523987,
          0.4534231126308441,
          0.011271392926573753
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.12588553130626678,
        "min_box_clearance_m": 0.5832690000534058,
        "pelvis_amplitude_m": 0.008124709129333496,
        "normal_forces_mean_n": [
          9.197943687438965,
          10.187948226928711
        ],
        "friction_weight_ratio_mean": 0.6700467467308044,
        "normal_vertical_fraction_max": 0.0019893355201929808,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 13.156773567199707,
        "foot_slip_speed_mean_m_s": 0.14927023649215698,
        "joint_speed_rms": 1.4676083326339722,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.031776607036590576,
        "object_tracking_error_m": 0.033390335738658905,
        "object_tracking_error_rad_max": 0.04980985447764397,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.012349097058176994,
          0.028894636780023575,
          0.45212602615356445,
          0.0112161161378026
        ],
        "steady_command_mae": [
          0.012349097058176994,
          0.028894636780023575,
          0.45212602615356445,
          0.0112161161378026
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.12603600323200226,
        "min_box_clearance_m": 0.5825892090797424,
        "pelvis_amplitude_m": 0.008396625518798828,
        "normal_forces_mean_n": [
          9.389147758483887,
          9.945302963256836
        ],
        "friction_weight_ratio_mean": 0.6682767271995544,
        "normal_vertical_fraction_max": 0.004887761548161507,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 14.320474624633789,
        "foot_slip_speed_mean_m_s": 0.1784580945968628,
        "joint_speed_rms": 1.4708656072616577,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03195418789982796,
        "object_tracking_error_m": 0.03410007059574127,
        "object_tracking_error_rad_max": 0.0485677570104599,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.015918847173452377,
          0.029258480295538902,
          0.4482583999633789,
          0.01137533225119114
        ],
        "steady_command_mae": [
          0.015918847173452377,
          0.029258480295538902,
          0.4482583999633789,
          0.01137533225119114
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.12441383302211761,
        "min_box_clearance_m": 0.5825978517532349,
        "pelvis_amplitude_m": 0.008183956146240234,
        "normal_forces_mean_n": [
          8.50265121459961,
          10.039426803588867
        ],
        "friction_weight_ratio_mean": 0.5823537707328796,
        "normal_vertical_fraction_max": 0.008320816792547703,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 12.117363929748535,
        "foot_slip_speed_mean_m_s": 0.14253456890583038,
        "joint_speed_rms": 1.4506016969680786,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.031615957617759705,
        "object_tracking_error_m": 0.03214326128363609,
        "object_tracking_error_rad_max": 0.05818573012948036,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.01673264242708683,
          0.031387317925691605,
          0.4454355239868164,
          0.011651384644210339
        ],
        "steady_command_mae": [
          0.01673264242708683,
          0.031387317925691605,
          0.4454355239868164,
          0.011651384644210339
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.12648281455039978,
        "min_box_clearance_m": 0.5823747515678406,
        "pelvis_amplitude_m": 0.008434295654296875,
        "normal_forces_mean_n": [
          9.192708969116211,
          10.167390823364258
        ],
        "friction_weight_ratio_mean": 0.6576586961746216,
        "normal_vertical_fraction_max": 0.0012534005800262094,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 13.491218566894531,
        "foot_slip_speed_mean_m_s": 0.14890199899673462,
        "joint_speed_rms": 1.4692323207855225,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.031942062079906464,
        "object_tracking_error_m": 0.03374987840652466,
        "object_tracking_error_rad_max": 0.05125470086932182,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.016060054302215576,
          0.027765462175011635,
          0.4590604901313782,
          0.011332178488373756
        ],
        "steady_command_mae": [
          0.016060054302215576,
          0.027765462175011635,
          0.4590604901313782,
          0.011332178488373756
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.12593580782413483,
        "min_box_clearance_m": 0.5840124487876892,
        "pelvis_amplitude_m": 0.008233964443206787,
        "normal_forces_mean_n": [
          9.107309341430664,
          10.380077362060547
        ],
        "friction_weight_ratio_mean": 0.682449460029602,
        "normal_vertical_fraction_max": 0.0036568790674209595,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 13.145928382873535,
        "foot_slip_speed_mean_m_s": 0.14166437089443207,
        "joint_speed_rms": 1.4688979387283325,
        "failures": [
          "physical_failure/body_support",
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom",
          "nonhand_support"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03202222287654877,
        "object_tracking_error_m": 0.0333079919219017,
        "object_tracking_error_rad_max": 0.04712003841996193,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      }
    ],
    "goal_limits": {
      "height_low": 0.6068800687789917,
      "height_high": 0.7268800735473633,
      "height_rate": 0.11247000098228455,
      "vx_high": 0.0,
      "forward_admitted": false,
      "reference_fps": 50,
      "episode_seconds": 30.0
    },
    "reference_free": false,
    "terminal_state_before_reset": true,
    "physical_model": {
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
      "control": "PPO joint-position offsets with PD each physics substep; no P0 feedforward or WBC"
    },
    "accepted_policy": false,
    "motion_quality": {
      "clip_0_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.1138010323047638,
          "lower_body_style_rmse_rad": 0.08353951573371887,
          "reference_compatibility_mean": 0.7687269545406158,
          "joint_acceleration_rms_rad_s2": 44.529396057128906,
          "box_relative_translation_drift_max_m": 0.05377168533331644,
          "box_relative_rotation_drift_max_rad": 0.046166731585710385
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.11375592648983002,
          "lower_body_style_rmse_rad": 0.08416897058486938,
          "reference_compatibility_mean": 0.7665100520781012,
          "joint_acceleration_rms_rad_s2": 44.31330871582031,
          "box_relative_translation_drift_max_m": 0.053848334334013884,
          "box_relative_rotation_drift_max_rad": 0.047840730732245276
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.11379756778478622,
          "lower_body_style_rmse_rad": 0.08352480083703995,
          "reference_compatibility_mean": 0.7636993412659506,
          "joint_acceleration_rms_rad_s2": 44.78684997558594,
          "box_relative_translation_drift_max_m": 0.054133563732441436,
          "box_relative_rotation_drift_max_rad": 0.047949759040310784
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.11527024954557419,
          "lower_body_style_rmse_rad": 0.08380361646413803,
          "reference_compatibility_mean": 0.7661313745458642,
          "joint_acceleration_rms_rad_s2": 43.53038024902344,
          "box_relative_translation_drift_max_m": 0.05447303232170755,
          "box_relative_rotation_drift_max_rad": 0.059495793679530555
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.11532902717590332,
          "lower_body_style_rmse_rad": 0.08390390872955322,
          "reference_compatibility_mean": 0.760924489066839,
          "joint_acceleration_rms_rad_s2": 43.96269989013672,
          "box_relative_translation_drift_max_m": 0.05432054569447959,
          "box_relative_rotation_drift_max_rad": 0.05904660523147655
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.11490022391080856,
          "lower_body_style_rmse_rad": 0.08370019495487213,
          "reference_compatibility_mean": 0.7734603459078749,
          "joint_acceleration_rms_rad_s2": 44.092735290527344,
          "box_relative_translation_drift_max_m": 0.05408896553139467,
          "box_relative_rotation_drift_max_rad": 0.056417560087056055
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.1155279278755188,
          "lower_body_style_rmse_rad": 0.08507634699344635,
          "reference_compatibility_mean": 0.7662272298608913,
          "joint_acceleration_rms_rad_s2": 43.559871673583984,
          "box_relative_translation_drift_max_m": 0.05440359164517699,
          "box_relative_rotation_drift_max_rad": 0.05938140764499778
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.1135270819067955,
          "lower_body_style_rmse_rad": 0.08358027786016464,
          "reference_compatibility_mean": 0.7678726022709309,
          "joint_acceleration_rms_rad_s2": 44.76818084716797,
          "box_relative_translation_drift_max_m": 0.0538938996009339,
          "box_relative_rotation_drift_max_rad": 0.046769169130036384
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.11487963050603867,
          "lower_body_style_rmse_rad": 0.08397126197814941,
          "reference_compatibility_mean": 0.7541921300383877,
          "joint_acceleration_rms_rad_s2": 44.42616271972656,
          "box_relative_translation_drift_max_m": 0.05505674804138337,
          "box_relative_rotation_drift_max_rad": 0.0583089906942191
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.11522220820188522,
          "lower_body_style_rmse_rad": 0.08394508063793182,
          "reference_compatibility_mean": 0.7692193104103409,
          "joint_acceleration_rms_rad_s2": 44.292991638183594,
          "box_relative_translation_drift_max_m": 0.05383705276236426,
          "box_relative_rotation_drift_max_rad": 0.056191687679544126
        }
      ],
      "clip_1_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.11378076672554016,
          "lower_body_style_rmse_rad": 0.08352365344762802,
          "reference_compatibility_mean": 0.7688308446332649,
          "joint_acceleration_rms_rad_s2": 44.75520324707031,
          "box_relative_translation_drift_max_m": 0.053731651807845296,
          "box_relative_rotation_drift_max_rad": 0.04616723332210381
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.11380438506603241,
          "lower_body_style_rmse_rad": 0.0841568186879158,
          "reference_compatibility_mean": 0.766592427101451,
          "joint_acceleration_rms_rad_s2": 44.146522521972656,
          "box_relative_translation_drift_max_m": 0.053723710221466124,
          "box_relative_rotation_drift_max_rad": 0.0478551592659327
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.1138051301240921,
          "lower_body_style_rmse_rad": 0.08339632302522659,
          "reference_compatibility_mean": 0.7637740886014444,
          "joint_acceleration_rms_rad_s2": 44.80767059326172,
          "box_relative_translation_drift_max_m": 0.05413449349263971,
          "box_relative_rotation_drift_max_rad": 0.04794997119560701
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.11527321487665176,
          "lower_body_style_rmse_rad": 0.08380705863237381,
          "reference_compatibility_mean": 0.7661296598810647,
          "joint_acceleration_rms_rad_s2": 43.55049514770508,
          "box_relative_translation_drift_max_m": 0.054493182856467114,
          "box_relative_rotation_drift_max_rad": 0.05951098527353351
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.11535559594631195,
          "lower_body_style_rmse_rad": 0.0837799459695816,
          "reference_compatibility_mean": 0.7609361327448977,
          "joint_acceleration_rms_rad_s2": 44.00465774536133,
          "box_relative_translation_drift_max_m": 0.05431107527579525,
          "box_relative_rotation_drift_max_rad": 0.05905761114209859
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.11489700525999069,
          "lower_body_style_rmse_rad": 0.0838046446442604,
          "reference_compatibility_mean": 0.7734585266686785,
          "joint_acceleration_rms_rad_s2": 44.09633255004883,
          "box_relative_translation_drift_max_m": 0.054104172591143154,
          "box_relative_rotation_drift_max_rad": 0.05641207701768732
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.11552790552377701,
          "lower_body_style_rmse_rad": 0.08497647196054459,
          "reference_compatibility_mean": 0.7662546063021973,
          "joint_acceleration_rms_rad_s2": 43.6200065612793,
          "box_relative_translation_drift_max_m": 0.05436762890929643,
          "box_relative_rotation_drift_max_rad": 0.05938239164348483
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.11353634297847748,
          "lower_body_style_rmse_rad": 0.08345704525709152,
          "reference_compatibility_mean": 0.7679844996435863,
          "joint_acceleration_rms_rad_s2": 44.81047821044922,
          "box_relative_translation_drift_max_m": 0.05386962174926151,
          "box_relative_rotation_drift_max_rad": 0.04676807134250458
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.11487729102373123,
          "lower_body_style_rmse_rad": 0.08396334201097488,
          "reference_compatibility_mean": 0.7542326609618667,
          "joint_acceleration_rms_rad_s2": 44.49744415283203,
          "box_relative_translation_drift_max_m": 0.05504944088973423,
          "box_relative_rotation_drift_max_rad": 0.05830501819664571
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.11522852629423141,
          "lower_body_style_rmse_rad": 0.08408999443054199,
          "reference_compatibility_mean": 0.7692445341666454,
          "joint_acceleration_rms_rad_s2": 44.32569122314453,
          "box_relative_translation_drift_max_m": 0.05384744867127821,
          "box_relative_rotation_drift_max_rad": 0.056198916831013614
        }
      ]
    },
    "directory": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795169166776259536",
    "checkpoint": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/dashboard/stage1/WholeBodyTracking/20261120_075709-stage1-locomotion/model_00999.pt",
    "final": false,
    "selection_score": 0.012138463052419517,
    "failure_counts": {
      "physical_failure/body_support": 20,
      "physical_failure/loss_of_grasp": 20,
      "incomplete_episode": 20,
      "contact_interruption": 20,
      "hand_slip": 20,
      "insufficient_friction_support": 20,
      "contact_near_box_bottom": 20,
      "nonhand_support": 20
    },
    "scenarios": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "completed_updates": 1000
  },
  {
    "passed": false,
    "score": 0.0,
    "suite": "stage1",
    "groups": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "trials": [
      {
        "scenario": "clip_0",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03804200887680054,
          0.08582483232021332,
          0.27572646737098694,
          0.008316206745803356
        ],
        "steady_command_mae": [
          0.03804200887680054,
          0.08582483232021332,
          0.27572646737098694,
          0.008316206745803356
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.13808372616767883,
        "min_box_clearance_m": 0.5818709135055542,
        "pelvis_amplitude_m": 0.004467487335205078,
        "normal_forces_mean_n": [
          6.203023910522461,
          11.39166259765625
        ],
        "friction_weight_ratio_mean": 0.5183441638946533,
        "normal_vertical_fraction_max": 0.02025599032640457,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.13495898246765137,
        "joint_speed_rms": 1.5368871688842773,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.031243741512298584,
        "object_tracking_error_m": 0.03210212662816048,
        "object_tracking_error_rad_max": 0.06668397784233093,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03767695277929306,
          0.08575190603733063,
          0.27565667033195496,
          0.008501386269927025
        ],
        "steady_command_mae": [
          0.03767695277929306,
          0.08575190603733063,
          0.27565667033195496,
          0.008501386269927025
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.13788846135139465,
        "min_box_clearance_m": 0.5817418098449707,
        "pelvis_amplitude_m": 0.004622042179107666,
        "normal_forces_mean_n": [
          6.24517297744751,
          11.350743293762207
        ],
        "friction_weight_ratio_mean": 0.5248609185218811,
        "normal_vertical_fraction_max": 0.018512476235628128,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.15615245699882507,
        "joint_speed_rms": 1.5370811223983765,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03144508972764015,
        "object_tracking_error_m": 0.03227929025888443,
        "object_tracking_error_rad_max": 0.06600157916545868,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03572230413556099,
          0.08586420118808746,
          0.27636653184890747,
          0.008404707536101341
        ],
        "steady_command_mae": [
          0.03572230413556099,
          0.08586420118808746,
          0.27636653184890747,
          0.008404707536101341
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.1379420906305313,
        "min_box_clearance_m": 0.5816471576690674,
        "pelvis_amplitude_m": 0.004468202590942383,
        "normal_forces_mean_n": [
          6.339865684509277,
          11.458404541015625
        ],
        "friction_weight_ratio_mean": 0.5214517712593079,
        "normal_vertical_fraction_max": 0.017369071021676064,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1301557421684265,
        "joint_speed_rms": 1.53826105594635,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03149387985467911,
        "object_tracking_error_m": 0.032384611666202545,
        "object_tracking_error_rad_max": 0.06616922467947006,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03407957777380943,
          0.08513785898685455,
          0.27859705686569214,
          0.008395028300583363
        ],
        "steady_command_mae": [
          0.03407957777380943,
          0.08513785898685455,
          0.27859705686569214,
          0.008395028300583363
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.14039622247219086,
        "min_box_clearance_m": 0.5777528285980225,
        "pelvis_amplitude_m": 0.004413187503814697,
        "normal_forces_mean_n": [
          5.893466949462891,
          10.847209930419922
        ],
        "friction_weight_ratio_mean": 0.4551662504673004,
        "normal_vertical_fraction_max": 0.006167484913021326,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.13712510466575623,
        "joint_speed_rms": 1.5450395345687866,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.0316624715924263,
        "object_tracking_error_m": 0.034609194844961166,
        "object_tracking_error_rad_max": 0.06965633481740952,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.036787886172533035,
          0.08508812636137009,
          0.28224337100982666,
          0.008518660441040993
        ],
        "steady_command_mae": [
          0.036787886172533035,
          0.08508812636137009,
          0.28224337100982666,
          0.008518660441040993
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.14084605872631073,
        "min_box_clearance_m": 0.5801162719726562,
        "pelvis_amplitude_m": 0.004527926445007324,
        "normal_forces_mean_n": [
          6.496653079986572,
          11.4186372756958
        ],
        "friction_weight_ratio_mean": 0.5524340271949768,
        "normal_vertical_fraction_max": 0.0022965555544942617,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.14179793000221252,
        "joint_speed_rms": 1.546834111213684,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03174494579434395,
        "object_tracking_error_m": 0.034221403300762177,
        "object_tracking_error_rad_max": 0.06382661312818527,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.037321656942367554,
          0.0830000638961792,
          0.271764874458313,
          0.008260702714323997
        ],
        "steady_command_mae": [
          0.037321656942367554,
          0.0830000638961792,
          0.271764874458313,
          0.008260702714323997
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.13992449641227722,
        "min_box_clearance_m": 0.5806325674057007,
        "pelvis_amplitude_m": 0.004381060600280762,
        "normal_forces_mean_n": [
          6.520245552062988,
          11.525035858154297
        ],
        "friction_weight_ratio_mean": 0.5410851836204529,
        "normal_vertical_fraction_max": 0.005563734564930201,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.13870581984519958,
        "joint_speed_rms": 1.5423771142959595,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.031490176916122437,
        "object_tracking_error_m": 0.03365375101566315,
        "object_tracking_error_rad_max": 0.06437008827924728,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03779004514217377,
          0.08699170500040054,
          0.2783432602882385,
          0.00853121280670166
        ],
        "steady_command_mae": [
          0.03779004514217377,
          0.08699170500040054,
          0.2783432602882385,
          0.00853121280670166
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.14069586992263794,
        "min_box_clearance_m": 0.5772270560264587,
        "pelvis_amplitude_m": 0.0047675371170043945,
        "normal_forces_mean_n": [
          5.669962406158447,
          10.793330192565918
        ],
        "friction_weight_ratio_mean": 0.43980997800827026,
        "normal_vertical_fraction_max": 0.008371442556381226,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.19511067867279053,
        "joint_speed_rms": 1.5601651668548584,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.031874772161245346,
        "object_tracking_error_m": 0.034848444163799286,
        "object_tracking_error_rad_max": 0.0696665570139885,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03702224791049957,
          0.08694826811552048,
          0.27947649359703064,
          0.008324837312102318
        ],
        "steady_command_mae": [
          0.03702224791049957,
          0.08694826811552048,
          0.27947649359703064,
          0.008324837312102318
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.13804034888744354,
        "min_box_clearance_m": 0.5820105075836182,
        "pelvis_amplitude_m": 0.004443764686584473,
        "normal_forces_mean_n": [
          6.244187355041504,
          11.398641586303711
        ],
        "friction_weight_ratio_mean": 0.5188490152359009,
        "normal_vertical_fraction_max": 0.019007667899131775,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.13400447368621826,
        "joint_speed_rms": 1.5362982749938965,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03136683255434036,
        "object_tracking_error_m": 0.03219271078705788,
        "object_tracking_error_rad_max": 0.06472709029912949,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03526642173528671,
          0.08570650964975357,
          0.29937440156936646,
          0.00860376376658678
        ],
        "steady_command_mae": [
          0.03526642173528671,
          0.08570650964975357,
          0.29937440156936646,
          0.00860376376658678
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.14059343934059143,
        "min_box_clearance_m": 0.5802949070930481,
        "pelvis_amplitude_m": 0.004616081714630127,
        "normal_forces_mean_n": [
          6.453734397888184,
          11.46552848815918
        ],
        "friction_weight_ratio_mean": 0.5405858755111694,
        "normal_vertical_fraction_max": 0.00462995283305645,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.14876195788383484,
        "joint_speed_rms": 1.5507419109344482,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.031758684664964676,
        "object_tracking_error_m": 0.03394635394215584,
        "object_tracking_error_rad_max": 0.06474640965461731,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03689302131533623,
          0.08104954659938812,
          0.2831784188747406,
          0.008266913704574108
        ],
        "steady_command_mae": [
          0.03689302131533623,
          0.08104954659938812,
          0.2831784188747406,
          0.008266913704574108
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.14049306511878967,
        "min_box_clearance_m": 0.5804102420806885,
        "pelvis_amplitude_m": 0.004431784152984619,
        "normal_forces_mean_n": [
          6.150725364685059,
          11.199655532836914
        ],
        "friction_weight_ratio_mean": 0.5136493444442749,
        "normal_vertical_fraction_max": 0.007545768283307552,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.13608907163143158,
        "joint_speed_rms": 1.5492321252822876,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.031755849719047546,
        "object_tracking_error_m": 0.03375009447336197,
        "object_tracking_error_rad_max": 0.0630292221903801,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03816936910152435,
          0.08591777831315994,
          0.27503642439842224,
          0.0083153722807765
        ],
        "steady_command_mae": [
          0.03816936910152435,
          0.08591777831315994,
          0.27503642439842224,
          0.0083153722807765
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.13810577988624573,
        "min_box_clearance_m": 0.5819171667098999,
        "pelvis_amplitude_m": 0.004460513591766357,
        "normal_forces_mean_n": [
          6.172190189361572,
          11.366387367248535
        ],
        "friction_weight_ratio_mean": 0.5190503001213074,
        "normal_vertical_fraction_max": 0.020221827551722527,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.13516417145729065,
        "joint_speed_rms": 1.5369043350219727,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03124818205833435,
        "object_tracking_error_m": 0.032102495431900024,
        "object_tracking_error_rad_max": 0.06635536253452301,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03757552057504654,
          0.0856788381934166,
          0.2706514894962311,
          0.008498286828398705
        ],
        "steady_command_mae": [
          0.03757552057504654,
          0.0856788381934166,
          0.2706514894962311,
          0.008498286828398705
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.1378859579563141,
        "min_box_clearance_m": 0.5817354917526245,
        "pelvis_amplitude_m": 0.004618644714355469,
        "normal_forces_mean_n": [
          6.289769649505615,
          11.405865669250488
        ],
        "friction_weight_ratio_mean": 0.526465654373169,
        "normal_vertical_fraction_max": 0.01864965818822384,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.15607455372810364,
        "joint_speed_rms": 1.536937952041626,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.031445521861314774,
        "object_tracking_error_m": 0.03227824717760086,
        "object_tracking_error_rad_max": 0.06602361053228378,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.036460500210523605,
          0.08639129996299744,
          0.27846360206604004,
          0.008405447006225586
        ],
        "steady_command_mae": [
          0.036460500210523605,
          0.08639129996299744,
          0.27846360206604004,
          0.008405447006225586
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.13773061335086823,
        "min_box_clearance_m": 0.5817227363586426,
        "pelvis_amplitude_m": 0.004469037055969238,
        "normal_forces_mean_n": [
          6.190751075744629,
          11.287202835083008
        ],
        "friction_weight_ratio_mean": 0.5247226357460022,
        "normal_vertical_fraction_max": 0.018109872937202454,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12908270955085754,
        "joint_speed_rms": 1.537110686302185,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03149876371026039,
        "object_tracking_error_m": 0.032370127737522125,
        "object_tracking_error_rad_max": 0.06600016355514526,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03447867929935455,
          0.08530040085315704,
          0.28097209334373474,
          0.008395278826355934
        ],
        "steady_command_mae": [
          0.03447867929935455,
          0.08530040085315704,
          0.28097209334373474,
          0.008395278826355934
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.14048154652118683,
        "min_box_clearance_m": 0.5779109001159668,
        "pelvis_amplitude_m": 0.004413127899169922,
        "normal_forces_mean_n": [
          5.821479320526123,
          10.772039413452148
        ],
        "friction_weight_ratio_mean": 0.4580860137939453,
        "normal_vertical_fraction_max": 0.005591321270912886,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1374046355485916,
        "joint_speed_rms": 1.544477105140686,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03166310861706734,
        "object_tracking_error_m": 0.03459557145833969,
        "object_tracking_error_rad_max": 0.06889548897743225,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03658675402402878,
          0.0851907730102539,
          0.2793722152709961,
          0.008518481627106667
        ],
        "steady_command_mae": [
          0.03658675402402878,
          0.0851907730102539,
          0.2793722152709961,
          0.008518481627106667
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.14077500998973846,
        "min_box_clearance_m": 0.5800858736038208,
        "pelvis_amplitude_m": 0.0045264363288879395,
        "normal_forces_mean_n": [
          6.52915096282959,
          11.448168754577637
        ],
        "friction_weight_ratio_mean": 0.5538949370384216,
        "normal_vertical_fraction_max": 0.002322172047570348,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1410352885723114,
        "joint_speed_rms": 1.5465760231018066,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03174227103590965,
        "object_tracking_error_m": 0.03421563282608986,
        "object_tracking_error_rad_max": 0.06407491862773895,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.037703048437833786,
          0.08363745361566544,
          0.2783917784690857,
          0.008266759105026722
        ],
        "steady_command_mae": [
          0.037703048437833786,
          0.08363745361566544,
          0.2783917784690857,
          0.008266759105026722
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.14011912047863007,
        "min_box_clearance_m": 0.5806408524513245,
        "pelvis_amplitude_m": 0.004382789134979248,
        "normal_forces_mean_n": [
          6.448692321777344,
          11.462316513061523
        ],
        "friction_weight_ratio_mean": 0.5386604070663452,
        "normal_vertical_fraction_max": 0.005360364448279142,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1416090577840805,
        "joint_speed_rms": 1.540550947189331,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03149811550974846,
        "object_tracking_error_m": 0.03366690129041672,
        "object_tracking_error_rad_max": 0.06390521675348282,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03733643889427185,
          0.08702906966209412,
          0.2782868444919586,
          0.00852656364440918
        ],
        "steady_command_mae": [
          0.03733643889427185,
          0.08702906966209412,
          0.2782868444919586,
          0.00852656364440918
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.1405826359987259,
        "min_box_clearance_m": 0.5773590207099915,
        "pelvis_amplitude_m": 0.0047646164894104,
        "normal_forces_mean_n": [
          5.819293022155762,
          10.913091659545898
        ],
        "friction_weight_ratio_mean": 0.4471908509731293,
        "normal_vertical_fraction_max": 0.00820908322930336,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.19502374529838562,
        "joint_speed_rms": 1.5604294538497925,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.031871646642684937,
        "object_tracking_error_m": 0.034822262823581696,
        "object_tracking_error_rad_max": 0.0695490762591362,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03756190091371536,
          0.0873861312866211,
          0.2786436975002289,
          0.008320128545165062
        ],
        "steady_command_mae": [
          0.03756190091371536,
          0.0873861312866211,
          0.2786436975002289,
          0.008320128545165062
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.13810017704963684,
        "min_box_clearance_m": 0.5820604562759399,
        "pelvis_amplitude_m": 0.004440665245056152,
        "normal_forces_mean_n": [
          6.2074174880981445,
          11.3799409866333
        ],
        "friction_weight_ratio_mean": 0.5184141397476196,
        "normal_vertical_fraction_max": 0.018934354186058044,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1339789628982544,
        "joint_speed_rms": 1.5362110137939453,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03137259557843208,
        "object_tracking_error_m": 0.03219236060976982,
        "object_tracking_error_rad_max": 0.0644347295165062,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.035493988543748856,
          0.0855669230222702,
          0.2963596284389496,
          0.008605754002928734
        ],
        "steady_command_mae": [
          0.035493988543748856,
          0.0855669230222702,
          0.2963596284389496,
          0.008605754002928734
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.1406794935464859,
        "min_box_clearance_m": 0.5803021788597107,
        "pelvis_amplitude_m": 0.004619300365447998,
        "normal_forces_mean_n": [
          6.386233329772949,
          11.417784690856934
        ],
        "friction_weight_ratio_mean": 0.5411781668663025,
        "normal_vertical_fraction_max": 0.00444383081048727,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.15109293162822723,
        "joint_speed_rms": 1.5504364967346191,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.031761445105075836,
        "object_tracking_error_m": 0.03395073488354683,
        "object_tracking_error_rad_max": 0.06453685462474823,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.036507029086351395,
          0.08047682791948318,
          0.28077641129493713,
          0.008261608891189098
        ],
        "steady_command_mae": [
          0.036507029086351395,
          0.08047682791948318,
          0.28077641129493713,
          0.008261608891189098
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.14050151407718658,
        "min_box_clearance_m": 0.5804635882377625,
        "pelvis_amplitude_m": 0.004425227642059326,
        "normal_forces_mean_n": [
          6.296761512756348,
          11.33452320098877
        ],
        "friction_weight_ratio_mean": 0.5169759392738342,
        "normal_vertical_fraction_max": 0.007157504092901945,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.13523046672344208,
        "joint_speed_rms": 1.549046277999878,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.031745221465826035,
        "object_tracking_error_m": 0.033743999898433685,
        "object_tracking_error_rad_max": 0.0630963146686554,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      }
    ],
    "goal_limits": {
      "height_low": 0.6068800687789917,
      "height_high": 0.7268800735473633,
      "height_rate": 0.11247000098228455,
      "vx_high": 0.0,
      "forward_admitted": false,
      "reference_fps": 50,
      "episode_seconds": 30.0
    },
    "reference_free": false,
    "terminal_state_before_reset": true,
    "physical_model": {
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
      "control": "PPO joint-position offsets with PD each physics substep; no P0 feedforward or WBC"
    },
    "accepted_policy": false,
    "motion_quality": {
      "clip_0_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.10562381893396378,
          "lower_body_style_rmse_rad": 0.06561952829360962,
          "reference_compatibility_mean": 0.8663001563748356,
          "joint_acceleration_rms_rad_s2": 65.26625061035156,
          "box_relative_translation_drift_max_m": 0.054177456209774016,
          "box_relative_rotation_drift_max_rad": 0.04349649478615422
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.10581427812576294,
          "lower_body_style_rmse_rad": 0.0680929496884346,
          "reference_compatibility_mean": 0.8585197611725688,
          "joint_acceleration_rms_rad_s2": 64.73358154296875,
          "box_relative_translation_drift_max_m": 0.05418649862606618,
          "box_relative_rotation_drift_max_rad": 0.0462353600247447
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.10565996170043945,
          "lower_body_style_rmse_rad": 0.0656748116016388,
          "reference_compatibility_mean": 0.8634093070251909,
          "joint_acceleration_rms_rad_s2": 65.15270233154297,
          "box_relative_translation_drift_max_m": 0.05458945137906955,
          "box_relative_rotation_drift_max_rad": 0.04534624777980132
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.1067960113286972,
          "lower_body_style_rmse_rad": 0.06715160608291626,
          "reference_compatibility_mean": 0.863161527318576,
          "joint_acceleration_rms_rad_s2": 63.841007232666016,
          "box_relative_translation_drift_max_m": 0.05855884117336023,
          "box_relative_rotation_drift_max_rad": 0.05630528445910562
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.10713247209787369,
          "lower_body_style_rmse_rad": 0.06699303537607193,
          "reference_compatibility_mean": 0.860819654539713,
          "joint_acceleration_rms_rad_s2": 63.83433151245117,
          "box_relative_translation_drift_max_m": 0.056408444272591965,
          "box_relative_rotation_drift_max_rad": 0.05607842532063081
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.10670141875743866,
          "lower_body_style_rmse_rad": 0.06579013168811798,
          "reference_compatibility_mean": 0.8698356725188342,
          "joint_acceleration_rms_rad_s2": 64.0269775390625,
          "box_relative_translation_drift_max_m": 0.05585024923009795,
          "box_relative_rotation_drift_max_rad": 0.05345840287509956
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.10745221376419067,
          "lower_body_style_rmse_rad": 0.06924265623092651,
          "reference_compatibility_mean": 0.8532540569345988,
          "joint_acceleration_rms_rad_s2": 64.21184539794922,
          "box_relative_translation_drift_max_m": 0.05826977431253009,
          "box_relative_rotation_drift_max_rad": 0.057870661948306444
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.10555500537157059,
          "lower_body_style_rmse_rad": 0.0655776634812355,
          "reference_compatibility_mean": 0.8663171670855329,
          "joint_acceleration_rms_rad_s2": 65.38904571533203,
          "box_relative_translation_drift_max_m": 0.05428734410347579,
          "box_relative_rotation_drift_max_rad": 0.04504601016907981
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.10687068104743958,
          "lower_body_style_rmse_rad": 0.0688944086432457,
          "reference_compatibility_mean": 0.8570346666183488,
          "joint_acceleration_rms_rad_s2": 64.36439514160156,
          "box_relative_translation_drift_max_m": 0.05602449313182169,
          "box_relative_rotation_drift_max_rad": 0.05544288791836919
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.10715996474027634,
          "lower_body_style_rmse_rad": 0.06611242890357971,
          "reference_compatibility_mean": 0.8689494525941187,
          "joint_acceleration_rms_rad_s2": 64.45350646972656,
          "box_relative_translation_drift_max_m": 0.05629409124925051,
          "box_relative_rotation_drift_max_rad": 0.053838038382473606
        }
      ],
      "clip_1_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.10560762882232666,
          "lower_body_style_rmse_rad": 0.06559325009584427,
          "reference_compatibility_mean": 0.8668356280112823,
          "joint_acceleration_rms_rad_s2": 65.28386688232422,
          "box_relative_translation_drift_max_m": 0.05410726937018291,
          "box_relative_rotation_drift_max_rad": 0.04347526812445328
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.10580714046955109,
          "lower_body_style_rmse_rad": 0.06809844076633453,
          "reference_compatibility_mean": 0.8585214682369008,
          "joint_acceleration_rms_rad_s2": 64.68985748291016,
          "box_relative_translation_drift_max_m": 0.05418574043693778,
          "box_relative_rotation_drift_max_rad": 0.046222824888735733
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.10562319308519363,
          "lower_body_style_rmse_rad": 0.0656537339091301,
          "reference_compatibility_mean": 0.8635025886379557,
          "joint_acceleration_rms_rad_s2": 65.0098648071289,
          "box_relative_translation_drift_max_m": 0.054430761254780545,
          "box_relative_rotation_drift_max_rad": 0.04537686783930297
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.10676980018615723,
          "lower_body_style_rmse_rad": 0.06714648753404617,
          "reference_compatibility_mean": 0.8633427245235448,
          "joint_acceleration_rms_rad_s2": 63.86875534057617,
          "box_relative_translation_drift_max_m": 0.05843746022924355,
          "box_relative_rotation_drift_max_rad": 0.05627609764519523
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.10713782161474228,
          "lower_body_style_rmse_rad": 0.06713808327913284,
          "reference_compatibility_mean": 0.8607979149668422,
          "joint_acceleration_rms_rad_s2": 63.78030776977539,
          "box_relative_translation_drift_max_m": 0.05639857697364608,
          "box_relative_rotation_drift_max_rad": 0.05606917930238977
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.1066809743642807,
          "lower_body_style_rmse_rad": 0.06576725840568542,
          "reference_compatibility_mean": 0.8704108053572247,
          "joint_acceleration_rms_rad_s2": 63.89105987548828,
          "box_relative_translation_drift_max_m": 0.05578296725582147,
          "box_relative_rotation_drift_max_rad": 0.05323857712105001
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.107465460896492,
          "lower_body_style_rmse_rad": 0.06924315541982651,
          "reference_compatibility_mean": 0.8532087382026227,
          "joint_acceleration_rms_rad_s2": 64.15711975097656,
          "box_relative_translation_drift_max_m": 0.058179932009763964,
          "box_relative_rotation_drift_max_rad": 0.057852507359992984
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.10553135722875595,
          "lower_body_style_rmse_rad": 0.06557503342628479,
          "reference_compatibility_mean": 0.8661575012126003,
          "joint_acceleration_rms_rad_s2": 65.4071044921875,
          "box_relative_translation_drift_max_m": 0.05422314882183278,
          "box_relative_rotation_drift_max_rad": 0.04514221806217381
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.10686943680047989,
          "lower_body_style_rmse_rad": 0.06888800114393234,
          "reference_compatibility_mean": 0.8569812618551887,
          "joint_acceleration_rms_rad_s2": 64.37895202636719,
          "box_relative_translation_drift_max_m": 0.055997732530338844,
          "box_relative_rotation_drift_max_rad": 0.05545450064583095
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.10718817263841629,
          "lower_body_style_rmse_rad": 0.06612040847539902,
          "reference_compatibility_mean": 0.8690837930059112,
          "joint_acceleration_rms_rad_s2": 64.4566879272461,
          "box_relative_translation_drift_max_m": 0.0563242075633194,
          "box_relative_rotation_drift_max_rad": 0.053836142345718034
        }
      ]
    },
    "directory": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795176993127086405",
    "checkpoint": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/dashboard/stage1/WholeBodyTracking/20261120_100628-stage1-locomotion/model_01499.pt",
    "final": false,
    "selection_score": 0.010238462405709121,
    "failure_counts": {
      "physical_failure/loss_of_grasp": 20,
      "incomplete_episode": 20,
      "contact_interruption": 20,
      "hand_slip": 20,
      "insufficient_friction_support": 20,
      "contact_near_box_bottom": 20
    },
    "scenarios": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "completed_updates": 1500
  },
  {
    "passed": false,
    "score": 0.0,
    "suite": "stage1",
    "groups": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "trials": [
      {
        "scenario": "clip_0",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.030764400959014893,
          0.01884046196937561,
          0.41437244415283203,
          0.012981915846467018
        ],
        "steady_command_mae": [
          0.030764400959014893,
          0.01884046196937561,
          0.41437244415283203,
          0.012981915846467018
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12019597738981247,
        "min_box_clearance_m": 0.57801353931427,
        "pelvis_amplitude_m": 0.008375704288482666,
        "normal_forces_mean_n": [
          6.915358543395996,
          13.34498405456543
        ],
        "friction_weight_ratio_mean": 0.4502415657043457,
        "normal_vertical_fraction_max": 0.04541514068841934,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.02882685326039791,
        "joint_speed_rms": 1.4597983360290527,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03002292290329933,
        "object_tracking_error_m": 0.03176635876297951,
        "object_tracking_error_rad_max": 0.10772749036550522,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02986907586455345,
          0.016600193455815315,
          0.4221642017364502,
          0.013177812099456787
        ],
        "steady_command_mae": [
          0.02986907586455345,
          0.016600193455815315,
          0.4221642017364502,
          0.013177812099456787
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12061294913291931,
        "min_box_clearance_m": 0.5780519247055054,
        "pelvis_amplitude_m": 0.008576691150665283,
        "normal_forces_mean_n": [
          7.016439914703369,
          13.466949462890625
        ],
        "friction_weight_ratio_mean": 0.4453728199005127,
        "normal_vertical_fraction_max": 0.044073618948459625,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.02928338013589382,
        "joint_speed_rms": 1.4578689336776733,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.030175045132637024,
        "object_tracking_error_m": 0.031996484845876694,
        "object_tracking_error_rad_max": 0.10518836975097656,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.027635017409920692,
          0.019429294392466545,
          0.43789058923721313,
          0.013104140758514404
        ],
        "steady_command_mae": [
          0.027635017409920692,
          0.019429294392466545,
          0.43789058923721313,
          0.013104140758514404
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12205438315868378,
        "min_box_clearance_m": 0.5781211256980896,
        "pelvis_amplitude_m": 0.008458077907562256,
        "normal_forces_mean_n": [
          6.9315619468688965,
          13.44774341583252
        ],
        "friction_weight_ratio_mean": 0.45326805114746094,
        "normal_vertical_fraction_max": 0.042627282440662384,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.15173333883285522,
        "joint_speed_rms": 1.4633218050003052,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.0303487628698349,
        "object_tracking_error_m": 0.032082561403512955,
        "object_tracking_error_rad_max": 0.1043858751654625,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02674848772585392,
          0.01766408048570156,
          0.43989133834838867,
          0.013050591573119164
        ],
        "steady_command_mae": [
          0.02674848772585392,
          0.01766408048570156,
          0.43989133834838867,
          0.013050591573119164
        ],
        "contact_continuity": 0.1600000262260437,
        "max_hand_slip_m": 0.1213001236319542,
        "min_box_clearance_m": 0.575259268283844,
        "pelvis_amplitude_m": 0.00835806131362915,
        "normal_forces_mean_n": [
          7.693157196044922,
          13.798578262329102
        ],
        "friction_weight_ratio_mean": 0.44517308473587036,
        "normal_vertical_fraction_max": 0.03825831413269043,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.14827053248882294,
        "joint_speed_rms": 1.4610896110534668,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.030136292800307274,
        "object_tracking_error_m": 0.03427188843488693,
        "object_tracking_error_rad_max": 0.10283848643302917,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03125227242708206,
          0.016637250781059265,
          0.44227299094200134,
          0.013260507956147194
        ],
        "steady_command_mae": [
          0.03125227242708206,
          0.016637250781059265,
          0.44227299094200134,
          0.013260507956147194
        ],
        "contact_continuity": 0.14000001549720764,
        "max_hand_slip_m": 0.12341945618391037,
        "min_box_clearance_m": 0.5768786668777466,
        "pelvis_amplitude_m": 0.00853651762008667,
        "normal_forces_mean_n": [
          7.475546836853027,
          13.746264457702637
        ],
        "friction_weight_ratio_mean": 0.4791705012321472,
        "normal_vertical_fraction_max": 0.033926356583833694,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.028094198554754257,
        "joint_speed_rms": 1.4665926694869995,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.030453478917479515,
        "object_tracking_error_m": 0.03400799259543419,
        "object_tracking_error_rad_max": 0.09861680865287781,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03204718232154846,
          0.016363980248570442,
          0.4256357252597809,
          0.01285694818943739
        ],
        "steady_command_mae": [
          0.03204718232154846,
          0.016363980248570442,
          0.4256357252597809,
          0.01285694818943739
        ],
        "contact_continuity": 0.15000002086162567,
        "max_hand_slip_m": 0.12019810825586319,
        "min_box_clearance_m": 0.5768611431121826,
        "pelvis_amplitude_m": 0.008210062980651855,
        "normal_forces_mean_n": [
          7.814248085021973,
          14.00648307800293
        ],
        "friction_weight_ratio_mean": 0.4695758819580078,
        "normal_vertical_fraction_max": 0.0381200835108757,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.028229499235749245,
        "joint_speed_rms": 1.4537347555160522,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02992994152009487,
        "object_tracking_error_m": 0.03338896110653877,
        "object_tracking_error_rad_max": 0.10164617747068405,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03250806778669357,
          0.017628511413931847,
          0.4257725775241852,
          0.013293623924255371
        ],
        "steady_command_mae": [
          0.03250806778669357,
          0.017628511413931847,
          0.4257725775241852,
          0.013293623924255371
        ],
        "contact_continuity": 0.15000002086162567,
        "max_hand_slip_m": 0.1236029639840126,
        "min_box_clearance_m": 0.5759114623069763,
        "pelvis_amplitude_m": 0.008777081966400146,
        "normal_forces_mean_n": [
          7.429415702819824,
          13.751886367797852
        ],
        "friction_weight_ratio_mean": 0.46409764885902405,
        "normal_vertical_fraction_max": 0.03231368213891983,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.02890706993639469,
        "joint_speed_rms": 1.4694722890853882,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.030577752739191055,
        "object_tracking_error_m": 0.034283436834812164,
        "object_tracking_error_rad_max": 0.10229324549436569,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02849995717406273,
          0.019090957939624786,
          0.4169539511203766,
          0.013003015890717506
        ],
        "steady_command_mae": [
          0.02849995717406273,
          0.019090957939624786,
          0.4169539511203766,
          0.013003015890717506
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12049316614866257,
        "min_box_clearance_m": 0.5781657695770264,
        "pelvis_amplitude_m": 0.00840085744857788,
        "normal_forces_mean_n": [
          6.941313743591309,
          13.387418746948242
        ],
        "friction_weight_ratio_mean": 0.4521613121032715,
        "normal_vertical_fraction_max": 0.04436655342578888,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.028930645436048508,
        "joint_speed_rms": 1.458423376083374,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.030178958550095558,
        "object_tracking_error_m": 0.031858187168836594,
        "object_tracking_error_rad_max": 0.10550703853368759,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.030739223584532738,
          0.017796559259295464,
          0.43946051597595215,
          0.013287603855133057
        ],
        "steady_command_mae": [
          0.030739223584532738,
          0.017796559259295464,
          0.43946051597595215,
          0.013287603855133057
        ],
        "contact_continuity": 0.14000001549720764,
        "max_hand_slip_m": 0.12370651215314865,
        "min_box_clearance_m": 0.5767396688461304,
        "pelvis_amplitude_m": 0.008632898330688477,
        "normal_forces_mean_n": [
          7.382293701171875,
          13.72313117980957
        ],
        "friction_weight_ratio_mean": 0.4720320701599121,
        "normal_vertical_fraction_max": 0.03616618737578392,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1537284255027771,
        "joint_speed_rms": 1.470859408378601,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.030451700091362,
        "object_tracking_error_m": 0.0337417833507061,
        "object_tracking_error_rad_max": 0.10061515867710114,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.030836110934615135,
          0.018723463639616966,
          0.43618208169937134,
          0.013081955723464489
        ],
        "steady_command_mae": [
          0.030836110934615135,
          0.018723463639616966,
          0.43618208169937134,
          0.013081955723464489
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.12349259108304977,
        "min_box_clearance_m": 0.5770003795623779,
        "pelvis_amplitude_m": 0.00849604606628418,
        "normal_forces_mean_n": [
          7.260990142822266,
          13.621914863586426
        ],
        "friction_weight_ratio_mean": 0.4618421196937561,
        "normal_vertical_fraction_max": 0.03582784906029701,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.02763378620147705,
        "joint_speed_rms": 1.4705196619033813,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03060024417936802,
        "object_tracking_error_m": 0.03342091292142868,
        "object_tracking_error_rad_max": 0.09915044903755188,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03111882135272026,
          0.01879449561238289,
          0.41558218002319336,
          0.012962877750396729
        ],
        "steady_command_mae": [
          0.03111882135272026,
          0.01879449561238289,
          0.41558218002319336,
          0.012962877750396729
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12022485584020615,
        "min_box_clearance_m": 0.5780029296875,
        "pelvis_amplitude_m": 0.008374571800231934,
        "normal_forces_mean_n": [
          6.929274559020996,
          13.361231803894043
        ],
        "friction_weight_ratio_mean": 0.4505843222141266,
        "normal_vertical_fraction_max": 0.04548579826951027,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.03061423823237419,
        "joint_speed_rms": 1.4588088989257812,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.030018577352166176,
        "object_tracking_error_m": 0.03176816552877426,
        "object_tracking_error_rad_max": 0.10779739916324615,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.030161971226334572,
          0.016558896750211716,
          0.4195876121520996,
          0.013170862570405006
        ],
        "steady_command_mae": [
          0.030161971226334572,
          0.016558896750211716,
          0.4195876121520996,
          0.013170862570405006
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12062518298625946,
        "min_box_clearance_m": 0.5780492424964905,
        "pelvis_amplitude_m": 0.00857400894165039,
        "normal_forces_mean_n": [
          7.022467613220215,
          13.47637939453125
        ],
        "friction_weight_ratio_mean": 0.445075124502182,
        "normal_vertical_fraction_max": 0.044103480875492096,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.031221169978380203,
        "joint_speed_rms": 1.4575579166412354,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.030173256993293762,
        "object_tracking_error_m": 0.03199728578329086,
        "object_tracking_error_rad_max": 0.10520514100790024,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02774834632873535,
          0.01947801187634468,
          0.43561673164367676,
          0.013101744465529919
        ],
        "steady_command_mae": [
          0.02774834632873535,
          0.01947801187634468,
          0.43561673164367676,
          0.013101744465529919
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12203816324472427,
        "min_box_clearance_m": 0.5781210064888,
        "pelvis_amplitude_m": 0.008455157279968262,
        "normal_forces_mean_n": [
          6.986070156097412,
          13.497782707214355
        ],
        "friction_weight_ratio_mean": 0.45431575179100037,
        "normal_vertical_fraction_max": 0.042695026844739914,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1519785374403,
        "joint_speed_rms": 1.4627872705459595,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.030349498614668846,
        "object_tracking_error_m": 0.03208078071475029,
        "object_tracking_error_rad_max": 0.10445253551006317,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02750394307076931,
          0.018510904163122177,
          0.43626266717910767,
          0.013089096173644066
        ],
        "steady_command_mae": [
          0.02750394307076931,
          0.018510904163122177,
          0.43626266717910767,
          0.013089096173644066
        ],
        "contact_continuity": 0.1600000262260437,
        "max_hand_slip_m": 0.12279889732599258,
        "min_box_clearance_m": 0.5770902037620544,
        "pelvis_amplitude_m": 0.00838547945022583,
        "normal_forces_mean_n": [
          7.757420539855957,
          13.847192764282227
        ],
        "friction_weight_ratio_mean": 0.486785888671875,
        "normal_vertical_fraction_max": 0.031428929418325424,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.14738395810127258,
        "joint_speed_rms": 1.4616926908493042,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.030249755829572678,
        "object_tracking_error_m": 0.033949028700590134,
        "object_tracking_error_rad_max": 0.10019645094871521,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.031102031469345093,
          0.01668628491461277,
          0.4417218565940857,
          0.013260483741760254
        ],
        "steady_command_mae": [
          0.031102031469345093,
          0.01668628491461277,
          0.4417218565940857,
          0.013260483741760254
        ],
        "contact_continuity": 0.14000001549720764,
        "max_hand_slip_m": 0.12338798493146896,
        "min_box_clearance_m": 0.5768551826477051,
        "pelvis_amplitude_m": 0.008537352085113525,
        "normal_forces_mean_n": [
          7.496241569519043,
          13.763984680175781
        ],
        "friction_weight_ratio_mean": 0.47825193405151367,
        "normal_vertical_fraction_max": 0.0340314581990242,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.028480883687734604,
        "joint_speed_rms": 1.467216968536377,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.030450919643044472,
        "object_tracking_error_m": 0.03400977700948715,
        "object_tracking_error_rad_max": 0.09875079989433289,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03181096911430359,
          0.016830122098326683,
          0.4243950843811035,
          0.012928962707519531
        ],
        "steady_command_mae": [
          0.03181096911430359,
          0.016830122098326683,
          0.4243950843811035,
          0.012928962707519531
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.12295009940862656,
        "min_box_clearance_m": 0.5768325924873352,
        "pelvis_amplitude_m": 0.008313417434692383,
        "normal_forces_mean_n": [
          7.3971734046936035,
          13.719828605651855
        ],
        "friction_weight_ratio_mean": 0.46191978454589844,
        "normal_vertical_fraction_max": 0.03741089999675751,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.02727712132036686,
        "joint_speed_rms": 1.461498498916626,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.030218398198485374,
        "object_tracking_error_m": 0.03347392752766609,
        "object_tracking_error_rad_max": 0.10058975964784622,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03257066756486893,
          0.017586898058652878,
          0.4261176586151123,
          0.01329425536096096
        ],
        "steady_command_mae": [
          0.03257066756486893,
          0.017586898058652878,
          0.4261176586151123,
          0.01329425536096096
        ],
        "contact_continuity": 0.15000002086162567,
        "max_hand_slip_m": 0.12362014502286911,
        "min_box_clearance_m": 0.575935959815979,
        "pelvis_amplitude_m": 0.008779644966125488,
        "normal_forces_mean_n": [
          7.459886074066162,
          13.783414840698242
        ],
        "friction_weight_ratio_mean": 0.46559077501296997,
        "normal_vertical_fraction_max": 0.03235378488898277,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.02860776148736477,
        "joint_speed_rms": 1.4700273275375366,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03058038279414177,
        "object_tracking_error_m": 0.03427800163626671,
        "object_tracking_error_rad_max": 0.10240668803453445,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.028798814862966537,
          0.019187655299901962,
          0.42024025321006775,
          0.013001596555113792
        ],
        "steady_command_mae": [
          0.028798814862966537,
          0.019187655299901962,
          0.42024025321006775,
          0.013001596555113792
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12051910161972046,
        "min_box_clearance_m": 0.578170657157898,
        "pelvis_amplitude_m": 0.00839930772781372,
        "normal_forces_mean_n": [
          6.950943946838379,
          13.394281387329102
        ],
        "friction_weight_ratio_mean": 0.4522460997104645,
        "normal_vertical_fraction_max": 0.044367119669914246,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.027826225385069847,
        "joint_speed_rms": 1.4592921733856201,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03018399514257908,
        "object_tracking_error_m": 0.03185601159930229,
        "object_tracking_error_rad_max": 0.10556051880121231,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.030848806723952293,
          0.018078625202178955,
          0.44124698638916016,
          0.013293921947479248
        ],
        "steady_command_mae": [
          0.030848806723952293,
          0.018078625202178955,
          0.44124698638916016,
          0.013293921947479248
        ],
        "contact_continuity": 0.14000001549720764,
        "max_hand_slip_m": 0.12369939684867859,
        "min_box_clearance_m": 0.5767350792884827,
        "pelvis_amplitude_m": 0.008638858795166016,
        "normal_forces_mean_n": [
          7.459794521331787,
          13.794839859008789
        ],
        "friction_weight_ratio_mean": 0.4741570055484772,
        "normal_vertical_fraction_max": 0.03636929392814636,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1536131203174591,
        "joint_speed_rms": 1.4708861112594604,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.03045559488236904,
        "object_tracking_error_m": 0.033737268298864365,
        "object_tracking_error_rad_max": 0.10084901750087738,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.030787089839577675,
          0.0184748787432909,
          0.4374025762081146,
          0.013087844476103783
        ],
        "steady_command_mae": [
          0.030787089839577675,
          0.0184748787432909,
          0.4374025762081146,
          0.013087844476103783
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.12350231409072876,
        "min_box_clearance_m": 0.5770286321640015,
        "pelvis_amplitude_m": 0.008501291275024414,
        "normal_forces_mean_n": [
          7.242371559143066,
          13.608072280883789
        ],
        "friction_weight_ratio_mean": 0.46186184883117676,
        "normal_vertical_fraction_max": 0.03578890487551689,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.028019238263368607,
        "joint_speed_rms": 1.4710326194763184,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.0306012574583292,
        "object_tracking_error_m": 0.03341767191886902,
        "object_tracking_error_rad_max": 0.09908945113420486,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      }
    ],
    "goal_limits": {
      "height_low": 0.6068800687789917,
      "height_high": 0.7268800735473633,
      "height_rate": 0.11247000098228455,
      "vx_high": 0.0,
      "forward_admitted": false,
      "reference_fps": 50,
      "episode_seconds": 30.0
    },
    "reference_free": false,
    "terminal_state_before_reset": true,
    "physical_model": {
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
      "control": "PPO joint-position offsets with PD each physics substep; no P0 feedforward or WBC"
    },
    "accepted_policy": false,
    "motion_quality": {
      "clip_0_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.09598325192928314,
          "lower_body_style_rmse_rad": 0.07564572989940643,
          "reference_compatibility_mean": 0.6925693053600398,
          "joint_acceleration_rms_rad_s2": 59.07049560546875,
          "box_relative_translation_drift_max_m": 0.048612733782380936,
          "box_relative_rotation_drift_max_rad": 0.11957585592273873
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.09614122658967972,
          "lower_body_style_rmse_rad": 0.07565982639789581,
          "reference_compatibility_mean": 0.6857628125629842,
          "joint_acceleration_rms_rad_s2": 58.982032775878906,
          "box_relative_translation_drift_max_m": 0.048908340309479235,
          "box_relative_rotation_drift_max_rad": 0.11639881709343798
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.09622150659561157,
          "lower_body_style_rmse_rad": 0.07533174008131027,
          "reference_compatibility_mean": 0.6889798889840173,
          "joint_acceleration_rms_rad_s2": 59.36373519897461,
          "box_relative_translation_drift_max_m": 0.049536554293999294,
          "box_relative_rotation_drift_max_rad": 0.11746588451423876
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.09632813930511475,
          "lower_body_style_rmse_rad": 0.07529444247484207,
          "reference_compatibility_mean": 0.6926951157980712,
          "joint_acceleration_rms_rad_s2": 58.8328857421875,
          "box_relative_translation_drift_max_m": 0.052212247794966665,
          "box_relative_rotation_drift_max_rad": 0.1157976784111097
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.09725508838891983,
          "lower_body_style_rmse_rad": 0.07591402530670166,
          "reference_compatibility_mean": 0.6865293724618221,
          "joint_acceleration_rms_rad_s2": 58.66195297241211,
          "box_relative_translation_drift_max_m": 0.05056639575745032,
          "box_relative_rotation_drift_max_rad": 0.1119626734315536
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.09641708433628082,
          "lower_body_style_rmse_rad": 0.07609604299068451,
          "reference_compatibility_mean": 0.6984699570560188,
          "joint_acceleration_rms_rad_s2": 58.66376876831055,
          "box_relative_translation_drift_max_m": 0.04978455502343307,
          "box_relative_rotation_drift_max_rad": 0.11444184076381715
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.09756220132112503,
          "lower_body_style_rmse_rad": 0.07675717771053314,
          "reference_compatibility_mean": 0.6780091881208218,
          "joint_acceleration_rms_rad_s2": 58.70753479003906,
          "box_relative_translation_drift_max_m": 0.05052841593872035,
          "box_relative_rotation_drift_max_rad": 0.1166895316649139
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.09606786072254181,
          "lower_body_style_rmse_rad": 0.07551967352628708,
          "reference_compatibility_mean": 0.6917102758547806,
          "joint_acceleration_rms_rad_s2": 59.05024719238281,
          "box_relative_translation_drift_max_m": 0.048900337817273626,
          "box_relative_rotation_drift_max_rad": 0.11705943071170741
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.0969899371266365,
          "lower_body_style_rmse_rad": 0.07522062957286835,
          "reference_compatibility_mean": 0.6830272833724695,
          "joint_acceleration_rms_rad_s2": 58.921775817871094,
          "box_relative_translation_drift_max_m": 0.05065691178196891,
          "box_relative_rotation_drift_max_rad": 0.1149847265035077
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.09739809483289719,
          "lower_body_style_rmse_rad": 0.07618491351604462,
          "reference_compatibility_mean": 0.6873415381794524,
          "joint_acceleration_rms_rad_s2": 59.04922103881836,
          "box_relative_translation_drift_max_m": 0.0502666842958512,
          "box_relative_rotation_drift_max_rad": 0.11209693008905558
        }
      ],
      "clip_1_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.09597302228212357,
          "lower_body_style_rmse_rad": 0.07559802383184433,
          "reference_compatibility_mean": 0.6929031402397404,
          "joint_acceleration_rms_rad_s2": 58.9588508605957,
          "box_relative_translation_drift_max_m": 0.048605149099870834,
          "box_relative_rotation_drift_max_rad": 0.11943787626112658
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.09613760560750961,
          "lower_body_style_rmse_rad": 0.07544218748807907,
          "reference_compatibility_mean": 0.6859424080465673,
          "joint_acceleration_rms_rad_s2": 58.94514465332031,
          "box_relative_translation_drift_max_m": 0.04888217450898544,
          "box_relative_rotation_drift_max_rad": 0.11632202566584916
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.09623436629772186,
          "lower_body_style_rmse_rad": 0.07532346248626709,
          "reference_compatibility_mean": 0.6890780486583454,
          "joint_acceleration_rms_rad_s2": 59.25678634643555,
          "box_relative_translation_drift_max_m": 0.04949134456915155,
          "box_relative_rotation_drift_max_rad": 0.11744334441120902
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.09662478417158127,
          "lower_body_style_rmse_rad": 0.07540161907672882,
          "reference_compatibility_mean": 0.6912209123123642,
          "joint_acceleration_rms_rad_s2": 58.836036682128906,
          "box_relative_translation_drift_max_m": 0.05066322071610726,
          "box_relative_rotation_drift_max_rad": 0.11551426785522356
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.09724827855825424,
          "lower_body_style_rmse_rad": 0.07591874897480011,
          "reference_compatibility_mean": 0.6865357670285213,
          "joint_acceleration_rms_rad_s2": 58.68147277832031,
          "box_relative_translation_drift_max_m": 0.05057896050343616,
          "box_relative_rotation_drift_max_rad": 0.11205360984842465
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.09682975709438324,
          "lower_body_style_rmse_rad": 0.07588355243206024,
          "reference_compatibility_mean": 0.6951791071546062,
          "joint_acceleration_rms_rad_s2": 58.55741882324219,
          "box_relative_translation_drift_max_m": 0.05044442963810377,
          "box_relative_rotation_drift_max_rad": 0.11350526592553142
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.09757013618946075,
          "lower_body_style_rmse_rad": 0.0769595056772232,
          "reference_compatibility_mean": 0.6780535747144889,
          "joint_acceleration_rms_rad_s2": 58.68822479248047,
          "box_relative_translation_drift_max_m": 0.05049794869525651,
          "box_relative_rotation_drift_max_rad": 0.11673417913278518
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.09605638682842255,
          "lower_body_style_rmse_rad": 0.07551489025354385,
          "reference_compatibility_mean": 0.691860592935261,
          "joint_acceleration_rms_rad_s2": 59.111759185791016,
          "box_relative_translation_drift_max_m": 0.04887313910230617,
          "box_relative_rotation_drift_max_rad": 0.11676550855709891
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.09701506048440933,
          "lower_body_style_rmse_rad": 0.07523860782384872,
          "reference_compatibility_mean": 0.6829162011864521,
          "joint_acceleration_rms_rad_s2": 58.84743118286133,
          "box_relative_translation_drift_max_m": 0.05059932147922189,
          "box_relative_rotation_drift_max_rad": 0.11523911303699347
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.09738703817129135,
          "lower_body_style_rmse_rad": 0.07618911564350128,
          "reference_compatibility_mean": 0.687123069675036,
          "joint_acceleration_rms_rad_s2": 59.07891845703125,
          "box_relative_translation_drift_max_m": 0.050270668642189695,
          "box_relative_rotation_drift_max_rad": 0.1119740141831197
        }
      ]
    },
    "directory": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795184787477293549",
    "checkpoint": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/dashboard/stage1/WholeBodyTracking/20261120_121653-stage1-locomotion/model_01999.pt",
    "final": false,
    "selection_score": 0.014138463156727643,
    "failure_counts": {
      "physical_failure/loss_of_grasp": 20,
      "incomplete_episode": 20,
      "contact_interruption": 20,
      "hand_slip": 20,
      "insufficient_friction_support": 20,
      "contact_near_box_bottom": 20
    },
    "scenarios": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "completed_updates": 2000
  },
  {
    "passed": false,
    "score": 0.0,
    "suite": "stage1",
    "groups": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "trials": [
      {
        "scenario": "clip_0",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.037813372910022736,
          0.027337919920682907,
          0.12875469028949738,
          0.011495399288833141
        ],
        "steady_command_mae": [
          0.037813372910022736,
          0.027337919920682907,
          0.12875469028949738,
          0.011495399288833141
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.11238191276788712,
        "min_box_clearance_m": 0.575922966003418,
        "pelvis_amplitude_m": 0.00811225175857544,
        "normal_forces_mean_n": [
          5.247701644897461,
          9.869989395141602
        ],
        "friction_weight_ratio_mean": 0.35709187388420105,
        "normal_vertical_fraction_max": 0.04616694152355194,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11995285749435425,
        "joint_speed_rms": 1.328381896018982,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.026307716965675354,
        "object_tracking_error_m": 0.03236387297511101,
        "object_tracking_error_rad_max": 0.10067116469144821,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03564820438623428,
          0.027532676234841347,
          0.13814690709114075,
          0.011505961418151855
        ],
        "steady_command_mae": [
          0.03564820438623428,
          0.027532676234841347,
          0.13814690709114075,
          0.011505961418151855
        ],
        "contact_continuity": 0.08000000566244125,
        "max_hand_slip_m": 0.1126246377825737,
        "min_box_clearance_m": 0.5769065618515015,
        "pelvis_amplitude_m": 0.008174777030944824,
        "normal_forces_mean_n": [
          5.4516425132751465,
          9.928540229797363
        ],
        "friction_weight_ratio_mean": 0.3823166489601135,
        "normal_vertical_fraction_max": 0.041567202657461166,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12070532143115997,
        "joint_speed_rms": 1.324749231338501,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02630535140633583,
        "object_tracking_error_m": 0.03242020681500435,
        "object_tracking_error_rad_max": 0.09481632709503174,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03544529154896736,
          0.02784709632396698,
          0.14360490441322327,
          0.011482691392302513
        ],
        "steady_command_mae": [
          0.03544529154896736,
          0.02784709632396698,
          0.14360490441322327,
          0.011482691392302513
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.11112853139638901,
        "min_box_clearance_m": 0.5759817361831665,
        "pelvis_amplitude_m": 0.007992148399353027,
        "normal_forces_mean_n": [
          5.573593616485596,
          10.079870223999023
        ],
        "friction_weight_ratio_mean": 0.3706720471382141,
        "normal_vertical_fraction_max": 0.041951730847358704,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11341716349124908,
        "joint_speed_rms": 1.3229701519012451,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.026311879977583885,
        "object_tracking_error_m": 0.032623060047626495,
        "object_tracking_error_rad_max": 0.09883560240268707,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03437133878469467,
          0.026928771287202835,
          0.13855309784412384,
          0.011713552288711071
        ],
        "steady_command_mae": [
          0.03437133878469467,
          0.026928771287202835,
          0.13855309784412384,
          0.011713552288711071
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.11486077308654785,
        "min_box_clearance_m": 0.5746883749961853,
        "pelvis_amplitude_m": 0.00849372148513794,
        "normal_forces_mean_n": [
          5.981595993041992,
          10.276886940002441
        ],
        "friction_weight_ratio_mean": 0.3911188244819641,
        "normal_vertical_fraction_max": 0.029218658804893494,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12039254605770111,
        "joint_speed_rms": 1.3364205360412598,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.026580017060041428,
        "object_tracking_error_m": 0.034631192684173584,
        "object_tracking_error_rad_max": 0.09367655962705612,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.038366347551345825,
          0.02641189657151699,
          0.1531665325164795,
          0.011623287573456764
        ],
        "steady_command_mae": [
          0.038366347551345825,
          0.02641189657151699,
          0.1531665325164795,
          0.011623287573456764
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.1135440468788147,
        "min_box_clearance_m": 0.5754235982894897,
        "pelvis_amplitude_m": 0.008382141590118408,
        "normal_forces_mean_n": [
          6.05118465423584,
          10.315295219421387
        ],
        "friction_weight_ratio_mean": 0.41032448410987854,
        "normal_vertical_fraction_max": 0.029538141563534737,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12649168074131012,
        "joint_speed_rms": 1.3342695236206055,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.026469672098755836,
        "object_tracking_error_m": 0.034443847835063934,
        "object_tracking_error_rad_max": 0.08978712558746338,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03849353641271591,
          0.027531031519174576,
          0.132342129945755,
          0.011459052562713623
        ],
        "steady_command_mae": [
          0.03849353641271591,
          0.027531031519174576,
          0.132342129945755,
          0.011459052562713623
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.11350692808628082,
        "min_box_clearance_m": 0.5758323669433594,
        "pelvis_amplitude_m": 0.008243441581726074,
        "normal_forces_mean_n": [
          5.967034339904785,
          10.341445922851562
        ],
        "friction_weight_ratio_mean": 0.4028488099575043,
        "normal_vertical_fraction_max": 0.032096751034259796,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12667378783226013,
        "joint_speed_rms": 1.3305038213729858,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.026360269635915756,
        "object_tracking_error_m": 0.03384847193956375,
        "object_tracking_error_rad_max": 0.0912022516131401,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03909342736005783,
          0.026767486706376076,
          0.14176133275032043,
          0.011566901579499245
        ],
        "steady_command_mae": [
          0.03909342736005783,
          0.026767486706376076,
          0.14176133275032043,
          0.011566901579499245
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.11358220875263214,
        "min_box_clearance_m": 0.5742572546005249,
        "pelvis_amplitude_m": 0.008667230606079102,
        "normal_forces_mean_n": [
          5.905638217926025,
          10.231844902038574
        ],
        "friction_weight_ratio_mean": 0.3874255120754242,
        "normal_vertical_fraction_max": 0.0295764971524477,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12635116279125214,
        "joint_speed_rms": 1.3347686529159546,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.026458963751792908,
        "object_tracking_error_m": 0.034816525876522064,
        "object_tracking_error_rad_max": 0.09392011165618896,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03539290279150009,
          0.026707112789154053,
          0.13173134624958038,
          0.011476528830826283
        ],
        "steady_command_mae": [
          0.03539290279150009,
          0.026707112789154053,
          0.13173134624958038,
          0.011476528830826283
        ],
        "contact_continuity": 0.08000000566244125,
        "max_hand_slip_m": 0.11293121427297592,
        "min_box_clearance_m": 0.5761533975601196,
        "pelvis_amplitude_m": 0.008061528205871582,
        "normal_forces_mean_n": [
          5.325331211090088,
          9.928726196289062
        ],
        "friction_weight_ratio_mean": 0.3671306073665619,
        "normal_vertical_fraction_max": 0.043993085622787476,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12057359516620636,
        "joint_speed_rms": 1.3263663053512573,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.026380550116300583,
        "object_tracking_error_m": 0.03242000937461853,
        "object_tracking_error_rad_max": 0.0983983650803566,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.036595456302165985,
          0.024491483345627785,
          0.12701338529586792,
          0.01180331688374281
        ],
        "steady_command_mae": [
          0.036595456302165985,
          0.024491483345627785,
          0.12701338529586792,
          0.01180331688374281
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.11479026079177856,
        "min_box_clearance_m": 0.575275719165802,
        "pelvis_amplitude_m": 0.00859689712524414,
        "normal_forces_mean_n": [
          5.909914016723633,
          10.337940216064453
        ],
        "friction_weight_ratio_mean": 0.40020686388015747,
        "normal_vertical_fraction_max": 0.031902335584163666,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1274586319923401,
        "joint_speed_rms": 1.3449617624282837,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.026770442724227905,
        "object_tracking_error_m": 0.03419782221317291,
        "object_tracking_error_rad_max": 0.092333123087883,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03762677684426308,
          0.027224784716963768,
          0.12806309759616852,
          0.01158373337239027
        ],
        "steady_command_mae": [
          0.03762677684426308,
          0.027224784716963768,
          0.12806309759616852,
          0.01158373337239027
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.1136903464794159,
        "min_box_clearance_m": 0.574735701084137,
        "pelvis_amplitude_m": 0.008420586585998535,
        "normal_forces_mean_n": [
          5.69835090637207,
          10.243013381958008
        ],
        "friction_weight_ratio_mean": 0.3762545883655548,
        "normal_vertical_fraction_max": 0.0337497815489769,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1211395263671875,
        "joint_speed_rms": 1.3365180492401123,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.0266621895134449,
        "object_tracking_error_m": 0.033998340368270874,
        "object_tracking_error_rad_max": 0.09678099304437637,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.037802018225193024,
          0.02727746032178402,
          0.12849360704421997,
          0.01150372065603733
        ],
        "steady_command_mae": [
          0.037802018225193024,
          0.02727746032178402,
          0.12849360704421997,
          0.01150372065603733
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.1124250665307045,
        "min_box_clearance_m": 0.5759141445159912,
        "pelvis_amplitude_m": 0.008137106895446777,
        "normal_forces_mean_n": [
          5.240050315856934,
          9.869535446166992
        ],
        "friction_weight_ratio_mean": 0.3577355146408081,
        "normal_vertical_fraction_max": 0.04608087241649628,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12023328244686127,
        "joint_speed_rms": 1.328776478767395,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02631393074989319,
        "object_tracking_error_m": 0.03236183524131775,
        "object_tracking_error_rad_max": 0.10082700848579407,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03580046817660332,
          0.027189826592803,
          0.144887775182724,
          0.011497879400849342
        ],
        "steady_command_mae": [
          0.03580046817660332,
          0.027189826592803,
          0.144887775182724,
          0.011497879400849342
        ],
        "contact_continuity": 0.08000000566244125,
        "max_hand_slip_m": 0.11266973614692688,
        "min_box_clearance_m": 0.5771109461784363,
        "pelvis_amplitude_m": 0.008148729801177979,
        "normal_forces_mean_n": [
          5.5098748207092285,
          9.956310272216797
        ],
        "friction_weight_ratio_mean": 0.3840680718421936,
        "normal_vertical_fraction_max": 0.04105556383728981,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12060166895389557,
        "joint_speed_rms": 1.3247957229614258,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.026302721351385117,
        "object_tracking_error_m": 0.03239356353878975,
        "object_tracking_error_rad_max": 0.09401144087314606,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03445949777960777,
          0.026801059022545815,
          0.13756075501441956,
          0.011575949378311634
        ],
        "steady_command_mae": [
          0.03445949777960777,
          0.026801059022545815,
          0.13756075501441956,
          0.011575949378311634
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.11318949609994888,
        "min_box_clearance_m": 0.576326310634613,
        "pelvis_amplitude_m": 0.008095502853393555,
        "normal_forces_mean_n": [
          5.557433128356934,
          10.068540573120117
        ],
        "friction_weight_ratio_mean": 0.3788228929042816,
        "normal_vertical_fraction_max": 0.04234177619218826,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11534446477890015,
        "joint_speed_rms": 1.3285162448883057,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.026528948917984962,
        "object_tracking_error_m": 0.03258660435676575,
        "object_tracking_error_rad_max": 0.0954061821103096,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.0338558666408062,
          0.026672953739762306,
          0.13713891804218292,
          0.011722469702363014
        ],
        "steady_command_mae": [
          0.0338558666408062,
          0.026672953739762306,
          0.13713891804218292,
          0.011722469702363014
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.11506041139364243,
        "min_box_clearance_m": 0.574689507484436,
        "pelvis_amplitude_m": 0.008502304553985596,
        "normal_forces_mean_n": [
          5.9274139404296875,
          10.238791465759277
        ],
        "friction_weight_ratio_mean": 0.3929607570171356,
        "normal_vertical_fraction_max": 0.029197607189416885,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12032343447208405,
        "joint_speed_rms": 1.3372031450271606,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02660997584462166,
        "object_tracking_error_m": 0.03462404012680054,
        "object_tracking_error_rad_max": 0.09377536922693253,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03791064769029617,
          0.026663338765501976,
          0.14523276686668396,
          0.011634385213255882
        ],
        "steady_command_mae": [
          0.03791064769029617,
          0.026663338765501976,
          0.14523276686668396,
          0.011634385213255882
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.11380767077207565,
        "min_box_clearance_m": 0.5754216909408569,
        "pelvis_amplitude_m": 0.008395850658416748,
        "normal_forces_mean_n": [
          6.0101165771484375,
          10.287748336791992
        ],
        "friction_weight_ratio_mean": 0.4120003581047058,
        "normal_vertical_fraction_max": 0.02955944649875164,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1258070319890976,
        "joint_speed_rms": 1.3353010416030884,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02650090493261814,
        "object_tracking_error_m": 0.03443795442581177,
        "object_tracking_error_rad_max": 0.09006600081920624,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.038180895149707794,
          0.02731858193874359,
          0.13144053518772125,
          0.011474072933197021
        ],
        "steady_command_mae": [
          0.038180895149707794,
          0.02731858193874359,
          0.13144053518772125,
          0.011474072933197021
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.11376425623893738,
        "min_box_clearance_m": 0.5757702589035034,
        "pelvis_amplitude_m": 0.008267343044281006,
        "normal_forces_mean_n": [
          5.934871673583984,
          10.344548225402832
        ],
        "friction_weight_ratio_mean": 0.39822813868522644,
        "normal_vertical_fraction_max": 0.032519225031137466,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12688329815864563,
        "joint_speed_rms": 1.3315271139144897,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.026385614648461342,
        "object_tracking_error_m": 0.033882737159729004,
        "object_tracking_error_rad_max": 0.09124615788459778,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03880694508552551,
          0.026663968339562416,
          0.14196085929870605,
          0.011591744609177113
        ],
        "steady_command_mae": [
          0.03880694508552551,
          0.026663968339562416,
          0.14196085929870605,
          0.011591744609177113
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.11373750865459442,
        "min_box_clearance_m": 0.574222981929779,
        "pelvis_amplitude_m": 0.008717834949493408,
        "normal_forces_mean_n": [
          5.897846221923828,
          10.223363876342773
        ],
        "friction_weight_ratio_mean": 0.3880467712879181,
        "normal_vertical_fraction_max": 0.02964465320110321,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1282736212015152,
        "joint_speed_rms": 1.3358463048934937,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.026494845747947693,
        "object_tracking_error_m": 0.034810472279787064,
        "object_tracking_error_rad_max": 0.09423333406448364,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03562464192509651,
          0.025933584198355675,
          0.1274261772632599,
          0.011493456549942493
        ],
        "steady_command_mae": [
          0.03562464192509651,
          0.025933584198355675,
          0.1274261772632599,
          0.011493456549942493
        ],
        "contact_continuity": 0.08000000566244125,
        "max_hand_slip_m": 0.1126885712146759,
        "min_box_clearance_m": 0.5761576890945435,
        "pelvis_amplitude_m": 0.008115708827972412,
        "normal_forces_mean_n": [
          5.357436180114746,
          9.920692443847656
        ],
        "friction_weight_ratio_mean": 0.3679004907608032,
        "normal_vertical_fraction_max": 0.044080786406993866,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12057379633188248,
        "joint_speed_rms": 1.3268330097198486,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02638862654566765,
        "object_tracking_error_m": 0.03240947052836418,
        "object_tracking_error_rad_max": 0.098884716629982,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03663123771548271,
          0.024412812665104866,
          0.12728795409202576,
          0.011804461479187012
        ],
        "steady_command_mae": [
          0.03663123771548271,
          0.024412812665104866,
          0.12728795409202576,
          0.011804461479187012
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.11481289565563202,
        "min_box_clearance_m": 0.5752530097961426,
        "pelvis_amplitude_m": 0.00859689712524414,
        "normal_forces_mean_n": [
          5.91610860824585,
          10.339401245117188
        ],
        "friction_weight_ratio_mean": 0.39900103211402893,
        "normal_vertical_fraction_max": 0.03194420039653778,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12744762003421783,
        "joint_speed_rms": 1.3447850942611694,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.026770558208227158,
        "object_tracking_error_m": 0.03420345112681389,
        "object_tracking_error_rad_max": 0.0923284962773323,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03773558884859085,
          0.02763577736914158,
          0.13492080569267273,
          0.01158076524734497
        ],
        "steady_command_mae": [
          0.03773558884859085,
          0.02763577736914158,
          0.13492080569267273,
          0.01158076524734497
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.1133442372083664,
        "min_box_clearance_m": 0.5747013688087463,
        "pelvis_amplitude_m": 0.008427917957305908,
        "normal_forces_mean_n": [
          5.738249778747559,
          10.270869255065918
        ],
        "friction_weight_ratio_mean": 0.3743477463722229,
        "normal_vertical_fraction_max": 0.03391740843653679,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12065805494785309,
        "joint_speed_rms": 1.3351726531982422,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02662649191915989,
        "object_tracking_error_m": 0.03400849178433418,
        "object_tracking_error_rad_max": 0.09662570059299469,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      }
    ],
    "goal_limits": {
      "height_low": 0.6068800687789917,
      "height_high": 0.7268800735473633,
      "height_rate": 0.11247000098228455,
      "vx_high": 0.0,
      "forward_admitted": false,
      "reference_fps": 50,
      "episode_seconds": 30.0
    },
    "reference_free": false,
    "terminal_state_before_reset": true,
    "physical_model": {
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
      "control": "PPO joint-position offsets with PD each physics substep; no P0 feedforward or WBC"
    },
    "accepted_policy": false,
    "motion_quality": {
      "clip_0_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.08981374651193619,
          "lower_body_style_rmse_rad": 0.07775221765041351,
          "reference_compatibility_mean": 0.751727549507645,
          "joint_acceleration_rms_rad_s2": 53.07354736328125,
          "box_relative_translation_drift_max_m": 0.047740986376051564,
          "box_relative_rotation_drift_max_rad": 0.10315049308946385
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.09000102430582047,
          "lower_body_style_rmse_rad": 0.07793334126472473,
          "reference_compatibility_mean": 0.7536819326457128,
          "joint_acceleration_rms_rad_s2": 52.71077346801758,
          "box_relative_translation_drift_max_m": 0.04762630723704309,
          "box_relative_rotation_drift_max_rad": 0.0965634271677724
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.08967989683151245,
          "lower_body_style_rmse_rad": 0.07737059891223907,
          "reference_compatibility_mean": 0.755692801065134,
          "joint_acceleration_rms_rad_s2": 52.77716827392578,
          "box_relative_translation_drift_max_m": 0.0477085211582501,
          "box_relative_rotation_drift_max_rad": 0.10242688705403276
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.09082470089197159,
          "lower_body_style_rmse_rad": 0.07907566428184509,
          "reference_compatibility_mean": 0.7517444584518421,
          "joint_acceleration_rms_rad_s2": 52.830509185791016,
          "box_relative_translation_drift_max_m": 0.04953766966155477,
          "box_relative_rotation_drift_max_rad": 0.10016437830316251
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.09098700433969498,
          "lower_body_style_rmse_rad": 0.07768414169549942,
          "reference_compatibility_mean": 0.7539482701078895,
          "joint_acceleration_rms_rad_s2": 52.457557678222656,
          "box_relative_translation_drift_max_m": 0.04872446672574097,
          "box_relative_rotation_drift_max_rad": 0.09559934410272972
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.09076085686683655,
          "lower_body_style_rmse_rad": 0.07742659747600555,
          "reference_compatibility_mean": 0.7573693006814535,
          "joint_acceleration_rms_rad_s2": 52.48493194580078,
          "box_relative_translation_drift_max_m": 0.04828843079675397,
          "box_relative_rotation_drift_max_rad": 0.09670115261271733
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.09103047102689743,
          "lower_body_style_rmse_rad": 0.07732689380645752,
          "reference_compatibility_mean": 0.7532971104879927,
          "joint_acceleration_rms_rad_s2": 52.723915100097656,
          "box_relative_translation_drift_max_m": 0.04922970460542268,
          "box_relative_rotation_drift_max_rad": 0.09943361525589
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.08990126103162766,
          "lower_body_style_rmse_rad": 0.07770375907421112,
          "reference_compatibility_mean": 0.7521300405953052,
          "joint_acceleration_rms_rad_s2": 53.01988220214844,
          "box_relative_translation_drift_max_m": 0.04801954702484443,
          "box_relative_rotation_drift_max_rad": 0.10083576070144315
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.09117966145277023,
          "lower_body_style_rmse_rad": 0.08164554089307785,
          "reference_compatibility_mean": 0.7397318944995254,
          "joint_acceleration_rms_rad_s2": 52.933807373046875,
          "box_relative_translation_drift_max_m": 0.048916688574510835,
          "box_relative_rotation_drift_max_rad": 0.09729447717774263
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.09083215147256851,
          "lower_body_style_rmse_rad": 0.07905671000480652,
          "reference_compatibility_mean": 0.7503183942743546,
          "joint_acceleration_rms_rad_s2": 53.09334945678711,
          "box_relative_translation_drift_max_m": 0.048926848434299335,
          "box_relative_rotation_drift_max_rad": 0.10195014023010086
        }
      ],
      "clip_1_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.08980999886989594,
          "lower_body_style_rmse_rad": 0.07775578647851944,
          "reference_compatibility_mean": 0.7517244981716197,
          "joint_acceleration_rms_rad_s2": 53.13825988769531,
          "box_relative_translation_drift_max_m": 0.04773262197916496,
          "box_relative_rotation_drift_max_rad": 0.1031792345517937
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.09002454578876495,
          "lower_body_style_rmse_rad": 0.07792249321937561,
          "reference_compatibility_mean": 0.7536836846543296,
          "joint_acceleration_rms_rad_s2": 52.6555061340332,
          "box_relative_translation_drift_max_m": 0.04754844556389285,
          "box_relative_rotation_drift_max_rad": 0.09555931999845678
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.09005653113126755,
          "lower_body_style_rmse_rad": 0.07979672402143478,
          "reference_compatibility_mean": 0.7489986190400841,
          "joint_acceleration_rms_rad_s2": 52.73999786376953,
          "box_relative_translation_drift_max_m": 0.0480435819692851,
          "box_relative_rotation_drift_max_rad": 0.09851811381690646
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.09085305780172348,
          "lower_body_style_rmse_rad": 0.07908184826374054,
          "reference_compatibility_mean": 0.750898958414521,
          "joint_acceleration_rms_rad_s2": 52.850563049316406,
          "box_relative_translation_drift_max_m": 0.04959803004060492,
          "box_relative_rotation_drift_max_rad": 0.10010479480262205
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.09102770686149597,
          "lower_body_style_rmse_rad": 0.07770824432373047,
          "reference_compatibility_mean": 0.7530743339445388,
          "joint_acceleration_rms_rad_s2": 52.48530578613281,
          "box_relative_translation_drift_max_m": 0.04879290702062866,
          "box_relative_rotation_drift_max_rad": 0.09577202018209406
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.09074588119983673,
          "lower_body_style_rmse_rad": 0.07743914425373077,
          "reference_compatibility_mean": 0.7563792395733373,
          "joint_acceleration_rms_rad_s2": 52.5360221862793,
          "box_relative_translation_drift_max_m": 0.04851811320764955,
          "box_relative_rotation_drift_max_rad": 0.09667614674729803
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.09107823669910431,
          "lower_body_style_rmse_rad": 0.0773630365729332,
          "reference_compatibility_mean": 0.7522366194557127,
          "joint_acceleration_rms_rad_s2": 52.76997375488281,
          "box_relative_translation_drift_max_m": 0.04924673580119412,
          "box_relative_rotation_drift_max_rad": 0.09965112533844324
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.08988044410943985,
          "lower_body_style_rmse_rad": 0.077713742852211,
          "reference_compatibility_mean": 0.7522115922391304,
          "joint_acceleration_rms_rad_s2": 52.97256851196289,
          "box_relative_translation_drift_max_m": 0.0478693779429057,
          "box_relative_rotation_drift_max_rad": 0.10130898716027649
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.09118667989969254,
          "lower_body_style_rmse_rad": 0.08164048939943314,
          "reference_compatibility_mean": 0.7396381437717154,
          "joint_acceleration_rms_rad_s2": 52.90324401855469,
          "box_relative_translation_drift_max_m": 0.048932769999856206,
          "box_relative_rotation_drift_max_rad": 0.09724562889278758
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.09078831970691681,
          "lower_body_style_rmse_rad": 0.07903413474559784,
          "reference_compatibility_mean": 0.7512475718405083,
          "joint_acceleration_rms_rad_s2": 53.0134391784668,
          "box_relative_translation_drift_max_m": 0.04887339265067755,
          "box_relative_rotation_drift_max_rad": 0.10205405193197928
        }
      ]
    },
    "directory": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795192603809404020",
    "checkpoint": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/dashboard/stage1/WholeBodyTracking/20261120_142731-stage1-locomotion/model_02499.pt",
    "final": false,
    "selection_score": 0.012138463126925323,
    "failure_counts": {
      "physical_failure/loss_of_grasp": 20,
      "incomplete_episode": 20,
      "contact_interruption": 20,
      "hand_slip": 20,
      "insufficient_friction_support": 20,
      "contact_near_box_bottom": 20
    },
    "scenarios": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "completed_updates": 2500
  },
  {
    "passed": false,
    "score": 0.0,
    "suite": "stage1",
    "groups": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "trials": [
      {
        "scenario": "clip_0",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02535833790898323,
          0.028148194774985313,
          0.11537271738052368,
          0.011606335639953613
        ],
        "steady_command_mae": [
          0.02535833790898323,
          0.028148194774985313,
          0.11537271738052368,
          0.011606335639953613
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.1155703216791153,
        "min_box_clearance_m": 0.5783482789993286,
        "pelvis_amplitude_m": 0.008714377880096436,
        "normal_forces_mean_n": [
          5.424756050109863,
          10.956327438354492
        ],
        "friction_weight_ratio_mean": 0.4572235643863678,
        "normal_vertical_fraction_max": 0.045754656195640564,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11063021421432495,
        "joint_speed_rms": 1.36384916305542,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.025402909144759178,
        "object_tracking_error_m": 0.03206696733832359,
        "object_tracking_error_rad_max": 0.09818773716688156,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.022958844900131226,
          0.02944537065923214,
          0.11129889637231827,
          0.011590123176574707
        ],
        "steady_command_mae": [
          0.022958844900131226,
          0.02944537065923214,
          0.11129889637231827,
          0.011590123176574707
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.11570630222558975,
        "min_box_clearance_m": 0.5784643292427063,
        "pelvis_amplitude_m": 0.008624613285064697,
        "normal_forces_mean_n": [
          5.492924213409424,
          10.923669815063477
        ],
        "friction_weight_ratio_mean": 0.46375665068626404,
        "normal_vertical_fraction_max": 0.04419485852122307,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11330682039260864,
        "joint_speed_rms": 1.3611563444137573,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.025416165590286255,
        "object_tracking_error_m": 0.032229743897914886,
        "object_tracking_error_rad_max": 0.09671599417924881,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.022509893402457237,
          0.02783045545220375,
          0.13099607825279236,
          0.011638033203780651
        ],
        "steady_command_mae": [
          0.022509893402457237,
          0.02783045545220375,
          0.13099607825279236,
          0.011638033203780651
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.11539675295352936,
        "min_box_clearance_m": 0.5784702897071838,
        "pelvis_amplitude_m": 0.008613526821136475,
        "normal_forces_mean_n": [
          5.655178546905518,
          11.118257522583008
        ],
        "friction_weight_ratio_mean": 0.4666195809841156,
        "normal_vertical_fraction_max": 0.04351862147450447,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1088973879814148,
        "joint_speed_rms": 1.363377571105957,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02556118369102478,
        "object_tracking_error_m": 0.03230399638414383,
        "object_tracking_error_rad_max": 0.09648285061120987,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.022507689893245697,
          0.027592280879616737,
          0.1225467100739479,
          0.01179358921945095
        ],
        "steady_command_mae": [
          0.022507689893245697,
          0.027592280879616737,
          0.1225467100739479,
          0.01179358921945095
        ],
        "contact_continuity": 0.1600000262260437,
        "max_hand_slip_m": 0.11704924702644348,
        "min_box_clearance_m": 0.578643798828125,
        "pelvis_amplitude_m": 0.008873999118804932,
        "normal_forces_mean_n": [
          6.032858371734619,
          11.023580551147461
        ],
        "friction_weight_ratio_mean": 0.5102378726005554,
        "normal_vertical_fraction_max": 0.02979753166437149,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11320425570011139,
        "joint_speed_rms": 1.3703060150146484,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.025726500898599625,
        "object_tracking_error_m": 0.03402652591466904,
        "object_tracking_error_rad_max": 0.08549907058477402,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.023897213861346245,
          0.027657732367515564,
          0.10676419734954834,
          0.011674046516418457
        ],
        "steady_command_mae": [
          0.023897213861346245,
          0.027657732367515564,
          0.10676419734954834,
          0.011674046516418457
        ],
        "contact_continuity": 0.14000001549720764,
        "max_hand_slip_m": 0.11772012710571289,
        "min_box_clearance_m": 0.576200544834137,
        "pelvis_amplitude_m": 0.008867442607879639,
        "normal_forces_mean_n": [
          5.690281391143799,
          10.983579635620117
        ],
        "friction_weight_ratio_mean": 0.4715335965156555,
        "normal_vertical_fraction_max": 0.03453893959522247,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11510972678661346,
        "joint_speed_rms": 1.3711450099945068,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.025571811944246292,
        "object_tracking_error_m": 0.034442417323589325,
        "object_tracking_error_rad_max": 0.09395316988229752,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.025591125711798668,
          0.029414096847176552,
          0.09597419947385788,
          0.011671137996017933
        ],
        "steady_command_mae": [
          0.025591125711798668,
          0.029414096847176552,
          0.09597419947385788,
          0.011671137996017933
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.1169295534491539,
        "min_box_clearance_m": 0.5763922929763794,
        "pelvis_amplitude_m": 0.008897125720977783,
        "normal_forces_mean_n": [
          5.697991371154785,
          11.10910415649414
        ],
        "friction_weight_ratio_mean": 0.46079081296920776,
        "normal_vertical_fraction_max": 0.03758791461586952,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11510022729635239,
        "joint_speed_rms": 1.3700566291809082,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.025526713579893112,
        "object_tracking_error_m": 0.03386470675468445,
        "object_tracking_error_rad_max": 0.0958162397146225,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02507190778851509,
          0.028538282960653305,
          0.09277412295341492,
          0.011700129136443138
        ],
        "steady_command_mae": [
          0.02507190778851509,
          0.028538282960653305,
          0.09277412295341492,
          0.011700129136443138
        ],
        "contact_continuity": 0.15000002086162567,
        "max_hand_slip_m": 0.11815851926803589,
        "min_box_clearance_m": 0.5783015489578247,
        "pelvis_amplitude_m": 0.008985042572021484,
        "normal_forces_mean_n": [
          5.837432384490967,
          10.8907470703125
        ],
        "friction_weight_ratio_mean": 0.5051184892654419,
        "normal_vertical_fraction_max": 0.02880893461406231,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11599956452846527,
        "joint_speed_rms": 1.3723567724227905,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.025719929486513138,
        "object_tracking_error_m": 0.0342455618083477,
        "object_tracking_error_rad_max": 0.08488137274980545,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.022550499066710472,
          0.027573153376579285,
          0.11243827641010284,
          0.011541604995727539
        ],
        "steady_command_mae": [
          0.022550499066710472,
          0.027573153376579285,
          0.11243827641010284,
          0.011541604995727539
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.11616398394107819,
        "min_box_clearance_m": 0.5783538222312927,
        "pelvis_amplitude_m": 0.008597970008850098,
        "normal_forces_mean_n": [
          5.465389728546143,
          11.017319679260254
        ],
        "friction_weight_ratio_mean": 0.45845770835876465,
        "normal_vertical_fraction_max": 0.04457952082157135,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1115289181470871,
        "joint_speed_rms": 1.3625849485397339,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.025444526225328445,
        "object_tracking_error_m": 0.03215739130973816,
        "object_tracking_error_rad_max": 0.09675805270671844,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.025598999112844467,
          0.02701791562139988,
          0.10539493709802628,
          0.011715603061020374
        ],
        "steady_command_mae": [
          0.025598999112844467,
          0.02701791562139988,
          0.10539493709802628,
          0.011715603061020374
        ],
        "contact_continuity": 0.14000001549720764,
        "max_hand_slip_m": 0.11727218329906464,
        "min_box_clearance_m": 0.5788836479187012,
        "pelvis_amplitude_m": 0.008958816528320312,
        "normal_forces_mean_n": [
          5.927403450012207,
          11.102300643920898
        ],
        "friction_weight_ratio_mean": 0.5007616281509399,
        "normal_vertical_fraction_max": 0.030737513676285744,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11582466214895248,
        "joint_speed_rms": 1.3717780113220215,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.025654559955000877,
        "object_tracking_error_m": 0.03373626619577408,
        "object_tracking_error_rad_max": 0.08571617305278778,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02396334707736969,
          0.027943486347794533,
          0.10817277431488037,
          0.011716032400727272
        ],
        "steady_command_mae": [
          0.02396334707736969,
          0.027943486347794533,
          0.10817277431488037,
          0.011716032400727272
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.11797969043254852,
        "min_box_clearance_m": 0.576046884059906,
        "pelvis_amplitude_m": 0.008863389492034912,
        "normal_forces_mean_n": [
          5.520336627960205,
          11.037104606628418
        ],
        "friction_weight_ratio_mean": 0.4512748718261719,
        "normal_vertical_fraction_max": 0.03834383934736252,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11227546632289886,
        "joint_speed_rms": 1.3754574060440063,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02582070790231228,
        "object_tracking_error_m": 0.03391169384121895,
        "object_tracking_error_rad_max": 0.09684620052576065,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.025263672694563866,
          0.027145657688379288,
          0.11152596771717072,
          0.01172950305044651
        ],
        "steady_command_mae": [
          0.025263672694563866,
          0.027145657688379288,
          0.11152596771717072,
          0.01172950305044651
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.116548553109169,
        "min_box_clearance_m": 0.5783050060272217,
        "pelvis_amplitude_m": 0.008922457695007324,
        "normal_forces_mean_n": [
          5.377100944519043,
          10.943853378295898
        ],
        "friction_weight_ratio_mean": 0.4570644497871399,
        "normal_vertical_fraction_max": 0.04573050141334534,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11137952655553818,
        "joint_speed_rms": 1.3704965114593506,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02554684318602085,
        "object_tracking_error_m": 0.03207008168101311,
        "object_tracking_error_rad_max": 0.09871000051498413,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02318984642624855,
          0.028500352054834366,
          0.1045965775847435,
          0.011749625205993652
        ],
        "steady_command_mae": [
          0.02318984642624855,
          0.028500352054834366,
          0.1045965775847435,
          0.011749625205993652
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.11661820858716965,
        "min_box_clearance_m": 0.5781192779541016,
        "pelvis_amplitude_m": 0.008913278579711914,
        "normal_forces_mean_n": [
          5.413454055786133,
          10.917306900024414
        ],
        "friction_weight_ratio_mean": 0.4539486765861511,
        "normal_vertical_fraction_max": 0.044727180153131485,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11105193942785263,
        "joint_speed_rms": 1.367651104927063,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02557435631752014,
        "object_tracking_error_m": 0.03229454159736633,
        "object_tracking_error_rad_max": 0.09735545516014099,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.022761721163988113,
          0.027038339525461197,
          0.13037171959877014,
          0.01168357115238905
        ],
        "steady_command_mae": [
          0.022761721163988113,
          0.027038339525461197,
          0.13037171959877014,
          0.01168357115238905
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.11577305197715759,
        "min_box_clearance_m": 0.5784401893615723,
        "pelvis_amplitude_m": 0.008692324161529541,
        "normal_forces_mean_n": [
          5.609014511108398,
          11.126848220825195
        ],
        "friction_weight_ratio_mean": 0.4670425355434418,
        "normal_vertical_fraction_max": 0.043516021221876144,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10902415215969086,
        "joint_speed_rms": 1.3650572299957275,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02560514770448208,
        "object_tracking_error_m": 0.03231228515505791,
        "object_tracking_error_rad_max": 0.09648928791284561,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02257605269551277,
          0.027651432901620865,
          0.12417372316122055,
          0.01179429329931736
        ],
        "steady_command_mae": [
          0.02257605269551277,
          0.027651432901620865,
          0.12417372316122055,
          0.01179429329931736
        ],
        "contact_continuity": 0.1600000262260437,
        "max_hand_slip_m": 0.11705586314201355,
        "min_box_clearance_m": 0.5786455869674683,
        "pelvis_amplitude_m": 0.008874177932739258,
        "normal_forces_mean_n": [
          6.046394348144531,
          11.044476509094238
        ],
        "friction_weight_ratio_mean": 0.5113322138786316,
        "normal_vertical_fraction_max": 0.029866520315408707,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11247523128986359,
        "joint_speed_rms": 1.3701683282852173,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.025728454813361168,
        "object_tracking_error_m": 0.03402598574757576,
        "object_tracking_error_rad_max": 0.08554531633853912,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.023771340027451515,
          0.027971262112259865,
          0.10700346529483795,
          0.011662280187010765
        ],
        "steady_command_mae": [
          0.023771340027451515,
          0.027971262112259865,
          0.10700346529483795,
          0.011662280187010765
        ],
        "contact_continuity": 0.14000001549720764,
        "max_hand_slip_m": 0.11763056367635727,
        "min_box_clearance_m": 0.576252281665802,
        "pelvis_amplitude_m": 0.008845925331115723,
        "normal_forces_mean_n": [
          5.696484088897705,
          10.98478889465332
        ],
        "friction_weight_ratio_mean": 0.4728116989135742,
        "normal_vertical_fraction_max": 0.03450187295675278,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11511632055044174,
        "joint_speed_rms": 1.3708510398864746,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.025563757866621017,
        "object_tracking_error_m": 0.034430574625730515,
        "object_tracking_error_rad_max": 0.09392396360635757,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02563660964369774,
          0.028916966170072556,
          0.0943591296672821,
          0.011707484722137451
        ],
        "steady_command_mae": [
          0.02563660964369774,
          0.028916966170072556,
          0.0943591296672821,
          0.011707484722137451
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.11735204607248306,
        "min_box_clearance_m": 0.5764264464378357,
        "pelvis_amplitude_m": 0.008959591388702393,
        "normal_forces_mean_n": [
          5.662898063659668,
          11.10193920135498
        ],
        "friction_weight_ratio_mean": 0.4588826596736908,
        "normal_vertical_fraction_max": 0.03741518035531044,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11520946025848389,
        "joint_speed_rms": 1.371650218963623,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.025564447045326233,
        "object_tracking_error_m": 0.03387957811355591,
        "object_tracking_error_rad_max": 0.09535781294107437,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.025158727541565895,
          0.028552547097206116,
          0.092105433344841,
          0.011705255135893822
        ],
        "steady_command_mae": [
          0.025158727541565895,
          0.028552547097206116,
          0.092105433344841,
          0.011705255135893822
        ],
        "contact_continuity": 0.15000002086162567,
        "max_hand_slip_m": 0.11816637963056564,
        "min_box_clearance_m": 0.5781559348106384,
        "pelvis_amplitude_m": 0.008995890617370605,
        "normal_forces_mean_n": [
          5.8300065994262695,
          10.888644218444824
        ],
        "friction_weight_ratio_mean": 0.5023790597915649,
        "normal_vertical_fraction_max": 0.029133927077054977,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11600282043218613,
        "joint_speed_rms": 1.3723057508468628,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.025719676166772842,
        "object_tracking_error_m": 0.034270741045475006,
        "object_tracking_error_rad_max": 0.08519317954778671,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.022454913705587387,
          0.026965398341417313,
          0.10979006439447403,
          0.011686325073242188
        ],
        "steady_command_mae": [
          0.022454913705587387,
          0.026965398341417313,
          0.10979006439447403,
          0.011686325073242188
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.11686903238296509,
        "min_box_clearance_m": 0.578332245349884,
        "pelvis_amplitude_m": 0.008853614330291748,
        "normal_forces_mean_n": [
          5.417611122131348,
          10.994863510131836
        ],
        "friction_weight_ratio_mean": 0.45728135108947754,
        "normal_vertical_fraction_max": 0.04512494057416916,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11368819326162338,
        "joint_speed_rms": 1.3698137998580933,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.0256083644926548,
        "object_tracking_error_m": 0.032165758311748505,
        "object_tracking_error_rad_max": 0.09726512432098389,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.025541791692376137,
          0.027314934879541397,
          0.10450625419616699,
          0.01171255111694336
        ],
        "steady_command_mae": [
          0.025541791692376137,
          0.027314934879541397,
          0.10450625419616699,
          0.01171255111694336
        ],
        "contact_continuity": 0.14000001549720764,
        "max_hand_slip_m": 0.11719325929880142,
        "min_box_clearance_m": 0.5788166522979736,
        "pelvis_amplitude_m": 0.008951246738433838,
        "normal_forces_mean_n": [
          5.9380903244018555,
          11.130902290344238
        ],
        "friction_weight_ratio_mean": 0.5010620355606079,
        "normal_vertical_fraction_max": 0.031113067641854286,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11570398509502411,
        "joint_speed_rms": 1.3714394569396973,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02564857341349125,
        "object_tracking_error_m": 0.033753350377082825,
        "object_tracking_error_rad_max": 0.08623330295085907,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.023983953520655632,
          0.028205540031194687,
          0.10666163265705109,
          0.011708986945450306
        ],
        "steady_command_mae": [
          0.023983953520655632,
          0.028205540031194687,
          0.10666163265705109,
          0.011708986945450306
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.11788244545459747,
        "min_box_clearance_m": 0.5760833024978638,
        "pelvis_amplitude_m": 0.00885075330734253,
        "normal_forces_mean_n": [
          5.548129081726074,
          11.058375358581543
        ],
        "friction_weight_ratio_mean": 0.45288124680519104,
        "normal_vertical_fraction_max": 0.03836618363857269,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11243017762899399,
        "joint_speed_rms": 1.3756165504455566,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.025814220309257507,
        "object_tracking_error_m": 0.033902913331985474,
        "object_tracking_error_rad_max": 0.09684846550226212,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      }
    ],
    "goal_limits": {
      "height_low": 0.6068800687789917,
      "height_high": 0.7268800735473633,
      "height_rate": 0.11247000098228455,
      "vx_high": 0.0,
      "forward_admitted": false,
      "reference_fps": 50,
      "episode_seconds": 30.0
    },
    "reference_free": false,
    "terminal_state_before_reset": true,
    "physical_model": {
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
      "control": "PPO joint-position offsets with PD each physics substep; no P0 feedforward or WBC"
    },
    "accepted_policy": false,
    "motion_quality": {
      "clip_0_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.08868023008108139,
          "lower_body_style_rmse_rad": 0.08578519523143768,
          "reference_compatibility_mean": 0.707190547766231,
          "joint_acceleration_rms_rad_s2": 53.292877197265625,
          "box_relative_translation_drift_max_m": 0.04719240196345932,
          "box_relative_rotation_drift_max_rad": 0.12192208531436034
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.08881564438343048,
          "lower_body_style_rmse_rad": 0.08443198353052139,
          "reference_compatibility_mean": 0.7110682912677379,
          "joint_acceleration_rms_rad_s2": 53.34371566772461,
          "box_relative_translation_drift_max_m": 0.04763401387361537,
          "box_relative_rotation_drift_max_rad": 0.1194144762653361
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.08877366036176682,
          "lower_body_style_rmse_rad": 0.08524370938539505,
          "reference_compatibility_mean": 0.7098269201861356,
          "joint_acceleration_rms_rad_s2": 53.3280143737793,
          "box_relative_translation_drift_max_m": 0.04736654427699675,
          "box_relative_rotation_drift_max_rad": 0.12057133937020971
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.0896906927227974,
          "lower_body_style_rmse_rad": 0.08655048906803131,
          "reference_compatibility_mean": 0.7038009925235723,
          "joint_acceleration_rms_rad_s2": 53.04280471801758,
          "box_relative_translation_drift_max_m": 0.04773222937378638,
          "box_relative_rotation_drift_max_rad": 0.11334325095182454
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.08964751660823822,
          "lower_body_style_rmse_rad": 0.08679009228944778,
          "reference_compatibility_mean": 0.7076752655067544,
          "joint_acceleration_rms_rad_s2": 53.07553482055664,
          "box_relative_translation_drift_max_m": 0.04956992921021999,
          "box_relative_rotation_drift_max_rad": 0.12080759959196086
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.08932546526193619,
          "lower_body_style_rmse_rad": 0.08663929998874664,
          "reference_compatibility_mean": 0.7038151590741774,
          "joint_acceleration_rms_rad_s2": 53.265872955322266,
          "box_relative_translation_drift_max_m": 0.049016569302059276,
          "box_relative_rotation_drift_max_rad": 0.12223111808615171
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.09012428671121597,
          "lower_body_style_rmse_rad": 0.08734742552042007,
          "reference_compatibility_mean": 0.7015813951893396,
          "joint_acceleration_rms_rad_s2": 52.91976547241211,
          "box_relative_translation_drift_max_m": 0.048051073130155886,
          "box_relative_rotation_drift_max_rad": 0.11179220320949496
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.08869985491037369,
          "lower_body_style_rmse_rad": 0.0855841338634491,
          "reference_compatibility_mean": 0.7106338484671352,
          "joint_acceleration_rms_rad_s2": 53.466678619384766,
          "box_relative_translation_drift_max_m": 0.04764114401609405,
          "box_relative_rotation_drift_max_rad": 0.12054274223155503
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.08969666808843613,
          "lower_body_style_rmse_rad": 0.08716163039207458,
          "reference_compatibility_mean": 0.7024943051158935,
          "joint_acceleration_rms_rad_s2": 53.07026672363281,
          "box_relative_translation_drift_max_m": 0.047511097454284376,
          "box_relative_rotation_drift_max_rad": 0.11210043595928824
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.08970881998538971,
          "lower_body_style_rmse_rad": 0.08662012964487076,
          "reference_compatibility_mean": 0.7015474417575216,
          "joint_acceleration_rms_rad_s2": 53.4918212890625,
          "box_relative_translation_drift_max_m": 0.049336734325107226,
          "box_relative_rotation_drift_max_rad": 0.12347894581444475
        }
      ],
      "clip_1_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.08893068879842758,
          "lower_body_style_rmse_rad": 0.08591820299625397,
          "reference_compatibility_mean": 0.6996842733842945,
          "joint_acceleration_rms_rad_s2": 53.6325798034668,
          "box_relative_translation_drift_max_m": 0.04718278830690006,
          "box_relative_rotation_drift_max_rad": 0.12217470152372686
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.08895882219076157,
          "lower_body_style_rmse_rad": 0.08612097799777985,
          "reference_compatibility_mean": 0.7016771807926961,
          "joint_acceleration_rms_rad_s2": 53.62617111206055,
          "box_relative_translation_drift_max_m": 0.04776777323376641,
          "box_relative_rotation_drift_max_rad": 0.11984269730807501
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.08878573030233383,
          "lower_body_style_rmse_rad": 0.08550482988357544,
          "reference_compatibility_mean": 0.7074520148048389,
          "joint_acceleration_rms_rad_s2": 53.414329528808594,
          "box_relative_translation_drift_max_m": 0.04733925945752948,
          "box_relative_rotation_drift_max_rad": 0.12057019874939125
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.08969566226005554,
          "lower_body_style_rmse_rad": 0.0865759402513504,
          "reference_compatibility_mean": 0.7036893168278685,
          "joint_acceleration_rms_rad_s2": 53.01761245727539,
          "box_relative_translation_drift_max_m": 0.04770580482832963,
          "box_relative_rotation_drift_max_rad": 0.1133967664395519
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.0896417498588562,
          "lower_body_style_rmse_rad": 0.08677610754966736,
          "reference_compatibility_mean": 0.7082099196191232,
          "joint_acceleration_rms_rad_s2": 53.063255310058594,
          "box_relative_translation_drift_max_m": 0.049562755528770805,
          "box_relative_rotation_drift_max_rad": 0.12070671141402774
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.08934605866670609,
          "lower_body_style_rmse_rad": 0.08695323020219803,
          "reference_compatibility_mean": 0.7019031535208009,
          "joint_acceleration_rms_rad_s2": 53.31474304199219,
          "box_relative_translation_drift_max_m": 0.049086839885037675,
          "box_relative_rotation_drift_max_rad": 0.12160644394452555
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.09012234210968018,
          "lower_body_style_rmse_rad": 0.08728422969579697,
          "reference_compatibility_mean": 0.7014298330888552,
          "joint_acceleration_rms_rad_s2": 52.91096878051758,
          "box_relative_translation_drift_max_m": 0.048136886004653594,
          "box_relative_rotation_drift_max_rad": 0.11209271244286001
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.08894552290439606,
          "lower_body_style_rmse_rad": 0.08575496077537537,
          "reference_compatibility_mean": 0.7019415625299175,
          "joint_acceleration_rms_rad_s2": 53.66243362426758,
          "box_relative_translation_drift_max_m": 0.047642774783090855,
          "box_relative_rotation_drift_max_rad": 0.12075726317353398
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.08967667818069458,
          "lower_body_style_rmse_rad": 0.0871628075838089,
          "reference_compatibility_mean": 0.7027199531498246,
          "joint_acceleration_rms_rad_s2": 53.08304977416992,
          "box_relative_translation_drift_max_m": 0.047569878211320166,
          "box_relative_rotation_drift_max_rad": 0.11262292851028055
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.0897032618522644,
          "lower_body_style_rmse_rad": 0.08661308139562607,
          "reference_compatibility_mean": 0.7018538588850973,
          "joint_acceleration_rms_rad_s2": 53.50558853149414,
          "box_relative_translation_drift_max_m": 0.049307675638120614,
          "box_relative_rotation_drift_max_rad": 0.12349899300075493
        }
      ]
    },
    "directory": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795200095046815929",
    "checkpoint": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/dashboard/stage1/WholeBodyTracking/20261120_163703-stage1-locomotion/model_02999.pt",
    "final": false,
    "selection_score": 0.013838463219312524,
    "failure_counts": {
      "physical_failure/loss_of_grasp": 20,
      "incomplete_episode": 20,
      "contact_interruption": 20,
      "hand_slip": 20,
      "insufficient_friction_support": 20,
      "contact_near_box_bottom": 20
    },
    "scenarios": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "completed_updates": 3000
  },
  {
    "passed": false,
    "score": 0.0,
    "suite": "stage1",
    "groups": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "trials": [
      {
        "scenario": "clip_0",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.028617549687623978,
          0.02598061040043831,
          0.31371158361434937,
          0.010370910167694092
        ],
        "steady_command_mae": [
          0.028617549687623978,
          0.02598061040043831,
          0.31371158361434937,
          0.010370910167694092
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.1151769757270813,
        "min_box_clearance_m": 0.5856822729110718,
        "pelvis_amplitude_m": 0.007690310478210449,
        "normal_forces_mean_n": [
          5.862799167633057,
          10.84326171875
        ],
        "friction_weight_ratio_mean": 0.5137620568275452,
        "normal_vertical_fraction_max": 0.023355167359113693,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09527641534805298,
        "joint_speed_rms": 1.3236247301101685,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02339683286845684,
        "object_tracking_error_m": 0.03157934173941612,
        "object_tracking_error_rad_max": 0.059394847601652145,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02681157924234867,
          0.027978086844086647,
          0.29626160860061646,
          0.010432923212647438
        ],
        "steady_command_mae": [
          0.02681157924234867,
          0.027978086844086647,
          0.29626160860061646,
          0.010432923212647438
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.11601945757865906,
        "min_box_clearance_m": 0.5846400260925293,
        "pelvis_amplitude_m": 0.007732868194580078,
        "normal_forces_mean_n": [
          5.960062026977539,
          10.920700073242188
        ],
        "friction_weight_ratio_mean": 0.47270146012306213,
        "normal_vertical_fraction_max": 0.02371225878596306,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09697575867176056,
        "joint_speed_rms": 1.3198567628860474,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02343437634408474,
        "object_tracking_error_m": 0.031938910484313965,
        "object_tracking_error_rad_max": 0.059719882905483246,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.026029696688055992,
          0.02572053112089634,
          0.3360268771648407,
          0.01048277597874403
        ],
        "steady_command_mae": [
          0.026029696688055992,
          0.02572053112089634,
          0.3360268771648407,
          0.01048277597874403
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.11638238281011581,
        "min_box_clearance_m": 0.5860453844070435,
        "pelvis_amplitude_m": 0.007748425006866455,
        "normal_forces_mean_n": [
          6.195725440979004,
          11.222848892211914
        ],
        "friction_weight_ratio_mean": 0.5096220970153809,
        "normal_vertical_fraction_max": 0.01912085711956024,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09246475249528885,
        "joint_speed_rms": 1.3255869150161743,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.023646336048841476,
        "object_tracking_error_m": 0.03173418715596199,
        "object_tracking_error_rad_max": 0.05770879611372948,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02519158646464348,
          0.02612624689936638,
          0.32160359621047974,
          0.010649526491761208
        ],
        "steady_command_mae": [
          0.02519158646464348,
          0.02612624689936638,
          0.32160359621047974,
          0.010649526491761208
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.11968313157558441,
        "min_box_clearance_m": 0.5855399370193481,
        "pelvis_amplitude_m": 0.008011698722839355,
        "normal_forces_mean_n": [
          6.6593475341796875,
          11.213911056518555
        ],
        "friction_weight_ratio_mean": 0.5290883779525757,
        "normal_vertical_fraction_max": 0.012733724899590015,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09724035114049911,
        "joint_speed_rms": 1.3312468528747559,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02378058061003685,
        "object_tracking_error_m": 0.03365715965628624,
        "object_tracking_error_rad_max": 0.049580954015254974,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.028014302253723145,
          0.027833838015794754,
          0.3061104714870453,
          0.010581588372588158
        ],
        "steady_command_mae": [
          0.028014302253723145,
          0.027833838015794754,
          0.3061104714870453,
          0.010581588372588158
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.11941760778427124,
        "min_box_clearance_m": 0.5844805240631104,
        "pelvis_amplitude_m": 0.008052945137023926,
        "normal_forces_mean_n": [
          6.447066307067871,
          11.207411766052246
        ],
        "friction_weight_ratio_mean": 0.5063482522964478,
        "normal_vertical_fraction_max": 0.011037557385861874,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09835965931415558,
        "joint_speed_rms": 1.3292303085327148,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.023667780682444572,
        "object_tracking_error_m": 0.033841900527477264,
        "object_tracking_error_rad_max": 0.05077223852276802,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02955310046672821,
          0.0270527396351099,
          0.28793686628341675,
          0.010566318407654762
        ],
        "steady_command_mae": [
          0.02955310046672821,
          0.0270527396351099,
          0.28793686628341675,
          0.010566318407654762
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.11854519695043564,
        "min_box_clearance_m": 0.5837803483009338,
        "pelvis_amplitude_m": 0.008043766021728516,
        "normal_forces_mean_n": [
          6.309725761413574,
          11.167015075683594
        ],
        "friction_weight_ratio_mean": 0.48002520203590393,
        "normal_vertical_fraction_max": 0.012817196547985077,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09966383874416351,
        "joint_speed_rms": 1.3285748958587646,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.023624464869499207,
        "object_tracking_error_m": 0.03338658809661865,
        "object_tracking_error_rad_max": 0.054898202419281006,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.028369754552841187,
          0.0261393990367651,
          0.2766660749912262,
          0.010638857260346413
        ],
        "steady_command_mae": [
          0.028369754552841187,
          0.0261393990367651,
          0.2766660749912262,
          0.010638857260346413
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12061460316181183,
        "min_box_clearance_m": 0.5843206644058228,
        "pelvis_amplitude_m": 0.008210182189941406,
        "normal_forces_mean_n": [
          6.373679161071777,
          11.062463760375977
        ],
        "friction_weight_ratio_mean": 0.5041888356208801,
        "normal_vertical_fraction_max": 0.011936794966459274,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10016987472772598,
        "joint_speed_rms": 1.330476999282837,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.023767029866576195,
        "object_tracking_error_m": 0.03408246487379074,
        "object_tracking_error_rad_max": 0.04890807345509529,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02648087777197361,
          0.025167325511574745,
          0.3150973320007324,
          0.010385548695921898
        ],
        "steady_command_mae": [
          0.02648087777197361,
          0.025167325511574745,
          0.3150973320007324,
          0.010385548695921898
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.11621659249067307,
        "min_box_clearance_m": 0.585458517074585,
        "pelvis_amplitude_m": 0.007692515850067139,
        "normal_forces_mean_n": [
          6.004511833190918,
          11.037139892578125
        ],
        "friction_weight_ratio_mean": 0.4896218180656433,
        "normal_vertical_fraction_max": 0.022415395826101303,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09665236622095108,
        "joint_speed_rms": 1.320822834968567,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.023494919762015343,
        "object_tracking_error_m": 0.031719375401735306,
        "object_tracking_error_rad_max": 0.0579768531024456,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02951079234480858,
          0.026790712028741837,
          0.30151501297950745,
          0.010626638308167458
        ],
        "steady_command_mae": [
          0.02951079234480858,
          0.026790712028741837,
          0.30151501297950745,
          0.010626638308167458
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.11849042028188705,
        "min_box_clearance_m": 0.5851022005081177,
        "pelvis_amplitude_m": 0.008151471614837646,
        "normal_forces_mean_n": [
          6.461671352386475,
          11.248186111450195
        ],
        "friction_weight_ratio_mean": 0.5136321783065796,
        "normal_vertical_fraction_max": 0.01020812802016735,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10028426349163055,
        "joint_speed_rms": 1.3306965827941895,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02372107468545437,
        "object_tracking_error_m": 0.033416248857975006,
        "object_tracking_error_rad_max": 0.052667561918497086,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.028106793761253357,
          0.026389896869659424,
          0.3252975046634674,
          0.010604167357087135
        ],
        "steady_command_mae": [
          0.028106793761253357,
          0.026389896869659424,
          0.3252975046634674,
          0.010604167357087135
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.11837425827980042,
        "min_box_clearance_m": 0.5842145681381226,
        "pelvis_amplitude_m": 0.00808483362197876,
        "normal_forces_mean_n": [
          6.225417613983154,
          11.149515151977539
        ],
        "friction_weight_ratio_mean": 0.4894014000892639,
        "normal_vertical_fraction_max": 0.012851250357925892,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09608932584524155,
        "joint_speed_rms": 1.3322861194610596,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02388695627450943,
        "object_tracking_error_m": 0.03327994421124458,
        "object_tracking_error_rad_max": 0.05501735582947731,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02866433933377266,
          0.026104366406798363,
          0.3134968876838684,
          0.010418510064482689
        ],
        "steady_command_mae": [
          0.02866433933377266,
          0.026104366406798363,
          0.3134968876838684,
          0.010418510064482689
        ],
        "contact_continuity": 0.05000000074505806,
        "max_hand_slip_m": 0.1165405884385109,
        "min_box_clearance_m": 0.5850856304168701,
        "pelvis_amplitude_m": 0.007776021957397461,
        "normal_forces_mean_n": [
          5.775996208190918,
          10.914633750915527
        ],
        "friction_weight_ratio_mean": 0.4818882942199707,
        "normal_vertical_fraction_max": 0.024014731869101524,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09440025687217712,
        "joint_speed_rms": 1.32503080368042,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.023456469178199768,
        "object_tracking_error_m": 0.031684186309576035,
        "object_tracking_error_rad_max": 0.060430459678173065,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02663484588265419,
          0.027620207518339157,
          0.2964014410972595,
          0.010473215952515602
        ],
        "steady_command_mae": [
          0.02663484588265419,
          0.027620207518339157,
          0.2964014410972595,
          0.010473215952515602
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.11625485122203827,
        "min_box_clearance_m": 0.5844299793243408,
        "pelvis_amplitude_m": 0.007804393768310547,
        "normal_forces_mean_n": [
          5.892023086547852,
          10.896757125854492
        ],
        "friction_weight_ratio_mean": 0.4710008502006531,
        "normal_vertical_fraction_max": 0.024468088522553444,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09743905812501907,
        "joint_speed_rms": 1.3217624425888062,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.023486189544200897,
        "object_tracking_error_m": 0.0319715216755867,
        "object_tracking_error_rad_max": 0.06057275831699371,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.026062507182359695,
          0.025589335709810257,
          0.3362598419189453,
          0.010479092597961426
        ],
        "steady_command_mae": [
          0.026062507182359695,
          0.025589335709810257,
          0.3362598419189453,
          0.010479092597961426
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.11628032475709915,
        "min_box_clearance_m": 0.5860635638237,
        "pelvis_amplitude_m": 0.0077416300773620605,
        "normal_forces_mean_n": [
          6.241016387939453,
          11.247312545776367
        ],
        "friction_weight_ratio_mean": 0.5093492269515991,
        "normal_vertical_fraction_max": 0.01905990205705166,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09225662797689438,
        "joint_speed_rms": 1.3247219324111938,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02363055944442749,
        "object_tracking_error_m": 0.03172951191663742,
        "object_tracking_error_rad_max": 0.05764409527182579,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.025272462517023087,
          0.026123013347387314,
          0.32429438829421997,
          0.010652363300323486
        ],
        "steady_command_mae": [
          0.025272462517023087,
          0.026123013347387314,
          0.32429438829421997,
          0.010652363300323486
        ],
        "contact_continuity": 0.12000001966953278,
        "max_hand_slip_m": 0.11977703124284744,
        "min_box_clearance_m": 0.585534393787384,
        "pelvis_amplitude_m": 0.008014798164367676,
        "normal_forces_mean_n": [
          6.6613006591796875,
          11.220090866088867
        ],
        "friction_weight_ratio_mean": 0.5290385484695435,
        "normal_vertical_fraction_max": 0.012733939103782177,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09610329568386078,
        "joint_speed_rms": 1.330719232559204,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.023782046511769295,
        "object_tracking_error_m": 0.033661093562841415,
        "object_tracking_error_rad_max": 0.049530308693647385,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.028034478425979614,
          0.027781296521425247,
          0.30705052614212036,
          0.01058652438223362
        ],
        "steady_command_mae": [
          0.028034478425979614,
          0.027781296521425247,
          0.30705052614212036,
          0.01058652438223362
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.1195673868060112,
        "min_box_clearance_m": 0.5848252773284912,
        "pelvis_amplitude_m": 0.008062183856964111,
        "normal_forces_mean_n": [
          6.458693504333496,
          11.214093208312988
        ],
        "friction_weight_ratio_mean": 0.5133892893791199,
        "normal_vertical_fraction_max": 0.011084609664976597,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09947841614484787,
        "joint_speed_rms": 1.3292557001113892,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.023678261786699295,
        "object_tracking_error_m": 0.033789169043302536,
        "object_tracking_error_rad_max": 0.05004510655999184,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.029631581157445908,
          0.02680649422109127,
          0.2865794897079468,
          0.01056607998907566
        ],
        "steady_command_mae": [
          0.029631581157445908,
          0.02680649422109127,
          0.2865794897079468,
          0.01056607998907566
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.11851160228252411,
        "min_box_clearance_m": 0.5840291976928711,
        "pelvis_amplitude_m": 0.008044540882110596,
        "normal_forces_mean_n": [
          6.334458351135254,
          11.16965103149414
        ],
        "friction_weight_ratio_mean": 0.4853248596191406,
        "normal_vertical_fraction_max": 0.012137322686612606,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10041303932666779,
        "joint_speed_rms": 1.3283370733261108,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.023611605167388916,
        "object_tracking_error_m": 0.03334467485547066,
        "object_tracking_error_rad_max": 0.05435703694820404,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.028354886919260025,
          0.026199351996183395,
          0.2769135534763336,
          0.010634267702698708
        ],
        "steady_command_mae": [
          0.028354886919260025,
          0.026199351996183395,
          0.2769135534763336,
          0.010634267702698708
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.12048480659723282,
        "min_box_clearance_m": 0.5843597650527954,
        "pelvis_amplitude_m": 0.008205771446228027,
        "normal_forces_mean_n": [
          6.399651527404785,
          11.06943130493164
        ],
        "friction_weight_ratio_mean": 0.5066368579864502,
        "normal_vertical_fraction_max": 0.011945687234401703,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10000617802143097,
        "joint_speed_rms": 1.3303112983703613,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.023759588599205017,
        "object_tracking_error_m": 0.03406918793916702,
        "object_tracking_error_rad_max": 0.048919979482889175,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02628994919359684,
          0.024802351370453835,
          0.3158785104751587,
          0.010426688008010387
        ],
        "steady_command_mae": [
          0.02628994919359684,
          0.024802351370453835,
          0.3158785104751587,
          0.010426688008010387
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.11659622192382812,
        "min_box_clearance_m": 0.5854284763336182,
        "pelvis_amplitude_m": 0.007765054702758789,
        "normal_forces_mean_n": [
          5.974421501159668,
          11.053520202636719
        ],
        "friction_weight_ratio_mean": 0.4898446202278137,
        "normal_vertical_fraction_max": 0.02247762866318226,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.0965600460767746,
        "joint_speed_rms": 1.3221585750579834,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.023546814918518066,
        "object_tracking_error_m": 0.031721025705337524,
        "object_tracking_error_rad_max": 0.058286819607019424,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.029523417353630066,
          0.026894506067037582,
          0.3021656572818756,
          0.010629558935761452
        ],
        "steady_command_mae": [
          0.029523417353630066,
          0.026894506067037582,
          0.3021656572818756,
          0.010629558935761452
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.11837861686944962,
        "min_box_clearance_m": 0.5851149559020996,
        "pelvis_amplitude_m": 0.008156120777130127,
        "normal_forces_mean_n": [
          6.4567999839782715,
          11.23331356048584
        ],
        "friction_weight_ratio_mean": 0.5141322016716003,
        "normal_vertical_fraction_max": 0.010205782018601894,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1005045548081398,
        "joint_speed_rms": 1.3302470445632935,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02372242510318756,
        "object_tracking_error_m": 0.03341122716665268,
        "object_tracking_error_rad_max": 0.052673790603876114,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.0280214361846447,
          0.02655656263232231,
          0.32446905970573425,
          0.010600602254271507
        ],
        "steady_command_mae": [
          0.0280214361846447,
          0.02655656263232231,
          0.32446905970573425,
          0.010600602254271507
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.11837740242481232,
        "min_box_clearance_m": 0.5841994285583496,
        "pelvis_amplitude_m": 0.008082151412963867,
        "normal_forces_mean_n": [
          6.225437164306641,
          11.15995979309082
        ],
        "friction_weight_ratio_mean": 0.4892262816429138,
        "normal_vertical_fraction_max": 0.012862126342952251,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09586651623249054,
        "joint_speed_rms": 1.3330581188201904,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.023886697366833687,
        "object_tracking_error_m": 0.03328339010477066,
        "object_tracking_error_rad_max": 0.05504681542515755,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      }
    ],
    "goal_limits": {
      "height_low": 0.6068800687789917,
      "height_high": 0.7268800735473633,
      "height_rate": 0.11247000098228455,
      "vx_high": 0.0,
      "forward_admitted": false,
      "reference_fps": 50,
      "episode_seconds": 30.0
    },
    "reference_free": false,
    "terminal_state_before_reset": true,
    "physical_model": {
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
      "control": "PPO joint-position offsets with PD each physics substep; no P0 feedforward or WBC"
    },
    "accepted_policy": false,
    "motion_quality": {
      "clip_0_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.08552000671625137,
          "lower_body_style_rmse_rad": 0.07972968369722366,
          "reference_compatibility_mean": 0.7861406398105356,
          "joint_acceleration_rms_rad_s2": 52.976829528808594,
          "box_relative_translation_drift_max_m": 0.03939828630295614,
          "box_relative_rotation_drift_max_rad": 0.09156653268749157
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.08555198460817337,
          "lower_body_style_rmse_rad": 0.08135330677032471,
          "reference_compatibility_mean": 0.7859209085815916,
          "joint_acceleration_rms_rad_s2": 53.22590637207031,
          "box_relative_translation_drift_max_m": 0.04057779552873983,
          "box_relative_rotation_drift_max_rad": 0.09046742894793709
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.08566688001155853,
          "lower_body_style_rmse_rad": 0.08116155117750168,
          "reference_compatibility_mean": 0.7849794083406516,
          "joint_acceleration_rms_rad_s2": 53.34197998046875,
          "box_relative_translation_drift_max_m": 0.039242177723116646,
          "box_relative_rotation_drift_max_rad": 0.0894919925587349
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.08644428104162216,
          "lower_body_style_rmse_rad": 0.08209109306335449,
          "reference_compatibility_mean": 0.7791357473112466,
          "joint_acceleration_rms_rad_s2": 52.999656677246094,
          "box_relative_translation_drift_max_m": 0.04057442425288657,
          "box_relative_rotation_drift_max_rad": 0.08427327665065153
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.08637721091508865,
          "lower_body_style_rmse_rad": 0.08222559839487076,
          "reference_compatibility_mean": 0.7802598684389357,
          "joint_acceleration_rms_rad_s2": 52.989253997802734,
          "box_relative_translation_drift_max_m": 0.04146149312776866,
          "box_relative_rotation_drift_max_rad": 0.08490747806540773
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.08614807575941086,
          "lower_body_style_rmse_rad": 0.0820605605840683,
          "reference_compatibility_mean": 0.7744864537634901,
          "joint_acceleration_rms_rad_s2": 52.89619827270508,
          "box_relative_translation_drift_max_m": 0.04159896087166017,
          "box_relative_rotation_drift_max_rad": 0.0886865833429351
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.08662419766187668,
          "lower_body_style_rmse_rad": 0.08251798897981644,
          "reference_compatibility_mean": 0.7700377356717159,
          "joint_acceleration_rms_rad_s2": 52.9651985168457,
          "box_relative_translation_drift_max_m": 0.04165227856908904,
          "box_relative_rotation_drift_max_rad": 0.08234124582519312
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.0855722576379776,
          "lower_body_style_rmse_rad": 0.08096595853567123,
          "reference_compatibility_mean": 0.7863219256066953,
          "joint_acceleration_rms_rad_s2": 53.36178970336914,
          "box_relative_translation_drift_max_m": 0.039965872343885156,
          "box_relative_rotation_drift_max_rad": 0.08958359079954434
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.08622009307146072,
          "lower_body_style_rmse_rad": 0.08235246688127518,
          "reference_compatibility_mean": 0.7746928758606462,
          "joint_acceleration_rms_rad_s2": 53.08083724975586,
          "box_relative_translation_drift_max_m": 0.04033891576571533,
          "box_relative_rotation_drift_max_rad": 0.08543699097556524
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.08656163513660431,
          "lower_body_style_rmse_rad": 0.08228854835033417,
          "reference_compatibility_mean": 0.7729919105823042,
          "joint_acceleration_rms_rad_s2": 52.887630462646484,
          "box_relative_translation_drift_max_m": 0.04106028353309817,
          "box_relative_rotation_drift_max_rad": 0.09057409727614132
        }
      ],
      "clip_1_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.08568248897790909,
          "lower_body_style_rmse_rad": 0.08145931363105774,
          "reference_compatibility_mean": 0.7842900467357966,
          "joint_acceleration_rms_rad_s2": 53.432743072509766,
          "box_relative_translation_drift_max_m": 0.03987153393837467,
          "box_relative_rotation_drift_max_rad": 0.09216105334047704
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.08565416932106018,
          "lower_body_style_rmse_rad": 0.08147518336772919,
          "reference_compatibility_mean": 0.7843167741479544,
          "joint_acceleration_rms_rad_s2": 53.03413772583008,
          "box_relative_translation_drift_max_m": 0.0406443747897602,
          "box_relative_rotation_drift_max_rad": 0.0913995008574815
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.08564635366201401,
          "lower_body_style_rmse_rad": 0.08115758001804352,
          "reference_compatibility_mean": 0.7851989678983553,
          "joint_acceleration_rms_rad_s2": 53.30923080444336,
          "box_relative_translation_drift_max_m": 0.039221830768366175,
          "box_relative_rotation_drift_max_rad": 0.08940348141662201
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.08646369725465775,
          "lower_body_style_rmse_rad": 0.08209976553916931,
          "reference_compatibility_mean": 0.7790533489892013,
          "joint_acceleration_rms_rad_s2": 52.932342529296875,
          "box_relative_translation_drift_max_m": 0.040573452995423975,
          "box_relative_rotation_drift_max_rad": 0.08413831642495873
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.08641204237937927,
          "lower_body_style_rmse_rad": 0.08222721517086029,
          "reference_compatibility_mean": 0.7800971110566323,
          "joint_acceleration_rms_rad_s2": 52.98634719848633,
          "box_relative_translation_drift_max_m": 0.04122545630094908,
          "box_relative_rotation_drift_max_rad": 0.08391451652704963
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.08612250536680222,
          "lower_body_style_rmse_rad": 0.08205664902925491,
          "reference_compatibility_mean": 0.7746113694571353,
          "joint_acceleration_rms_rad_s2": 52.998695373535156,
          "box_relative_translation_drift_max_m": 0.04143275763551616,
          "box_relative_rotation_drift_max_rad": 0.08795934109711324
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.08661887049674988,
          "lower_body_style_rmse_rad": 0.08250568062067032,
          "reference_compatibility_mean": 0.770224428937113,
          "joint_acceleration_rms_rad_s2": 52.9666862487793,
          "box_relative_translation_drift_max_m": 0.04158913296916617,
          "box_relative_rotation_drift_max_rad": 0.08240064017662536
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.08568954467773438,
          "lower_body_style_rmse_rad": 0.08139578998088837,
          "reference_compatibility_mean": 0.7847631184912343,
          "joint_acceleration_rms_rad_s2": 53.29639434814453,
          "box_relative_translation_drift_max_m": 0.03991616485294114,
          "box_relative_rotation_drift_max_rad": 0.08975648981601633
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.086229607462883,
          "lower_body_style_rmse_rad": 0.08236099779605865,
          "reference_compatibility_mean": 0.7746433121316108,
          "joint_acceleration_rms_rad_s2": 52.986907958984375,
          "box_relative_translation_drift_max_m": 0.04030359853652523,
          "box_relative_rotation_drift_max_rad": 0.08561711449345127
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.08656079322099686,
          "lower_body_style_rmse_rad": 0.08215682208538055,
          "reference_compatibility_mean": 0.7730568259748456,
          "joint_acceleration_rms_rad_s2": 52.949066162109375,
          "box_relative_translation_drift_max_m": 0.04109904505865462,
          "box_relative_rotation_drift_max_rad": 0.09063206022288413
        }
      ]
    },
    "directory": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795207462435354552",
    "checkpoint": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/dashboard/stage1/WholeBodyTracking/20261120_184153-stage1-locomotion/model_03499.pt",
    "final": false,
    "selection_score": 0.010038462391553017,
    "failure_counts": {
      "physical_failure/loss_of_grasp": 20,
      "incomplete_episode": 20,
      "contact_interruption": 20,
      "hand_slip": 20,
      "insufficient_friction_support": 20,
      "contact_near_box_bottom": 20
    },
    "scenarios": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "completed_updates": 3500
  },
  {
    "passed": false,
    "score": 0.0,
    "suite": "stage1",
    "groups": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "trials": [
      {
        "scenario": "clip_0",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03301553428173065,
          0.008544763550162315,
          0.31644219160079956,
          0.008797514252364635
        ],
        "steady_command_mae": [
          0.03301553428173065,
          0.008544763550162315,
          0.31644219160079956,
          0.008797514252364635
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.12213871628046036,
        "min_box_clearance_m": 0.5892385244369507,
        "pelvis_amplitude_m": 0.005370736122131348,
        "normal_forces_mean_n": [
          5.147602558135986,
          9.337301254272461
        ],
        "friction_weight_ratio_mean": 0.5104843378067017,
        "normal_vertical_fraction_max": 0.02566104382276535,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10361222177743912,
        "joint_speed_rms": 1.40432608127594,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021991532295942307,
        "object_tracking_error_m": 0.031062046065926552,
        "object_tracking_error_rad_max": 0.03885091096162796,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03095804713666439,
          0.008668983355164528,
          0.3260027766227722,
          0.008837079629302025
        ],
        "steady_command_mae": [
          0.03095804713666439,
          0.008668983355164528,
          0.3260027766227722,
          0.008837079629302025
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.12176582962274551,
        "min_box_clearance_m": 0.5871095061302185,
        "pelvis_amplitude_m": 0.005386412143707275,
        "normal_forces_mean_n": [
          5.036919116973877,
          9.25709056854248
        ],
        "friction_weight_ratio_mean": 0.46157756447792053,
        "normal_vertical_fraction_max": 0.02502313256263733,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10178355872631073,
        "joint_speed_rms": 1.3943774700164795,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02199016883969307,
        "object_tracking_error_m": 0.031595852226018906,
        "object_tracking_error_rad_max": 0.043578095734119415,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.031141500920057297,
          0.009185602888464928,
          0.33684346079826355,
          0.008927762508392334
        ],
        "steady_command_mae": [
          0.031141500920057297,
          0.009185602888464928,
          0.33684346079826355,
          0.008927762508392334
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.12200399488210678,
        "min_box_clearance_m": 0.5885246396064758,
        "pelvis_amplitude_m": 0.005410254001617432,
        "normal_forces_mean_n": [
          5.259061813354492,
          9.47716236114502
        ],
        "friction_weight_ratio_mean": 0.5040935277938843,
        "normal_vertical_fraction_max": 0.025112757459282875,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10457686334848404,
        "joint_speed_rms": 1.4027650356292725,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022252660244703293,
        "object_tracking_error_m": 0.03133556991815567,
        "object_tracking_error_rad_max": 0.04100821539759636,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.0310249961912632,
          0.00957112293690443,
          0.36318549513816833,
          0.008918380364775658
        ],
        "steady_command_mae": [
          0.0310249961912632,
          0.00957112293690443,
          0.36318549513816833,
          0.008918380364775658
        ],
        "contact_continuity": 0.15000002086162567,
        "max_hand_slip_m": 0.12343495339155197,
        "min_box_clearance_m": 0.5861973166465759,
        "pelvis_amplitude_m": 0.005278825759887695,
        "normal_forces_mean_n": [
          5.51282262802124,
          9.222482681274414
        ],
        "friction_weight_ratio_mean": 0.5042815208435059,
        "normal_vertical_fraction_max": 0.013376272283494473,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09195312857627869,
        "joint_speed_rms": 1.383725881576538,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02214955724775791,
        "object_tracking_error_m": 0.0338464230298996,
        "object_tracking_error_rad_max": 0.03467193990945816,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.034030552953481674,
          0.010088788345456123,
          0.36310604214668274,
          0.008993673138320446
        ],
        "steady_command_mae": [
          0.034030552953481674,
          0.010088788345456123,
          0.36310604214668274,
          0.008993673138320446
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.12416507303714752,
        "min_box_clearance_m": 0.5882218480110168,
        "pelvis_amplitude_m": 0.005461215972900391,
        "normal_forces_mean_n": [
          5.573192119598389,
          9.551969528198242
        ],
        "friction_weight_ratio_mean": 0.5342512130737305,
        "normal_vertical_fraction_max": 0.027416400611400604,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09879900515079498,
        "joint_speed_rms": 1.3925530910491943,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02226213365793228,
        "object_tracking_error_m": 0.03310670331120491,
        "object_tracking_error_rad_max": 0.03123224526643753,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03528446704149246,
          0.010679720900952816,
          0.35553693771362305,
          0.008783161640167236
        ],
        "steady_command_mae": [
          0.03528446704149246,
          0.010679720900952816,
          0.35553693771362305,
          0.008783161640167236
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.1223975196480751,
        "min_box_clearance_m": 0.5865124464035034,
        "pelvis_amplitude_m": 0.005292415618896484,
        "normal_forces_mean_n": [
          5.3446550369262695,
          9.447405815124512
        ],
        "friction_weight_ratio_mean": 0.4843710958957672,
        "normal_vertical_fraction_max": 0.02677544206380844,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09298615157604218,
        "joint_speed_rms": 1.3836541175842285,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021968752145767212,
        "object_tracking_error_m": 0.032943617552518845,
        "object_tracking_error_rad_max": 0.03815760463476181,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.033794503659009933,
          0.009838107042014599,
          0.35152995586395264,
          0.008902251720428467
        ],
        "steady_command_mae": [
          0.033794503659009933,
          0.009838107042014599,
          0.35152995586395264,
          0.008902251720428467
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.12427093088626862,
        "min_box_clearance_m": 0.5872442722320557,
        "pelvis_amplitude_m": 0.0055193305015563965,
        "normal_forces_mean_n": [
          5.304577827453613,
          9.31639289855957
        ],
        "friction_weight_ratio_mean": 0.513339638710022,
        "normal_vertical_fraction_max": 0.027439314872026443,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.0970141738653183,
        "joint_speed_rms": 1.3902567625045776,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022200055420398712,
        "object_tracking_error_m": 0.03341475874185562,
        "object_tracking_error_rad_max": 0.03442906588315964,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03033861517906189,
          0.008342144079506397,
          0.32897961139678955,
          0.008753180503845215
        ],
        "steady_command_mae": [
          0.03033861517906189,
          0.008342144079506397,
          0.32897961139678955,
          0.008753180503845215
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.12210539728403091,
        "min_box_clearance_m": 0.5892603993415833,
        "pelvis_amplitude_m": 0.005318045616149902,
        "normal_forces_mean_n": [
          5.276967525482178,
          9.458003044128418
        ],
        "friction_weight_ratio_mean": 0.5107540488243103,
        "normal_vertical_fraction_max": 0.025276774540543556,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10540810972452164,
        "joint_speed_rms": 1.3955433368682861,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022043902426958084,
        "object_tracking_error_m": 0.031124943867325783,
        "object_tracking_error_rad_max": 0.038219913840293884,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03489090874791145,
          0.007876326330006123,
          0.3350178599357605,
          0.009045409969985485
        ],
        "steady_command_mae": [
          0.03489090874791145,
          0.007876326330006123,
          0.3350178599357605,
          0.009045409969985485
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.1236494854092598,
        "min_box_clearance_m": 0.5867254734039307,
        "pelvis_amplitude_m": 0.005514919757843018,
        "normal_forces_mean_n": [
          5.32642936706543,
          9.463569641113281
        ],
        "friction_weight_ratio_mean": 0.49161797761917114,
        "normal_vertical_fraction_max": 0.027227649465203285,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10358855873346329,
        "joint_speed_rms": 1.3949053287506104,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022315602749586105,
        "object_tracking_error_m": 0.03313811123371124,
        "object_tracking_error_rad_max": 0.03677060827612877,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03354555368423462,
          0.008973302319645882,
          0.34204405546188354,
          0.008905124850571156
        ],
        "steady_command_mae": [
          0.03354555368423462,
          0.008973302319645882,
          0.34204405546188354,
          0.008905124850571156
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.12393143028020859,
        "min_box_clearance_m": 0.5865309238433838,
        "pelvis_amplitude_m": 0.005462706089019775,
        "normal_forces_mean_n": [
          5.208527565002441,
          9.435480117797852
        ],
        "friction_weight_ratio_mean": 0.4747537076473236,
        "normal_vertical_fraction_max": 0.026711786165833473,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09341953694820404,
        "joint_speed_rms": 1.398085594177246,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02236981689929962,
        "object_tracking_error_m": 0.032871395349502563,
        "object_tracking_error_rad_max": 0.038549721240997314,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03307035192847252,
          0.008270642720162868,
          0.31524235010147095,
          0.008810723200440407
        ],
        "steady_command_mae": [
          0.03307035192847252,
          0.008270642720162868,
          0.31524235010147095,
          0.008810723200440407
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.12217897176742554,
        "min_box_clearance_m": 0.5892393589019775,
        "pelvis_amplitude_m": 0.005380809307098389,
        "normal_forces_mean_n": [
          5.1882734298706055,
          9.358610153198242
        ],
        "friction_weight_ratio_mean": 0.5090570449829102,
        "normal_vertical_fraction_max": 0.02566104382276535,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10339190065860748,
        "joint_speed_rms": 1.4039934873580933,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021997736766934395,
        "object_tracking_error_m": 0.031060855835676193,
        "object_tracking_error_rad_max": 0.03886433318257332,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03087395429611206,
          0.008641665801405907,
          0.3270077109336853,
          0.008837747387588024
        ],
        "steady_command_mae": [
          0.03087395429611206,
          0.008641665801405907,
          0.3270077109336853,
          0.008837747387588024
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.1217450499534607,
        "min_box_clearance_m": 0.5870086550712585,
        "pelvis_amplitude_m": 0.005388855934143066,
        "normal_forces_mean_n": [
          5.0424981117248535,
          9.258407592773438
        ],
        "friction_weight_ratio_mean": 0.4591566026210785,
        "normal_vertical_fraction_max": 0.02502313256263733,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1013815850019455,
        "joint_speed_rms": 1.394362211227417,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021984346210956573,
        "object_tracking_error_m": 0.03160820156335831,
        "object_tracking_error_rad_max": 0.04391714558005333,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.031240949407219887,
          0.009270790033042431,
          0.34038519859313965,
          0.008930695243179798
        ],
        "steady_command_mae": [
          0.031240949407219887,
          0.009270790033042431,
          0.34038519859313965,
          0.008930695243179798
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.1219741702079773,
        "min_box_clearance_m": 0.5885215401649475,
        "pelvis_amplitude_m": 0.005405783653259277,
        "normal_forces_mean_n": [
          5.277160167694092,
          9.484725952148438
        ],
        "friction_weight_ratio_mean": 0.5046747326850891,
        "normal_vertical_fraction_max": 0.025112757459282875,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10515016317367554,
        "joint_speed_rms": 1.4029512405395508,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022257136180996895,
        "object_tracking_error_m": 0.031333617866039276,
        "object_tracking_error_rad_max": 0.04108675941824913,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03119666315615177,
          0.009648637846112251,
          0.3648233711719513,
          0.008910680189728737
        ],
        "steady_command_mae": [
          0.03119666315615177,
          0.009648637846112251,
          0.3648233711719513,
          0.008910680189728737
        ],
        "contact_continuity": 0.15000002086162567,
        "max_hand_slip_m": 0.12327633798122406,
        "min_box_clearance_m": 0.5859930515289307,
        "pelvis_amplitude_m": 0.0052651166915893555,
        "normal_forces_mean_n": [
          5.517369270324707,
          9.237317085266113
        ],
        "friction_weight_ratio_mean": 0.49744516611099243,
        "normal_vertical_fraction_max": 0.013370739296078682,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09198155254125595,
        "joint_speed_rms": 1.3835639953613281,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022132141515612602,
        "object_tracking_error_m": 0.03387272730469704,
        "object_tracking_error_rad_max": 0.03530433401465416,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.0339522510766983,
          0.009979763068258762,
          0.36269861459732056,
          0.008998704142868519
        ],
        "steady_command_mae": [
          0.0339522510766983,
          0.009979763068258762,
          0.36269861459732056,
          0.008998704142868519
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.12402024120092392,
        "min_box_clearance_m": 0.5876797437667847,
        "pelvis_amplitude_m": 0.00546419620513916,
        "normal_forces_mean_n": [
          5.488978862762451,
          9.513821601867676
        ],
        "friction_weight_ratio_mean": 0.5268245935440063,
        "normal_vertical_fraction_max": 0.027416400611400604,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09807559847831726,
        "joint_speed_rms": 1.3925983905792236,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022258717566728592,
        "object_tracking_error_m": 0.03318754583597183,
        "object_tracking_error_rad_max": 0.032776251435279846,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.035353995859622955,
          0.010282652452588081,
          0.3545142114162445,
          0.008917272090911865
        ],
        "steady_command_mae": [
          0.035353995859622955,
          0.010282652452588081,
          0.3545142114162445,
          0.008917272090911865
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12362778931856155,
        "min_box_clearance_m": 0.5877168774604797,
        "pelvis_amplitude_m": 0.005439341068267822,
        "normal_forces_mean_n": [
          5.455068111419678,
          9.540349960327148
        ],
        "friction_weight_ratio_mean": 0.511370062828064,
        "normal_vertical_fraction_max": 0.02677544206380844,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09475471079349518,
        "joint_speed_rms": 1.3911443948745728,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022167053073644638,
        "object_tracking_error_m": 0.03274783492088318,
        "object_tracking_error_rad_max": 0.03472428768873215,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.033769868314266205,
          0.00991077534854412,
          0.3519563674926758,
          0.008903468027710915
        ],
        "steady_command_mae": [
          0.033769868314266205,
          0.00991077534854412,
          0.3519563674926758,
          0.008903468027710915
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.12437251955270767,
        "min_box_clearance_m": 0.587236762046814,
        "pelvis_amplitude_m": 0.005521595478057861,
        "normal_forces_mean_n": [
          5.4614458084106445,
          9.398921012878418
        ],
        "friction_weight_ratio_mean": 0.5017319917678833,
        "normal_vertical_fraction_max": 0.027439314872026443,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09681187570095062,
        "joint_speed_rms": 1.3867970705032349,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022197984158992767,
        "object_tracking_error_m": 0.03342176601290703,
        "object_tracking_error_rad_max": 0.034301627427339554,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03044017031788826,
          0.008256705477833748,
          0.32482725381851196,
          0.008759796619415283
        ],
        "steady_command_mae": [
          0.03044017031788826,
          0.008256705477833748,
          0.32482725381851196,
          0.008759796619415283
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.12221755087375641,
        "min_box_clearance_m": 0.5892552137374878,
        "pelvis_amplitude_m": 0.005320608615875244,
        "normal_forces_mean_n": [
          5.286704063415527,
          9.465643882751465
        ],
        "friction_weight_ratio_mean": 0.5116263031959534,
        "normal_vertical_fraction_max": 0.025276774540543556,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10516148805618286,
        "joint_speed_rms": 1.3959943056106567,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022054079920053482,
        "object_tracking_error_m": 0.031124114990234375,
        "object_tracking_error_rad_max": 0.03825623169541359,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.03497496619820595,
          0.007695061154663563,
          0.3326321542263031,
          0.009039747528731823
        ],
        "steady_command_mae": [
          0.03497496619820595,
          0.007695061154663563,
          0.3326321542263031,
          0.009039747528731823
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12299055606126785,
        "min_box_clearance_m": 0.586276113986969,
        "pelvis_amplitude_m": 0.005510449409484863,
        "normal_forces_mean_n": [
          5.238227367401123,
          9.368021965026855
        ],
        "friction_weight_ratio_mean": 0.4825672209262848,
        "normal_vertical_fraction_max": 0.027227649465203285,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10419262945652008,
        "joint_speed_rms": 1.3944143056869507,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022299982607364655,
        "object_tracking_error_m": 0.033183153718709946,
        "object_tracking_error_rad_max": 0.03902893513441086,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.033408720046281815,
          0.008844034746289253,
          0.34300917387008667,
          0.008905434980988503
        ],
        "steady_command_mae": [
          0.033408720046281815,
          0.008844034746289253,
          0.34300917387008667,
          0.008905434980988503
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.12399722635746002,
        "min_box_clearance_m": 0.5865226984024048,
        "pelvis_amplitude_m": 0.0054662227630615234,
        "normal_forces_mean_n": [
          5.214928150177002,
          9.436078071594238
        ],
        "friction_weight_ratio_mean": 0.4747917056083679,
        "normal_vertical_fraction_max": 0.026711786165833473,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.0929546058177948,
        "joint_speed_rms": 1.3979355096817017,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02237771824002266,
        "object_tracking_error_m": 0.032871849834918976,
        "object_tracking_error_rad_max": 0.03863395005464554,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      }
    ],
    "goal_limits": {
      "height_low": 0.6068800687789917,
      "height_high": 0.7268800735473633,
      "height_rate": 0.11247000098228455,
      "vx_high": 0.0,
      "forward_admitted": false,
      "reference_fps": 50,
      "episode_seconds": 30.0
    },
    "reference_free": false,
    "terminal_state_before_reset": true,
    "physical_model": {
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
      "control": "PPO joint-position offsets with PD each physics substep; no P0 feedforward or WBC"
    },
    "accepted_policy": false,
    "motion_quality": {
      "clip_0_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.09428401291370392,
          "lower_body_style_rmse_rad": 0.07721925526857376,
          "reference_compatibility_mean": 0.8588253021583523,
          "joint_acceleration_rms_rad_s2": 57.6012077331543,
          "box_relative_translation_drift_max_m": 0.03595961056412528,
          "box_relative_rotation_drift_max_rad": 0.07329732167418229
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.09403175115585327,
          "lower_body_style_rmse_rad": 0.07689538598060608,
          "reference_compatibility_mean": 0.8585969936445135,
          "joint_acceleration_rms_rad_s2": 57.628780364990234,
          "box_relative_translation_drift_max_m": 0.037689018891342185,
          "box_relative_rotation_drift_max_rad": 0.07808863061604175
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.09433633089065552,
          "lower_body_style_rmse_rad": 0.07703197747468948,
          "reference_compatibility_mean": 0.8568500451992597,
          "joint_acceleration_rms_rad_s2": 57.76902770996094,
          "box_relative_translation_drift_max_m": 0.03632829765285222,
          "box_relative_rotation_drift_max_rad": 0.07489396871891855
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.09446791559457779,
          "lower_body_style_rmse_rad": 0.07691948860883713,
          "reference_compatibility_mean": 0.8632542044138425,
          "joint_acceleration_rms_rad_s2": 56.80528259277344,
          "box_relative_translation_drift_max_m": 0.03874646261487951,
          "box_relative_rotation_drift_max_rad": 0.07603170208594102
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.0948123186826706,
          "lower_body_style_rmse_rad": 0.07692248374223709,
          "reference_compatibility_mean": 0.8551193764904476,
          "joint_acceleration_rms_rad_s2": 56.8919792175293,
          "box_relative_translation_drift_max_m": 0.03711854658935319,
          "box_relative_rotation_drift_max_rad": 0.07046993450432595
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.09421280771493912,
          "lower_body_style_rmse_rad": 0.0769215077161789,
          "reference_compatibility_mean": 0.8625713070647482,
          "joint_acceleration_rms_rad_s2": 56.57120132446289,
          "box_relative_translation_drift_max_m": 0.038449156518071397,
          "box_relative_rotation_drift_max_rad": 0.07804252294078659
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.0947151780128479,
          "lower_body_style_rmse_rad": 0.0773608535528183,
          "reference_compatibility_mean": 0.8525675141283197,
          "joint_acceleration_rms_rad_s2": 56.976890563964844,
          "box_relative_translation_drift_max_m": 0.0377361914605514,
          "box_relative_rotation_drift_max_rad": 0.0750263517045079
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.09418483078479767,
          "lower_body_style_rmse_rad": 0.07691887021064758,
          "reference_compatibility_mean": 0.8622422484994606,
          "joint_acceleration_rms_rad_s2": 57.44154739379883,
          "box_relative_translation_drift_max_m": 0.03636877960237467,
          "box_relative_rotation_drift_max_rad": 0.07303257615720846
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.0946950763463974,
          "lower_body_style_rmse_rad": 0.07702695578336716,
          "reference_compatibility_mean": 0.8530031578542884,
          "joint_acceleration_rms_rad_s2": 57.30055618286133,
          "box_relative_translation_drift_max_m": 0.038078729619134055,
          "box_relative_rotation_drift_max_rad": 0.07749052774991466
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.09490863233804703,
          "lower_body_style_rmse_rad": 0.07726948708295822,
          "reference_compatibility_mean": 0.8542971699375059,
          "joint_acceleration_rms_rad_s2": 57.436790466308594,
          "box_relative_translation_drift_max_m": 0.03828648678955509,
          "box_relative_rotation_drift_max_rad": 0.07832144268829723
        }
      ],
      "clip_1_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.09430009871721268,
          "lower_body_style_rmse_rad": 0.0772794708609581,
          "reference_compatibility_mean": 0.8585673674773172,
          "joint_acceleration_rms_rad_s2": 57.5589599609375,
          "box_relative_translation_drift_max_m": 0.03592159535951574,
          "box_relative_rotation_drift_max_rad": 0.07316770881582232
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.09402485936880112,
          "lower_body_style_rmse_rad": 0.0768844336271286,
          "reference_compatibility_mean": 0.858566455450178,
          "joint_acceleration_rms_rad_s2": 57.620601654052734,
          "box_relative_translation_drift_max_m": 0.03776582735479417,
          "box_relative_rotation_drift_max_rad": 0.07853714281264929
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.0943281278014183,
          "lower_body_style_rmse_rad": 0.07717394083738327,
          "reference_compatibility_mean": 0.8568940998768682,
          "joint_acceleration_rms_rad_s2": 57.80686950683594,
          "box_relative_translation_drift_max_m": 0.036267366776618785,
          "box_relative_rotation_drift_max_rad": 0.07453447719088833
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.09442974627017975,
          "lower_body_style_rmse_rad": 0.07690681517124176,
          "reference_compatibility_mean": 0.8640500631347662,
          "joint_acceleration_rms_rad_s2": 56.72585678100586,
          "box_relative_translation_drift_max_m": 0.038861617242617025,
          "box_relative_rotation_drift_max_rad": 0.07671072384847878
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.09478358924388885,
          "lower_body_style_rmse_rad": 0.0769292488694191,
          "reference_compatibility_mean": 0.8550252322996739,
          "joint_acceleration_rms_rad_s2": 56.882667541503906,
          "box_relative_translation_drift_max_m": 0.03744923135071922,
          "box_relative_rotation_drift_max_rad": 0.0720232954806501
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.09460941702127457,
          "lower_body_style_rmse_rad": 0.077016681432724,
          "reference_compatibility_mean": 0.8547687568075624,
          "joint_acceleration_rms_rad_s2": 56.7675895690918,
          "box_relative_translation_drift_max_m": 0.03736442462661007,
          "box_relative_rotation_drift_max_rad": 0.0733695022504277
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.09472602605819702,
          "lower_body_style_rmse_rad": 0.07736510038375854,
          "reference_compatibility_mean": 0.8525313433274745,
          "joint_acceleration_rms_rad_s2": 56.70098876953125,
          "box_relative_translation_drift_max_m": 0.03778035598086901,
          "box_relative_rotation_drift_max_rad": 0.07490076475297504
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.09423362463712692,
          "lower_body_style_rmse_rad": 0.07685615867376328,
          "reference_compatibility_mean": 0.8621334582330837,
          "joint_acceleration_rms_rad_s2": 57.44169616699219,
          "box_relative_translation_drift_max_m": 0.03629375349071587,
          "box_relative_rotation_drift_max_rad": 0.0726793476693234
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.0946427509188652,
          "lower_body_style_rmse_rad": 0.07702632248401642,
          "reference_compatibility_mean": 0.8531202116333738,
          "joint_acceleration_rms_rad_s2": 57.238853454589844,
          "box_relative_translation_drift_max_m": 0.03826754981321256,
          "box_relative_rotation_drift_max_rad": 0.07976795915433975
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.09494228661060333,
          "lower_body_style_rmse_rad": 0.07726740092039108,
          "reference_compatibility_mean": 0.8541952177938518,
          "joint_acceleration_rms_rad_s2": 57.385799407958984,
          "box_relative_translation_drift_max_m": 0.03829938547862449,
          "box_relative_rotation_drift_max_rad": 0.07843960017976752
        }
      ]
    },
    "directory": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795214808532584110",
    "checkpoint": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/dashboard/stage1/WholeBodyTracking/20261120_204522-stage1-locomotion/model_03999.pt",
    "final": false,
    "selection_score": 0.010738462524918412,
    "failure_counts": {
      "physical_failure/loss_of_grasp": 20,
      "incomplete_episode": 20,
      "contact_interruption": 20,
      "hand_slip": 20,
      "insufficient_friction_support": 20,
      "contact_near_box_bottom": 20
    },
    "scenarios": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "completed_updates": 4000
  },
  {
    "passed": false,
    "score": 0.0,
    "suite": "stage1",
    "groups": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "trials": [
      {
        "scenario": "clip_0",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.01695164665579796,
          0.013593807816505432,
          0.24568286538124084,
          0.008930969052016735
        ],
        "steady_command_mae": [
          0.01695164665579796,
          0.013593807816505432,
          0.24568286538124084,
          0.008930969052016735
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.11785107105970383,
        "min_box_clearance_m": 0.5894309878349304,
        "pelvis_amplitude_m": 0.006616175174713135,
        "normal_forces_mean_n": [
          4.7212724685668945,
          8.491155624389648
        ],
        "friction_weight_ratio_mean": 0.4996945858001709,
        "normal_vertical_fraction_max": 0.02559470571577549,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10281714051961899,
        "joint_speed_rms": 1.3790016174316406,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.020309021696448326,
        "object_tracking_error_m": 0.031364839524030685,
        "object_tracking_error_rad_max": 0.030569417402148247,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.015040263533592224,
          0.01317695714533329,
          0.2518547475337982,
          0.009012579917907715
        ],
        "steady_command_mae": [
          0.015040263533592224,
          0.01317695714533329,
          0.2518547475337982,
          0.009012579917907715
        ],
        "contact_continuity": 0.05000000074505806,
        "max_hand_slip_m": 0.11798879504203796,
        "min_box_clearance_m": 0.5881975889205933,
        "pelvis_amplitude_m": 0.0066776275634765625,
        "normal_forces_mean_n": [
          4.763829231262207,
          8.503483772277832
        ],
        "friction_weight_ratio_mean": 0.4549158215522766,
        "normal_vertical_fraction_max": 0.025034261867403984,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10147948563098907,
        "joint_speed_rms": 1.3766348361968994,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.020345613360404968,
        "object_tracking_error_m": 0.0317419096827507,
        "object_tracking_error_rad_max": 0.03259897977113724,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.01438012532889843,
          0.013121378608047962,
          0.26257649064064026,
          0.008997833356261253
        ],
        "steady_command_mae": [
          0.01438012532889843,
          0.013121378608047962,
          0.26257649064064026,
          0.008997833356261253
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.11795222014188766,
        "min_box_clearance_m": 0.5901402831077576,
        "pelvis_amplitude_m": 0.0066353678703308105,
        "normal_forces_mean_n": [
          5.026048183441162,
          8.728177070617676
        ],
        "friction_weight_ratio_mean": 0.5157743692398071,
        "normal_vertical_fraction_max": 0.02509181760251522,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10094109922647476,
        "joint_speed_rms": 1.3774805068969727,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.020467335358262062,
        "object_tracking_error_m": 0.03151489049196243,
        "object_tracking_error_rad_max": 0.027359778061509132,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.013305353932082653,
          0.01196964643895626,
          0.24568679928779602,
          0.009197687730193138
        ],
        "steady_command_mae": [
          0.013305353932082653,
          0.01196964643895626,
          0.24568679928779602,
          0.009197687730193138
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.12111291289329529,
        "min_box_clearance_m": 0.5885539650917053,
        "pelvis_amplitude_m": 0.006813466548919678,
        "normal_forces_mean_n": [
          5.0832390785217285,
          8.329374313354492
        ],
        "friction_weight_ratio_mean": 0.5258076190948486,
        "normal_vertical_fraction_max": 0.01768641360104084,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10495191812515259,
        "joint_speed_rms": 1.3851031064987183,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.020599793642759323,
        "object_tracking_error_m": 0.033823318779468536,
        "object_tracking_error_rad_max": 0.018136978149414062,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.016658300533890724,
          0.012441758997738361,
          0.26005738973617554,
          0.009213602170348167
        ],
        "steady_command_mae": [
          0.016658300533890724,
          0.012441758997738361,
          0.26005738973617554,
          0.009213602170348167
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.11940161883831024,
        "min_box_clearance_m": 0.5878891944885254,
        "pelvis_amplitude_m": 0.0068773627281188965,
        "normal_forces_mean_n": [
          4.974125862121582,
          8.54450798034668
        ],
        "friction_weight_ratio_mean": 0.5037000775337219,
        "normal_vertical_fraction_max": 0.027418602257966995,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10215382277965546,
        "joint_speed_rms": 1.3833999633789062,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.020539462566375732,
        "object_tracking_error_m": 0.03349662199616432,
        "object_tracking_error_rad_max": 0.024402247741818428,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.017720704898238182,
          0.01271551288664341,
          0.2558654248714447,
          0.009108138270676136
        ],
        "steady_command_mae": [
          0.017720704898238182,
          0.01271551288664341,
          0.2558654248714447,
          0.009108138270676136
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.1188092976808548,
        "min_box_clearance_m": 0.589932918548584,
        "pelvis_amplitude_m": 0.00681990385055542,
        "normal_forces_mean_n": [
          5.142239093780518,
          8.704996109008789
        ],
        "friction_weight_ratio_mean": 0.5390639305114746,
        "normal_vertical_fraction_max": 0.02677786909043789,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10312138497829437,
        "joint_speed_rms": 1.3795197010040283,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02047795243561268,
        "object_tracking_error_m": 0.03274484723806381,
        "object_tracking_error_rad_max": 0.021323073655366898,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.017730046063661575,
          0.012392302043735981,
          0.2677549421787262,
          0.009115743450820446
        ],
        "steady_command_mae": [
          0.017730046063661575,
          0.012392302043735981,
          0.2677549421787262,
          0.009115743450820446
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12104903906583786,
        "min_box_clearance_m": 0.5891966223716736,
        "pelvis_amplitude_m": 0.006948947906494141,
        "normal_forces_mean_n": [
          4.94396448135376,
          8.48029613494873
        ],
        "friction_weight_ratio_mean": 0.5310201644897461,
        "normal_vertical_fraction_max": 0.027439314872026443,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09948582947254181,
        "joint_speed_rms": 1.388770341873169,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.020573928952217102,
        "object_tracking_error_m": 0.033536382019519806,
        "object_tracking_error_rad_max": 0.017169484868645668,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.015041710808873177,
          0.013662705197930336,
          0.24094036221504211,
          0.008903229609131813
        ],
        "steady_command_mae": [
          0.015041710808873177,
          0.013662705197930336,
          0.24094036221504211,
          0.008903229609131813
        ],
        "contact_continuity": 0.05000000074505806,
        "max_hand_slip_m": 0.11800039559602737,
        "min_box_clearance_m": 0.5887866020202637,
        "pelvis_amplitude_m": 0.006584107875823975,
        "normal_forces_mean_n": [
          4.632443904876709,
          8.42833137512207
        ],
        "friction_weight_ratio_mean": 0.4729907512664795,
        "normal_vertical_fraction_max": 0.0252752173691988,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10403431951999664,
        "joint_speed_rms": 1.3780232667922974,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.020339762791991234,
        "object_tracking_error_m": 0.03156356140971184,
        "object_tracking_error_rad_max": 0.031215980648994446,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.01845439337193966,
          0.01183206494897604,
          0.2594132125377655,
          0.00915901642292738
        ],
        "steady_command_mae": [
          0.01845439337193966,
          0.01183206494897604,
          0.2594132125377655,
          0.00915901642292738
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.1196058839559555,
        "min_box_clearance_m": 0.5878996849060059,
        "pelvis_amplitude_m": 0.006849884986877441,
        "normal_forces_mean_n": [
          5.013576984405518,
          8.707414627075195
        ],
        "friction_weight_ratio_mean": 0.4934595227241516,
        "normal_vertical_fraction_max": 0.027232011780142784,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.0983496606349945,
        "joint_speed_rms": 1.38526451587677,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.020546365529298782,
        "object_tracking_error_m": 0.033292390406131744,
        "object_tracking_error_rad_max": 0.02403080090880394,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.016530368477106094,
          0.012043694034218788,
          0.25766056776046753,
          0.009006190113723278
        ],
        "steady_command_mae": [
          0.016530368477106094,
          0.012043694034218788,
          0.25766056776046753,
          0.009006190113723278
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.11915794759988785,
        "min_box_clearance_m": 0.5884519815444946,
        "pelvis_amplitude_m": 0.00679248571395874,
        "normal_forces_mean_n": [
          4.784045696258545,
          8.49193286895752
        ],
        "friction_weight_ratio_mean": 0.5069468021392822,
        "normal_vertical_fraction_max": 0.026725420728325844,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1022016778588295,
        "joint_speed_rms": 1.3883414268493652,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02061615139245987,
        "object_tracking_error_m": 0.03292957693338394,
        "object_tracking_error_rad_max": 0.02528083510696888,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.01731288805603981,
          0.014390110969543457,
          0.2515650987625122,
          0.00887749157845974
        ],
        "steady_command_mae": [
          0.01731288805603981,
          0.014390110969543457,
          0.2515650987625122,
          0.00887749157845974
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.1173485592007637,
        "min_box_clearance_m": 0.5903850793838501,
        "pelvis_amplitude_m": 0.006532430648803711,
        "normal_forces_mean_n": [
          4.8930182456970215,
          8.578483581542969
        ],
        "friction_weight_ratio_mean": 0.5185771584510803,
        "normal_vertical_fraction_max": 0.02559470571577549,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10210531949996948,
        "joint_speed_rms": 1.3757599592208862,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.020229488611221313,
        "object_tracking_error_m": 0.031234050169587135,
        "object_tracking_error_rad_max": 0.027968721464276314,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.01503036916255951,
          0.013020278885960579,
          0.25041383504867554,
          0.00905622262507677
        ],
        "steady_command_mae": [
          0.01503036916255951,
          0.013020278885960579,
          0.25041383504867554,
          0.00905622262507677
        ],
        "contact_continuity": 0.05000000074505806,
        "max_hand_slip_m": 0.11837493628263474,
        "min_box_clearance_m": 0.5882264971733093,
        "pelvis_amplitude_m": 0.006750166416168213,
        "normal_forces_mean_n": [
          4.59487247467041,
          8.4024076461792
        ],
        "friction_weight_ratio_mean": 0.4610964357852936,
        "normal_vertical_fraction_max": 0.025034261867403984,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1021040678024292,
        "joint_speed_rms": 1.3820079565048218,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.020410839468240738,
        "object_tracking_error_m": 0.0317404568195343,
        "object_tracking_error_rad_max": 0.03251401707530022,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.014570556581020355,
          0.013027392327785492,
          0.262145459651947,
          0.009014618583023548
        ],
        "steady_command_mae": [
          0.014570556581020355,
          0.013027392327785492,
          0.262145459651947,
          0.009014618583023548
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.11799130588769913,
        "min_box_clearance_m": 0.5901367664337158,
        "pelvis_amplitude_m": 0.006659448146820068,
        "normal_forces_mean_n": [
          5.039607524871826,
          8.728485107421875
        ],
        "friction_weight_ratio_mean": 0.5152201056480408,
        "normal_vertical_fraction_max": 0.02509181760251522,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10132865607738495,
        "joint_speed_rms": 1.378867745399475,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.020483380183577538,
        "object_tracking_error_m": 0.03151557967066765,
        "object_tracking_error_rad_max": 0.02735077776014805,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.013332439586520195,
          0.012064341455698013,
          0.24703732132911682,
          0.009197640232741833
        ],
        "steady_command_mae": [
          0.013332439586520195,
          0.012064341455698013,
          0.24703732132911682,
          0.009197640232741833
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.12099169194698334,
        "min_box_clearance_m": 0.5884087085723877,
        "pelvis_amplitude_m": 0.006810367107391357,
        "normal_forces_mean_n": [
          5.100136756896973,
          8.335474014282227
        ],
        "friction_weight_ratio_mean": 0.5232815742492676,
        "normal_vertical_fraction_max": 0.01737319678068161,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10441677272319794,
        "joint_speed_rms": 1.385008454322815,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02059033326804638,
        "object_tracking_error_m": 0.03383609652519226,
        "object_tracking_error_rad_max": 0.01860291138291359,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.016628649085760117,
          0.01246262900531292,
          0.26039987802505493,
          0.00922329444438219
        ],
        "steady_command_mae": [
          0.016628649085760117,
          0.01246262900531292,
          0.26039987802505493,
          0.00922329444438219
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.11946388334035873,
        "min_box_clearance_m": 0.5878773927688599,
        "pelvis_amplitude_m": 0.006890833377838135,
        "normal_forces_mean_n": [
          4.990894794464111,
          8.557150840759277
        ],
        "friction_weight_ratio_mean": 0.5032732486724854,
        "normal_vertical_fraction_max": 0.027418602257966995,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10220398008823395,
        "joint_speed_rms": 1.3837709426879883,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.020551498979330063,
        "object_tracking_error_m": 0.033498793840408325,
        "object_tracking_error_rad_max": 0.024394962936639786,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.01783869042992592,
          0.012852703221142292,
          0.2540901005268097,
          0.009104931727051735
        ],
        "steady_command_mae": [
          0.01783869042992592,
          0.012852703221142292,
          0.2540901005268097,
          0.009104931727051735
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.11936644464731216,
        "min_box_clearance_m": 0.5898827910423279,
        "pelvis_amplitude_m": 0.0068111419677734375,
        "normal_forces_mean_n": [
          5.146258354187012,
          8.771514892578125
        ],
        "friction_weight_ratio_mean": 0.5399259328842163,
        "normal_vertical_fraction_max": 0.02677786909043789,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10325910896062851,
        "joint_speed_rms": 1.3835912942886353,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.020466485992074013,
        "object_tracking_error_m": 0.032767586410045624,
        "object_tracking_error_rad_max": 0.020107148215174675,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.017745735123753548,
          0.012539091520011425,
          0.2669345438480377,
          0.00911257229745388
        ],
        "steady_command_mae": [
          0.017745735123753548,
          0.012539091520011425,
          0.2669345438480377,
          0.00911257229745388
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12101221084594727,
        "min_box_clearance_m": 0.5892010927200317,
        "pelvis_amplitude_m": 0.006941497325897217,
        "normal_forces_mean_n": [
          5.002884864807129,
          8.51228141784668
        ],
        "friction_weight_ratio_mean": 0.5298510789871216,
        "normal_vertical_fraction_max": 0.027439314872026443,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09940222650766373,
        "joint_speed_rms": 1.3882646560668945,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.020566215738654137,
        "object_tracking_error_m": 0.03353618457913399,
        "object_tracking_error_rad_max": 0.01708592288196087,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.015048173256218433,
          0.013221177272498608,
          0.24374350905418396,
          0.008879756554961205
        ],
        "steady_command_mae": [
          0.015048173256218433,
          0.013221177272498608,
          0.24374350905418396,
          0.008879756554961205
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.11645876616239548,
        "min_box_clearance_m": 0.5889371633529663,
        "pelvis_amplitude_m": 0.006547451019287109,
        "normal_forces_mean_n": [
          4.676251411437988,
          8.344464302062988
        ],
        "friction_weight_ratio_mean": 0.490988165140152,
        "normal_vertical_fraction_max": 0.0252752173691988,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10348799079656601,
        "joint_speed_rms": 1.3720992803573608,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02027527056634426,
        "object_tracking_error_m": 0.03149973601102829,
        "object_tracking_error_rad_max": 0.033167362213134766,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.018346110358834267,
          0.011684305965900421,
          0.2563213109970093,
          0.009169971570372581
        ],
        "steady_command_mae": [
          0.018346110358834267,
          0.011684305965900421,
          0.2563213109970093,
          0.009169971570372581
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.11966738849878311,
        "min_box_clearance_m": 0.5879002809524536,
        "pelvis_amplitude_m": 0.00686115026473999,
        "normal_forces_mean_n": [
          5.01377010345459,
          8.71252727508545
        ],
        "friction_weight_ratio_mean": 0.49354782700538635,
        "normal_vertical_fraction_max": 0.027232011780142784,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.09915847331285477,
        "joint_speed_rms": 1.3861534595489502,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02055640146136284,
        "object_tracking_error_m": 0.03329409658908844,
        "object_tracking_error_rad_max": 0.023987604305148125,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.016520392149686813,
          0.011926506645977497,
          0.2557908892631531,
          0.00900939665734768
        ],
        "steady_command_mae": [
          0.016520392149686813,
          0.011926506645977497,
          0.2557908892631531,
          0.00900939665734768
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.11916891485452652,
        "min_box_clearance_m": 0.5884559750556946,
        "pelvis_amplitude_m": 0.006799757480621338,
        "normal_forces_mean_n": [
          4.748815059661865,
          8.483589172363281
        ],
        "friction_weight_ratio_mean": 0.5059390068054199,
        "normal_vertical_fraction_max": 0.026725420728325844,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1022435873746872,
        "joint_speed_rms": 1.389723777770996,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.020618712529540062,
        "object_tracking_error_m": 0.032929129898548126,
        "object_tracking_error_rad_max": 0.025291379541158676,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      }
    ],
    "goal_limits": {
      "height_low": 0.6068800687789917,
      "height_high": 0.7268800735473633,
      "height_rate": 0.11247000098228455,
      "vx_high": 0.0,
      "forward_admitted": false,
      "reference_fps": 50,
      "episode_seconds": 30.0
    },
    "reference_free": false,
    "terminal_state_before_reset": true,
    "physical_model": {
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
      "control": "PPO joint-position offsets with PD each physics substep; no P0 feedforward or WBC"
    },
    "accepted_policy": false,
    "motion_quality": {
      "clip_0_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.09418580681085587,
          "lower_body_style_rmse_rad": 0.08014652132987976,
          "reference_compatibility_mean": 0.8449958280461999,
          "joint_acceleration_rms_rad_s2": 56.63563919067383,
          "box_relative_translation_drift_max_m": 0.03483263113515009,
          "box_relative_rotation_drift_max_rad": 0.06007923964558195
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.09411722421646118,
          "lower_body_style_rmse_rad": 0.08018938452005386,
          "reference_compatibility_mean": 0.8422286199669113,
          "joint_acceleration_rms_rad_s2": 56.95589065551758,
          "box_relative_translation_drift_max_m": 0.0360143209134871,
          "box_relative_rotation_drift_max_rad": 0.06214154952699419
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.09418613463640213,
          "lower_body_style_rmse_rad": 0.0785161703824997,
          "reference_compatibility_mean": 0.8463156649714871,
          "joint_acceleration_rms_rad_s2": 56.68478012084961,
          "box_relative_translation_drift_max_m": 0.034678164931716424,
          "box_relative_rotation_drift_max_rad": 0.05762058435689468
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.09473688900470734,
          "lower_body_style_rmse_rad": 0.08047108352184296,
          "reference_compatibility_mean": 0.8385200076809088,
          "joint_acceleration_rms_rad_s2": 56.98863220214844,
          "box_relative_translation_drift_max_m": 0.036639531259413424,
          "box_relative_rotation_drift_max_rad": 0.0556236900795041
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.09494820237159729,
          "lower_body_style_rmse_rad": 0.0802159532904625,
          "reference_compatibility_mean": 0.8355674917121577,
          "joint_acceleration_rms_rad_s2": 56.3743896484375,
          "box_relative_translation_drift_max_m": 0.03669401100244888,
          "box_relative_rotation_drift_max_rad": 0.06140476886905047
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.0948118269443512,
          "lower_body_style_rmse_rad": 0.08020610362291336,
          "reference_compatibility_mean": 0.8374946468821214,
          "joint_acceleration_rms_rad_s2": 55.87966537475586,
          "box_relative_translation_drift_max_m": 0.03511464160026636,
          "box_relative_rotation_drift_max_rad": 0.057718220942515004
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.09507322311401367,
          "lower_body_style_rmse_rad": 0.08067014068365097,
          "reference_compatibility_mean": 0.8328490572072393,
          "joint_acceleration_rms_rad_s2": 57.09867858886719,
          "box_relative_translation_drift_max_m": 0.03574943590684765,
          "box_relative_rotation_drift_max_rad": 0.05483892789831749
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.0939895436167717,
          "lower_body_style_rmse_rad": 0.07850857079029083,
          "reference_compatibility_mean": 0.8477834264247524,
          "joint_acceleration_rms_rad_s2": 57.12913131713867,
          "box_relative_translation_drift_max_m": 0.03568933432773704,
          "box_relative_rotation_drift_max_rad": 0.06054905550282334
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.09470835328102112,
          "lower_body_style_rmse_rad": 0.08018212020397186,
          "reference_compatibility_mean": 0.8384070901227478,
          "joint_acceleration_rms_rad_s2": 56.90859603881836,
          "box_relative_translation_drift_max_m": 0.03650817741732428,
          "box_relative_rotation_drift_max_rad": 0.06005958273744299
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.09499478340148926,
          "lower_body_style_rmse_rad": 0.0804307609796524,
          "reference_compatibility_mean": 0.8408584794737193,
          "joint_acceleration_rms_rad_s2": 56.822509765625,
          "box_relative_translation_drift_max_m": 0.03617684134993382,
          "box_relative_rotation_drift_max_rad": 0.06167756271421841
        }
      ],
      "clip_1_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.09400060772895813,
          "lower_body_style_rmse_rad": 0.07845460623502731,
          "reference_compatibility_mean": 0.8491031983012624,
          "joint_acceleration_rms_rad_s2": 56.53070831298828,
          "box_relative_translation_drift_max_m": 0.03431299297353861,
          "box_relative_rotation_drift_max_rad": 0.05778760579569427
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.09424236416816711,
          "lower_body_style_rmse_rad": 0.08022487163543701,
          "reference_compatibility_mean": 0.8385525031189843,
          "joint_acceleration_rms_rad_s2": 57.338016510009766,
          "box_relative_translation_drift_max_m": 0.03594023009757873,
          "box_relative_rotation_drift_max_rad": 0.06171015076694998
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.09422413259744644,
          "lower_body_style_rmse_rad": 0.08015141636133194,
          "reference_compatibility_mean": 0.8447402160535897,
          "joint_acceleration_rms_rad_s2": 56.76415252685547,
          "box_relative_translation_drift_max_m": 0.03466352614028358,
          "box_relative_rotation_drift_max_rad": 0.05762200408381073
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.09473443031311035,
          "lower_body_style_rmse_rad": 0.08046065270900726,
          "reference_compatibility_mean": 0.8386225547096204,
          "joint_acceleration_rms_rad_s2": 56.97734451293945,
          "box_relative_translation_drift_max_m": 0.036719503156906974,
          "box_relative_rotation_drift_max_rad": 0.056106072399803926
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.09498657286167145,
          "lower_body_style_rmse_rad": 0.0802278146147728,
          "reference_compatibility_mean": 0.835047827720613,
          "joint_acceleration_rms_rad_s2": 56.38440704345703,
          "box_relative_translation_drift_max_m": 0.036690594546705174,
          "box_relative_rotation_drift_max_rad": 0.061419187425554266
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.0947718694806099,
          "lower_body_style_rmse_rad": 0.08018273860216141,
          "reference_compatibility_mean": 0.8373796490507223,
          "joint_acceleration_rms_rad_s2": 56.363590240478516,
          "box_relative_translation_drift_max_m": 0.035262976891045766,
          "box_relative_rotation_drift_max_rad": 0.05597101619630856
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.09507008641958237,
          "lower_body_style_rmse_rad": 0.08066607266664505,
          "reference_compatibility_mean": 0.8330086602994772,
          "joint_acceleration_rms_rad_s2": 57.04839324951172,
          "box_relative_translation_drift_max_m": 0.03576517676837639,
          "box_relative_rotation_drift_max_rad": 0.054822370965796556
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.09384393692016602,
          "lower_body_style_rmse_rad": 0.07845532149076462,
          "reference_compatibility_mean": 0.8494778944083914,
          "joint_acceleration_rms_rad_s2": 56.226051330566406,
          "box_relative_translation_drift_max_m": 0.035439208121692434,
          "box_relative_rotation_drift_max_rad": 0.06301252730563636
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.09473246335983276,
          "lower_body_style_rmse_rad": 0.08019739389419556,
          "reference_compatibility_mean": 0.8378381283402122,
          "joint_acceleration_rms_rad_s2": 56.94939422607422,
          "box_relative_translation_drift_max_m": 0.03649514347165617,
          "box_relative_rotation_drift_max_rad": 0.060027243689935096
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.09499136358499527,
          "lower_body_style_rmse_rad": 0.08042746782302856,
          "reference_compatibility_mean": 0.8406008678085748,
          "joint_acceleration_rms_rad_s2": 56.91020202636719,
          "box_relative_translation_drift_max_m": 0.036173982002322386,
          "box_relative_rotation_drift_max_rad": 0.06165282605248557
        }
      ]
    },
    "directory": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795222066333557483",
    "checkpoint": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/dashboard/stage1/WholeBodyTracking/20261120_224707-stage1-locomotion/model_04499.pt",
    "final": false,
    "selection_score": 0.009988462401983832,
    "failure_counts": {
      "physical_failure/loss_of_grasp": 20,
      "incomplete_episode": 20,
      "contact_interruption": 20,
      "hand_slip": 20,
      "insufficient_friction_support": 20,
      "contact_near_box_bottom": 20
    },
    "scenarios": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "completed_updates": 4500
  },
  {
    "passed": false,
    "score": 0.0,
    "suite": "stage1",
    "groups": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "trials": [
      {
        "scenario": "clip_0",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02428818680346012,
          0.014989381656050682,
          0.24132902920246124,
          0.012285685166716576
        ],
        "steady_command_mae": [
          0.02428818680346012,
          0.014989381656050682,
          0.24132902920246124,
          0.012285685166716576
        ],
        "contact_continuity": 0.05000000074505806,
        "max_hand_slip_m": 0.11861641705036163,
        "min_box_clearance_m": 0.5881714820861816,
        "pelvis_amplitude_m": 0.010579943656921387,
        "normal_forces_mean_n": [
          5.6916728019714355,
          8.371442794799805
        ],
        "friction_weight_ratio_mean": 0.46737366914749146,
        "normal_vertical_fraction_max": 0.025684449821710587,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11209873110055923,
        "joint_speed_rms": 1.446961760520935,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022031279280781746,
        "object_tracking_error_m": 0.031533923000097275,
        "object_tracking_error_rad_max": 0.0331222340464592,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.022640246897935867,
          0.015011454932391644,
          0.25740760564804077,
          0.012355041690170765
        ],
        "steady_command_mae": [
          0.022640246897935867,
          0.015011454932391644,
          0.25740760564804077,
          0.012355041690170765
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.11934003233909607,
        "min_box_clearance_m": 0.5893410444259644,
        "pelvis_amplitude_m": 0.010615944862365723,
        "normal_forces_mean_n": [
          5.980307579040527,
          8.577142715454102
        ],
        "friction_weight_ratio_mean": 0.49861449003219604,
        "normal_vertical_fraction_max": 0.025043543428182602,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10943013429641724,
        "joint_speed_rms": 1.4483997821807861,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022069348022341728,
        "object_tracking_error_m": 0.03157161921262741,
        "object_tracking_error_rad_max": 0.028061145916581154,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.021464385092258453,
          0.014301443472504616,
          0.26593032479286194,
          0.01212373934686184
        ],
        "steady_command_mae": [
          0.021464385092258453,
          0.014301443472504616,
          0.26593032479286194,
          0.01212373934686184
        ],
        "contact_continuity": 0.08000000566244125,
        "max_hand_slip_m": 0.11743860691785812,
        "min_box_clearance_m": 0.5899149179458618,
        "pelvis_amplitude_m": 0.01031351089477539,
        "normal_forces_mean_n": [
          6.4430742263793945,
          8.90522575378418
        ],
        "friction_weight_ratio_mean": 0.5259761810302734,
        "normal_vertical_fraction_max": 0.025183329358696938,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10692869126796722,
        "joint_speed_rms": 1.4309451580047607,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021934837102890015,
        "object_tracking_error_m": 0.03150224685668945,
        "object_tracking_error_rad_max": 0.027963804081082344,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.020813729614019394,
          0.01514747180044651,
          0.2686527371406555,
          0.012466144748032093
        ],
        "steady_command_mae": [
          0.020813729614019394,
          0.01514747180044651,
          0.2686527371406555,
          0.012466144748032093
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.12112981826066971,
        "min_box_clearance_m": 0.5878658890724182,
        "pelvis_amplitude_m": 0.010622382164001465,
        "normal_forces_mean_n": [
          6.461613655090332,
          8.543473243713379
        ],
        "friction_weight_ratio_mean": 0.5231255888938904,
        "normal_vertical_fraction_max": 0.01834748685359955,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10885299742221832,
        "joint_speed_rms": 1.451999306678772,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02213793247938156,
        "object_tracking_error_m": 0.034004729241132736,
        "object_tracking_error_rad_max": 0.017308946698904037,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.022618550807237625,
          0.0144913699477911,
          0.2694009244441986,
          0.01246192492544651
        ],
        "steady_command_mae": [
          0.022618550807237625,
          0.0144913699477911,
          0.2694009244441986,
          0.01246192492544651
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.11957386136054993,
        "min_box_clearance_m": 0.5893580913543701,
        "pelvis_amplitude_m": 0.010635316371917725,
        "normal_forces_mean_n": [
          6.534748077392578,
          8.872541427612305
        ],
        "friction_weight_ratio_mean": 0.5509692430496216,
        "normal_vertical_fraction_max": 0.027419375255703926,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10951592028141022,
        "joint_speed_rms": 1.4380489587783813,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022075995802879333,
        "object_tracking_error_m": 0.03330749273300171,
        "object_tracking_error_rad_max": 0.017271004617214203,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02371555007994175,
          0.014256772585213184,
          0.25702136754989624,
          0.012355005368590355
        ],
        "steady_command_mae": [
          0.02371555007994175,
          0.014256772585213184,
          0.25702136754989624,
          0.012355005368590355
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.1190979853272438,
        "min_box_clearance_m": 0.5886385440826416,
        "pelvis_amplitude_m": 0.01059955358505249,
        "normal_forces_mean_n": [
          6.3066205978393555,
          8.795254707336426
        ],
        "friction_weight_ratio_mean": 0.5280267596244812,
        "normal_vertical_fraction_max": 0.02677796594798565,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11082339286804199,
        "joint_speed_rms": 1.4357844591140747,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02200312539935112,
        "object_tracking_error_m": 0.032975003123283386,
        "object_tracking_error_rad_max": 0.022349493578076363,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.0233589019626379,
          0.014164634048938751,
          0.26301202178001404,
          0.012333107180893421
        ],
        "steady_command_mae": [
          0.0233589019626379,
          0.014164634048938751,
          0.26301202178001404,
          0.012333107180893421
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12030337005853653,
        "min_box_clearance_m": 0.5880084037780762,
        "pelvis_amplitude_m": 0.010617434978485107,
        "normal_forces_mean_n": [
          6.600410461425781,
          8.856454849243164
        ],
        "friction_weight_ratio_mean": 0.5063323378562927,
        "normal_vertical_fraction_max": 0.027439311146736145,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10969652235507965,
        "joint_speed_rms": 1.4348880052566528,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022021491080522537,
        "object_tracking_error_m": 0.033708471804857254,
        "object_tracking_error_rad_max": 0.01825513131916523,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.021475518122315407,
          0.015116957016289234,
          0.24431034922599792,
          0.012243461795151234
        ],
        "steady_command_mae": [
          0.021475518122315407,
          0.015116957016289234,
          0.24431034922599792,
          0.012243461795151234
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.11889474093914032,
        "min_box_clearance_m": 0.5882211327552795,
        "pelvis_amplitude_m": 0.010574042797088623,
        "normal_forces_mean_n": [
          5.938063144683838,
          8.572973251342773
        ],
        "friction_weight_ratio_mean": 0.46643561124801636,
        "normal_vertical_fraction_max": 0.025297271087765694,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11243768036365509,
        "joint_speed_rms": 1.4414081573486328,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02205229550600052,
        "object_tracking_error_m": 0.03160755708813667,
        "object_tracking_error_rad_max": 0.03253506124019623,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.022660065442323685,
          0.01441948302090168,
          0.2618238031864166,
          0.012502479366958141
        ],
        "steady_command_mae": [
          0.022660065442323685,
          0.01441948302090168,
          0.2618238031864166,
          0.012502479366958141
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.1197592094540596,
        "min_box_clearance_m": 0.5894180536270142,
        "pelvis_amplitude_m": 0.010735571384429932,
        "normal_forces_mean_n": [
          6.710123538970947,
          9.055593490600586
        ],
        "friction_weight_ratio_mean": 0.5321747064590454,
        "normal_vertical_fraction_max": 0.02722989208996296,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11063683032989502,
        "joint_speed_rms": 1.4353255033493042,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02217273600399494,
        "object_tracking_error_m": 0.03308352828025818,
        "object_tracking_error_rad_max": 0.017544617876410484,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.022513497620821,
          0.015048357658088207,
          0.24735626578330994,
          0.012420654296875
        ],
        "steady_command_mae": [
          0.022513497620821,
          0.015048357658088207,
          0.24735626578330994,
          0.012420654296875
        ],
        "contact_continuity": 0.09000001102685928,
        "max_hand_slip_m": 0.12108304351568222,
        "min_box_clearance_m": 0.589321494102478,
        "pelvis_amplitude_m": 0.0108184814453125,
        "normal_forces_mean_n": [
          6.339590549468994,
          8.762776374816895
        ],
        "friction_weight_ratio_mean": 0.5097810626029968,
        "normal_vertical_fraction_max": 0.02673540636897087,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11269064247608185,
        "joint_speed_rms": 1.448664665222168,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022388365119695663,
        "object_tracking_error_m": 0.03282812237739563,
        "object_tracking_error_rad_max": 0.019392309710383415,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.024288270622491837,
          0.014985625632107258,
          0.24257779121398926,
          0.012292802333831787
        ],
        "steady_command_mae": [
          0.024288270622491837,
          0.014985625632107258,
          0.24257779121398926,
          0.012292802333831787
        ],
        "contact_continuity": 0.05000000074505806,
        "max_hand_slip_m": 0.1187688559293747,
        "min_box_clearance_m": 0.5881530046463013,
        "pelvis_amplitude_m": 0.010594427585601807,
        "normal_forces_mean_n": [
          5.776925086975098,
          8.428449630737305
        ],
        "friction_weight_ratio_mean": 0.4592558741569519,
        "normal_vertical_fraction_max": 0.025684449821710587,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11154882609844208,
        "joint_speed_rms": 1.44511878490448,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022037316113710403,
        "object_tracking_error_m": 0.0315437912940979,
        "object_tracking_error_rad_max": 0.032960955053567886,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02263135090470314,
          0.015183274634182453,
          0.25638678669929504,
          0.012361085042357445
        ],
        "steady_command_mae": [
          0.02263135090470314,
          0.015183274634182453,
          0.25638678669929504,
          0.012361085042357445
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.11941300332546234,
        "min_box_clearance_m": 0.5893537998199463,
        "pelvis_amplitude_m": 0.010625898838043213,
        "normal_forces_mean_n": [
          5.988300323486328,
          8.580403327941895
        ],
        "friction_weight_ratio_mean": 0.49883532524108887,
        "normal_vertical_fraction_max": 0.025043543428182602,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10894818603992462,
        "joint_speed_rms": 1.447938323020935,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022074248641729355,
        "object_tracking_error_m": 0.03157183527946472,
        "object_tracking_error_rad_max": 0.027980247512459755,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.021300695836544037,
          0.01528245210647583,
          0.2565752863883972,
          0.012312555685639381
        ],
        "steady_command_mae": [
          0.021300695836544037,
          0.01528245210647583,
          0.2565752863883972,
          0.012312555685639381
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.11904094368219376,
        "min_box_clearance_m": 0.5888465642929077,
        "pelvis_amplitude_m": 0.010622262954711914,
        "normal_forces_mean_n": [
          6.1228837966918945,
          8.707529067993164
        ],
        "friction_weight_ratio_mean": 0.49077892303466797,
        "normal_vertical_fraction_max": 0.025183329358696938,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10914790630340576,
        "joint_speed_rms": 1.441062331199646,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022170081734657288,
        "object_tracking_error_m": 0.031682245433330536,
        "object_tracking_error_rad_max": 0.030205631628632545,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.020854061469435692,
          0.015035321936011314,
          0.26837676763534546,
          0.012464511208236217
        ],
        "steady_command_mae": [
          0.020854061469435692,
          0.015035321936011314,
          0.26837676763534546,
          0.012464511208236217
        ],
        "contact_continuity": 0.1300000250339508,
        "max_hand_slip_m": 0.12145400792360306,
        "min_box_clearance_m": 0.5879389047622681,
        "pelvis_amplitude_m": 0.010619282722473145,
        "normal_forces_mean_n": [
          6.639961242675781,
          8.684926986694336
        ],
        "friction_weight_ratio_mean": 0.5150169134140015,
        "normal_vertical_fraction_max": 0.018863648176193237,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10871119797229767,
        "joint_speed_rms": 1.4508317708969116,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022138496860861778,
        "object_tracking_error_m": 0.034013550728559494,
        "object_tracking_error_rad_max": 0.016271954402327538,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.022617030888795853,
          0.014536556787788868,
          0.26904886960983276,
          0.012491405010223389
        ],
        "steady_command_mae": [
          0.022617030888795853,
          0.014536556787788868,
          0.26904886960983276,
          0.012491405010223389
        ],
        "contact_continuity": 0.11000001430511475,
        "max_hand_slip_m": 0.11982841044664383,
        "min_box_clearance_m": 0.58927321434021,
        "pelvis_amplitude_m": 0.010684788227081299,
        "normal_forces_mean_n": [
          6.56008243560791,
          8.846277236938477
        ],
        "friction_weight_ratio_mean": 0.5487062931060791,
        "normal_vertical_fraction_max": 0.027419375255703926,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.10993915796279907,
        "joint_speed_rms": 1.4370194673538208,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.0221149530261755,
        "object_tracking_error_m": 0.033315908163785934,
        "object_tracking_error_rad_max": 0.01759159006178379,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.023654770106077194,
          0.01448045950382948,
          0.25824421644210815,
          0.012375366874039173
        ],
        "steady_command_mae": [
          0.023654770106077194,
          0.01448045950382948,
          0.25824421644210815,
          0.012375366874039173
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.11907199770212173,
        "min_box_clearance_m": 0.5886749625205994,
        "pelvis_amplitude_m": 0.010635912418365479,
        "normal_forces_mean_n": [
          6.4273223876953125,
          8.825758934020996
        ],
        "friction_weight_ratio_mean": 0.5242399573326111,
        "normal_vertical_fraction_max": 0.02677796594798565,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11086126416921616,
        "joint_speed_rms": 1.432273030281067,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022025397047400475,
        "object_tracking_error_m": 0.032962433993816376,
        "object_tracking_error_rad_max": 0.022588709369301796,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02334021031856537,
          0.014354512095451355,
          0.2608064115047455,
          0.012385403737425804
        ],
        "steady_command_mae": [
          0.02334021031856537,
          0.014354512095451355,
          0.2608064115047455,
          0.012385403737425804
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12067833542823792,
        "min_box_clearance_m": 0.5879757404327393,
        "pelvis_amplitude_m": 0.01070404052734375,
        "normal_forces_mean_n": [
          6.553764343261719,
          8.822224617004395
        ],
        "friction_weight_ratio_mean": 0.5017579197883606,
        "normal_vertical_fraction_max": 0.027439311146736145,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11016805469989777,
        "joint_speed_rms": 1.4372910261154175,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022085921838879585,
        "object_tracking_error_m": 0.03371652588248253,
        "object_tracking_error_rad_max": 0.01830713450908661,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.021436315029859543,
          0.015285479836165905,
          0.2438811957836151,
          0.012255323119461536
        ],
        "steady_command_mae": [
          0.021436315029859543,
          0.015285479836165905,
          0.2438811957836151,
          0.012255323119461536
        ],
        "contact_continuity": 0.06000000238418579,
        "max_hand_slip_m": 0.11917994916439056,
        "min_box_clearance_m": 0.5885434746742249,
        "pelvis_amplitude_m": 0.010591328144073486,
        "normal_forces_mean_n": [
          5.933036804199219,
          8.5657958984375
        ],
        "friction_weight_ratio_mean": 0.474248468875885,
        "normal_vertical_fraction_max": 0.025297271087765694,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1125255823135376,
        "joint_speed_rms": 1.4423236846923828,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022066738456487656,
        "object_tracking_error_m": 0.03157873451709747,
        "object_tracking_error_rad_max": 0.03133797645568848,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.02247525379061699,
          0.015792744234204292,
          0.2560400068759918,
          0.012666893191635609
        ],
        "steady_command_mae": [
          0.02247525379061699,
          0.015792744234204292,
          0.2560400068759918,
          0.012666893191635609
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12046080082654953,
        "min_box_clearance_m": 0.5893349051475525,
        "pelvis_amplitude_m": 0.011003375053405762,
        "normal_forces_mean_n": [
          6.375094413757324,
          8.769933700561523
        ],
        "friction_weight_ratio_mean": 0.5339409112930298,
        "normal_vertical_fraction_max": 0.02722989208996296,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1127486601471901,
        "joint_speed_rms": 1.4455516338348389,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02237834595143795,
        "object_tracking_error_m": 0.03308950737118721,
        "object_tracking_error_rad_max": 0.019012780860066414,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.022387761622667313,
          0.01524420641362667,
          0.2527354657649994,
          0.012280857190489769
        ],
        "steady_command_mae": [
          0.022387761622667313,
          0.01524420641362667,
          0.2527354657649994,
          0.012280857190489769
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.11972536891698837,
        "min_box_clearance_m": 0.5896320343017578,
        "pelvis_amplitude_m": 0.010594069957733154,
        "normal_forces_mean_n": [
          6.283374309539795,
          8.730198860168457
        ],
        "friction_weight_ratio_mean": 0.5382202863693237,
        "normal_vertical_fraction_max": 0.02673540636897087,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11119663715362549,
        "joint_speed_rms": 1.4424874782562256,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.022202732041478157,
        "object_tracking_error_m": 0.03278098627924919,
        "object_tracking_error_rad_max": 0.019152771681547165,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      }
    ],
    "goal_limits": {
      "height_low": 0.6068800687789917,
      "height_high": 0.7268800735473633,
      "height_rate": 0.11247000098228455,
      "vx_high": 0.0,
      "forward_admitted": false,
      "reference_fps": 50,
      "episode_seconds": 30.0
    },
    "reference_free": false,
    "terminal_state_before_reset": true,
    "physical_model": {
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
      "control": "PPO joint-position offsets with PD each physics substep; no P0 feedforward or WBC"
    },
    "accepted_policy": false,
    "motion_quality": {
      "clip_0_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.09874150156974792,
          "lower_body_style_rmse_rad": 0.0959266871213913,
          "reference_compatibility_mean": 0.6363791902757029,
          "joint_acceleration_rms_rad_s2": 59.58608627319336,
          "box_relative_translation_drift_max_m": 0.03314759387061163,
          "box_relative_rotation_drift_max_rad": 0.060760640921215664
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.09871769696474075,
          "lower_body_style_rmse_rad": 0.09523235261440277,
          "reference_compatibility_mean": 0.6368817052162336,
          "joint_acceleration_rms_rad_s2": 60.19906997680664,
          "box_relative_translation_drift_max_m": 0.03287973090428203,
          "box_relative_rotation_drift_max_rad": 0.05569058468502436
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.09823205322027206,
          "lower_body_style_rmse_rad": 0.09448020160198212,
          "reference_compatibility_mean": 0.6488884456545219,
          "joint_acceleration_rms_rad_s2": 58.23128890991211,
          "box_relative_translation_drift_max_m": 0.03279442843770626,
          "box_relative_rotation_drift_max_rad": 0.05701977508411719
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.09872220456600189,
          "lower_body_style_rmse_rad": 0.09485328942537308,
          "reference_compatibility_mean": 0.6417187052108119,
          "joint_acceleration_rms_rad_s2": 60.704036712646484,
          "box_relative_translation_drift_max_m": 0.03521948991363849,
          "box_relative_rotation_drift_max_rad": 0.05459699574800964
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.09886150062084198,
          "lower_body_style_rmse_rad": 0.09504920989274979,
          "reference_compatibility_mean": 0.6393449768810815,
          "joint_acceleration_rms_rad_s2": 58.129459381103516,
          "box_relative_translation_drift_max_m": 0.03386302094196484,
          "box_relative_rotation_drift_max_rad": 0.05412080276329279
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.0988282710313797,
          "lower_body_style_rmse_rad": 0.09504223614931107,
          "reference_compatibility_mean": 0.6381716527165555,
          "joint_acceleration_rms_rad_s2": 57.763736724853516,
          "box_relative_translation_drift_max_m": 0.03410826123323718,
          "box_relative_rotation_drift_max_rad": 0.05786224636384573
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.09879080951213837,
          "lower_body_style_rmse_rad": 0.09543541818857193,
          "reference_compatibility_mean": 0.639484620056322,
          "joint_acceleration_rms_rad_s2": 58.0561637878418,
          "box_relative_translation_drift_max_m": 0.03483544355422907,
          "box_relative_rotation_drift_max_rad": 0.05564754676533931
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.09864845871925354,
          "lower_body_style_rmse_rad": 0.09595590084791183,
          "reference_compatibility_mean": 0.6371323263494432,
          "joint_acceleration_rms_rad_s2": 59.2296257019043,
          "box_relative_translation_drift_max_m": 0.033641113802859064,
          "box_relative_rotation_drift_max_rad": 0.05996859021263151
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.09859149158000946,
          "lower_body_style_rmse_rad": 0.09517169743776321,
          "reference_compatibility_mean": 0.633797877796721,
          "joint_acceleration_rms_rad_s2": 58.02432632446289,
          "box_relative_translation_drift_max_m": 0.0336301584249952,
          "box_relative_rotation_drift_max_rad": 0.052532191164769274
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.0994972363114357,
          "lower_body_style_rmse_rad": 0.09557846933603287,
          "reference_compatibility_mean": 0.6304465810499624,
          "joint_acceleration_rms_rad_s2": 58.720096588134766,
          "box_relative_translation_drift_max_m": 0.03339841646047181,
          "box_relative_rotation_drift_max_rad": 0.053465178828948176
        }
      ],
      "clip_1_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.09873007982969284,
          "lower_body_style_rmse_rad": 0.09592034667730331,
          "reference_compatibility_mean": 0.636006611227912,
          "joint_acceleration_rms_rad_s2": 59.4461669921875,
          "box_relative_translation_drift_max_m": 0.033165339438536626,
          "box_relative_rotation_drift_max_rad": 0.06041702908339844
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.09872520714998245,
          "lower_body_style_rmse_rad": 0.09522853046655655,
          "reference_compatibility_mean": 0.636781413345964,
          "joint_acceleration_rms_rad_s2": 60.18624496459961,
          "box_relative_translation_drift_max_m": 0.03285496361269831,
          "box_relative_rotation_drift_max_rad": 0.05552004730267571
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.09874261170625687,
          "lower_body_style_rmse_rad": 0.09536014497280121,
          "reference_compatibility_mean": 0.6366987726838658,
          "joint_acceleration_rms_rad_s2": 58.94895935058594,
          "box_relative_translation_drift_max_m": 0.03320746074143276,
          "box_relative_rotation_drift_max_rad": 0.0584474260311562
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.09869890660047531,
          "lower_body_style_rmse_rad": 0.0948580875992775,
          "reference_compatibility_mean": 0.6419883462151359,
          "joint_acceleration_rms_rad_s2": 60.520103454589844,
          "box_relative_translation_drift_max_m": 0.035261821771555416,
          "box_relative_rotation_drift_max_rad": 0.053550840953062055
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.0989927127957344,
          "lower_body_style_rmse_rad": 0.09506805986166,
          "reference_compatibility_mean": 0.6373706072026776,
          "joint_acceleration_rms_rad_s2": 57.9517707824707,
          "box_relative_translation_drift_max_m": 0.03385493177358372,
          "box_relative_rotation_drift_max_rad": 0.054241012244298184
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.09889234602451324,
          "lower_body_style_rmse_rad": 0.095246821641922,
          "reference_compatibility_mean": 0.6369621211867994,
          "joint_acceleration_rms_rad_s2": 57.38284683227539,
          "box_relative_translation_drift_max_m": 0.03402306704416483,
          "box_relative_rotation_drift_max_rad": 0.05806693167138005
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.09892185777425766,
          "lower_body_style_rmse_rad": 0.09545135498046875,
          "reference_compatibility_mean": 0.6361843263294938,
          "joint_acceleration_rms_rad_s2": 58.21357345581055,
          "box_relative_translation_drift_max_m": 0.034753419155427095,
          "box_relative_rotation_drift_max_rad": 0.055309850976504246
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.0986887663602829,
          "lower_body_style_rmse_rad": 0.09537699818611145,
          "reference_compatibility_mean": 0.6371996095337628,
          "joint_acceleration_rms_rad_s2": 59.28016662597656,
          "box_relative_translation_drift_max_m": 0.03345151393816789,
          "box_relative_rotation_drift_max_rad": 0.05878868494026451
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.09916343539953232,
          "lower_body_style_rmse_rad": 0.09610174596309662,
          "reference_compatibility_mean": 0.6233289927210127,
          "joint_acceleration_rms_rad_s2": 58.57809829711914,
          "box_relative_translation_drift_max_m": 0.03332782604636687,
          "box_relative_rotation_drift_max_rad": 0.05399615349746287
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.09911441057920456,
          "lower_body_style_rmse_rad": 0.09551987797021866,
          "reference_compatibility_mean": 0.6391205105299017,
          "joint_acceleration_rms_rad_s2": 58.3778190612793,
          "box_relative_translation_drift_max_m": 0.03346071459768781,
          "box_relative_rotation_drift_max_rad": 0.05438368662058178
        }
      ]
    },
    "directory": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795229296945062893",
    "checkpoint": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/dashboard/stage1/WholeBodyTracking/20261121_004805-stage1-locomotion/model_04999.pt",
    "final": false,
    "selection_score": 0.010338462422100398,
    "failure_counts": {
      "physical_failure/loss_of_grasp": 20,
      "incomplete_episode": 20,
      "contact_interruption": 20,
      "hand_slip": 20,
      "insufficient_friction_support": 20,
      "contact_near_box_bottom": 20
    },
    "scenarios": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "completed_updates": 5000
  },
  {
    "passed": false,
    "score": 0.0,
    "suite": "stage1",
    "groups": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "trials": [
      {
        "scenario": "clip_0",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.01874137483537197,
          0.030061090365052223,
          0.20176856219768524,
          0.012036013416945934
        ],
        "steady_command_mae": [
          0.01874137483537197,
          0.030061090365052223,
          0.20176856219768524,
          0.012036013416945934
        ],
        "contact_continuity": 0.03999999910593033,
        "max_hand_slip_m": 0.11798594146966934,
        "min_box_clearance_m": 0.5895888805389404,
        "pelvis_amplitude_m": 0.010477721691131592,
        "normal_forces_mean_n": [
          5.7873921394348145,
          8.537501335144043
        ],
        "friction_weight_ratio_mean": 0.4919000267982483,
        "normal_vertical_fraction_max": 0.02573559619486332,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12312760204076767,
        "joint_speed_rms": 1.435508131980896,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02150592766702175,
        "object_tracking_error_m": 0.03126842901110649,
        "object_tracking_error_rad_max": 0.02933366410434246,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.016334425657987595,
          0.028881724923849106,
          0.2078697383403778,
          0.012150978669524193
        ],
        "steady_command_mae": [
          0.016334425657987595,
          0.028881724923849106,
          0.2078697383403778,
          0.012150978669524193
        ],
        "contact_continuity": 0.05000000074505806,
        "max_hand_slip_m": 0.1171155497431755,
        "min_box_clearance_m": 0.5901045799255371,
        "pelvis_amplitude_m": 0.010574579238891602,
        "normal_forces_mean_n": [
          5.579116344451904,
          8.315252304077148
        ],
        "friction_weight_ratio_mean": 0.5478769540786743,
        "normal_vertical_fraction_max": 0.025088990107178688,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1203695684671402,
        "joint_speed_rms": 1.4327545166015625,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021567996591329575,
        "object_tracking_error_m": 0.03136304393410683,
        "object_tracking_error_rad_max": 0.027890410274267197,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.014778132550418377,
          0.033503204584121704,
          0.1844865083694458,
          0.012091636657714844
        ],
        "steady_command_mae": [
          0.014778132550418377,
          0.033503204584121704,
          0.1844865083694458,
          0.012091636657714844
        ],
        "contact_continuity": 0.05000000074505806,
        "max_hand_slip_m": 0.11833055317401886,
        "min_box_clearance_m": 0.5896172523498535,
        "pelvis_amplitude_m": 0.010470569133758545,
        "normal_forces_mean_n": [
          5.968878746032715,
          8.621996879577637
        ],
        "friction_weight_ratio_mean": 0.49986523389816284,
        "normal_vertical_fraction_max": 0.02523774467408657,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12409726530313492,
        "joint_speed_rms": 1.4338386058807373,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021680064499378204,
        "object_tracking_error_m": 0.031531427055597305,
        "object_tracking_error_rad_max": 0.027321109548211098,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.015313535928726196,
          0.030021730810403824,
          0.2033965289592743,
          0.012390983290970325
        ],
        "steady_command_mae": [
          0.015313535928726196,
          0.030021730810403824,
          0.2033965289592743,
          0.012390983290970325
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12219838798046112,
        "min_box_clearance_m": 0.5883790254592896,
        "pelvis_amplitude_m": 0.010777771472930908,
        "normal_forces_mean_n": [
          6.325139999389648,
          8.561767578125
        ],
        "friction_weight_ratio_mean": 0.5058482885360718,
        "normal_vertical_fraction_max": 0.020986447110772133,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12240336090326309,
        "joint_speed_rms": 1.432031512260437,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021804004907608032,
        "object_tracking_error_m": 0.03391360491514206,
        "object_tracking_error_rad_max": 0.01538755465298891,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.018373075872659683,
          0.027939409017562866,
          0.20619530975818634,
          0.012417006306350231
        ],
        "steady_command_mae": [
          0.018373075872659683,
          0.027939409017562866,
          0.20619530975818634,
          0.012417006306350231
        ],
        "contact_continuity": 0.08000000566244125,
        "max_hand_slip_m": 0.12015974521636963,
        "min_box_clearance_m": 0.5888708829879761,
        "pelvis_amplitude_m": 0.010891973972320557,
        "normal_forces_mean_n": [
          6.357710838317871,
          8.838034629821777
        ],
        "friction_weight_ratio_mean": 0.5071629285812378,
        "normal_vertical_fraction_max": 0.027426211163401604,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1220085620880127,
        "joint_speed_rms": 1.4332518577575684,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02174651063978672,
        "object_tracking_error_m": 0.03331290930509567,
        "object_tracking_error_rad_max": 0.020474469289183617,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.019176941365003586,
          0.02728160098195076,
          0.19674988090991974,
          0.012299001216888428
        ],
        "steady_command_mae": [
          0.019176941365003586,
          0.02728160098195076,
          0.19674988090991974,
          0.012299001216888428
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.1195649653673172,
        "min_box_clearance_m": 0.587671160697937,
        "pelvis_amplitude_m": 0.01077336072921753,
        "normal_forces_mean_n": [
          6.209864139556885,
          8.770370483398438
        ],
        "friction_weight_ratio_mean": 0.4709387719631195,
        "normal_vertical_fraction_max": 0.02678491361439228,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12406709045171738,
        "joint_speed_rms": 1.432138204574585,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.0216542836278677,
        "object_tracking_error_m": 0.033066146075725555,
        "object_tracking_error_rad_max": 0.024055510759353638,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.019059693440794945,
          0.029318958520889282,
          0.18917030096054077,
          0.012310671620070934
        ],
        "steady_command_mae": [
          0.019059693440794945,
          0.029318958520889282,
          0.18917030096054077,
          0.012310671620070934
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.12107862532138824,
        "min_box_clearance_m": 0.5875518918037415,
        "pelvis_amplitude_m": 0.01087278127670288,
        "normal_forces_mean_n": [
          6.1626081466674805,
          8.59853458404541
        ],
        "friction_weight_ratio_mean": 0.47479382157325745,
        "normal_vertical_fraction_max": 0.027439309284090996,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12186304479837418,
        "joint_speed_rms": 1.4347541332244873,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02170237898826599,
        "object_tracking_error_m": 0.03372956067323685,
        "object_tracking_error_rad_max": 0.020537197589874268,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.015663539990782738,
          0.03242003172636032,
          0.19030852615833282,
          0.01205453835427761
        ],
        "steady_command_mae": [
          0.015663539990782738,
          0.03242003172636032,
          0.19030852615833282,
          0.01205453835427761
        ],
        "contact_continuity": 0.03999999910593033,
        "max_hand_slip_m": 0.11825330555438995,
        "min_box_clearance_m": 0.5897248983383179,
        "pelvis_amplitude_m": 0.01046973466873169,
        "normal_forces_mean_n": [
          5.718306541442871,
          8.47662353515625
        ],
        "friction_weight_ratio_mean": 0.5003270506858826,
        "normal_vertical_fraction_max": 0.02534523233771324,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12388672679662704,
        "joint_speed_rms": 1.4355452060699463,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021592125296592712,
        "object_tracking_error_m": 0.0313442163169384,
        "object_tracking_error_rad_max": 0.027724387124180794,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.017793335020542145,
          0.03140973672270775,
          0.2045786827802658,
          0.012394380755722523
        ],
        "steady_command_mae": [
          0.017793335020542145,
          0.03140973672270775,
          0.2045786827802658,
          0.012394380755722523
        ],
        "contact_continuity": 0.08000000566244125,
        "max_hand_slip_m": 0.11975832283496857,
        "min_box_clearance_m": 0.5892634391784668,
        "pelvis_amplitude_m": 0.010832369327545166,
        "normal_forces_mean_n": [
          6.329281806945801,
          8.827484130859375
        ],
        "friction_weight_ratio_mean": 0.510442852973938,
        "normal_vertical_fraction_max": 0.027239376679062843,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12215955555438995,
        "joint_speed_rms": 1.434064507484436,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021808307617902756,
        "object_tracking_error_m": 0.033019550144672394,
        "object_tracking_error_rad_max": 0.020749356597661972,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_0",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.017314303666353226,
          0.03258020430803299,
          0.17281892895698547,
          0.01221402920782566
        ],
        "steady_command_mae": [
          0.017314303666353226,
          0.03258020430803299,
          0.17281892895698547,
          0.01221402920782566
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.12046933174133301,
        "min_box_clearance_m": 0.5898703932762146,
        "pelvis_amplitude_m": 0.010707616806030273,
        "normal_forces_mean_n": [
          6.258011817932129,
          8.754576683044434
        ],
        "friction_weight_ratio_mean": 0.5094625353813171,
        "normal_vertical_fraction_max": 0.026761336252093315,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.1270231008529663,
        "joint_speed_rms": 1.4356471300125122,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021854493767023087,
        "object_tracking_error_m": 0.03270329535007477,
        "object_tracking_error_rad_max": 0.018950266763567924,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1000,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.01853693090379238,
          0.03147707134485245,
          0.1997244656085968,
          0.012080681510269642
        ],
        "steady_command_mae": [
          0.01853693090379238,
          0.03147707134485245,
          0.1997244656085968,
          0.012080681510269642
        ],
        "contact_continuity": 0.03999999910593033,
        "max_hand_slip_m": 0.11901840567588806,
        "min_box_clearance_m": 0.5898236036300659,
        "pelvis_amplitude_m": 0.010569512844085693,
        "normal_forces_mean_n": [
          5.494641304016113,
          8.293180465698242
        ],
        "friction_weight_ratio_mean": 0.4968017637729645,
        "normal_vertical_fraction_max": 0.02573559619486332,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12255358695983887,
        "joint_speed_rms": 1.4379338026046753,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021590786054730415,
        "object_tracking_error_m": 0.031276702880859375,
        "object_tracking_error_rad_max": 0.028038332238793373,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1001,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.01709951087832451,
          0.028525790199637413,
          0.2085292637348175,
          0.012199973687529564
        ],
        "steady_command_mae": [
          0.01709951087832451,
          0.028525790199637413,
          0.2085292637348175,
          0.012199973687529564
        ],
        "contact_continuity": 0.03999999910593033,
        "max_hand_slip_m": 0.1191016286611557,
        "min_box_clearance_m": 0.5900274515151978,
        "pelvis_amplitude_m": 0.010664582252502441,
        "normal_forces_mean_n": [
          5.71195650100708,
          8.46380615234375
        ],
        "friction_weight_ratio_mean": 0.49701470136642456,
        "normal_vertical_fraction_max": 0.025088990107178688,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.11997328698635101,
        "joint_speed_rms": 1.4328705072402954,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021660882979631424,
        "object_tracking_error_m": 0.03143676370382309,
        "object_tracking_error_rad_max": 0.025818463414907455,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1002,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.014661120250821114,
          0.03347467631101608,
          0.18402746319770813,
          0.012087583541870117
        ],
        "steady_command_mae": [
          0.014661120250821114,
          0.03347467631101608,
          0.18402746319770813,
          0.012087583541870117
        ],
        "contact_continuity": 0.05000000074505806,
        "max_hand_slip_m": 0.11836694926023483,
        "min_box_clearance_m": 0.5896480083465576,
        "pelvis_amplitude_m": 0.010463714599609375,
        "normal_forces_mean_n": [
          5.9770307540893555,
          8.621283531188965
        ],
        "friction_weight_ratio_mean": 0.499626487493515,
        "normal_vertical_fraction_max": 0.02523774467408657,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12432374060153961,
        "joint_speed_rms": 1.4338024854660034,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021677058190107346,
        "object_tracking_error_m": 0.031528789550065994,
        "object_tracking_error_rad_max": 0.02718651480972767,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1003,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.014938689768314362,
          0.03065483272075653,
          0.19978389143943787,
          0.012391233816742897
        ],
        "steady_command_mae": [
          0.014938689768314362,
          0.03065483272075653,
          0.19978389143943787,
          0.012391233816742897
        ],
        "contact_continuity": 0.10000000894069672,
        "max_hand_slip_m": 0.12220703810453415,
        "min_box_clearance_m": 0.5883786678314209,
        "pelvis_amplitude_m": 0.010776281356811523,
        "normal_forces_mean_n": [
          6.360515117645264,
          8.587423324584961
        ],
        "friction_weight_ratio_mean": 0.5060815215110779,
        "normal_vertical_fraction_max": 0.020987670868635178,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12270717322826385,
        "joint_speed_rms": 1.4322490692138672,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02180434949696064,
        "object_tracking_error_m": 0.033912498503923416,
        "object_tracking_error_rad_max": 0.015396886505186558,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1004,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.01842629164457321,
          0.027877727523446083,
          0.20545236766338348,
          0.012419009581208229
        ],
        "steady_command_mae": [
          0.01842629164457321,
          0.027877727523446083,
          0.20545236766338348,
          0.012419009581208229
        ],
        "contact_continuity": 0.08000000566244125,
        "max_hand_slip_m": 0.12017269432544708,
        "min_box_clearance_m": 0.5888550281524658,
        "pelvis_amplitude_m": 0.010894417762756348,
        "normal_forces_mean_n": [
          6.345587253570557,
          8.804564476013184
        ],
        "friction_weight_ratio_mean": 0.5041378140449524,
        "normal_vertical_fraction_max": 0.027426211163401604,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12198977172374725,
        "joint_speed_rms": 1.4339351654052734,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021748265251517296,
        "object_tracking_error_m": 0.03331432491540909,
        "object_tracking_error_rad_max": 0.020523419603705406,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1005,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.01875210925936699,
          0.02876482531428337,
          0.19116082787513733,
          0.012301266193389893
        ],
        "steady_command_mae": [
          0.01875210925936699,
          0.02876482531428337,
          0.19116082787513733,
          0.012301266193389893
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.11956460773944855,
        "min_box_clearance_m": 0.5875622034072876,
        "pelvis_amplitude_m": 0.010777652263641357,
        "normal_forces_mean_n": [
          6.1759161949157715,
          8.74100399017334
        ],
        "friction_weight_ratio_mean": 0.4695817530155182,
        "normal_vertical_fraction_max": 0.02678491361439228,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.123928502202034,
        "joint_speed_rms": 1.4325343370437622,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.0216554906219244,
        "object_tracking_error_m": 0.033081479370594025,
        "object_tracking_error_rad_max": 0.02443121187388897,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1006,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.018953707069158554,
          0.029679615050554276,
          0.18923994898796082,
          0.012305689044296741
        ],
        "steady_command_mae": [
          0.018953707069158554,
          0.029679615050554276,
          0.18923994898796082,
          0.012305689044296741
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.12111443281173706,
        "min_box_clearance_m": 0.5875608921051025,
        "pelvis_amplitude_m": 0.010868191719055176,
        "normal_forces_mean_n": [
          6.131884574890137,
          8.571813583374023
        ],
        "friction_weight_ratio_mean": 0.47362464666366577,
        "normal_vertical_fraction_max": 0.027439309284090996,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12241635471582413,
        "joint_speed_rms": 1.4341821670532227,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02169978991150856,
        "object_tracking_error_m": 0.03372986987233162,
        "object_tracking_error_rad_max": 0.020490460097789764,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1007,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.016372598707675934,
          0.03227667883038521,
          0.19123108685016632,
          0.012105261906981468
        ],
        "steady_command_mae": [
          0.016372598707675934,
          0.03227667883038521,
          0.19123108685016632,
          0.012105261906981468
        ],
        "contact_continuity": 0.03999999910593033,
        "max_hand_slip_m": 0.11914903670549393,
        "min_box_clearance_m": 0.5900262594223022,
        "pelvis_amplitude_m": 0.010562896728515625,
        "normal_forces_mean_n": [
          5.738214492797852,
          8.501923561096191
        ],
        "friction_weight_ratio_mean": 0.49704378843307495,
        "normal_vertical_fraction_max": 0.02534523233771324,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12474717199802399,
        "joint_speed_rms": 1.433730959892273,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021684914827346802,
        "object_tracking_error_m": 0.03133310005068779,
        "object_tracking_error_rad_max": 0.026308421045541763,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1008,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.017887892201542854,
          0.0314413346350193,
          0.20404215157032013,
          0.012392831034958363
        ],
        "steady_command_mae": [
          0.017887892201542854,
          0.0314413346350193,
          0.20404215157032013,
          0.012392831034958363
        ],
        "contact_continuity": 0.08000000566244125,
        "max_hand_slip_m": 0.11972779780626297,
        "min_box_clearance_m": 0.589262068271637,
        "pelvis_amplitude_m": 0.010830819606781006,
        "normal_forces_mean_n": [
          6.28142786026001,
          8.791770935058594
        ],
        "friction_weight_ratio_mean": 0.5119377374649048,
        "normal_vertical_fraction_max": 0.027239376679062843,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12213484197854996,
        "joint_speed_rms": 1.4344465732574463,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.02180650271475315,
        "object_tracking_error_m": 0.03301806375384331,
        "object_tracking_error_rad_max": 0.020770899951457977,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      },
      {
        "scenario": "clip_1",
        "seed": 1009,
        "survival_s": 0.1,
        "survived": false,
        "command_mae": [
          0.0175604447722435,
          0.03143664449453354,
          0.18266546726226807,
          0.012210738845169544
        ],
        "steady_command_mae": [
          0.0175604447722435,
          0.03143664449453354,
          0.18266546726226807,
          0.012210738845169544
        ],
        "contact_continuity": 0.07000000774860382,
        "max_hand_slip_m": 0.12038196623325348,
        "min_box_clearance_m": 0.5898586511611938,
        "pelvis_amplitude_m": 0.010698974132537842,
        "normal_forces_mean_n": [
          6.233684539794922,
          8.73442554473877
        ],
        "friction_weight_ratio_mean": 0.5142385363578796,
        "normal_vertical_fraction_max": 0.026761336252093315,
        "contact_height_above_bottom_min_m": 0.0,
        "nonhand_box_contact_max_n": 0.0,
        "foot_slip_speed_mean_m_s": 0.12715139985084534,
        "joint_speed_rms": 1.4364160299301147,
        "failures": [
          "physical_failure/loss_of_grasp",
          "incomplete_episode",
          "contact_interruption",
          "hand_slip",
          "insufficient_friction_support",
          "contact_near_box_bottom"
        ],
        "success": false,
        "robot_tracking_error_m": 0.021849509328603745,
        "object_tracking_error_m": 0.03269972279667854,
        "object_tracking_error_rad_max": 0.019092923030257225,
        "reference_pelvis_amplitude_m": 0.12000000476837158
      }
    ],
    "goal_limits": {
      "height_low": 0.6068800687789917,
      "height_high": 0.7268800735473633,
      "height_rate": 0.11247000098228455,
      "vx_high": 0.0,
      "forward_admitted": false,
      "reference_fps": 50,
      "episode_seconds": 30.0
    },
    "reference_free": false,
    "terminal_state_before_reset": true,
    "physical_model": {
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
      "control": "PPO joint-position offsets with PD each physics substep; no P0 feedforward or WBC"
    },
    "accepted_policy": false,
    "motion_quality": {
      "clip_0_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.10171646624803543,
          "lower_body_style_rmse_rad": 0.09468592703342438,
          "reference_compatibility_mean": 0.6668916392941266,
          "joint_acceleration_rms_rad_s2": 57.932228088378906,
          "box_relative_translation_drift_max_m": 0.032886211772286664,
          "box_relative_rotation_drift_max_rad": 0.048986296728042174
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.10171610862016678,
          "lower_body_style_rmse_rad": 0.09456217288970947,
          "reference_compatibility_mean": 0.6637870161934618,
          "joint_acceleration_rms_rad_s2": 57.59783935546875,
          "box_relative_translation_drift_max_m": 0.032615457992210765,
          "box_relative_rotation_drift_max_rad": 0.049022043252770015
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.1016525849699974,
          "lower_body_style_rmse_rad": 0.09482713788747787,
          "reference_compatibility_mean": 0.6680834821238508,
          "joint_acceleration_rms_rad_s2": 57.63589859008789,
          "box_relative_translation_drift_max_m": 0.033396159282242405,
          "box_relative_rotation_drift_max_rad": 0.047656842792968584
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.10208148509263992,
          "lower_body_style_rmse_rad": 0.09409089386463165,
          "reference_compatibility_mean": 0.6565230659734531,
          "joint_acceleration_rms_rad_s2": 56.92254638671875,
          "box_relative_translation_drift_max_m": 0.03532761939900159,
          "box_relative_rotation_drift_max_rad": 0.04334121680394966
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.1022593230009079,
          "lower_body_style_rmse_rad": 0.09530818462371826,
          "reference_compatibility_mean": 0.6514661061805835,
          "joint_acceleration_rms_rad_s2": 56.86941146850586,
          "box_relative_translation_drift_max_m": 0.034255027181520514,
          "box_relative_rotation_drift_max_rad": 0.04617213789459057
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.10208599269390106,
          "lower_body_style_rmse_rad": 0.0943443775177002,
          "reference_compatibility_mean": 0.6548339077701193,
          "joint_acceleration_rms_rad_s2": 56.84711456298828,
          "box_relative_translation_drift_max_m": 0.03504492008805205,
          "box_relative_rotation_drift_max_rad": 0.049725498941022586
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.10230069607496262,
          "lower_body_style_rmse_rad": 0.09428534656763077,
          "reference_compatibility_mean": 0.6528190241206169,
          "joint_acceleration_rms_rad_s2": 57.10758590698242,
          "box_relative_translation_drift_max_m": 0.03521911312123594,
          "box_relative_rotation_drift_max_rad": 0.04724887121789102
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.10164067149162292,
          "lower_body_style_rmse_rad": 0.09466531872749329,
          "reference_compatibility_mean": 0.6675556502071461,
          "joint_acceleration_rms_rad_s2": 58.12871551513672,
          "box_relative_translation_drift_max_m": 0.033248906173298225,
          "box_relative_rotation_drift_max_rad": 0.04722032172558822
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.10210279375314713,
          "lower_body_style_rmse_rad": 0.0956575945019722,
          "reference_compatibility_mean": 0.6530401024346035,
          "joint_acceleration_rms_rad_s2": 56.878990173339844,
          "box_relative_translation_drift_max_m": 0.033900824378922556,
          "box_relative_rotation_drift_max_rad": 0.04601622319526483
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.10239670425653458,
          "lower_body_style_rmse_rad": 0.09470371901988983,
          "reference_compatibility_mean": 0.6587303553185238,
          "joint_acceleration_rms_rad_s2": 56.97249221801758,
          "box_relative_translation_drift_max_m": 0.03375256580594606,
          "box_relative_rotation_drift_max_rad": 0.04279324028735476
        }
      ],
      "clip_1_rollout": [
        {
          "seed_index": 0,
          "upper_body_style_rmse_rad": 0.10198214650154114,
          "lower_body_style_rmse_rad": 0.09471025317907333,
          "reference_compatibility_mean": 0.6629595814412458,
          "joint_acceleration_rms_rad_s2": 57.95216369628906,
          "box_relative_translation_drift_max_m": 0.032742285921335684,
          "box_relative_rotation_drift_max_rad": 0.04694334602541759
        },
        {
          "seed_index": 1,
          "upper_body_style_rmse_rad": 0.1019829586148262,
          "lower_body_style_rmse_rad": 0.0946386456489563,
          "reference_compatibility_mean": 0.6600783472170951,
          "joint_acceleration_rms_rad_s2": 57.83352279663086,
          "box_relative_translation_drift_max_m": 0.032742995411247006,
          "box_relative_rotation_drift_max_rad": 0.045069184918592756
        },
        {
          "seed_index": 2,
          "upper_body_style_rmse_rad": 0.1016540601849556,
          "lower_body_style_rmse_rad": 0.09475968033075333,
          "reference_compatibility_mean": 0.6682254944763779,
          "joint_acceleration_rms_rad_s2": 57.615013122558594,
          "box_relative_translation_drift_max_m": 0.03339684577896217,
          "box_relative_rotation_drift_max_rad": 0.04752963990647475
        },
        {
          "seed_index": 3,
          "upper_body_style_rmse_rad": 0.10209423303604126,
          "lower_body_style_rmse_rad": 0.09409675002098083,
          "reference_compatibility_mean": 0.656535956511709,
          "joint_acceleration_rms_rad_s2": 56.894222259521484,
          "box_relative_translation_drift_max_m": 0.03534240745174636,
          "box_relative_rotation_drift_max_rad": 0.043518204933964355
        },
        {
          "seed_index": 4,
          "upper_body_style_rmse_rad": 0.1022636741399765,
          "lower_body_style_rmse_rad": 0.09530574083328247,
          "reference_compatibility_mean": 0.6514172195328266,
          "joint_acceleration_rms_rad_s2": 56.90572738647461,
          "box_relative_translation_drift_max_m": 0.03425696085940327,
          "box_relative_rotation_drift_max_rad": 0.04619729545734303
        },
        {
          "seed_index": 5,
          "upper_body_style_rmse_rad": 0.10210899263620377,
          "lower_body_style_rmse_rad": 0.09434855729341507,
          "reference_compatibility_mean": 0.6545619188520566,
          "joint_acceleration_rms_rad_s2": 56.829410552978516,
          "box_relative_translation_drift_max_m": 0.03512912220289047,
          "box_relative_rotation_drift_max_rad": 0.05023056635608008
        },
        {
          "seed_index": 6,
          "upper_body_style_rmse_rad": 0.10228127986192703,
          "lower_body_style_rmse_rad": 0.09427809715270996,
          "reference_compatibility_mean": 0.6527990121641158,
          "joint_acceleration_rms_rad_s2": 57.137786865234375,
          "box_relative_translation_drift_max_m": 0.0352328558001928,
          "box_relative_rotation_drift_max_rad": 0.04702493569198824
        },
        {
          "seed_index": 7,
          "upper_body_style_rmse_rad": 0.10189051926136017,
          "lower_body_style_rmse_rad": 0.09475428611040115,
          "reference_compatibility_mean": 0.663856721373924,
          "joint_acceleration_rms_rad_s2": 57.75625991821289,
          "box_relative_translation_drift_max_m": 0.03294077946475321,
          "box_relative_rotation_drift_max_rad": 0.04501629386982183
        },
        {
          "seed_index": 8,
          "upper_body_style_rmse_rad": 0.10209178924560547,
          "lower_body_style_rmse_rad": 0.09565791487693787,
          "reference_compatibility_mean": 0.6530739336133583,
          "joint_acceleration_rms_rad_s2": 56.95000457763672,
          "box_relative_translation_drift_max_m": 0.033895033919211115,
          "box_relative_rotation_drift_max_rad": 0.045944396699893045
        },
        {
          "seed_index": 9,
          "upper_body_style_rmse_rad": 0.10240694135427475,
          "lower_body_style_rmse_rad": 0.09471503645181656,
          "reference_compatibility_mean": 0.6589107237677839,
          "joint_acceleration_rms_rad_s2": 57.067874908447266,
          "box_relative_translation_drift_max_m": 0.033756333978398084,
          "box_relative_rotation_drift_max_rad": 0.043231882255588425
        }
      ]
    },
    "directory": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795236555511488308",
    "checkpoint": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/dashboard/stage1/WholeBodyTracking/20261121_024914-stage1-locomotion/model_05499.pt",
    "final": false,
    "selection_score": 0.007988461962399575,
    "failure_counts": {
      "physical_failure/loss_of_grasp": 20,
      "incomplete_episode": 20,
      "contact_interruption": 20,
      "hand_slip": 20,
      "insufficient_friction_support": 20,
      "contact_near_box_bottom": 20
    },
    "scenarios": {
      "clip_0": {
        "success_rate": 0.0,
        "trials": 10
      },
      "clip_1": {
        "success_rate": 0.0,
        "trials": 10
      }
    },
    "completed_updates": 5500
  }
]

## Stage 2 measured evaluations

[]

## Style ablation

"Not executed; cannot claim an improvement"

## Motion-quality analysis

{
  "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795184787477293549": {
    "clip_0_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.09598325192928314,
        "lower_body_style_rmse_rad": 0.07564572989940643,
        "reference_compatibility_mean": 0.6925693053600398,
        "joint_acceleration_rms_rad_s2": 59.07049560546875,
        "box_relative_translation_drift_max_m": 0.048612733782380936,
        "box_relative_rotation_drift_max_rad": 0.11957585592273873
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.09614122658967972,
        "lower_body_style_rmse_rad": 0.07565982639789581,
        "reference_compatibility_mean": 0.6857628125629842,
        "joint_acceleration_rms_rad_s2": 58.982032775878906,
        "box_relative_translation_drift_max_m": 0.048908340309479235,
        "box_relative_rotation_drift_max_rad": 0.11639881709343798
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.09622150659561157,
        "lower_body_style_rmse_rad": 0.07533174008131027,
        "reference_compatibility_mean": 0.6889798889840173,
        "joint_acceleration_rms_rad_s2": 59.36373519897461,
        "box_relative_translation_drift_max_m": 0.049536554293999294,
        "box_relative_rotation_drift_max_rad": 0.11746588451423876
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.09632813930511475,
        "lower_body_style_rmse_rad": 0.07529444247484207,
        "reference_compatibility_mean": 0.6926951157980712,
        "joint_acceleration_rms_rad_s2": 58.8328857421875,
        "box_relative_translation_drift_max_m": 0.052212247794966665,
        "box_relative_rotation_drift_max_rad": 0.1157976784111097
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.09725508838891983,
        "lower_body_style_rmse_rad": 0.07591402530670166,
        "reference_compatibility_mean": 0.6865293724618221,
        "joint_acceleration_rms_rad_s2": 58.66195297241211,
        "box_relative_translation_drift_max_m": 0.05056639575745032,
        "box_relative_rotation_drift_max_rad": 0.1119626734315536
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.09641708433628082,
        "lower_body_style_rmse_rad": 0.07609604299068451,
        "reference_compatibility_mean": 0.6984699570560188,
        "joint_acceleration_rms_rad_s2": 58.66376876831055,
        "box_relative_translation_drift_max_m": 0.04978455502343307,
        "box_relative_rotation_drift_max_rad": 0.11444184076381715
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.09756220132112503,
        "lower_body_style_rmse_rad": 0.07675717771053314,
        "reference_compatibility_mean": 0.6780091881208218,
        "joint_acceleration_rms_rad_s2": 58.70753479003906,
        "box_relative_translation_drift_max_m": 0.05052841593872035,
        "box_relative_rotation_drift_max_rad": 0.1166895316649139
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.09606786072254181,
        "lower_body_style_rmse_rad": 0.07551967352628708,
        "reference_compatibility_mean": 0.6917102758547806,
        "joint_acceleration_rms_rad_s2": 59.05024719238281,
        "box_relative_translation_drift_max_m": 0.048900337817273626,
        "box_relative_rotation_drift_max_rad": 0.11705943071170741
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.0969899371266365,
        "lower_body_style_rmse_rad": 0.07522062957286835,
        "reference_compatibility_mean": 0.6830272833724695,
        "joint_acceleration_rms_rad_s2": 58.921775817871094,
        "box_relative_translation_drift_max_m": 0.05065691178196891,
        "box_relative_rotation_drift_max_rad": 0.1149847265035077
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.09739809483289719,
        "lower_body_style_rmse_rad": 0.07618491351604462,
        "reference_compatibility_mean": 0.6873415381794524,
        "joint_acceleration_rms_rad_s2": 59.04922103881836,
        "box_relative_translation_drift_max_m": 0.0502666842958512,
        "box_relative_rotation_drift_max_rad": 0.11209693008905558
      }
    ],
    "clip_1_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.09597302228212357,
        "lower_body_style_rmse_rad": 0.07559802383184433,
        "reference_compatibility_mean": 0.6929031402397404,
        "joint_acceleration_rms_rad_s2": 58.9588508605957,
        "box_relative_translation_drift_max_m": 0.048605149099870834,
        "box_relative_rotation_drift_max_rad": 0.11943787626112658
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.09613760560750961,
        "lower_body_style_rmse_rad": 0.07544218748807907,
        "reference_compatibility_mean": 0.6859424080465673,
        "joint_acceleration_rms_rad_s2": 58.94514465332031,
        "box_relative_translation_drift_max_m": 0.04888217450898544,
        "box_relative_rotation_drift_max_rad": 0.11632202566584916
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.09623436629772186,
        "lower_body_style_rmse_rad": 0.07532346248626709,
        "reference_compatibility_mean": 0.6890780486583454,
        "joint_acceleration_rms_rad_s2": 59.25678634643555,
        "box_relative_translation_drift_max_m": 0.04949134456915155,
        "box_relative_rotation_drift_max_rad": 0.11744334441120902
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.09662478417158127,
        "lower_body_style_rmse_rad": 0.07540161907672882,
        "reference_compatibility_mean": 0.6912209123123642,
        "joint_acceleration_rms_rad_s2": 58.836036682128906,
        "box_relative_translation_drift_max_m": 0.05066322071610726,
        "box_relative_rotation_drift_max_rad": 0.11551426785522356
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.09724827855825424,
        "lower_body_style_rmse_rad": 0.07591874897480011,
        "reference_compatibility_mean": 0.6865357670285213,
        "joint_acceleration_rms_rad_s2": 58.68147277832031,
        "box_relative_translation_drift_max_m": 0.05057896050343616,
        "box_relative_rotation_drift_max_rad": 0.11205360984842465
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.09682975709438324,
        "lower_body_style_rmse_rad": 0.07588355243206024,
        "reference_compatibility_mean": 0.6951791071546062,
        "joint_acceleration_rms_rad_s2": 58.55741882324219,
        "box_relative_translation_drift_max_m": 0.05044442963810377,
        "box_relative_rotation_drift_max_rad": 0.11350526592553142
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.09757013618946075,
        "lower_body_style_rmse_rad": 0.0769595056772232,
        "reference_compatibility_mean": 0.6780535747144889,
        "joint_acceleration_rms_rad_s2": 58.68822479248047,
        "box_relative_translation_drift_max_m": 0.05049794869525651,
        "box_relative_rotation_drift_max_rad": 0.11673417913278518
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.09605638682842255,
        "lower_body_style_rmse_rad": 0.07551489025354385,
        "reference_compatibility_mean": 0.691860592935261,
        "joint_acceleration_rms_rad_s2": 59.111759185791016,
        "box_relative_translation_drift_max_m": 0.04887313910230617,
        "box_relative_rotation_drift_max_rad": 0.11676550855709891
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.09701506048440933,
        "lower_body_style_rmse_rad": 0.07523860782384872,
        "reference_compatibility_mean": 0.6829162011864521,
        "joint_acceleration_rms_rad_s2": 58.84743118286133,
        "box_relative_translation_drift_max_m": 0.05059932147922189,
        "box_relative_rotation_drift_max_rad": 0.11523911303699347
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.09738703817129135,
        "lower_body_style_rmse_rad": 0.07618911564350128,
        "reference_compatibility_mean": 0.687123069675036,
        "joint_acceleration_rms_rad_s2": 59.07891845703125,
        "box_relative_translation_drift_max_m": 0.050270668642189695,
        "box_relative_rotation_drift_max_rad": 0.1119740141831197
      }
    ]
  },
  "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795236555511488308": {
    "clip_0_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.10171646624803543,
        "lower_body_style_rmse_rad": 0.09468592703342438,
        "reference_compatibility_mean": 0.6668916392941266,
        "joint_acceleration_rms_rad_s2": 57.932228088378906,
        "box_relative_translation_drift_max_m": 0.032886211772286664,
        "box_relative_rotation_drift_max_rad": 0.048986296728042174
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.10171610862016678,
        "lower_body_style_rmse_rad": 0.09456217288970947,
        "reference_compatibility_mean": 0.6637870161934618,
        "joint_acceleration_rms_rad_s2": 57.59783935546875,
        "box_relative_translation_drift_max_m": 0.032615457992210765,
        "box_relative_rotation_drift_max_rad": 0.049022043252770015
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.1016525849699974,
        "lower_body_style_rmse_rad": 0.09482713788747787,
        "reference_compatibility_mean": 0.6680834821238508,
        "joint_acceleration_rms_rad_s2": 57.63589859008789,
        "box_relative_translation_drift_max_m": 0.033396159282242405,
        "box_relative_rotation_drift_max_rad": 0.047656842792968584
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.10208148509263992,
        "lower_body_style_rmse_rad": 0.09409089386463165,
        "reference_compatibility_mean": 0.6565230659734531,
        "joint_acceleration_rms_rad_s2": 56.92254638671875,
        "box_relative_translation_drift_max_m": 0.03532761939900159,
        "box_relative_rotation_drift_max_rad": 0.04334121680394966
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.1022593230009079,
        "lower_body_style_rmse_rad": 0.09530818462371826,
        "reference_compatibility_mean": 0.6514661061805835,
        "joint_acceleration_rms_rad_s2": 56.86941146850586,
        "box_relative_translation_drift_max_m": 0.034255027181520514,
        "box_relative_rotation_drift_max_rad": 0.04617213789459057
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.10208599269390106,
        "lower_body_style_rmse_rad": 0.0943443775177002,
        "reference_compatibility_mean": 0.6548339077701193,
        "joint_acceleration_rms_rad_s2": 56.84711456298828,
        "box_relative_translation_drift_max_m": 0.03504492008805205,
        "box_relative_rotation_drift_max_rad": 0.049725498941022586
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.10230069607496262,
        "lower_body_style_rmse_rad": 0.09428534656763077,
        "reference_compatibility_mean": 0.6528190241206169,
        "joint_acceleration_rms_rad_s2": 57.10758590698242,
        "box_relative_translation_drift_max_m": 0.03521911312123594,
        "box_relative_rotation_drift_max_rad": 0.04724887121789102
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.10164067149162292,
        "lower_body_style_rmse_rad": 0.09466531872749329,
        "reference_compatibility_mean": 0.6675556502071461,
        "joint_acceleration_rms_rad_s2": 58.12871551513672,
        "box_relative_translation_drift_max_m": 0.033248906173298225,
        "box_relative_rotation_drift_max_rad": 0.04722032172558822
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.10210279375314713,
        "lower_body_style_rmse_rad": 0.0956575945019722,
        "reference_compatibility_mean": 0.6530401024346035,
        "joint_acceleration_rms_rad_s2": 56.878990173339844,
        "box_relative_translation_drift_max_m": 0.033900824378922556,
        "box_relative_rotation_drift_max_rad": 0.04601622319526483
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.10239670425653458,
        "lower_body_style_rmse_rad": 0.09470371901988983,
        "reference_compatibility_mean": 0.6587303553185238,
        "joint_acceleration_rms_rad_s2": 56.97249221801758,
        "box_relative_translation_drift_max_m": 0.03375256580594606,
        "box_relative_rotation_drift_max_rad": 0.04279324028735476
      }
    ],
    "clip_1_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.10198214650154114,
        "lower_body_style_rmse_rad": 0.09471025317907333,
        "reference_compatibility_mean": 0.6629595814412458,
        "joint_acceleration_rms_rad_s2": 57.95216369628906,
        "box_relative_translation_drift_max_m": 0.032742285921335684,
        "box_relative_rotation_drift_max_rad": 0.04694334602541759
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.1019829586148262,
        "lower_body_style_rmse_rad": 0.0946386456489563,
        "reference_compatibility_mean": 0.6600783472170951,
        "joint_acceleration_rms_rad_s2": 57.83352279663086,
        "box_relative_translation_drift_max_m": 0.032742995411247006,
        "box_relative_rotation_drift_max_rad": 0.045069184918592756
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.1016540601849556,
        "lower_body_style_rmse_rad": 0.09475968033075333,
        "reference_compatibility_mean": 0.6682254944763779,
        "joint_acceleration_rms_rad_s2": 57.615013122558594,
        "box_relative_translation_drift_max_m": 0.03339684577896217,
        "box_relative_rotation_drift_max_rad": 0.04752963990647475
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.10209423303604126,
        "lower_body_style_rmse_rad": 0.09409675002098083,
        "reference_compatibility_mean": 0.656535956511709,
        "joint_acceleration_rms_rad_s2": 56.894222259521484,
        "box_relative_translation_drift_max_m": 0.03534240745174636,
        "box_relative_rotation_drift_max_rad": 0.043518204933964355
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.1022636741399765,
        "lower_body_style_rmse_rad": 0.09530574083328247,
        "reference_compatibility_mean": 0.6514172195328266,
        "joint_acceleration_rms_rad_s2": 56.90572738647461,
        "box_relative_translation_drift_max_m": 0.03425696085940327,
        "box_relative_rotation_drift_max_rad": 0.04619729545734303
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.10210899263620377,
        "lower_body_style_rmse_rad": 0.09434855729341507,
        "reference_compatibility_mean": 0.6545619188520566,
        "joint_acceleration_rms_rad_s2": 56.829410552978516,
        "box_relative_translation_drift_max_m": 0.03512912220289047,
        "box_relative_rotation_drift_max_rad": 0.05023056635608008
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.10228127986192703,
        "lower_body_style_rmse_rad": 0.09427809715270996,
        "reference_compatibility_mean": 0.6527990121641158,
        "joint_acceleration_rms_rad_s2": 57.137786865234375,
        "box_relative_translation_drift_max_m": 0.0352328558001928,
        "box_relative_rotation_drift_max_rad": 0.04702493569198824
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.10189051926136017,
        "lower_body_style_rmse_rad": 0.09475428611040115,
        "reference_compatibility_mean": 0.663856721373924,
        "joint_acceleration_rms_rad_s2": 57.75625991821289,
        "box_relative_translation_drift_max_m": 0.03294077946475321,
        "box_relative_rotation_drift_max_rad": 0.04501629386982183
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.10209178924560547,
        "lower_body_style_rmse_rad": 0.09565791487693787,
        "reference_compatibility_mean": 0.6530739336133583,
        "joint_acceleration_rms_rad_s2": 56.95000457763672,
        "box_relative_translation_drift_max_m": 0.033895033919211115,
        "box_relative_rotation_drift_max_rad": 0.045944396699893045
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.10240694135427475,
        "lower_body_style_rmse_rad": 0.09471503645181656,
        "reference_compatibility_mean": 0.6589107237677839,
        "joint_acceleration_rms_rad_s2": 57.067874908447266,
        "box_relative_translation_drift_max_m": 0.033756333978398084,
        "box_relative_rotation_drift_max_rad": 0.043231882255588425
      }
    ]
  },
  "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795214808532584110": {
    "clip_0_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.09428401291370392,
        "lower_body_style_rmse_rad": 0.07721925526857376,
        "reference_compatibility_mean": 0.8588253021583523,
        "joint_acceleration_rms_rad_s2": 57.6012077331543,
        "box_relative_translation_drift_max_m": 0.03595961056412528,
        "box_relative_rotation_drift_max_rad": 0.07329732167418229
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.09403175115585327,
        "lower_body_style_rmse_rad": 0.07689538598060608,
        "reference_compatibility_mean": 0.8585969936445135,
        "joint_acceleration_rms_rad_s2": 57.628780364990234,
        "box_relative_translation_drift_max_m": 0.037689018891342185,
        "box_relative_rotation_drift_max_rad": 0.07808863061604175
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.09433633089065552,
        "lower_body_style_rmse_rad": 0.07703197747468948,
        "reference_compatibility_mean": 0.8568500451992597,
        "joint_acceleration_rms_rad_s2": 57.76902770996094,
        "box_relative_translation_drift_max_m": 0.03632829765285222,
        "box_relative_rotation_drift_max_rad": 0.07489396871891855
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.09446791559457779,
        "lower_body_style_rmse_rad": 0.07691948860883713,
        "reference_compatibility_mean": 0.8632542044138425,
        "joint_acceleration_rms_rad_s2": 56.80528259277344,
        "box_relative_translation_drift_max_m": 0.03874646261487951,
        "box_relative_rotation_drift_max_rad": 0.07603170208594102
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.0948123186826706,
        "lower_body_style_rmse_rad": 0.07692248374223709,
        "reference_compatibility_mean": 0.8551193764904476,
        "joint_acceleration_rms_rad_s2": 56.8919792175293,
        "box_relative_translation_drift_max_m": 0.03711854658935319,
        "box_relative_rotation_drift_max_rad": 0.07046993450432595
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.09421280771493912,
        "lower_body_style_rmse_rad": 0.0769215077161789,
        "reference_compatibility_mean": 0.8625713070647482,
        "joint_acceleration_rms_rad_s2": 56.57120132446289,
        "box_relative_translation_drift_max_m": 0.038449156518071397,
        "box_relative_rotation_drift_max_rad": 0.07804252294078659
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.0947151780128479,
        "lower_body_style_rmse_rad": 0.0773608535528183,
        "reference_compatibility_mean": 0.8525675141283197,
        "joint_acceleration_rms_rad_s2": 56.976890563964844,
        "box_relative_translation_drift_max_m": 0.0377361914605514,
        "box_relative_rotation_drift_max_rad": 0.0750263517045079
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.09418483078479767,
        "lower_body_style_rmse_rad": 0.07691887021064758,
        "reference_compatibility_mean": 0.8622422484994606,
        "joint_acceleration_rms_rad_s2": 57.44154739379883,
        "box_relative_translation_drift_max_m": 0.03636877960237467,
        "box_relative_rotation_drift_max_rad": 0.07303257615720846
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.0946950763463974,
        "lower_body_style_rmse_rad": 0.07702695578336716,
        "reference_compatibility_mean": 0.8530031578542884,
        "joint_acceleration_rms_rad_s2": 57.30055618286133,
        "box_relative_translation_drift_max_m": 0.038078729619134055,
        "box_relative_rotation_drift_max_rad": 0.07749052774991466
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.09490863233804703,
        "lower_body_style_rmse_rad": 0.07726948708295822,
        "reference_compatibility_mean": 0.8542971699375059,
        "joint_acceleration_rms_rad_s2": 57.436790466308594,
        "box_relative_translation_drift_max_m": 0.03828648678955509,
        "box_relative_rotation_drift_max_rad": 0.07832144268829723
      }
    ],
    "clip_1_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.09430009871721268,
        "lower_body_style_rmse_rad": 0.0772794708609581,
        "reference_compatibility_mean": 0.8585673674773172,
        "joint_acceleration_rms_rad_s2": 57.5589599609375,
        "box_relative_translation_drift_max_m": 0.03592159535951574,
        "box_relative_rotation_drift_max_rad": 0.07316770881582232
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.09402485936880112,
        "lower_body_style_rmse_rad": 0.0768844336271286,
        "reference_compatibility_mean": 0.858566455450178,
        "joint_acceleration_rms_rad_s2": 57.620601654052734,
        "box_relative_translation_drift_max_m": 0.03776582735479417,
        "box_relative_rotation_drift_max_rad": 0.07853714281264929
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.0943281278014183,
        "lower_body_style_rmse_rad": 0.07717394083738327,
        "reference_compatibility_mean": 0.8568940998768682,
        "joint_acceleration_rms_rad_s2": 57.80686950683594,
        "box_relative_translation_drift_max_m": 0.036267366776618785,
        "box_relative_rotation_drift_max_rad": 0.07453447719088833
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.09442974627017975,
        "lower_body_style_rmse_rad": 0.07690681517124176,
        "reference_compatibility_mean": 0.8640500631347662,
        "joint_acceleration_rms_rad_s2": 56.72585678100586,
        "box_relative_translation_drift_max_m": 0.038861617242617025,
        "box_relative_rotation_drift_max_rad": 0.07671072384847878
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.09478358924388885,
        "lower_body_style_rmse_rad": 0.0769292488694191,
        "reference_compatibility_mean": 0.8550252322996739,
        "joint_acceleration_rms_rad_s2": 56.882667541503906,
        "box_relative_translation_drift_max_m": 0.03744923135071922,
        "box_relative_rotation_drift_max_rad": 0.0720232954806501
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.09460941702127457,
        "lower_body_style_rmse_rad": 0.077016681432724,
        "reference_compatibility_mean": 0.8547687568075624,
        "joint_acceleration_rms_rad_s2": 56.7675895690918,
        "box_relative_translation_drift_max_m": 0.03736442462661007,
        "box_relative_rotation_drift_max_rad": 0.0733695022504277
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.09472602605819702,
        "lower_body_style_rmse_rad": 0.07736510038375854,
        "reference_compatibility_mean": 0.8525313433274745,
        "joint_acceleration_rms_rad_s2": 56.70098876953125,
        "box_relative_translation_drift_max_m": 0.03778035598086901,
        "box_relative_rotation_drift_max_rad": 0.07490076475297504
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.09423362463712692,
        "lower_body_style_rmse_rad": 0.07685615867376328,
        "reference_compatibility_mean": 0.8621334582330837,
        "joint_acceleration_rms_rad_s2": 57.44169616699219,
        "box_relative_translation_drift_max_m": 0.03629375349071587,
        "box_relative_rotation_drift_max_rad": 0.0726793476693234
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.0946427509188652,
        "lower_body_style_rmse_rad": 0.07702632248401642,
        "reference_compatibility_mean": 0.8531202116333738,
        "joint_acceleration_rms_rad_s2": 57.238853454589844,
        "box_relative_translation_drift_max_m": 0.03826754981321256,
        "box_relative_rotation_drift_max_rad": 0.07976795915433975
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.09494228661060333,
        "lower_body_style_rmse_rad": 0.07726740092039108,
        "reference_compatibility_mean": 0.8541952177938518,
        "joint_acceleration_rms_rad_s2": 57.385799407958984,
        "box_relative_translation_drift_max_m": 0.03829938547862449,
        "box_relative_rotation_drift_max_rad": 0.07843960017976752
      }
    ]
  },
  "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795207476248684651": {
    "clip_0_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.1011236310005188,
        "lower_body_style_rmse_rad": 0.07091598957777023,
        "reference_compatibility_mean": 0.8916152402312975,
        "joint_acceleration_rms_rad_s2": 35.44654846191406,
        "box_relative_translation_drift_max_m": 0.055032013139381546,
        "box_relative_rotation_drift_max_rad": 0.0577934280140449
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.10118065774440765,
        "lower_body_style_rmse_rad": 0.06938589364290237,
        "reference_compatibility_mean": 0.8978695632190753,
        "joint_acceleration_rms_rad_s2": 35.460506439208984,
        "box_relative_translation_drift_max_m": 0.05526999823395054,
        "box_relative_rotation_drift_max_rad": 0.0576396737830099
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.10127242654561996,
        "lower_body_style_rmse_rad": 0.07040072977542877,
        "reference_compatibility_mean": 0.8913868134977714,
        "joint_acceleration_rms_rad_s2": 35.46141052246094,
        "box_relative_translation_drift_max_m": 0.055387622526558204,
        "box_relative_rotation_drift_max_rad": 0.057702098532900384
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.1026809960603714,
        "lower_body_style_rmse_rad": 0.06993930041790009,
        "reference_compatibility_mean": 0.8947683870789792,
        "joint_acceleration_rms_rad_s2": 35.41193389892578,
        "box_relative_translation_drift_max_m": 0.05582342089336574,
        "box_relative_rotation_drift_max_rad": 0.056288578996422096
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.10239977389574051,
        "lower_body_style_rmse_rad": 0.06987731158733368,
        "reference_compatibility_mean": 0.8960112054653229,
        "joint_acceleration_rms_rad_s2": 35.404476165771484,
        "box_relative_translation_drift_max_m": 0.05630313691592539,
        "box_relative_rotation_drift_max_rad": 0.056402919599480336
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.10195469111204147,
        "lower_body_style_rmse_rad": 0.06963054090738297,
        "reference_compatibility_mean": 0.8968813848439755,
        "joint_acceleration_rms_rad_s2": 35.16630554199219,
        "box_relative_translation_drift_max_m": 0.05567731253626865,
        "box_relative_rotation_drift_max_rad": 0.055434688010912815
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.10267283767461777,
        "lower_body_style_rmse_rad": 0.07017690688371658,
        "reference_compatibility_mean": 0.8968996933592539,
        "joint_acceleration_rms_rad_s2": 35.494327545166016,
        "box_relative_translation_drift_max_m": 0.05606714325953691,
        "box_relative_rotation_drift_max_rad": 0.05586839788136181
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.10106883943080902,
        "lower_body_style_rmse_rad": 0.06888579577207565,
        "reference_compatibility_mean": 0.8945554656795061,
        "joint_acceleration_rms_rad_s2": 35.451602935791016,
        "box_relative_translation_drift_max_m": 0.055003584079820984,
        "box_relative_rotation_drift_max_rad": 0.058193806118581604
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.10212024301290512,
        "lower_body_style_rmse_rad": 0.06975320726633072,
        "reference_compatibility_mean": 0.8929567264311775,
        "joint_acceleration_rms_rad_s2": 35.37553405761719,
        "box_relative_translation_drift_max_m": 0.05554324268456987,
        "box_relative_rotation_drift_max_rad": 0.05577375390653555
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.1025315672159195,
        "lower_body_style_rmse_rad": 0.07125764340162277,
        "reference_compatibility_mean": 0.8893355464147215,
        "joint_acceleration_rms_rad_s2": 35.46196365356445,
        "box_relative_translation_drift_max_m": 0.056141880787567815,
        "box_relative_rotation_drift_max_rad": 0.05334515468737263
      }
    ],
    "clip_1_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.10112810134887695,
        "lower_body_style_rmse_rad": 0.07078329473733902,
        "reference_compatibility_mean": 0.8922674070849499,
        "joint_acceleration_rms_rad_s2": 35.4002799987793,
        "box_relative_translation_drift_max_m": 0.05500582950432958,
        "box_relative_rotation_drift_max_rad": 0.057817870604326756
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.10116524249315262,
        "lower_body_style_rmse_rad": 0.06936813145875931,
        "reference_compatibility_mean": 0.8983877347516275,
        "joint_acceleration_rms_rad_s2": 35.437095642089844,
        "box_relative_translation_drift_max_m": 0.05521471095620653,
        "box_relative_rotation_drift_max_rad": 0.05741072127008877
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.10128884762525558,
        "lower_body_style_rmse_rad": 0.07042166590690613,
        "reference_compatibility_mean": 0.8913291012966844,
        "joint_acceleration_rms_rad_s2": 35.418277740478516,
        "box_relative_translation_drift_max_m": 0.055345358991513806,
        "box_relative_rotation_drift_max_rad": 0.05769765779039082
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.10268091410398483,
        "lower_body_style_rmse_rad": 0.06997094303369522,
        "reference_compatibility_mean": 0.8945481717540271,
        "joint_acceleration_rms_rad_s2": 35.24541473388672,
        "box_relative_translation_drift_max_m": 0.05575785314101226,
        "box_relative_rotation_drift_max_rad": 0.056331909176344244
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.1024090051651001,
        "lower_body_style_rmse_rad": 0.06996136158704758,
        "reference_compatibility_mean": 0.8958861527228066,
        "joint_acceleration_rms_rad_s2": 35.47512435913086,
        "box_relative_translation_drift_max_m": 0.05604262115962388,
        "box_relative_rotation_drift_max_rad": 0.0570354416449782
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.10193710774183273,
        "lower_body_style_rmse_rad": 0.06974803656339645,
        "reference_compatibility_mean": 0.8966164223177925,
        "joint_acceleration_rms_rad_s2": 35.24787902832031,
        "box_relative_translation_drift_max_m": 0.055672686363275804,
        "box_relative_rotation_drift_max_rad": 0.0556883922628906
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.10267023742198944,
        "lower_body_style_rmse_rad": 0.07015026360750198,
        "reference_compatibility_mean": 0.8969182810504648,
        "joint_acceleration_rms_rad_s2": 35.54161071777344,
        "box_relative_translation_drift_max_m": 0.05630709631957172,
        "box_relative_rotation_drift_max_rad": 0.055799864114629956
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.10104888677597046,
        "lower_body_style_rmse_rad": 0.06887713074684143,
        "reference_compatibility_mean": 0.8946126843867749,
        "joint_acceleration_rms_rad_s2": 35.441864013671875,
        "box_relative_translation_drift_max_m": 0.0549970878861285,
        "box_relative_rotation_drift_max_rad": 0.05811983593503357
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.10213208198547363,
        "lower_body_style_rmse_rad": 0.0695912092924118,
        "reference_compatibility_mean": 0.89304133280671,
        "joint_acceleration_rms_rad_s2": 35.367801666259766,
        "box_relative_translation_drift_max_m": 0.05554431753064702,
        "box_relative_rotation_drift_max_rad": 0.05594884957510276
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.10254174470901489,
        "lower_body_style_rmse_rad": 0.07136812806129456,
        "reference_compatibility_mean": 0.8885135512515283,
        "joint_acceleration_rms_rad_s2": 35.5484733581543,
        "box_relative_translation_drift_max_m": 0.05612691031137436,
        "box_relative_rotation_drift_max_rad": 0.05343115292379399
      }
    ]
  },
  "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795222066333557483": {
    "clip_0_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.09418580681085587,
        "lower_body_style_rmse_rad": 0.08014652132987976,
        "reference_compatibility_mean": 0.8449958280461999,
        "joint_acceleration_rms_rad_s2": 56.63563919067383,
        "box_relative_translation_drift_max_m": 0.03483263113515009,
        "box_relative_rotation_drift_max_rad": 0.06007923964558195
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.09411722421646118,
        "lower_body_style_rmse_rad": 0.08018938452005386,
        "reference_compatibility_mean": 0.8422286199669113,
        "joint_acceleration_rms_rad_s2": 56.95589065551758,
        "box_relative_translation_drift_max_m": 0.0360143209134871,
        "box_relative_rotation_drift_max_rad": 0.06214154952699419
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.09418613463640213,
        "lower_body_style_rmse_rad": 0.0785161703824997,
        "reference_compatibility_mean": 0.8463156649714871,
        "joint_acceleration_rms_rad_s2": 56.68478012084961,
        "box_relative_translation_drift_max_m": 0.034678164931716424,
        "box_relative_rotation_drift_max_rad": 0.05762058435689468
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.09473688900470734,
        "lower_body_style_rmse_rad": 0.08047108352184296,
        "reference_compatibility_mean": 0.8385200076809088,
        "joint_acceleration_rms_rad_s2": 56.98863220214844,
        "box_relative_translation_drift_max_m": 0.036639531259413424,
        "box_relative_rotation_drift_max_rad": 0.0556236900795041
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.09494820237159729,
        "lower_body_style_rmse_rad": 0.0802159532904625,
        "reference_compatibility_mean": 0.8355674917121577,
        "joint_acceleration_rms_rad_s2": 56.3743896484375,
        "box_relative_translation_drift_max_m": 0.03669401100244888,
        "box_relative_rotation_drift_max_rad": 0.06140476886905047
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.0948118269443512,
        "lower_body_style_rmse_rad": 0.08020610362291336,
        "reference_compatibility_mean": 0.8374946468821214,
        "joint_acceleration_rms_rad_s2": 55.87966537475586,
        "box_relative_translation_drift_max_m": 0.03511464160026636,
        "box_relative_rotation_drift_max_rad": 0.057718220942515004
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.09507322311401367,
        "lower_body_style_rmse_rad": 0.08067014068365097,
        "reference_compatibility_mean": 0.8328490572072393,
        "joint_acceleration_rms_rad_s2": 57.09867858886719,
        "box_relative_translation_drift_max_m": 0.03574943590684765,
        "box_relative_rotation_drift_max_rad": 0.05483892789831749
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.0939895436167717,
        "lower_body_style_rmse_rad": 0.07850857079029083,
        "reference_compatibility_mean": 0.8477834264247524,
        "joint_acceleration_rms_rad_s2": 57.12913131713867,
        "box_relative_translation_drift_max_m": 0.03568933432773704,
        "box_relative_rotation_drift_max_rad": 0.06054905550282334
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.09470835328102112,
        "lower_body_style_rmse_rad": 0.08018212020397186,
        "reference_compatibility_mean": 0.8384070901227478,
        "joint_acceleration_rms_rad_s2": 56.90859603881836,
        "box_relative_translation_drift_max_m": 0.03650817741732428,
        "box_relative_rotation_drift_max_rad": 0.06005958273744299
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.09499478340148926,
        "lower_body_style_rmse_rad": 0.0804307609796524,
        "reference_compatibility_mean": 0.8408584794737193,
        "joint_acceleration_rms_rad_s2": 56.822509765625,
        "box_relative_translation_drift_max_m": 0.03617684134993382,
        "box_relative_rotation_drift_max_rad": 0.06167756271421841
      }
    ],
    "clip_1_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.09400060772895813,
        "lower_body_style_rmse_rad": 0.07845460623502731,
        "reference_compatibility_mean": 0.8491031983012624,
        "joint_acceleration_rms_rad_s2": 56.53070831298828,
        "box_relative_translation_drift_max_m": 0.03431299297353861,
        "box_relative_rotation_drift_max_rad": 0.05778760579569427
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.09424236416816711,
        "lower_body_style_rmse_rad": 0.08022487163543701,
        "reference_compatibility_mean": 0.8385525031189843,
        "joint_acceleration_rms_rad_s2": 57.338016510009766,
        "box_relative_translation_drift_max_m": 0.03594023009757873,
        "box_relative_rotation_drift_max_rad": 0.06171015076694998
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.09422413259744644,
        "lower_body_style_rmse_rad": 0.08015141636133194,
        "reference_compatibility_mean": 0.8447402160535897,
        "joint_acceleration_rms_rad_s2": 56.76415252685547,
        "box_relative_translation_drift_max_m": 0.03466352614028358,
        "box_relative_rotation_drift_max_rad": 0.05762200408381073
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.09473443031311035,
        "lower_body_style_rmse_rad": 0.08046065270900726,
        "reference_compatibility_mean": 0.8386225547096204,
        "joint_acceleration_rms_rad_s2": 56.97734451293945,
        "box_relative_translation_drift_max_m": 0.036719503156906974,
        "box_relative_rotation_drift_max_rad": 0.056106072399803926
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.09498657286167145,
        "lower_body_style_rmse_rad": 0.0802278146147728,
        "reference_compatibility_mean": 0.835047827720613,
        "joint_acceleration_rms_rad_s2": 56.38440704345703,
        "box_relative_translation_drift_max_m": 0.036690594546705174,
        "box_relative_rotation_drift_max_rad": 0.061419187425554266
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.0947718694806099,
        "lower_body_style_rmse_rad": 0.08018273860216141,
        "reference_compatibility_mean": 0.8373796490507223,
        "joint_acceleration_rms_rad_s2": 56.363590240478516,
        "box_relative_translation_drift_max_m": 0.035262976891045766,
        "box_relative_rotation_drift_max_rad": 0.05597101619630856
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.09507008641958237,
        "lower_body_style_rmse_rad": 0.08066607266664505,
        "reference_compatibility_mean": 0.8330086602994772,
        "joint_acceleration_rms_rad_s2": 57.04839324951172,
        "box_relative_translation_drift_max_m": 0.03576517676837639,
        "box_relative_rotation_drift_max_rad": 0.054822370965796556
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.09384393692016602,
        "lower_body_style_rmse_rad": 0.07845532149076462,
        "reference_compatibility_mean": 0.8494778944083914,
        "joint_acceleration_rms_rad_s2": 56.226051330566406,
        "box_relative_translation_drift_max_m": 0.035439208121692434,
        "box_relative_rotation_drift_max_rad": 0.06301252730563636
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.09473246335983276,
        "lower_body_style_rmse_rad": 0.08019739389419556,
        "reference_compatibility_mean": 0.8378381283402122,
        "joint_acceleration_rms_rad_s2": 56.94939422607422,
        "box_relative_translation_drift_max_m": 0.03649514347165617,
        "box_relative_rotation_drift_max_rad": 0.060027243689935096
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.09499136358499527,
        "lower_body_style_rmse_rad": 0.08042746782302856,
        "reference_compatibility_mean": 0.8406008678085748,
        "joint_acceleration_rms_rad_s2": 56.91020202636719,
        "box_relative_translation_drift_max_m": 0.036173982002322386,
        "box_relative_rotation_drift_max_rad": 0.06165282605248557
      }
    ]
  },
  "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795200095046815929": {
    "clip_0_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.08868023008108139,
        "lower_body_style_rmse_rad": 0.08578519523143768,
        "reference_compatibility_mean": 0.707190547766231,
        "joint_acceleration_rms_rad_s2": 53.292877197265625,
        "box_relative_translation_drift_max_m": 0.04719240196345932,
        "box_relative_rotation_drift_max_rad": 0.12192208531436034
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.08881564438343048,
        "lower_body_style_rmse_rad": 0.08443198353052139,
        "reference_compatibility_mean": 0.7110682912677379,
        "joint_acceleration_rms_rad_s2": 53.34371566772461,
        "box_relative_translation_drift_max_m": 0.04763401387361537,
        "box_relative_rotation_drift_max_rad": 0.1194144762653361
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.08877366036176682,
        "lower_body_style_rmse_rad": 0.08524370938539505,
        "reference_compatibility_mean": 0.7098269201861356,
        "joint_acceleration_rms_rad_s2": 53.3280143737793,
        "box_relative_translation_drift_max_m": 0.04736654427699675,
        "box_relative_rotation_drift_max_rad": 0.12057133937020971
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.0896906927227974,
        "lower_body_style_rmse_rad": 0.08655048906803131,
        "reference_compatibility_mean": 0.7038009925235723,
        "joint_acceleration_rms_rad_s2": 53.04280471801758,
        "box_relative_translation_drift_max_m": 0.04773222937378638,
        "box_relative_rotation_drift_max_rad": 0.11334325095182454
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.08964751660823822,
        "lower_body_style_rmse_rad": 0.08679009228944778,
        "reference_compatibility_mean": 0.7076752655067544,
        "joint_acceleration_rms_rad_s2": 53.07553482055664,
        "box_relative_translation_drift_max_m": 0.04956992921021999,
        "box_relative_rotation_drift_max_rad": 0.12080759959196086
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.08932546526193619,
        "lower_body_style_rmse_rad": 0.08663929998874664,
        "reference_compatibility_mean": 0.7038151590741774,
        "joint_acceleration_rms_rad_s2": 53.265872955322266,
        "box_relative_translation_drift_max_m": 0.049016569302059276,
        "box_relative_rotation_drift_max_rad": 0.12223111808615171
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.09012428671121597,
        "lower_body_style_rmse_rad": 0.08734742552042007,
        "reference_compatibility_mean": 0.7015813951893396,
        "joint_acceleration_rms_rad_s2": 52.91976547241211,
        "box_relative_translation_drift_max_m": 0.048051073130155886,
        "box_relative_rotation_drift_max_rad": 0.11179220320949496
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.08869985491037369,
        "lower_body_style_rmse_rad": 0.0855841338634491,
        "reference_compatibility_mean": 0.7106338484671352,
        "joint_acceleration_rms_rad_s2": 53.466678619384766,
        "box_relative_translation_drift_max_m": 0.04764114401609405,
        "box_relative_rotation_drift_max_rad": 0.12054274223155503
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.08969666808843613,
        "lower_body_style_rmse_rad": 0.08716163039207458,
        "reference_compatibility_mean": 0.7024943051158935,
        "joint_acceleration_rms_rad_s2": 53.07026672363281,
        "box_relative_translation_drift_max_m": 0.047511097454284376,
        "box_relative_rotation_drift_max_rad": 0.11210043595928824
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.08970881998538971,
        "lower_body_style_rmse_rad": 0.08662012964487076,
        "reference_compatibility_mean": 0.7015474417575216,
        "joint_acceleration_rms_rad_s2": 53.4918212890625,
        "box_relative_translation_drift_max_m": 0.049336734325107226,
        "box_relative_rotation_drift_max_rad": 0.12347894581444475
      }
    ],
    "clip_1_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.08893068879842758,
        "lower_body_style_rmse_rad": 0.08591820299625397,
        "reference_compatibility_mean": 0.6996842733842945,
        "joint_acceleration_rms_rad_s2": 53.6325798034668,
        "box_relative_translation_drift_max_m": 0.04718278830690006,
        "box_relative_rotation_drift_max_rad": 0.12217470152372686
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.08895882219076157,
        "lower_body_style_rmse_rad": 0.08612097799777985,
        "reference_compatibility_mean": 0.7016771807926961,
        "joint_acceleration_rms_rad_s2": 53.62617111206055,
        "box_relative_translation_drift_max_m": 0.04776777323376641,
        "box_relative_rotation_drift_max_rad": 0.11984269730807501
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.08878573030233383,
        "lower_body_style_rmse_rad": 0.08550482988357544,
        "reference_compatibility_mean": 0.7074520148048389,
        "joint_acceleration_rms_rad_s2": 53.414329528808594,
        "box_relative_translation_drift_max_m": 0.04733925945752948,
        "box_relative_rotation_drift_max_rad": 0.12057019874939125
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.08969566226005554,
        "lower_body_style_rmse_rad": 0.0865759402513504,
        "reference_compatibility_mean": 0.7036893168278685,
        "joint_acceleration_rms_rad_s2": 53.01761245727539,
        "box_relative_translation_drift_max_m": 0.04770580482832963,
        "box_relative_rotation_drift_max_rad": 0.1133967664395519
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.0896417498588562,
        "lower_body_style_rmse_rad": 0.08677610754966736,
        "reference_compatibility_mean": 0.7082099196191232,
        "joint_acceleration_rms_rad_s2": 53.063255310058594,
        "box_relative_translation_drift_max_m": 0.049562755528770805,
        "box_relative_rotation_drift_max_rad": 0.12070671141402774
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.08934605866670609,
        "lower_body_style_rmse_rad": 0.08695323020219803,
        "reference_compatibility_mean": 0.7019031535208009,
        "joint_acceleration_rms_rad_s2": 53.31474304199219,
        "box_relative_translation_drift_max_m": 0.049086839885037675,
        "box_relative_rotation_drift_max_rad": 0.12160644394452555
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.09012234210968018,
        "lower_body_style_rmse_rad": 0.08728422969579697,
        "reference_compatibility_mean": 0.7014298330888552,
        "joint_acceleration_rms_rad_s2": 52.91096878051758,
        "box_relative_translation_drift_max_m": 0.048136886004653594,
        "box_relative_rotation_drift_max_rad": 0.11209271244286001
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.08894552290439606,
        "lower_body_style_rmse_rad": 0.08575496077537537,
        "reference_compatibility_mean": 0.7019415625299175,
        "joint_acceleration_rms_rad_s2": 53.66243362426758,
        "box_relative_translation_drift_max_m": 0.047642774783090855,
        "box_relative_rotation_drift_max_rad": 0.12075726317353398
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.08967667818069458,
        "lower_body_style_rmse_rad": 0.0871628075838089,
        "reference_compatibility_mean": 0.7027199531498246,
        "joint_acceleration_rms_rad_s2": 53.08304977416992,
        "box_relative_translation_drift_max_m": 0.047569878211320166,
        "box_relative_rotation_drift_max_rad": 0.11262292851028055
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.0897032618522644,
        "lower_body_style_rmse_rad": 0.08661308139562607,
        "reference_compatibility_mean": 0.7018538588850973,
        "joint_acceleration_rms_rad_s2": 53.50558853149414,
        "box_relative_translation_drift_max_m": 0.049307675638120614,
        "box_relative_rotation_drift_max_rad": 0.12349899300075493
      }
    ]
  },
  "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795192603809404020": {
    "clip_0_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.08981374651193619,
        "lower_body_style_rmse_rad": 0.07775221765041351,
        "reference_compatibility_mean": 0.751727549507645,
        "joint_acceleration_rms_rad_s2": 53.07354736328125,
        "box_relative_translation_drift_max_m": 0.047740986376051564,
        "box_relative_rotation_drift_max_rad": 0.10315049308946385
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.09000102430582047,
        "lower_body_style_rmse_rad": 0.07793334126472473,
        "reference_compatibility_mean": 0.7536819326457128,
        "joint_acceleration_rms_rad_s2": 52.71077346801758,
        "box_relative_translation_drift_max_m": 0.04762630723704309,
        "box_relative_rotation_drift_max_rad": 0.0965634271677724
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.08967989683151245,
        "lower_body_style_rmse_rad": 0.07737059891223907,
        "reference_compatibility_mean": 0.755692801065134,
        "joint_acceleration_rms_rad_s2": 52.77716827392578,
        "box_relative_translation_drift_max_m": 0.0477085211582501,
        "box_relative_rotation_drift_max_rad": 0.10242688705403276
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.09082470089197159,
        "lower_body_style_rmse_rad": 0.07907566428184509,
        "reference_compatibility_mean": 0.7517444584518421,
        "joint_acceleration_rms_rad_s2": 52.830509185791016,
        "box_relative_translation_drift_max_m": 0.04953766966155477,
        "box_relative_rotation_drift_max_rad": 0.10016437830316251
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.09098700433969498,
        "lower_body_style_rmse_rad": 0.07768414169549942,
        "reference_compatibility_mean": 0.7539482701078895,
        "joint_acceleration_rms_rad_s2": 52.457557678222656,
        "box_relative_translation_drift_max_m": 0.04872446672574097,
        "box_relative_rotation_drift_max_rad": 0.09559934410272972
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.09076085686683655,
        "lower_body_style_rmse_rad": 0.07742659747600555,
        "reference_compatibility_mean": 0.7573693006814535,
        "joint_acceleration_rms_rad_s2": 52.48493194580078,
        "box_relative_translation_drift_max_m": 0.04828843079675397,
        "box_relative_rotation_drift_max_rad": 0.09670115261271733
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.09103047102689743,
        "lower_body_style_rmse_rad": 0.07732689380645752,
        "reference_compatibility_mean": 0.7532971104879927,
        "joint_acceleration_rms_rad_s2": 52.723915100097656,
        "box_relative_translation_drift_max_m": 0.04922970460542268,
        "box_relative_rotation_drift_max_rad": 0.09943361525589
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.08990126103162766,
        "lower_body_style_rmse_rad": 0.07770375907421112,
        "reference_compatibility_mean": 0.7521300405953052,
        "joint_acceleration_rms_rad_s2": 53.01988220214844,
        "box_relative_translation_drift_max_m": 0.04801954702484443,
        "box_relative_rotation_drift_max_rad": 0.10083576070144315
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.09117966145277023,
        "lower_body_style_rmse_rad": 0.08164554089307785,
        "reference_compatibility_mean": 0.7397318944995254,
        "joint_acceleration_rms_rad_s2": 52.933807373046875,
        "box_relative_translation_drift_max_m": 0.048916688574510835,
        "box_relative_rotation_drift_max_rad": 0.09729447717774263
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.09083215147256851,
        "lower_body_style_rmse_rad": 0.07905671000480652,
        "reference_compatibility_mean": 0.7503183942743546,
        "joint_acceleration_rms_rad_s2": 53.09334945678711,
        "box_relative_translation_drift_max_m": 0.048926848434299335,
        "box_relative_rotation_drift_max_rad": 0.10195014023010086
      }
    ],
    "clip_1_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.08980999886989594,
        "lower_body_style_rmse_rad": 0.07775578647851944,
        "reference_compatibility_mean": 0.7517244981716197,
        "joint_acceleration_rms_rad_s2": 53.13825988769531,
        "box_relative_translation_drift_max_m": 0.04773262197916496,
        "box_relative_rotation_drift_max_rad": 0.1031792345517937
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.09002454578876495,
        "lower_body_style_rmse_rad": 0.07792249321937561,
        "reference_compatibility_mean": 0.7536836846543296,
        "joint_acceleration_rms_rad_s2": 52.6555061340332,
        "box_relative_translation_drift_max_m": 0.04754844556389285,
        "box_relative_rotation_drift_max_rad": 0.09555931999845678
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.09005653113126755,
        "lower_body_style_rmse_rad": 0.07979672402143478,
        "reference_compatibility_mean": 0.7489986190400841,
        "joint_acceleration_rms_rad_s2": 52.73999786376953,
        "box_relative_translation_drift_max_m": 0.0480435819692851,
        "box_relative_rotation_drift_max_rad": 0.09851811381690646
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.09085305780172348,
        "lower_body_style_rmse_rad": 0.07908184826374054,
        "reference_compatibility_mean": 0.750898958414521,
        "joint_acceleration_rms_rad_s2": 52.850563049316406,
        "box_relative_translation_drift_max_m": 0.04959803004060492,
        "box_relative_rotation_drift_max_rad": 0.10010479480262205
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.09102770686149597,
        "lower_body_style_rmse_rad": 0.07770824432373047,
        "reference_compatibility_mean": 0.7530743339445388,
        "joint_acceleration_rms_rad_s2": 52.48530578613281,
        "box_relative_translation_drift_max_m": 0.04879290702062866,
        "box_relative_rotation_drift_max_rad": 0.09577202018209406
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.09074588119983673,
        "lower_body_style_rmse_rad": 0.07743914425373077,
        "reference_compatibility_mean": 0.7563792395733373,
        "joint_acceleration_rms_rad_s2": 52.5360221862793,
        "box_relative_translation_drift_max_m": 0.04851811320764955,
        "box_relative_rotation_drift_max_rad": 0.09667614674729803
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.09107823669910431,
        "lower_body_style_rmse_rad": 0.0773630365729332,
        "reference_compatibility_mean": 0.7522366194557127,
        "joint_acceleration_rms_rad_s2": 52.76997375488281,
        "box_relative_translation_drift_max_m": 0.04924673580119412,
        "box_relative_rotation_drift_max_rad": 0.09965112533844324
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.08988044410943985,
        "lower_body_style_rmse_rad": 0.077713742852211,
        "reference_compatibility_mean": 0.7522115922391304,
        "joint_acceleration_rms_rad_s2": 52.97256851196289,
        "box_relative_translation_drift_max_m": 0.0478693779429057,
        "box_relative_rotation_drift_max_rad": 0.10130898716027649
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.09118667989969254,
        "lower_body_style_rmse_rad": 0.08164048939943314,
        "reference_compatibility_mean": 0.7396381437717154,
        "joint_acceleration_rms_rad_s2": 52.90324401855469,
        "box_relative_translation_drift_max_m": 0.048932769999856206,
        "box_relative_rotation_drift_max_rad": 0.09724562889278758
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.09078831970691681,
        "lower_body_style_rmse_rad": 0.07903413474559784,
        "reference_compatibility_mean": 0.7512475718405083,
        "joint_acceleration_rms_rad_s2": 53.0134391784668,
        "box_relative_translation_drift_max_m": 0.04887339265067755,
        "box_relative_rotation_drift_max_rad": 0.10205405193197928
      }
    ]
  },
  "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795176993127086405": {
    "clip_0_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.10562381893396378,
        "lower_body_style_rmse_rad": 0.06561952829360962,
        "reference_compatibility_mean": 0.8663001563748356,
        "joint_acceleration_rms_rad_s2": 65.26625061035156,
        "box_relative_translation_drift_max_m": 0.054177456209774016,
        "box_relative_rotation_drift_max_rad": 0.04349649478615422
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.10581427812576294,
        "lower_body_style_rmse_rad": 0.0680929496884346,
        "reference_compatibility_mean": 0.8585197611725688,
        "joint_acceleration_rms_rad_s2": 64.73358154296875,
        "box_relative_translation_drift_max_m": 0.05418649862606618,
        "box_relative_rotation_drift_max_rad": 0.0462353600247447
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.10565996170043945,
        "lower_body_style_rmse_rad": 0.0656748116016388,
        "reference_compatibility_mean": 0.8634093070251909,
        "joint_acceleration_rms_rad_s2": 65.15270233154297,
        "box_relative_translation_drift_max_m": 0.05458945137906955,
        "box_relative_rotation_drift_max_rad": 0.04534624777980132
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.1067960113286972,
        "lower_body_style_rmse_rad": 0.06715160608291626,
        "reference_compatibility_mean": 0.863161527318576,
        "joint_acceleration_rms_rad_s2": 63.841007232666016,
        "box_relative_translation_drift_max_m": 0.05855884117336023,
        "box_relative_rotation_drift_max_rad": 0.05630528445910562
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.10713247209787369,
        "lower_body_style_rmse_rad": 0.06699303537607193,
        "reference_compatibility_mean": 0.860819654539713,
        "joint_acceleration_rms_rad_s2": 63.83433151245117,
        "box_relative_translation_drift_max_m": 0.056408444272591965,
        "box_relative_rotation_drift_max_rad": 0.05607842532063081
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.10670141875743866,
        "lower_body_style_rmse_rad": 0.06579013168811798,
        "reference_compatibility_mean": 0.8698356725188342,
        "joint_acceleration_rms_rad_s2": 64.0269775390625,
        "box_relative_translation_drift_max_m": 0.05585024923009795,
        "box_relative_rotation_drift_max_rad": 0.05345840287509956
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.10745221376419067,
        "lower_body_style_rmse_rad": 0.06924265623092651,
        "reference_compatibility_mean": 0.8532540569345988,
        "joint_acceleration_rms_rad_s2": 64.21184539794922,
        "box_relative_translation_drift_max_m": 0.05826977431253009,
        "box_relative_rotation_drift_max_rad": 0.057870661948306444
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.10555500537157059,
        "lower_body_style_rmse_rad": 0.0655776634812355,
        "reference_compatibility_mean": 0.8663171670855329,
        "joint_acceleration_rms_rad_s2": 65.38904571533203,
        "box_relative_translation_drift_max_m": 0.05428734410347579,
        "box_relative_rotation_drift_max_rad": 0.04504601016907981
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.10687068104743958,
        "lower_body_style_rmse_rad": 0.0688944086432457,
        "reference_compatibility_mean": 0.8570346666183488,
        "joint_acceleration_rms_rad_s2": 64.36439514160156,
        "box_relative_translation_drift_max_m": 0.05602449313182169,
        "box_relative_rotation_drift_max_rad": 0.05544288791836919
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.10715996474027634,
        "lower_body_style_rmse_rad": 0.06611242890357971,
        "reference_compatibility_mean": 0.8689494525941187,
        "joint_acceleration_rms_rad_s2": 64.45350646972656,
        "box_relative_translation_drift_max_m": 0.05629409124925051,
        "box_relative_rotation_drift_max_rad": 0.053838038382473606
      }
    ],
    "clip_1_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.10560762882232666,
        "lower_body_style_rmse_rad": 0.06559325009584427,
        "reference_compatibility_mean": 0.8668356280112823,
        "joint_acceleration_rms_rad_s2": 65.28386688232422,
        "box_relative_translation_drift_max_m": 0.05410726937018291,
        "box_relative_rotation_drift_max_rad": 0.04347526812445328
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.10580714046955109,
        "lower_body_style_rmse_rad": 0.06809844076633453,
        "reference_compatibility_mean": 0.8585214682369008,
        "joint_acceleration_rms_rad_s2": 64.68985748291016,
        "box_relative_translation_drift_max_m": 0.05418574043693778,
        "box_relative_rotation_drift_max_rad": 0.046222824888735733
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.10562319308519363,
        "lower_body_style_rmse_rad": 0.0656537339091301,
        "reference_compatibility_mean": 0.8635025886379557,
        "joint_acceleration_rms_rad_s2": 65.0098648071289,
        "box_relative_translation_drift_max_m": 0.054430761254780545,
        "box_relative_rotation_drift_max_rad": 0.04537686783930297
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.10676980018615723,
        "lower_body_style_rmse_rad": 0.06714648753404617,
        "reference_compatibility_mean": 0.8633427245235448,
        "joint_acceleration_rms_rad_s2": 63.86875534057617,
        "box_relative_translation_drift_max_m": 0.05843746022924355,
        "box_relative_rotation_drift_max_rad": 0.05627609764519523
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.10713782161474228,
        "lower_body_style_rmse_rad": 0.06713808327913284,
        "reference_compatibility_mean": 0.8607979149668422,
        "joint_acceleration_rms_rad_s2": 63.78030776977539,
        "box_relative_translation_drift_max_m": 0.05639857697364608,
        "box_relative_rotation_drift_max_rad": 0.05606917930238977
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.1066809743642807,
        "lower_body_style_rmse_rad": 0.06576725840568542,
        "reference_compatibility_mean": 0.8704108053572247,
        "joint_acceleration_rms_rad_s2": 63.89105987548828,
        "box_relative_translation_drift_max_m": 0.05578296725582147,
        "box_relative_rotation_drift_max_rad": 0.05323857712105001
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.107465460896492,
        "lower_body_style_rmse_rad": 0.06924315541982651,
        "reference_compatibility_mean": 0.8532087382026227,
        "joint_acceleration_rms_rad_s2": 64.15711975097656,
        "box_relative_translation_drift_max_m": 0.058179932009763964,
        "box_relative_rotation_drift_max_rad": 0.057852507359992984
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.10553135722875595,
        "lower_body_style_rmse_rad": 0.06557503342628479,
        "reference_compatibility_mean": 0.8661575012126003,
        "joint_acceleration_rms_rad_s2": 65.4071044921875,
        "box_relative_translation_drift_max_m": 0.05422314882183278,
        "box_relative_rotation_drift_max_rad": 0.04514221806217381
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.10686943680047989,
        "lower_body_style_rmse_rad": 0.06888800114393234,
        "reference_compatibility_mean": 0.8569812618551887,
        "joint_acceleration_rms_rad_s2": 64.37895202636719,
        "box_relative_translation_drift_max_m": 0.055997732530338844,
        "box_relative_rotation_drift_max_rad": 0.05545450064583095
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.10718817263841629,
        "lower_body_style_rmse_rad": 0.06612040847539902,
        "reference_compatibility_mean": 0.8690837930059112,
        "joint_acceleration_rms_rad_s2": 64.4566879272461,
        "box_relative_translation_drift_max_m": 0.0563242075633194,
        "box_relative_rotation_drift_max_rad": 0.053836142345718034
      }
    ]
  },
  "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795229296945062893": {
    "clip_0_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.09874150156974792,
        "lower_body_style_rmse_rad": 0.0959266871213913,
        "reference_compatibility_mean": 0.6363791902757029,
        "joint_acceleration_rms_rad_s2": 59.58608627319336,
        "box_relative_translation_drift_max_m": 0.03314759387061163,
        "box_relative_rotation_drift_max_rad": 0.060760640921215664
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.09871769696474075,
        "lower_body_style_rmse_rad": 0.09523235261440277,
        "reference_compatibility_mean": 0.6368817052162336,
        "joint_acceleration_rms_rad_s2": 60.19906997680664,
        "box_relative_translation_drift_max_m": 0.03287973090428203,
        "box_relative_rotation_drift_max_rad": 0.05569058468502436
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.09823205322027206,
        "lower_body_style_rmse_rad": 0.09448020160198212,
        "reference_compatibility_mean": 0.6488884456545219,
        "joint_acceleration_rms_rad_s2": 58.23128890991211,
        "box_relative_translation_drift_max_m": 0.03279442843770626,
        "box_relative_rotation_drift_max_rad": 0.05701977508411719
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.09872220456600189,
        "lower_body_style_rmse_rad": 0.09485328942537308,
        "reference_compatibility_mean": 0.6417187052108119,
        "joint_acceleration_rms_rad_s2": 60.704036712646484,
        "box_relative_translation_drift_max_m": 0.03521948991363849,
        "box_relative_rotation_drift_max_rad": 0.05459699574800964
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.09886150062084198,
        "lower_body_style_rmse_rad": 0.09504920989274979,
        "reference_compatibility_mean": 0.6393449768810815,
        "joint_acceleration_rms_rad_s2": 58.129459381103516,
        "box_relative_translation_drift_max_m": 0.03386302094196484,
        "box_relative_rotation_drift_max_rad": 0.05412080276329279
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.0988282710313797,
        "lower_body_style_rmse_rad": 0.09504223614931107,
        "reference_compatibility_mean": 0.6381716527165555,
        "joint_acceleration_rms_rad_s2": 57.763736724853516,
        "box_relative_translation_drift_max_m": 0.03410826123323718,
        "box_relative_rotation_drift_max_rad": 0.05786224636384573
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.09879080951213837,
        "lower_body_style_rmse_rad": 0.09543541818857193,
        "reference_compatibility_mean": 0.639484620056322,
        "joint_acceleration_rms_rad_s2": 58.0561637878418,
        "box_relative_translation_drift_max_m": 0.03483544355422907,
        "box_relative_rotation_drift_max_rad": 0.05564754676533931
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.09864845871925354,
        "lower_body_style_rmse_rad": 0.09595590084791183,
        "reference_compatibility_mean": 0.6371323263494432,
        "joint_acceleration_rms_rad_s2": 59.2296257019043,
        "box_relative_translation_drift_max_m": 0.033641113802859064,
        "box_relative_rotation_drift_max_rad": 0.05996859021263151
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.09859149158000946,
        "lower_body_style_rmse_rad": 0.09517169743776321,
        "reference_compatibility_mean": 0.633797877796721,
        "joint_acceleration_rms_rad_s2": 58.02432632446289,
        "box_relative_translation_drift_max_m": 0.0336301584249952,
        "box_relative_rotation_drift_max_rad": 0.052532191164769274
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.0994972363114357,
        "lower_body_style_rmse_rad": 0.09557846933603287,
        "reference_compatibility_mean": 0.6304465810499624,
        "joint_acceleration_rms_rad_s2": 58.720096588134766,
        "box_relative_translation_drift_max_m": 0.03339841646047181,
        "box_relative_rotation_drift_max_rad": 0.053465178828948176
      }
    ],
    "clip_1_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.09873007982969284,
        "lower_body_style_rmse_rad": 0.09592034667730331,
        "reference_compatibility_mean": 0.636006611227912,
        "joint_acceleration_rms_rad_s2": 59.4461669921875,
        "box_relative_translation_drift_max_m": 0.033165339438536626,
        "box_relative_rotation_drift_max_rad": 0.06041702908339844
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.09872520714998245,
        "lower_body_style_rmse_rad": 0.09522853046655655,
        "reference_compatibility_mean": 0.636781413345964,
        "joint_acceleration_rms_rad_s2": 60.18624496459961,
        "box_relative_translation_drift_max_m": 0.03285496361269831,
        "box_relative_rotation_drift_max_rad": 0.05552004730267571
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.09874261170625687,
        "lower_body_style_rmse_rad": 0.09536014497280121,
        "reference_compatibility_mean": 0.6366987726838658,
        "joint_acceleration_rms_rad_s2": 58.94895935058594,
        "box_relative_translation_drift_max_m": 0.03320746074143276,
        "box_relative_rotation_drift_max_rad": 0.0584474260311562
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.09869890660047531,
        "lower_body_style_rmse_rad": 0.0948580875992775,
        "reference_compatibility_mean": 0.6419883462151359,
        "joint_acceleration_rms_rad_s2": 60.520103454589844,
        "box_relative_translation_drift_max_m": 0.035261821771555416,
        "box_relative_rotation_drift_max_rad": 0.053550840953062055
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.0989927127957344,
        "lower_body_style_rmse_rad": 0.09506805986166,
        "reference_compatibility_mean": 0.6373706072026776,
        "joint_acceleration_rms_rad_s2": 57.9517707824707,
        "box_relative_translation_drift_max_m": 0.03385493177358372,
        "box_relative_rotation_drift_max_rad": 0.054241012244298184
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.09889234602451324,
        "lower_body_style_rmse_rad": 0.095246821641922,
        "reference_compatibility_mean": 0.6369621211867994,
        "joint_acceleration_rms_rad_s2": 57.38284683227539,
        "box_relative_translation_drift_max_m": 0.03402306704416483,
        "box_relative_rotation_drift_max_rad": 0.05806693167138005
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.09892185777425766,
        "lower_body_style_rmse_rad": 0.09545135498046875,
        "reference_compatibility_mean": 0.6361843263294938,
        "joint_acceleration_rms_rad_s2": 58.21357345581055,
        "box_relative_translation_drift_max_m": 0.034753419155427095,
        "box_relative_rotation_drift_max_rad": 0.055309850976504246
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.0986887663602829,
        "lower_body_style_rmse_rad": 0.09537699818611145,
        "reference_compatibility_mean": 0.6371996095337628,
        "joint_acceleration_rms_rad_s2": 59.28016662597656,
        "box_relative_translation_drift_max_m": 0.03345151393816789,
        "box_relative_rotation_drift_max_rad": 0.05878868494026451
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.09916343539953232,
        "lower_body_style_rmse_rad": 0.09610174596309662,
        "reference_compatibility_mean": 0.6233289927210127,
        "joint_acceleration_rms_rad_s2": 58.57809829711914,
        "box_relative_translation_drift_max_m": 0.03332782604636687,
        "box_relative_rotation_drift_max_rad": 0.05399615349746287
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.09911441057920456,
        "lower_body_style_rmse_rad": 0.09551987797021866,
        "reference_compatibility_mean": 0.6391205105299017,
        "joint_acceleration_rms_rad_s2": 58.3778190612793,
        "box_relative_translation_drift_max_m": 0.03346071459768781,
        "box_relative_rotation_drift_max_rad": 0.05438368662058178
      }
    ]
  },
  "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795161406155359032": {
    "clip_0_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.1011236310005188,
        "lower_body_style_rmse_rad": 0.07091598957777023,
        "reference_compatibility_mean": 0.8916152402312975,
        "joint_acceleration_rms_rad_s2": 35.44654846191406,
        "box_relative_translation_drift_max_m": 0.055032013139381546,
        "box_relative_rotation_drift_max_rad": 0.0577934280140449
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.10118065774440765,
        "lower_body_style_rmse_rad": 0.06938589364290237,
        "reference_compatibility_mean": 0.8978695632190753,
        "joint_acceleration_rms_rad_s2": 35.460506439208984,
        "box_relative_translation_drift_max_m": 0.05526999823395054,
        "box_relative_rotation_drift_max_rad": 0.0576396737830099
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.10127242654561996,
        "lower_body_style_rmse_rad": 0.07040072977542877,
        "reference_compatibility_mean": 0.8913868134977714,
        "joint_acceleration_rms_rad_s2": 35.46141052246094,
        "box_relative_translation_drift_max_m": 0.055387622526558204,
        "box_relative_rotation_drift_max_rad": 0.057702098532900384
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.1026809960603714,
        "lower_body_style_rmse_rad": 0.06993930041790009,
        "reference_compatibility_mean": 0.8947683870789792,
        "joint_acceleration_rms_rad_s2": 35.41193389892578,
        "box_relative_translation_drift_max_m": 0.05582342089336574,
        "box_relative_rotation_drift_max_rad": 0.056288578996422096
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.10239977389574051,
        "lower_body_style_rmse_rad": 0.06987731158733368,
        "reference_compatibility_mean": 0.8960112054653229,
        "joint_acceleration_rms_rad_s2": 35.404476165771484,
        "box_relative_translation_drift_max_m": 0.05630313691592539,
        "box_relative_rotation_drift_max_rad": 0.056402919599480336
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.10195469111204147,
        "lower_body_style_rmse_rad": 0.06963054090738297,
        "reference_compatibility_mean": 0.8968813848439755,
        "joint_acceleration_rms_rad_s2": 35.16630554199219,
        "box_relative_translation_drift_max_m": 0.05567731253626865,
        "box_relative_rotation_drift_max_rad": 0.055434688010912815
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.10267283767461777,
        "lower_body_style_rmse_rad": 0.07017690688371658,
        "reference_compatibility_mean": 0.8968996933592539,
        "joint_acceleration_rms_rad_s2": 35.494327545166016,
        "box_relative_translation_drift_max_m": 0.05606714325953691,
        "box_relative_rotation_drift_max_rad": 0.05586839788136181
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.10106883943080902,
        "lower_body_style_rmse_rad": 0.06888579577207565,
        "reference_compatibility_mean": 0.8945554656795061,
        "joint_acceleration_rms_rad_s2": 35.451602935791016,
        "box_relative_translation_drift_max_m": 0.055003584079820984,
        "box_relative_rotation_drift_max_rad": 0.058193806118581604
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.10212024301290512,
        "lower_body_style_rmse_rad": 0.06975320726633072,
        "reference_compatibility_mean": 0.8929567264311775,
        "joint_acceleration_rms_rad_s2": 35.37553405761719,
        "box_relative_translation_drift_max_m": 0.05554324268456987,
        "box_relative_rotation_drift_max_rad": 0.05577375390653555
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.1025315672159195,
        "lower_body_style_rmse_rad": 0.07125764340162277,
        "reference_compatibility_mean": 0.8893355464147215,
        "joint_acceleration_rms_rad_s2": 35.46196365356445,
        "box_relative_translation_drift_max_m": 0.056141880787567815,
        "box_relative_rotation_drift_max_rad": 0.05334515468737263
      }
    ],
    "clip_1_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.10112810134887695,
        "lower_body_style_rmse_rad": 0.07078329473733902,
        "reference_compatibility_mean": 0.8922674070849499,
        "joint_acceleration_rms_rad_s2": 35.4002799987793,
        "box_relative_translation_drift_max_m": 0.05500582950432958,
        "box_relative_rotation_drift_max_rad": 0.057817870604326756
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.10116524249315262,
        "lower_body_style_rmse_rad": 0.06936813145875931,
        "reference_compatibility_mean": 0.8983877347516275,
        "joint_acceleration_rms_rad_s2": 35.437095642089844,
        "box_relative_translation_drift_max_m": 0.05521471095620653,
        "box_relative_rotation_drift_max_rad": 0.05741072127008877
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.10128884762525558,
        "lower_body_style_rmse_rad": 0.07042166590690613,
        "reference_compatibility_mean": 0.8913291012966844,
        "joint_acceleration_rms_rad_s2": 35.418277740478516,
        "box_relative_translation_drift_max_m": 0.055345358991513806,
        "box_relative_rotation_drift_max_rad": 0.05769765779039082
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.10268091410398483,
        "lower_body_style_rmse_rad": 0.06997094303369522,
        "reference_compatibility_mean": 0.8945481717540271,
        "joint_acceleration_rms_rad_s2": 35.24541473388672,
        "box_relative_translation_drift_max_m": 0.05575785314101226,
        "box_relative_rotation_drift_max_rad": 0.056331909176344244
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.1024090051651001,
        "lower_body_style_rmse_rad": 0.06996136158704758,
        "reference_compatibility_mean": 0.8958861527228066,
        "joint_acceleration_rms_rad_s2": 35.47512435913086,
        "box_relative_translation_drift_max_m": 0.05604262115962388,
        "box_relative_rotation_drift_max_rad": 0.0570354416449782
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.10193710774183273,
        "lower_body_style_rmse_rad": 0.06974803656339645,
        "reference_compatibility_mean": 0.8966164223177925,
        "joint_acceleration_rms_rad_s2": 35.24787902832031,
        "box_relative_translation_drift_max_m": 0.055672686363275804,
        "box_relative_rotation_drift_max_rad": 0.0556883922628906
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.10267023742198944,
        "lower_body_style_rmse_rad": 0.07015026360750198,
        "reference_compatibility_mean": 0.8969182810504648,
        "joint_acceleration_rms_rad_s2": 35.54161071777344,
        "box_relative_translation_drift_max_m": 0.05630709631957172,
        "box_relative_rotation_drift_max_rad": 0.055799864114629956
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.10104888677597046,
        "lower_body_style_rmse_rad": 0.06887713074684143,
        "reference_compatibility_mean": 0.8946126843867749,
        "joint_acceleration_rms_rad_s2": 35.441864013671875,
        "box_relative_translation_drift_max_m": 0.0549970878861285,
        "box_relative_rotation_drift_max_rad": 0.05811983593503357
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.10213208198547363,
        "lower_body_style_rmse_rad": 0.0695912092924118,
        "reference_compatibility_mean": 0.89304133280671,
        "joint_acceleration_rms_rad_s2": 35.367801666259766,
        "box_relative_translation_drift_max_m": 0.05554431753064702,
        "box_relative_rotation_drift_max_rad": 0.05594884957510276
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.10254174470901489,
        "lower_body_style_rmse_rad": 0.07136812806129456,
        "reference_compatibility_mean": 0.8885135512515283,
        "joint_acceleration_rms_rad_s2": 35.5484733581543,
        "box_relative_translation_drift_max_m": 0.05612691031137436,
        "box_relative_rotation_drift_max_rad": 0.05343115292379399
      }
    ]
  },
  "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795229309593863029": {
    "clip_0_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.1011236310005188,
        "lower_body_style_rmse_rad": 0.07091598957777023,
        "reference_compatibility_mean": 0.8916152402312975,
        "joint_acceleration_rms_rad_s2": 35.44654846191406,
        "box_relative_translation_drift_max_m": 0.055032013139381546,
        "box_relative_rotation_drift_max_rad": 0.0577934280140449
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.10118065774440765,
        "lower_body_style_rmse_rad": 0.06938589364290237,
        "reference_compatibility_mean": 0.8978695632190753,
        "joint_acceleration_rms_rad_s2": 35.460506439208984,
        "box_relative_translation_drift_max_m": 0.05526999823395054,
        "box_relative_rotation_drift_max_rad": 0.0576396737830099
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.10127242654561996,
        "lower_body_style_rmse_rad": 0.07040072977542877,
        "reference_compatibility_mean": 0.8913868134977714,
        "joint_acceleration_rms_rad_s2": 35.46141052246094,
        "box_relative_translation_drift_max_m": 0.055387622526558204,
        "box_relative_rotation_drift_max_rad": 0.057702098532900384
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.1026809960603714,
        "lower_body_style_rmse_rad": 0.06993930041790009,
        "reference_compatibility_mean": 0.8947683870789792,
        "joint_acceleration_rms_rad_s2": 35.41193389892578,
        "box_relative_translation_drift_max_m": 0.05582342089336574,
        "box_relative_rotation_drift_max_rad": 0.056288578996422096
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.10239977389574051,
        "lower_body_style_rmse_rad": 0.06987731158733368,
        "reference_compatibility_mean": 0.8960112054653229,
        "joint_acceleration_rms_rad_s2": 35.404476165771484,
        "box_relative_translation_drift_max_m": 0.05630313691592539,
        "box_relative_rotation_drift_max_rad": 0.056402919599480336
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.10195469111204147,
        "lower_body_style_rmse_rad": 0.06963054090738297,
        "reference_compatibility_mean": 0.8968813848439755,
        "joint_acceleration_rms_rad_s2": 35.16630554199219,
        "box_relative_translation_drift_max_m": 0.05567731253626865,
        "box_relative_rotation_drift_max_rad": 0.055434688010912815
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.10267283767461777,
        "lower_body_style_rmse_rad": 0.07017690688371658,
        "reference_compatibility_mean": 0.8968996933592539,
        "joint_acceleration_rms_rad_s2": 35.494327545166016,
        "box_relative_translation_drift_max_m": 0.05606714325953691,
        "box_relative_rotation_drift_max_rad": 0.05586839788136181
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.10106883943080902,
        "lower_body_style_rmse_rad": 0.06888579577207565,
        "reference_compatibility_mean": 0.8945554656795061,
        "joint_acceleration_rms_rad_s2": 35.451602935791016,
        "box_relative_translation_drift_max_m": 0.055003584079820984,
        "box_relative_rotation_drift_max_rad": 0.058193806118581604
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.10212024301290512,
        "lower_body_style_rmse_rad": 0.06975320726633072,
        "reference_compatibility_mean": 0.8929567264311775,
        "joint_acceleration_rms_rad_s2": 35.37553405761719,
        "box_relative_translation_drift_max_m": 0.05554324268456987,
        "box_relative_rotation_drift_max_rad": 0.05577375390653555
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.1025315672159195,
        "lower_body_style_rmse_rad": 0.07125764340162277,
        "reference_compatibility_mean": 0.8893355464147215,
        "joint_acceleration_rms_rad_s2": 35.46196365356445,
        "box_relative_translation_drift_max_m": 0.056141880787567815,
        "box_relative_rotation_drift_max_rad": 0.05334515468737263
      }
    ],
    "clip_1_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.10112810134887695,
        "lower_body_style_rmse_rad": 0.07078329473733902,
        "reference_compatibility_mean": 0.8922674070849499,
        "joint_acceleration_rms_rad_s2": 35.4002799987793,
        "box_relative_translation_drift_max_m": 0.05500582950432958,
        "box_relative_rotation_drift_max_rad": 0.057817870604326756
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.10116524249315262,
        "lower_body_style_rmse_rad": 0.06936813145875931,
        "reference_compatibility_mean": 0.8983877347516275,
        "joint_acceleration_rms_rad_s2": 35.437095642089844,
        "box_relative_translation_drift_max_m": 0.05521471095620653,
        "box_relative_rotation_drift_max_rad": 0.05741072127008877
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.10128884762525558,
        "lower_body_style_rmse_rad": 0.07042166590690613,
        "reference_compatibility_mean": 0.8913291012966844,
        "joint_acceleration_rms_rad_s2": 35.418277740478516,
        "box_relative_translation_drift_max_m": 0.055345358991513806,
        "box_relative_rotation_drift_max_rad": 0.05769765779039082
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.10268091410398483,
        "lower_body_style_rmse_rad": 0.06997094303369522,
        "reference_compatibility_mean": 0.8945481717540271,
        "joint_acceleration_rms_rad_s2": 35.24541473388672,
        "box_relative_translation_drift_max_m": 0.05575785314101226,
        "box_relative_rotation_drift_max_rad": 0.056331909176344244
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.1024090051651001,
        "lower_body_style_rmse_rad": 0.06996136158704758,
        "reference_compatibility_mean": 0.8958861527228066,
        "joint_acceleration_rms_rad_s2": 35.47512435913086,
        "box_relative_translation_drift_max_m": 0.05604262115962388,
        "box_relative_rotation_drift_max_rad": 0.0570354416449782
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.10193710774183273,
        "lower_body_style_rmse_rad": 0.06974803656339645,
        "reference_compatibility_mean": 0.8966164223177925,
        "joint_acceleration_rms_rad_s2": 35.24787902832031,
        "box_relative_translation_drift_max_m": 0.055672686363275804,
        "box_relative_rotation_drift_max_rad": 0.0556883922628906
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.10267023742198944,
        "lower_body_style_rmse_rad": 0.07015026360750198,
        "reference_compatibility_mean": 0.8969182810504648,
        "joint_acceleration_rms_rad_s2": 35.54161071777344,
        "box_relative_translation_drift_max_m": 0.05630709631957172,
        "box_relative_rotation_drift_max_rad": 0.055799864114629956
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.10104888677597046,
        "lower_body_style_rmse_rad": 0.06887713074684143,
        "reference_compatibility_mean": 0.8946126843867749,
        "joint_acceleration_rms_rad_s2": 35.441864013671875,
        "box_relative_translation_drift_max_m": 0.0549970878861285,
        "box_relative_rotation_drift_max_rad": 0.05811983593503357
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.10213208198547363,
        "lower_body_style_rmse_rad": 0.0695912092924118,
        "reference_compatibility_mean": 0.89304133280671,
        "joint_acceleration_rms_rad_s2": 35.367801666259766,
        "box_relative_translation_drift_max_m": 0.05554431753064702,
        "box_relative_rotation_drift_max_rad": 0.05594884957510276
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.10254174470901489,
        "lower_body_style_rmse_rad": 0.07136812806129456,
        "reference_compatibility_mean": 0.8885135512515283,
        "joint_acceleration_rms_rad_s2": 35.5484733581543,
        "box_relative_translation_drift_max_m": 0.05612691031137436,
        "box_relative_rotation_drift_max_rad": 0.05343115292379399
      }
    ]
  },
  "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795184803218754746": {
    "clip_0_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.1011236310005188,
        "lower_body_style_rmse_rad": 0.07091598957777023,
        "reference_compatibility_mean": 0.8916152402312975,
        "joint_acceleration_rms_rad_s2": 35.44654846191406,
        "box_relative_translation_drift_max_m": 0.055032013139381546,
        "box_relative_rotation_drift_max_rad": 0.0577934280140449
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.10118065774440765,
        "lower_body_style_rmse_rad": 0.06938589364290237,
        "reference_compatibility_mean": 0.8978695632190753,
        "joint_acceleration_rms_rad_s2": 35.460506439208984,
        "box_relative_translation_drift_max_m": 0.05526999823395054,
        "box_relative_rotation_drift_max_rad": 0.0576396737830099
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.10127242654561996,
        "lower_body_style_rmse_rad": 0.07040072977542877,
        "reference_compatibility_mean": 0.8913868134977714,
        "joint_acceleration_rms_rad_s2": 35.46141052246094,
        "box_relative_translation_drift_max_m": 0.055387622526558204,
        "box_relative_rotation_drift_max_rad": 0.057702098532900384
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.1026809960603714,
        "lower_body_style_rmse_rad": 0.06993930041790009,
        "reference_compatibility_mean": 0.8947683870789792,
        "joint_acceleration_rms_rad_s2": 35.41193389892578,
        "box_relative_translation_drift_max_m": 0.05582342089336574,
        "box_relative_rotation_drift_max_rad": 0.056288578996422096
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.10239977389574051,
        "lower_body_style_rmse_rad": 0.06987731158733368,
        "reference_compatibility_mean": 0.8960112054653229,
        "joint_acceleration_rms_rad_s2": 35.404476165771484,
        "box_relative_translation_drift_max_m": 0.05630313691592539,
        "box_relative_rotation_drift_max_rad": 0.056402919599480336
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.10195469111204147,
        "lower_body_style_rmse_rad": 0.06963054090738297,
        "reference_compatibility_mean": 0.8968813848439755,
        "joint_acceleration_rms_rad_s2": 35.16630554199219,
        "box_relative_translation_drift_max_m": 0.05567731253626865,
        "box_relative_rotation_drift_max_rad": 0.055434688010912815
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.10267283767461777,
        "lower_body_style_rmse_rad": 0.07017690688371658,
        "reference_compatibility_mean": 0.8968996933592539,
        "joint_acceleration_rms_rad_s2": 35.494327545166016,
        "box_relative_translation_drift_max_m": 0.05606714325953691,
        "box_relative_rotation_drift_max_rad": 0.05586839788136181
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.10106883943080902,
        "lower_body_style_rmse_rad": 0.06888579577207565,
        "reference_compatibility_mean": 0.8945554656795061,
        "joint_acceleration_rms_rad_s2": 35.451602935791016,
        "box_relative_translation_drift_max_m": 0.055003584079820984,
        "box_relative_rotation_drift_max_rad": 0.058193806118581604
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.10212024301290512,
        "lower_body_style_rmse_rad": 0.06975320726633072,
        "reference_compatibility_mean": 0.8929567264311775,
        "joint_acceleration_rms_rad_s2": 35.37553405761719,
        "box_relative_translation_drift_max_m": 0.05554324268456987,
        "box_relative_rotation_drift_max_rad": 0.05577375390653555
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.1025315672159195,
        "lower_body_style_rmse_rad": 0.07125764340162277,
        "reference_compatibility_mean": 0.8893355464147215,
        "joint_acceleration_rms_rad_s2": 35.46196365356445,
        "box_relative_translation_drift_max_m": 0.056141880787567815,
        "box_relative_rotation_drift_max_rad": 0.05334515468737263
      }
    ],
    "clip_1_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.10112810134887695,
        "lower_body_style_rmse_rad": 0.07078329473733902,
        "reference_compatibility_mean": 0.8922674070849499,
        "joint_acceleration_rms_rad_s2": 35.4002799987793,
        "box_relative_translation_drift_max_m": 0.05500582950432958,
        "box_relative_rotation_drift_max_rad": 0.057817870604326756
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.10116524249315262,
        "lower_body_style_rmse_rad": 0.06936813145875931,
        "reference_compatibility_mean": 0.8983877347516275,
        "joint_acceleration_rms_rad_s2": 35.437095642089844,
        "box_relative_translation_drift_max_m": 0.05521471095620653,
        "box_relative_rotation_drift_max_rad": 0.05741072127008877
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.10128884762525558,
        "lower_body_style_rmse_rad": 0.07042166590690613,
        "reference_compatibility_mean": 0.8913291012966844,
        "joint_acceleration_rms_rad_s2": 35.418277740478516,
        "box_relative_translation_drift_max_m": 0.055345358991513806,
        "box_relative_rotation_drift_max_rad": 0.05769765779039082
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.10268091410398483,
        "lower_body_style_rmse_rad": 0.06997094303369522,
        "reference_compatibility_mean": 0.8945481717540271,
        "joint_acceleration_rms_rad_s2": 35.24541473388672,
        "box_relative_translation_drift_max_m": 0.05575785314101226,
        "box_relative_rotation_drift_max_rad": 0.056331909176344244
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.1024090051651001,
        "lower_body_style_rmse_rad": 0.06996136158704758,
        "reference_compatibility_mean": 0.8958861527228066,
        "joint_acceleration_rms_rad_s2": 35.47512435913086,
        "box_relative_translation_drift_max_m": 0.05604262115962388,
        "box_relative_rotation_drift_max_rad": 0.0570354416449782
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.10193710774183273,
        "lower_body_style_rmse_rad": 0.06974803656339645,
        "reference_compatibility_mean": 0.8966164223177925,
        "joint_acceleration_rms_rad_s2": 35.24787902832031,
        "box_relative_translation_drift_max_m": 0.055672686363275804,
        "box_relative_rotation_drift_max_rad": 0.0556883922628906
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.10267023742198944,
        "lower_body_style_rmse_rad": 0.07015026360750198,
        "reference_compatibility_mean": 0.8969182810504648,
        "joint_acceleration_rms_rad_s2": 35.54161071777344,
        "box_relative_translation_drift_max_m": 0.05630709631957172,
        "box_relative_rotation_drift_max_rad": 0.055799864114629956
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.10104888677597046,
        "lower_body_style_rmse_rad": 0.06887713074684143,
        "reference_compatibility_mean": 0.8946126843867749,
        "joint_acceleration_rms_rad_s2": 35.441864013671875,
        "box_relative_translation_drift_max_m": 0.0549970878861285,
        "box_relative_rotation_drift_max_rad": 0.05811983593503357
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.10213208198547363,
        "lower_body_style_rmse_rad": 0.0695912092924118,
        "reference_compatibility_mean": 0.89304133280671,
        "joint_acceleration_rms_rad_s2": 35.367801666259766,
        "box_relative_translation_drift_max_m": 0.05554431753064702,
        "box_relative_rotation_drift_max_rad": 0.05594884957510276
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.10254174470901489,
        "lower_body_style_rmse_rad": 0.07136812806129456,
        "reference_compatibility_mean": 0.8885135512515283,
        "joint_acceleration_rms_rad_s2": 35.5484733581543,
        "box_relative_translation_drift_max_m": 0.05612691031137436,
        "box_relative_rotation_drift_max_rad": 0.05343115292379399
      }
    ]
  },
  "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795207462435354552": {
    "clip_0_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.08552000671625137,
        "lower_body_style_rmse_rad": 0.07972968369722366,
        "reference_compatibility_mean": 0.7861406398105356,
        "joint_acceleration_rms_rad_s2": 52.976829528808594,
        "box_relative_translation_drift_max_m": 0.03939828630295614,
        "box_relative_rotation_drift_max_rad": 0.09156653268749157
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.08555198460817337,
        "lower_body_style_rmse_rad": 0.08135330677032471,
        "reference_compatibility_mean": 0.7859209085815916,
        "joint_acceleration_rms_rad_s2": 53.22590637207031,
        "box_relative_translation_drift_max_m": 0.04057779552873983,
        "box_relative_rotation_drift_max_rad": 0.09046742894793709
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.08566688001155853,
        "lower_body_style_rmse_rad": 0.08116155117750168,
        "reference_compatibility_mean": 0.7849794083406516,
        "joint_acceleration_rms_rad_s2": 53.34197998046875,
        "box_relative_translation_drift_max_m": 0.039242177723116646,
        "box_relative_rotation_drift_max_rad": 0.0894919925587349
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.08644428104162216,
        "lower_body_style_rmse_rad": 0.08209109306335449,
        "reference_compatibility_mean": 0.7791357473112466,
        "joint_acceleration_rms_rad_s2": 52.999656677246094,
        "box_relative_translation_drift_max_m": 0.04057442425288657,
        "box_relative_rotation_drift_max_rad": 0.08427327665065153
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.08637721091508865,
        "lower_body_style_rmse_rad": 0.08222559839487076,
        "reference_compatibility_mean": 0.7802598684389357,
        "joint_acceleration_rms_rad_s2": 52.989253997802734,
        "box_relative_translation_drift_max_m": 0.04146149312776866,
        "box_relative_rotation_drift_max_rad": 0.08490747806540773
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.08614807575941086,
        "lower_body_style_rmse_rad": 0.0820605605840683,
        "reference_compatibility_mean": 0.7744864537634901,
        "joint_acceleration_rms_rad_s2": 52.89619827270508,
        "box_relative_translation_drift_max_m": 0.04159896087166017,
        "box_relative_rotation_drift_max_rad": 0.0886865833429351
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.08662419766187668,
        "lower_body_style_rmse_rad": 0.08251798897981644,
        "reference_compatibility_mean": 0.7700377356717159,
        "joint_acceleration_rms_rad_s2": 52.9651985168457,
        "box_relative_translation_drift_max_m": 0.04165227856908904,
        "box_relative_rotation_drift_max_rad": 0.08234124582519312
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.0855722576379776,
        "lower_body_style_rmse_rad": 0.08096595853567123,
        "reference_compatibility_mean": 0.7863219256066953,
        "joint_acceleration_rms_rad_s2": 53.36178970336914,
        "box_relative_translation_drift_max_m": 0.039965872343885156,
        "box_relative_rotation_drift_max_rad": 0.08958359079954434
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.08622009307146072,
        "lower_body_style_rmse_rad": 0.08235246688127518,
        "reference_compatibility_mean": 0.7746928758606462,
        "joint_acceleration_rms_rad_s2": 53.08083724975586,
        "box_relative_translation_drift_max_m": 0.04033891576571533,
        "box_relative_rotation_drift_max_rad": 0.08543699097556524
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.08656163513660431,
        "lower_body_style_rmse_rad": 0.08228854835033417,
        "reference_compatibility_mean": 0.7729919105823042,
        "joint_acceleration_rms_rad_s2": 52.887630462646484,
        "box_relative_translation_drift_max_m": 0.04106028353309817,
        "box_relative_rotation_drift_max_rad": 0.09057409727614132
      }
    ],
    "clip_1_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.08568248897790909,
        "lower_body_style_rmse_rad": 0.08145931363105774,
        "reference_compatibility_mean": 0.7842900467357966,
        "joint_acceleration_rms_rad_s2": 53.432743072509766,
        "box_relative_translation_drift_max_m": 0.03987153393837467,
        "box_relative_rotation_drift_max_rad": 0.09216105334047704
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.08565416932106018,
        "lower_body_style_rmse_rad": 0.08147518336772919,
        "reference_compatibility_mean": 0.7843167741479544,
        "joint_acceleration_rms_rad_s2": 53.03413772583008,
        "box_relative_translation_drift_max_m": 0.0406443747897602,
        "box_relative_rotation_drift_max_rad": 0.0913995008574815
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.08564635366201401,
        "lower_body_style_rmse_rad": 0.08115758001804352,
        "reference_compatibility_mean": 0.7851989678983553,
        "joint_acceleration_rms_rad_s2": 53.30923080444336,
        "box_relative_translation_drift_max_m": 0.039221830768366175,
        "box_relative_rotation_drift_max_rad": 0.08940348141662201
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.08646369725465775,
        "lower_body_style_rmse_rad": 0.08209976553916931,
        "reference_compatibility_mean": 0.7790533489892013,
        "joint_acceleration_rms_rad_s2": 52.932342529296875,
        "box_relative_translation_drift_max_m": 0.040573452995423975,
        "box_relative_rotation_drift_max_rad": 0.08413831642495873
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.08641204237937927,
        "lower_body_style_rmse_rad": 0.08222721517086029,
        "reference_compatibility_mean": 0.7800971110566323,
        "joint_acceleration_rms_rad_s2": 52.98634719848633,
        "box_relative_translation_drift_max_m": 0.04122545630094908,
        "box_relative_rotation_drift_max_rad": 0.08391451652704963
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.08612250536680222,
        "lower_body_style_rmse_rad": 0.08205664902925491,
        "reference_compatibility_mean": 0.7746113694571353,
        "joint_acceleration_rms_rad_s2": 52.998695373535156,
        "box_relative_translation_drift_max_m": 0.04143275763551616,
        "box_relative_rotation_drift_max_rad": 0.08795934109711324
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.08661887049674988,
        "lower_body_style_rmse_rad": 0.08250568062067032,
        "reference_compatibility_mean": 0.770224428937113,
        "joint_acceleration_rms_rad_s2": 52.9666862487793,
        "box_relative_translation_drift_max_m": 0.04158913296916617,
        "box_relative_rotation_drift_max_rad": 0.08240064017662536
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.08568954467773438,
        "lower_body_style_rmse_rad": 0.08139578998088837,
        "reference_compatibility_mean": 0.7847631184912343,
        "joint_acceleration_rms_rad_s2": 53.29639434814453,
        "box_relative_translation_drift_max_m": 0.03991616485294114,
        "box_relative_rotation_drift_max_rad": 0.08975648981601633
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.086229607462883,
        "lower_body_style_rmse_rad": 0.08236099779605865,
        "reference_compatibility_mean": 0.7746433121316108,
        "joint_acceleration_rms_rad_s2": 52.986907958984375,
        "box_relative_translation_drift_max_m": 0.04030359853652523,
        "box_relative_rotation_drift_max_rad": 0.08561711449345127
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.08656079322099686,
        "lower_body_style_rmse_rad": 0.08215682208538055,
        "reference_compatibility_mean": 0.7730568259748456,
        "joint_acceleration_rms_rad_s2": 52.949066162109375,
        "box_relative_translation_drift_max_m": 0.04109904505865462,
        "box_relative_rotation_drift_max_rad": 0.09063206022288413
      }
    ]
  },
  "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795169166776259536": {
    "clip_0_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.1138010323047638,
        "lower_body_style_rmse_rad": 0.08353951573371887,
        "reference_compatibility_mean": 0.7687269545406158,
        "joint_acceleration_rms_rad_s2": 44.529396057128906,
        "box_relative_translation_drift_max_m": 0.05377168533331644,
        "box_relative_rotation_drift_max_rad": 0.046166731585710385
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.11375592648983002,
        "lower_body_style_rmse_rad": 0.08416897058486938,
        "reference_compatibility_mean": 0.7665100520781012,
        "joint_acceleration_rms_rad_s2": 44.31330871582031,
        "box_relative_translation_drift_max_m": 0.053848334334013884,
        "box_relative_rotation_drift_max_rad": 0.047840730732245276
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.11379756778478622,
        "lower_body_style_rmse_rad": 0.08352480083703995,
        "reference_compatibility_mean": 0.7636993412659506,
        "joint_acceleration_rms_rad_s2": 44.78684997558594,
        "box_relative_translation_drift_max_m": 0.054133563732441436,
        "box_relative_rotation_drift_max_rad": 0.047949759040310784
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.11527024954557419,
        "lower_body_style_rmse_rad": 0.08380361646413803,
        "reference_compatibility_mean": 0.7661313745458642,
        "joint_acceleration_rms_rad_s2": 43.53038024902344,
        "box_relative_translation_drift_max_m": 0.05447303232170755,
        "box_relative_rotation_drift_max_rad": 0.059495793679530555
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.11532902717590332,
        "lower_body_style_rmse_rad": 0.08390390872955322,
        "reference_compatibility_mean": 0.760924489066839,
        "joint_acceleration_rms_rad_s2": 43.96269989013672,
        "box_relative_translation_drift_max_m": 0.05432054569447959,
        "box_relative_rotation_drift_max_rad": 0.05904660523147655
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.11490022391080856,
        "lower_body_style_rmse_rad": 0.08370019495487213,
        "reference_compatibility_mean": 0.7734603459078749,
        "joint_acceleration_rms_rad_s2": 44.092735290527344,
        "box_relative_translation_drift_max_m": 0.05408896553139467,
        "box_relative_rotation_drift_max_rad": 0.056417560087056055
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.1155279278755188,
        "lower_body_style_rmse_rad": 0.08507634699344635,
        "reference_compatibility_mean": 0.7662272298608913,
        "joint_acceleration_rms_rad_s2": 43.559871673583984,
        "box_relative_translation_drift_max_m": 0.05440359164517699,
        "box_relative_rotation_drift_max_rad": 0.05938140764499778
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.1135270819067955,
        "lower_body_style_rmse_rad": 0.08358027786016464,
        "reference_compatibility_mean": 0.7678726022709309,
        "joint_acceleration_rms_rad_s2": 44.76818084716797,
        "box_relative_translation_drift_max_m": 0.0538938996009339,
        "box_relative_rotation_drift_max_rad": 0.046769169130036384
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.11487963050603867,
        "lower_body_style_rmse_rad": 0.08397126197814941,
        "reference_compatibility_mean": 0.7541921300383877,
        "joint_acceleration_rms_rad_s2": 44.42616271972656,
        "box_relative_translation_drift_max_m": 0.05505674804138337,
        "box_relative_rotation_drift_max_rad": 0.0583089906942191
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.11522220820188522,
        "lower_body_style_rmse_rad": 0.08394508063793182,
        "reference_compatibility_mean": 0.7692193104103409,
        "joint_acceleration_rms_rad_s2": 44.292991638183594,
        "box_relative_translation_drift_max_m": 0.05383705276236426,
        "box_relative_rotation_drift_max_rad": 0.056191687679544126
      }
    ],
    "clip_1_rollout": [
      {
        "seed_index": 0,
        "upper_body_style_rmse_rad": 0.11378076672554016,
        "lower_body_style_rmse_rad": 0.08352365344762802,
        "reference_compatibility_mean": 0.7688308446332649,
        "joint_acceleration_rms_rad_s2": 44.75520324707031,
        "box_relative_translation_drift_max_m": 0.053731651807845296,
        "box_relative_rotation_drift_max_rad": 0.04616723332210381
      },
      {
        "seed_index": 1,
        "upper_body_style_rmse_rad": 0.11380438506603241,
        "lower_body_style_rmse_rad": 0.0841568186879158,
        "reference_compatibility_mean": 0.766592427101451,
        "joint_acceleration_rms_rad_s2": 44.146522521972656,
        "box_relative_translation_drift_max_m": 0.053723710221466124,
        "box_relative_rotation_drift_max_rad": 0.0478551592659327
      },
      {
        "seed_index": 2,
        "upper_body_style_rmse_rad": 0.1138051301240921,
        "lower_body_style_rmse_rad": 0.08339632302522659,
        "reference_compatibility_mean": 0.7637740886014444,
        "joint_acceleration_rms_rad_s2": 44.80767059326172,
        "box_relative_translation_drift_max_m": 0.05413449349263971,
        "box_relative_rotation_drift_max_rad": 0.04794997119560701
      },
      {
        "seed_index": 3,
        "upper_body_style_rmse_rad": 0.11527321487665176,
        "lower_body_style_rmse_rad": 0.08380705863237381,
        "reference_compatibility_mean": 0.7661296598810647,
        "joint_acceleration_rms_rad_s2": 43.55049514770508,
        "box_relative_translation_drift_max_m": 0.054493182856467114,
        "box_relative_rotation_drift_max_rad": 0.05951098527353351
      },
      {
        "seed_index": 4,
        "upper_body_style_rmse_rad": 0.11535559594631195,
        "lower_body_style_rmse_rad": 0.0837799459695816,
        "reference_compatibility_mean": 0.7609361327448977,
        "joint_acceleration_rms_rad_s2": 44.00465774536133,
        "box_relative_translation_drift_max_m": 0.05431107527579525,
        "box_relative_rotation_drift_max_rad": 0.05905761114209859
      },
      {
        "seed_index": 5,
        "upper_body_style_rmse_rad": 0.11489700525999069,
        "lower_body_style_rmse_rad": 0.0838046446442604,
        "reference_compatibility_mean": 0.7734585266686785,
        "joint_acceleration_rms_rad_s2": 44.09633255004883,
        "box_relative_translation_drift_max_m": 0.054104172591143154,
        "box_relative_rotation_drift_max_rad": 0.05641207701768732
      },
      {
        "seed_index": 6,
        "upper_body_style_rmse_rad": 0.11552790552377701,
        "lower_body_style_rmse_rad": 0.08497647196054459,
        "reference_compatibility_mean": 0.7662546063021973,
        "joint_acceleration_rms_rad_s2": 43.6200065612793,
        "box_relative_translation_drift_max_m": 0.05436762890929643,
        "box_relative_rotation_drift_max_rad": 0.05938239164348483
      },
      {
        "seed_index": 7,
        "upper_body_style_rmse_rad": 0.11353634297847748,
        "lower_body_style_rmse_rad": 0.08345704525709152,
        "reference_compatibility_mean": 0.7679844996435863,
        "joint_acceleration_rms_rad_s2": 44.81047821044922,
        "box_relative_translation_drift_max_m": 0.05386962174926151,
        "box_relative_rotation_drift_max_rad": 0.04676807134250458
      },
      {
        "seed_index": 8,
        "upper_body_style_rmse_rad": 0.11487729102373123,
        "lower_body_style_rmse_rad": 0.08396334201097488,
        "reference_compatibility_mean": 0.7542326609618667,
        "joint_acceleration_rms_rad_s2": 44.49744415283203,
        "box_relative_translation_drift_max_m": 0.05504944088973423,
        "box_relative_rotation_drift_max_rad": 0.05830501819664571
      },
      {
        "seed_index": 9,
        "upper_body_style_rmse_rad": 0.11522852629423141,
        "lower_body_style_rmse_rad": 0.08408999443054199,
        "reference_compatibility_mean": 0.7692445341666454,
        "joint_acceleration_rms_rad_s2": 44.32569122314453,
        "box_relative_translation_drift_max_m": 0.05384744867127821,
        "box_relative_rotation_drift_max_rad": 0.056198916831013614
      }
    ]
  }
}

## Best checkpoints, acceptance and inference artifacts

{
  "best_stage1": {
    "path": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/best_stage1/iteration_499_1795161423076710349/model.pt",
    "sha256": "12ed1d3ee9faa6c646db18594a7a3959e54642cd310ce2ac27d20e1a1eec9ce9",
    "bytes": 7331318,
    "iteration": 499,
    "completed_updates": 500,
    "curriculum_level": 0,
    "selection_score": 0.014638463350442742,
    "passed": false,
    "evaluation": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/evaluations/stage1_1795161406155359032"
  },
  "best_stage2": null,
  "valid_stage1": null,
  "valid_stage2": null,
  "final_checkpoint": null
}

Unaccepted models stay in best_stage*/ and must not be presented as usable final policies. Accepted models, full config and ONNX metadata are copied into deliverables/. ONNX parity is tested at training export and the CPU exporter; per-model errors are in .actor.json. Viewer/interactive/evaluation/export commands are in README_FULLBODY_CARRY.md.

## Stop reason, failures and remaining work

{
  "blocker": "Job timeout/budget reached: stage1_training",
  "gpu_seconds": {
    "stage1": 86410.06642652652
  },
  "stage1_corrections": 3,
  "stage2_corrections": null,
  "last_job": {
    "output": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/jobs/stage1_training_1795236568203928995",
    "exit_code": -6,
    "wall_seconds": 3550.451997013064,
    "peak_gpu_memory_mib": 8298,
    "error": "Job timeout/budget reached: stage1_training",
    "failure_evidence": [],
    "worker": {
      "passed": false,
      "updates": 244,
      "resume_verified": true,
      "resumed_from": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/dashboard/stage1/WholeBodyTracking/20261121_024914-stage1-locomotion/model_05499.pt",
      "latest": {
        "iteration": 5743,
        "num_envs": 8192,
        "samples": 196608,
        "minibatches": 128,
        "epochs": 5,
        "rollout_s": 12.922106869053096,
        "update_s": 1.2473314311355352,
        "simulation_s": 12.41454818774946,
        "steps_per_s": 13875.49709697262,
        "cuda_reserved_mib": 1176.0,
        "curriculum_level": 0,
        "losses": {
          "Value": 0.34585936647708876,
          "Surrogate": -0.0007682581286644563,
          "Entropy": -4.364343240112066,
          "KL": 0.012634177007566905,
          "actor_loss": 0.007960428774822503,
          "critic_loss": 0.34585936647708876,
          "symmetry_actor_loss": 0.0,
          "symmetry_critic_loss": 0.0
        },
        "physical": {
          "action_clip_frac": 0.0,
          "termination/reset_frac": 0.0037841796875,
          "termination/non_timeout_frac": 0.0001220703125,
          "termination/timeout_frac": 0.0,
          "termination/clip_timeout_frac": 0.003662109375,
          "termination/physical_failure_frac": 0.0001220703125,
          "termination/physical_failure/fall_frac": 0.0,
          "termination/physical_failure/drop_frac": 0.0,
          "termination/physical_failure/separation_frac": 0.0,
          "termination/physical_failure/loss_of_grasp_frac": 0.0001220703125,
          "termination/physical_failure/body_support_frac": 0.0,
          "termination/physical_failure/nonfinite_frac": 0.0,
          "termination/track_failure_frac": 0.0,
          "termination/track_failure/ref_pos_z_frac": 0.0,
          "termination/track_failure/ref_ori_frac": 0.0,
          "termination/track_failure/body_pos_z_frac": 0.0,
          "termination/track_failure/object_pos_frac": 0.0,
          "termination/track_failure/object_ori_frac": 0.0,
          "termination/body_proximity_frac": 0.0,
          "termination/body_proximity/group_0_frac": 0.0,
          "hybrid/termination/track/reset_frac": 0.0037841796875,
          "hybrid/termination/gen/reset_frac": 0.0,
          "fullbody/termination_timeout": 0.0,
          "fullbody/termination_clip_timeout": 0.003662109375,
          "fullbody/termination_physical_failure": 0.0001220703125,
          "fullbody/termination_track_failure": 0.0,
          "fullbody/termination_body_proximity": 0.0,
          "average_episode_length": 274.46234130859375,
          "carry/error_vx": 0.017992112785577774,
          "carry/command_vx": 0.001304726698435843,
          "carry/error_vy": 0.012632188387215137,
          "carry/command_vy": 2.5292230930062942e-05,
          "carry/error_yaw_rate": 0.12644405663013458,
          "carry/command_yaw_rate": 9.194988524541259e-05,
          "carry/error_pelvis_height": 0.002408841624855995,
          "carry/command_pelvis_height": 0.6734164953231812,
          "carry/bilateral_contact": 0.9791688323020935,
          "carry/left_hand_normal_n": 41.999107360839844,
          "carry/right_hand_normal_n": 41.69758224487305,
          "carry/upward_friction_weight_ratio": 1.0462279319763184,
          "carry/hand_slip_speed_m_s": 0.0802733525633812,
          "carry/box_clearance_m": 0.5167125463485718,
          "carry/normal_vertical_fraction": 0.03262244537472725,
          "carry/min_contact_height_above_bottom_m": 0.23413905501365662,
          "carry/nonhand_box_contact_n": 0.0,
          "carry/curriculum_level": 0.0,
          "reward/episode/rew_motion_global_ref_position_error_exp": 0.08203232288360596,
          "reward/episode/rew_motion_global_ref_orientation_error_exp": 0.0811440646648407,
          "reward/episode/rew_motion_relative_body_position_error_exp": 0.1632499396800995,
          "reward/episode/rew_motion_relative_body_orientation_error_exp": 0.14436064660549164,
          "reward/episode/rew_motion_global_body_lin_vel": 0.162614107131958,
          "reward/episode/rew_motion_global_body_ang_vel": 0.15936020016670227,
          "reward/episode/rew_object_global_ref_position_error_exp": 0.15238460898399353,
          "reward/episode/rew_object_global_ref_orientation_error_exp": 0.1632155030965805,
          "reward/episode/rew_action_rate_l2": -0.06495791673660278,
          "reward/episode/rew_limits_dof_pos": -1.0004606032509855e-08,
          "reward/episode/rew_velocity_tracking": 0.48360833525657654,
          "reward/episode/rew_yaw_tracking": 0.13332568109035492,
          "reward/episode/rew_height_tracking": 0.49030637741088867,
          "reward/episode/rew_grasp": 0.9444819092750549,
          "reward/episode/rew_stable_carry": 0.14584675431251526,
          "reward/episode/rew_box_orientation": 0.1622399240732193,
          "reward/episode/rew_hand_slip": 0.14066709578037262,
          "reward/episode/rew_goal_compatible_style_reward": 0.0,
          "reward/episode/rew_nonhand_contact": 0.0,
          "reward/episode/termination/timeout": 0.0,
          "reward/episode/termination/clip_timeout": 0.9677419066429138,
          "reward/episode/termination/physical_failure": 0.032258063554763794,
          "reward/episode/termination/physical_failure/fall": 0.0,
          "reward/episode/termination/physical_failure/drop": 0.0,
          "reward/episode/termination/physical_failure/separation": 0.0,
          "reward/episode/termination/physical_failure/loss_of_grasp": 0.032258063554763794,
          "reward/episode/termination/physical_failure/body_support": 0.0,
          "reward/episode/termination/physical_failure/nonfinite": 0.0,
          "reward/episode/termination/track_failure": 0.0,
          "reward/episode/termination/track_failure/ref_pos_z": 0.0,
          "reward/episode/termination/track_failure/ref_ori": 0.0,
          "reward/episode/termination/track_failure/body_pos_z": 0.0,
          "reward/episode/termination/track_failure/object_pos": 0.0,
          "reward/episode/termination/track_failure/object_ori": 0.0,
          "reward/episode/termination/body_proximity": 0.0,
          "reward/episode/termination/body_proximity/group_0": 0.0,
          "reward/episode/hybrid/reward/track/rew_motion_global_ref_position_error_exp": 0.08203232288360596,
          "reward/episode/hybrid/reward/track/rew_motion_global_ref_orientation_error_exp": 0.0811440646648407,
          "reward/episode/hybrid/reward/track/rew_motion_relative_body_position_error_exp": 0.1632499396800995,
          "reward/episode/hybrid/reward/track/rew_motion_relative_body_orientation_error_exp": 0.14436064660549164,
          "reward/episode/hybrid/reward/track/rew_motion_global_body_lin_vel": 0.162614107131958,
          "reward/episode/hybrid/reward/track/rew_motion_global_body_ang_vel": 0.15936020016670227,
          "reward/episode/hybrid/reward/track/rew_object_global_ref_position_error_exp": 0.15238460898399353,
          "reward/episode/hybrid/reward/track/rew_object_global_ref_orientation_error_exp": 0.1632155030965805,
          "reward/episode/hybrid/mean_reward/track": 106.31639099121094,
          "reward/raw_episode/raw_rew_motion_global_ref_position_error_exp": 8.203232765197754,
          "reward/raw_episode/raw_rew_motion_global_ref_orientation_error_exp": 8.11440658569336,
          "reward/raw_episode/raw_rew_motion_relative_body_position_error_exp": 8.162493705749512,
          "reward/raw_episode/raw_rew_motion_relative_body_orientation_error_exp": 7.218033313751221,
          "reward/raw_episode/raw_rew_motion_global_body_lin_vel": 8.130707740783691,
          "reward/raw_episode/raw_rew_motion_global_body_ang_vel": 7.968011379241943,
          "reward/raw_episode/raw_rew_object_global_ref_position_error_exp": 7.619229793548584,
          "reward/raw_episode/raw_rew_object_global_ref_orientation_error_exp": 8.160775184631348,
          "reward/raw_episode/raw_rew_action_rate_l2": 32.47895812988281,
          "reward/raw_episode/raw_rew_limits_dof_pos": 5.002303993251189e-08,
          "reward/raw_episode/raw_rew_velocity_tracking": 8.060137748718262,
          "reward/raw_episode/raw_rew_yaw_tracking": 6.666284084320068,
          "reward/raw_episode/raw_rew_height_tracking": 8.171772956848145,
          "reward/raw_episode/raw_rew_grasp": 7.870682239532471,
          "reward/raw_episode/raw_rew_stable_carry": 7.2923359870910645,
          "reward/raw_episode/raw_rew_box_orientation": 8.111998558044434,
          "reward/raw_episode/raw_rew_hand_slip": 7.03335428237915,
          "reward/raw_episode/raw_rew_goal_compatible_style_reward": 0.0,
          "reward/raw_episode/raw_rew_nonhand_contact": 0.0
        },
        "mean_live_episode_s": 3.976518392562866
      },
      "log_dir": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/dashboard/stage1/WholeBodyTracking/20261121_044933-stage1-locomotion"
    }
  }
}

Unimplemented or unverified capabilities must be read from the measured acceptance tables, not inferred from finite PPO losses or rising rewards. Forward reference contact consistency is a known blocker. No unseen forward+height combinations, lateral motion or turning are certified. For vy/yaw extension, first admit compatible dynamic references and separately benchmark each command family. Failed policies and failed references are retained rather than hidden.

## Reproduction

See README_FULLBODY_CARRY.md for environment activation, validation, Stage 1/2, resume, automatic controller, TensorBoard, checkpoint evaluation, ONNX export, Viewer, interactive four-dimensional commands and goal grid. TensorBoard for this workspace: http://127.0.0.1:6011 .
