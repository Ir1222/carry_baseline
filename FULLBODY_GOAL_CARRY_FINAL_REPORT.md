# FullBody Goal Carry — measured experiment report

Status: **RUNNING / BENCHMARK**. This file is a progress report while RUNNING. Only independent physical acceptance grants a usable policy.

Branch: `feature/fullbody-goal-carry-autotrain`. Current source commit: `136ef0d05f425cef54323caa5f584c7e8ebe8128`. P0 preservation commit: `ed106a7`. Initial run source: `136ef0d05f425cef54323caa5f584c7e8ebe8128`. Additional source versions are retained as `source_*.tar`.

Run directory: `/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333`. PID, process identity and current command: {"name": "benchmark_8192", "pid": 359072, "identity": "163818672", "output": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/jobs/benchmark_8192_1795153031824246930", "started_at": 1795153031.8270357, "stage": null}

## P0 and source integrity

{
  "passed": true,
  "policy_success": false,
  "immutable_p0_sources_unchanged": true,
  "cpu_tests": "18 passed",
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
  "note": "Ready for bounded squat/stand PPO training; no policy skill or forward capability established"
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
  "source_commit": "136ef0d05f425cef54323caa5f584c7e8ebe8128"
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
  "gpu_seconds": {},
  "stage1_corrections": null,
  "stage2_corrections": null,
  "last_job": {
    "output": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/jobs/benchmark_4096_1795152814934836057",
    "exit_code": 0,
    "wall_seconds": 215.81155135692097,
    "peak_gpu_memory_mib": 5860,
    "error": null,
    "failure_evidence": [],
    "worker": {
      "passed": true,
      "updates": 16,
      "resume_verified": false,
      "latest": {
        "iteration": 15,
        "num_envs": 4096,
        "samples": 98304,
        "minibatches": 64,
        "epochs": 5,
        "rollout_s": 10.354734911117703,
        "update_s": 0.6558900729287416,
        "simulation_s": 9.709628629265353,
        "steps_per_s": 8928.10354929307,
        "cuda_reserved_mib": 606.0,
        "curriculum_level": 0,
        "losses": {
          "Value": 0.4224679066799581,
          "Surrogate": -0.018651142353246542,
          "Entropy": 5.580766171216965,
          "KL": 0.010969717610356611,
          "actor_loss": -0.029812675292487257,
          "critic_loss": 0.4224679066799581,
          "symmetry_actor_loss": 0.0,
          "symmetry_critic_loss": 0.0
        },
        "physical": {
          "action_clip_frac": 0.0,
          "termination/reset_frac": 0.12548828125,
          "termination/non_timeout_frac": 0.12255859375,
          "termination/timeout_frac": 0.0,
          "termination/clip_timeout_frac": 0.0029296875,
          "termination/physical_failure_frac": 0.1171875,
          "termination/physical_failure/fall_frac": 0.0,
          "termination/physical_failure/drop_frac": 0.0,
          "termination/physical_failure/separation_frac": 0.0,
          "termination/physical_failure/loss_of_grasp_frac": 0.10595703125,
          "termination/physical_failure/body_support_frac": 0.013916015625,
          "termination/physical_failure/nonfinite_frac": 0.0,
          "termination/track_failure_frac": 0.005615234375,
          "termination/track_failure/ref_pos_z_frac": 0.0,
          "termination/track_failure/ref_ori_frac": 0.0,
          "termination/track_failure/body_pos_z_frac": 0.0,
          "termination/track_failure/object_pos_frac": 0.0,
          "termination/track_failure/object_ori_frac": 0.005615234375,
          "termination/body_proximity_frac": 0.0,
          "termination/body_proximity/group_0_frac": 0.0,
          "hybrid/termination/track/reset_frac": 0.12548828125,
          "hybrid/termination/gen/reset_frac": 0.0,
          "fullbody/termination_timeout": 0.0,
          "fullbody/termination_clip_timeout": 0.0029296875,
          "fullbody/termination_physical_failure": 0.1171875,
          "fullbody/termination_track_failure": 0.005615234375,
          "fullbody/termination_body_proximity": 0.0,
          "average_episode_length": 8.403282165527344,
          "carry/error_vx": 0.09263059496879578,
          "carry/command_vx": -0.0005774041055701673,
          "carry/error_vy": 0.032782621681690216,
          "carry/command_vy": -4.106950200366555e-06,
          "carry/error_yaw_rate": 0.3741019368171692,
          "carry/command_yaw_rate": -1.4559948795067612e-05,
          "carry/error_pelvis_height": 0.033726613968610764,
          "carry/command_pelvis_height": 0.6864051818847656,
          "carry/bilateral_contact": 0.5497314929962158,
          "carry/left_hand_normal_n": 7.705808639526367,
          "carry/right_hand_normal_n": 7.965642929077148,
          "carry/upward_friction_weight_ratio": 0.6470264196395874,
          "carry/hand_slip_speed_m_s": 0.40388739109039307,
          "carry/box_clearance_m": 0.555405855178833,
          "carry/nonhand_box_contact_n": 0.661733865737915,
          "carry/curriculum_level": 0.0,
          "reward/episode/rew_motion_global_ref_position_error_exp": 0.0026474050246179104,
          "reward/episode/rew_motion_global_ref_orientation_error_exp": 0.0026160674169659615,
          "reward/episode/rew_motion_relative_body_position_error_exp": 0.005352914333343506,
          "reward/episode/rew_motion_relative_body_orientation_error_exp": 0.00478110508993268,
          "reward/episode/rew_motion_global_body_lin_vel": 0.004153974819928408,
          "reward/episode/rew_motion_global_body_ang_vel": 0.0039831348694860935,
          "reward/episode/rew_object_global_ref_position_error_exp": 0.005250684916973114,
          "reward/episode/rew_object_global_ref_orientation_error_exp": 0.0045945653691887856,
          "reward/episode/rew_action_rate_l2": -0.0027005858719348907,
          "reward/episode/rew_limits_dof_pos": -2.8372121319009125e-10,
          "reward/episode/rew_velocity_tracking": 0.012483793310821056,
          "reward/episode/rew_yaw_tracking": 0.0022897995077073574,
          "reward/episode/rew_height_tracking": 0.011526200920343399,
          "reward/episode/rew_grasp": 0.004134987015277147,
          "reward/episode/rew_stable_carry": 0.001104694209061563,
          "reward/episode/rew_box_orientation": 0.003999094944447279,
          "reward/episode/rew_hand_slip": 0.0006614295416511595,
          "reward/episode/rew_goal_compatible_style_reward": 0.0,
          "reward/episode/rew_nonhand_contact": -0.00041763941408134997,
          "reward/episode/termination/timeout": 0.0,
          "reward/episode/termination/clip_timeout": 0.023346303030848503,
          "reward/episode/termination/physical_failure": 0.9338521361351013,
          "reward/episode/termination/physical_failure/fall": 0.0,
          "reward/episode/termination/physical_failure/drop": 0.0,
          "reward/episode/termination/physical_failure/separation": 0.0,
          "reward/episode/termination/physical_failure/loss_of_grasp": 0.844357967376709,
          "reward/episode/termination/physical_failure/body_support": 0.11089494079351425,
          "reward/episode/termination/physical_failure/nonfinite": 0.0,
          "reward/episode/termination/track_failure": 0.04474708065390587,
          "reward/episode/termination/track_failure/ref_pos_z": 0.0,
          "reward/episode/termination/track_failure/ref_ori": 0.0,
          "reward/episode/termination/track_failure/body_pos_z": 0.0,
          "reward/episode/termination/track_failure/object_pos": 0.0,
          "reward/episode/termination/track_failure/object_ori": 0.04474708065390587,
          "reward/episode/termination/body_proximity": 0.0,
          "reward/episode/termination/body_proximity/group_0": 0.0,
          "reward/episode/hybrid/reward/track/rew_motion_global_ref_position_error_exp": 0.0026474050246179104,
          "reward/episode/hybrid/reward/track/rew_motion_global_ref_orientation_error_exp": 0.0026160674169659615,
          "reward/episode/hybrid/reward/track/rew_motion_relative_body_position_error_exp": 0.005352914333343506,
          "reward/episode/hybrid/reward/track/rew_motion_relative_body_orientation_error_exp": 0.00478110508993268,
          "reward/episode/hybrid/reward/track/rew_motion_global_body_lin_vel": 0.004153974819928408,
          "reward/episode/hybrid/reward/track/rew_motion_global_body_ang_vel": 0.0039831348694860935,
          "reward/episode/hybrid/reward/track/rew_object_global_ref_position_error_exp": 0.005250684916973114,
          "reward/episode/hybrid/reward/track/rew_object_global_ref_orientation_error_exp": 0.0045945653691887856,
          "reward/episode/hybrid/mean_reward/track": 1.9938490390777588,
          "reward/raw_episode/raw_rew_motion_global_ref_position_error_exp": 0.264740526676178,
          "reward/raw_episode/raw_rew_motion_global_ref_orientation_error_exp": 0.26160672307014465,
          "reward/raw_episode/raw_rew_motion_relative_body_position_error_exp": 0.2676457464694977,
          "reward/raw_episode/raw_rew_motion_relative_body_orientation_error_exp": 0.23905524611473083,
          "reward/raw_episode/raw_rew_motion_global_body_lin_vel": 0.2076987475156784,
          "reward/raw_episode/raw_rew_motion_global_body_ang_vel": 0.1991567313671112,
          "reward/raw_episode/raw_rew_object_global_ref_position_error_exp": 0.2625342309474945,
          "reward/raw_episode/raw_rew_object_global_ref_orientation_error_exp": 0.22972828149795532,
          "reward/raw_episode/raw_rew_action_rate_l2": 1.3502929210662842,
          "reward/raw_episode/raw_rew_limits_dof_pos": 1.418606010439305e-09,
          "reward/raw_episode/raw_rew_velocity_tracking": 0.20806322991847992,
          "reward/raw_episode/raw_rew_yaw_tracking": 0.11448997259140015,
          "reward/raw_episode/raw_rew_height_tracking": 0.1921033412218094,
          "reward/raw_episode/raw_rew_grasp": 0.068916454911232,
          "reward/raw_episode/raw_rew_stable_carry": 0.05523470789194107,
          "reward/raw_episode/raw_rew_box_orientation": 0.19995474815368652,
          "reward/raw_episode/raw_rew_hand_slip": 0.033071476966142654,
          "reward/raw_episode/raw_rew_goal_compatible_style_reward": 0.0,
          "reward/raw_episode/raw_rew_nonhand_contact": 0.010440985672175884
        },
        "mean_live_episode_s": 0.09964843839406967
      },
      "log_dir": "/home/han/pyx/g1_carry_baseline_new/artifacts/fullbody_goal_carry/run_20261120_133333/dashboard/benchmark/WholeBodyTracking/20261120_053341-bench4096-locomotion"
    }
  }
}

Unimplemented or unverified capabilities must be read from the measured acceptance tables, not inferred from finite PPO losses or rising rewards. Forward reference contact consistency is a known blocker. No unseen forward+height combinations, lateral motion or turning are certified. For vy/yaw extension, first admit compatible dynamic references and separately benchmark each command family. Failed policies and failed references are retained rather than hidden.

## Reproduction

See README_FULLBODY_CARRY.md for environment activation, validation, Stage 1/2, resume, automatic controller, TensorBoard, checkpoint evaluation, ONNX export, Viewer, interactive four-dimensional commands and goal grid. TensorBoard for this workspace: http://127.0.0.1:6011 .
