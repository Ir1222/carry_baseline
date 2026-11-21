# Stage 1 正式长训前审查

审查日期：2026-11-21。基线分支 `feature/fullbody-goal-carry-autotrain`，基线提交 `b0356f47989769656886217f3a90513134b9a9d8`。

## 结论：BLOCKER，暂不建议直接启动本轮15000次更新

发现确定的初始化一致性问题：**Reset噪声虽为零，参考关节角仍被95%软限位裁剪**，P0合法蹲起参考的腰俯仰偏差0.025900rad，左右腕偏航各偏差0.080621rad。训练实际初始姿态不等于验证参考。上一轮把奖励限位边界改为实际限位时，漏检了Reset仍使用95%软限位；本次按要求没有修复或更改这项行为。

这里的BLOCKER指正式运行前尚未解决的初始化契约问题，**不是证明PPO数学上不可能学习**。旧模型在新版首帧Reset下能够存活更久，短训练中蹲起也有改善。不能把所有失败归结为迭代不足，也不能仅归结为termination过严。

| 项目 | 结论 | 依据 |
|---|---|---|
| Actor/Critic、PPO、导出链路 | PASS | 348D/184D；真实短训练、Checkpoint/ONNX保存正常 |
| 三参考动作在动作裁剪范围内 | PASS | 所有帧、所有关节均在±100内 |
| 动作缩放、探索及力矩余量 | WARNING | 行走腕部动作需约±84；初始标准差0.3；行走初期约8.4%关节-子步发生力矩裁剪 |
| 初始化与参考/P0一致性 | **BLOCKER** | 零噪声仍被软限位裁剪；不是完整保留参考物理姿态 |
| 早期终止与学习窗口 | WARNING | 行走短训练回合约0.119秒，失握主导；Track误差不是主要早期原因 |
| 参考命令与坐标 | PASS | heading-frame vx/vy、world-z角速度、地面相对pelvis高度一致；runtime命令误差0 |
| 奖励/终止与参考时间 | WARNING | Robot/Object使用同一帧；物理推进后仍与步开始参考比较，有20ms相位偏差 |
| 联合训练覆盖 | PASS | 蹲起/行走各半环境，Track=1、Gen=0，完整29DoF |
| 正式训练/Stage 2 | 未启动 | 本次仅诊断、有限短训练及旧Policy短评估 |

行走仍按用户已批准的HMI Track目标准入参与审查；没有重新要求P0控制器先通过，也没有把它改标为physics-validated。单次失败、参考关节目标探针失败和32次短训练均不足以证明15000次一定失败。

## 1. 修改范围与证据

只增加 `stage1_diagnostics.py`、Stage1环境的只读日志Hook、`audit_stage1_pretrain.py` 和审查测试。Hook在真实termination检查之后记录，不重复调用termination，不写物理状态，不影响动作、奖励、采样、PPO或终止判定。按动作族增加真实完成回合长度、接触、滑移、Robot/Object误差、力矩裁剪与分原因终止日志。

没有修改任何NPZ、Manifest、物理资产、控制增益、动作比例、PPO配置、奖励、终止阈值或最终验收标准。所有证据位于本地 `../artifacts/stage1_pretrain_audit/`，旧Checkpoint未覆盖。短训模型仅用于审查，不是交付Policy。

三参考重新执行完整FK、速度导数、四元数、HMI MotionLoader检查，最大FK位置误差分别8.36e-8m、1.16e-7m、8.38e-8m，全部通过。SHA256与b0356f4的Manifest完全一致：

| Clip | SHA256 |
|---|---|
| continuous_grasped_squat_stand | `412681d73670e24c4a32401970710513ba9e3c2dd8b3205e2bf4c4a6a4f33a90` |
| original_forward_carry | `fe03f9072560cc75096c5a0cbcd1ae781a1fe9607c23fa8781ed257ebed98550` |
| repeated_grasped_squat_stand | `d6238a97fa785d94cdf9579f82c002f2b088c34267ba35465e0ed350932ca835` |

## 2. 动作可达性、PD与噪声

严格使用 `CarryEnv._configure_default_dof_pos()` 的已验证Reset `pd_target_joint_pos`，不是G1站姿配置默认值。计算：

```
action_scales[j] = 0.25 * effort_limit[j] / Kp[j]
a_ref[t,j] = (q_ref[t,j] - q_default[j]) / action_scales[j]
tau_raw = Kp*(q_default + action_scales*a - q) - Kd*qd
tau = clip(tau_raw, -effort_limit, effort_limit)
```

Physics/PD为1ms，Policy为20ms，decimation20，Reference50FPS。无期望关节速度前馈项；因此a_ref只是位置目标的逆映射，不是完整逆动力学或保证可以执行的控制器。

相对原始HMI preset，多数Kp乘4、Kd乘2，踝关节至少Kp250/Kd12。因action scale与Kp成反比，提高增益同时缩小了相同归一化动作对应的关节角变化。虽然仍是Track PPO，它的动作参数化和抓持早停条件不能直接当作与原始某次Track实验完全相同。

| Clip | 全关节动作极小/极大 | 超过±100比例 | 精确位置跟踪时最大阻尼力矩/限幅 | 原始动作差平方和均值 |
|---|---:|---:|---:|---:|
| 单周期蹲起 | -5.7764 / 7.3929 | 0 | 0.06482 | 0.01541 |
| 双周期蹲起 | -5.7764 / 7.3929 | 0 | 0.06482 | 0.01660 |
| 行走 | -84.9299 / 83.9899 | 0 | 1.31239 | 1.75591 |

行走的最大纯阻尼项超过限幅，意味着严格跟踪该位置/速度时必须有额外位置偏移来抵消阻尼，不能把“动作没有超过100”当作动态可执行性证明。参考位置探针使用真实PD和自由箱体，没有箱体写入或额外控制器。

仅在数值上加入阻尼抵消项 `a_ref + Kd*qd_ref/(Kp*action_scales)` 后，三条参考仍均未超过±100；未把该项加入控制器。这里只说明不存在由该项立即导致的动作裁剪障碍，不包含重力、惯性或接触力矩的可行性证明。

初始Policy高斯标准差0.3，映射后的每关节位置标准差为 `0.3*action_scales`（约0.00559～0.04107rad），力矩扰动标准差为额定限幅的7.5%，三倍标准差约22.5%。它与Reset噪声不同：Reset的关节、根位置/姿态/速度噪声配置全部为0，仍有上述软限位裁剪。固定物理下Kp/Kd缩放为1，控制延迟和随机外力未开启。

行走相对于高位侧向抓持默认姿态的某些腕部目标需约280个初始动作标准差。Actor输出未用tanh限制到±1，故不是硬不可达，但从零附近均值学习大偏移且在6个控制步左右丢失抓持，是明显的探索难点。动作变化惩罚使用原始动作，行走的归一化差平方和也明显大于蹲起；本次未改权重。

每关节完整统计（rad、N·m单位；动作本身无量纲；单/双周期的微小差别保留在原始CSV/JSON）：

| 关节 | Kp | Kd | 力矩限幅 | action scale | 单周期 a_min～a_max | 双周期 a_min～a_max | 行走 a_min～a_max |
|---|---:|---:|---:|---:|---:|---:|---:|
| left_hip_pitch_joint | 160.717 | 5.116 | 88 | 0.136887 | -2.5708～0.0000 | -2.5708～0.0000 | -0.6112～6.9761 |
| left_hip_roll_joint | 396.394 | 12.618 | 139 | 0.087665 | -0.0444～0.0026 | -0.0444～0.0026 | -1.2136～3.1899 |
| left_hip_yaw_joint | 160.717 | 5.116 | 88 | 0.136887 | -0.0713～-0.0000 | -0.0713～-0.0000 | 1.7343～7.6737 |
| left_knee_joint | 396.394 | 12.618 | 139 | 0.087665 | 0.0000～7.3449 | 0.0000～7.3449 | -5.9377～6.2097 |
| left_ankle_pitch_joint | 250.000 | 12.000 | 50 | 0.050000 | -5.7359～0.0000 | -5.7359～0.0000 | -5.4742～7.7285 |
| left_ankle_roll_joint | 250.000 | 12.000 | 50 | 0.050000 | -0.0769～-0.0000 | -0.0769～-0.0000 | -2.1567～5.5898 |
| right_hip_pitch_joint | 160.717 | 5.116 | 88 | 0.136887 | -2.5866～-0.0000 | -2.5866～-0.0000 | 1.2144～7.3781 |
| right_hip_roll_joint | 396.394 | 12.618 | 139 | 0.087665 | -0.0000～0.0358 | -0.0000～0.0358 | -3.7274～1.8483 |
| right_hip_yaw_joint | 160.717 | 5.116 | 88 | 0.136887 | -0.0000～0.0521 | -0.0000～0.0521 | -7.0837～-1.1092 |
| right_knee_joint | 396.394 | 12.618 | 139 | 0.087665 | -0.0000～7.3929 | -0.0000～7.3929 | -6.8350～5.3127 |
| right_ankle_pitch_joint | 250.000 | 12.000 | 50 | 0.050000 | -5.7764～0.0000 | -5.7764～0.0000 | -7.0603～8.3298 |
| right_ankle_roll_joint | 250.000 | 12.000 | 50 | 0.050000 | -0.0000～0.1041 | -0.0000～0.1041 | -5.6774～2.5979 |
| waist_yaw_joint | 160.717 | 5.116 | 88 | 0.136887 | 0.0000～0.0505 | 0.0000～0.0505 | -1.3383～1.0797 |
| waist_roll_joint | 114.005 | 3.629 | 50 | 0.109644 | -0.0043～0.0031 | -0.0043～0.0031 | -1.4732～0.9279 |
| waist_pitch_joint | 114.005 | 3.629 | 50 | 0.109644 | -0.0002～0.0000 | -0.0002～0.0000 | -3.4634～-0.1997 |
| left_shoulder_pitch_joint | 57.002 | 1.814 | 25 | 0.109644 | -0.0717～0.0250 | -0.0717～0.0250 | 9.8677～11.2934 |
| left_shoulder_roll_joint | 57.002 | 1.814 | 25 | 0.109644 | -0.0641～-0.0000 | -0.0641～-0.0000 | -5.0107～-3.4948 |
| left_shoulder_yaw_joint | 57.002 | 1.814 | 25 | 0.109644 | -0.0188～0.0000 | -0.0188～0.0000 | 7.9687～9.0451 |
| left_elbow_joint | 57.002 | 1.814 | 25 | 0.109644 | -0.0000～0.0462 | -0.0000～0.0462 | -4.4734～-3.8252 |
| left_wrist_roll_joint | 57.002 | 1.814 | 25 | 0.109644 | -0.0044～0.0234 | -0.0044～0.0234 | -16.1601～-16.1601 |
| left_wrist_pitch_joint | 67.113 | 2.136 | 5 | 0.018625 | -0.2450～-0.0000 | -0.2450～-0.0000 | 67.0987～72.6003 |
| left_wrist_yaw_joint | 67.113 | 2.136 | 5 | 0.018625 | -0.0005～0.0000 | -0.0005～0.0000 | -84.9299～-83.9899 |
| right_shoulder_pitch_joint | 57.002 | 1.814 | 25 | 0.109644 | -0.0004～0.0319 | -0.0004～0.0319 | 8.4445～10.1622 |
| right_shoulder_roll_joint | 57.002 | 1.814 | 25 | 0.109644 | -0.0767～0.0083 | -0.0767～0.0083 | 3.1568～4.3913 |
| right_shoulder_yaw_joint | 57.002 | 1.814 | 25 | 0.109644 | -0.0184～0.0059 | -0.0184～0.0059 | -5.5127～-3.4925 |
| right_elbow_joint | 57.002 | 1.814 | 25 | 0.109644 | -0.0451～0.0028 | -0.0451～0.0028 | -3.4322～-2.3725 |
| right_wrist_roll_joint | 57.002 | 1.814 | 25 | 0.109644 | 0.0000～0.0218 | -0.0000～0.0218 | 16.2938～16.6911 |
| right_wrist_pitch_joint | 67.113 | 2.136 | 5 | 0.018625 | -0.1910～0.0001 | -0.1910～0.0001 | 71.7653～71.7653 |
| right_wrist_yaw_joint | 67.113 | 2.136 | 5 | 0.018625 | -0.0000～0.0004 | -0.0000～0.0004 | 83.9899～83.9899 |

## 3. Reset与termination

Stage1首个Reset已经移除旧入口的20ms零动作推进。本次审查中首观测的Robot根位置/Object位置与参考误差0，348D/184D维度正确。关节状态则由 `MotionCommand.reset()` 用 `simulator.dof_pos_limits` 裁剪；后者由 `robot.soft_dof_pos_limit=0.95` 生成。Reward的 `soft_dof_pos_limit=1.0` 不会改变这个Reset裁剪范围。

| 规则 | 实际含义 |
|---|---|
| fall | pelvis离地<0.45m，或根z轴与世界z轴点积<0.5 |
| drop | 真实箱体凸包底离地<0.03m，随蹲起合法下降不触发 |
| separation | 箱体根与Robot根距离>0.9m |
| loss_of_grasp | 每个1ms子步双手各法向力>0.5N才计为接触；20子步平均接触率须>0.99才清零unsupported；否则每控制步累计0.02秒；episode>0.1秒且unsupported>0.02秒时失败 |
| body_support | episode>0.1秒，非sphere_hand且非foot_contact_point的Robot–Box总法向力>0.5N |
| nonfinite | Robot/Object根状态或Robot关节位置非有限 |
| track_failure | 根z误差>0.4m；投影重力z差>0.4；指定足/腕z误差>0.25m；箱体位置误差>0.3m或姿态误差>0.8rad |
| body_proximity | 左右足接触点距离<0.05m |
| clip_timeout | 到本Clip最后一帧；按真实clip边界正常结束，不当作物理失败 |

`loss_of_grasp`并非“平均双手力>0.5N即可”，而是近乎20/20个子步均接触。只有19/20接触也会累计unsupported；宽限过后累计至少两个不合格控制步即可失败。实际最早通常是第6个控制步（约0.12秒）。这是比原始HMI Track额外增加的严格抓持条件。

Track阈值0.4m/0.25m/0.3m与12cm合法蹲起不会直接冲突，且检查的是相对参考误差。此次早期rollout中fall、drop、separation和足部接近均不是主导原因。真实失握与非手部接触保持生效，失败仍优先于timeout；没有通过关闭它们延长Episode。

## 4. 真实短rollout

第一组：64环境、种子1000，既测原训练Reset分布（各族32环境），也测单周期高位/低位、行走首帧和双周期首帧。每条件至多2秒，只计首次Episode、在自动Reset之前捕获终态。各环境复制同一指定姿态不等于64个独立种子；不是最终成功率实验。

| 控制来源，训练Reset | 动作族 | 平均存活s | 双手接触率（按有效控制步） | Robot/Object均值误差m | 力矩裁剪（关节×子步） |
|---|---|---:|---:|---:|---:|
| 零动作 | 蹲起 | 0.1831 | 72.87% | 0.02245 / 0.07220 | 0.181% |
| 零动作 | 行走 | 0.1175 | 5.35% | 0.06366 / 0.05190 | 8.379% |
| 当前参考位置目标 | 蹲起 | 0.1600 | 68.32% | 0.01536 / 0.05920 | 0.0438% |
| 当前参考位置目标 | 行走 | 0.1238 | 10.78% | 0.01679 / 0.03471 | 0% |
| 提前一帧参考位置目标 | 蹲起 | 0.1850 | 72.08% | 0.01760 / 0.07220 | 0.0373% |
| 提前一帧参考位置目标 | 行走 | 0.1194 | 7.46% | 0.01656 / 0.03069 | 0.0090% |

这些参考动作探针只诊断控制/Reset，不是Actor，更不是用参考直接驱动来宣称Policy通过。它们说明单纯q_ref目标不自动产生需要的侧向夹紧力；提前20ms也没有消除早期失败。不能据此重新设置“必须P0控制器成功才准入”的门槛。

训练Reset中当前参考探针：蹲起32次里25次body_support、7次loss_of_grasp；行走32次里30次loss_of_grasp、2次body_support。多种终止可重叠，其他表中的百分比不强求相加100%。

旧的 `model_05500.onnx` 也在**新版Stage1 Reset和物理配置**中测试，并未加载进新PPO。64环境2秒短测，高位/低位/双周期起始状态全部存活到2秒；行走首帧平均0.342秒，52/64为Object位置超差、12/64失握，不能拿只训练过蹲起的旧Policy证明行走参考不能学习。

另用16环境、seed1001、最长14秒检查旧模型完整片段（302.33秒，GPU峰值3228MiB）：

| 初态 | 实际存活范围s | 结束原因 | 接触率 | Robot/Object误差m |
|---|---:|---|---:|---:|
| 单周期首帧 | 7.02～7.02 | 16/16自然Clip Timeout | 98.67% | 0.01649 / 0.08415 |
| 单周期低位第175帧 | 3.52～3.52 | 16/16自然Clip Timeout | 97.38% | 0.01447 / 0.09014 |
| 行走首帧 | 0.12～0.38 | 5次失握，11次Object位置超差 | 81.20% | 0.16218 / 0.10382 |
| 双周期首帧 | 13.02～13.02 | 16/16自然Clip Timeout | 99.28% | 0.01579 / 0.08610 |

存活到Clip结束**不等于蹲起幅度、全身动作或最终物理验收通过**。旧模型的Object位置误差约8～9cm，明显超过最终4cm门槛，部分接触率也不足99%；本次不是10个独立种子的正式验收。旧模型Metadata的q_default、action_scales、PD gains及20ms频率与当前环境一致（仅浮点舍入差异），没有用不匹配的控制接口解释这些结果。

补充接触细查：32环境、seed1002、仅参考位置目标、每条件最多0.5秒，运行22.45秒。高位首帧中14/32回合因loss_of_grasp结束，**这14个回合最后一个1ms子步均有双手接触，最后20ms窗口接触率仍未满足>0.99**。这表明当前规则会截断正在恢复接触的状态，不等同于最后时刻双手均已脱离。行走首帧32/32失握，最后子步也均未形成双手接触；此类失败不能解释成仅1ms接触抖动。

高位首帧另有18/32触发body_support，终态非手部总法向力约0.502～0.623N。该规则不检查接触方向/持续时间或是否承担箱体重量，标签body_support实际上意味着“检测到超过0.5N的非手部接触”，不能仅凭标签断言机器人在用身体托箱。低位的非手部力可达约3.24～11.52N，不能把所有此类失败当作无关紧要的瞬态。保持原判定，记录证据供后续独立审议。

## 5. 真实短训练与分族日志

从头运行原HMI PPO，256环境、seed42、32次更新，每次24控制步/环境；未改奖励、PPO参数或阈值。运行249.19秒（含启动/导出），GPU峰值3452MiB，正常结束，有限数与接口检查通过。不是收敛测试。

最后一次ONNX导出的PyTorch/ONNX最大绝对误差6.56e-7。完整路径由 `short_train_seed42_data/worker/worker_result.json` 的log_dir记录；该短训目录中的 `model_00031.pt` / `.onnx` 对应32次已完成更新。

| 累计完成回合指标 | 蹲起 | 行走 |
|---|---:|---:|
| 完成Episode数量 | 10936 | 16501 |
| 平均回合秒 | 0.17745 | 0.11875 |
| ≤0.2秒即结束 | 82.40% | 100% |
| 双手接触连续率（每回合先平均，再按回合平均） | 46.27% | 4.59% |
| Robot/Object跟踪误差m | 0.02768 / 0.04076 | 0.06513 / 0.04991 |
| 手箱相对速度m/s | 0.3796 | 1.8413 |
| 左/右法向力均值N | 6.05 / 6.20 | 4.81 / 6.43 |
| 力矩裁剪比例 | 0.352% | 8.426% |
| loss_of_grasp | 77.22% | 97.84% |
| body_support | 19.83% | 0.024% |
| track_failure | 8.17% | 0% |

前8次和后8次更新采用累计计数差计算，不混淆累计均值与当前窗口：

| 动作族 | 前8次回合秒 → 后8次 | 接触率 | 失握终止率 | Track失败率 |
|---|---|---|---|---|
| 蹲起 | 0.12861 → 0.27550 | 28.38% → 68.34% | 93.57% → 47.90% | 0.053% → 31.88% |
| 行走 | 0.11902 → 0.11863 | 5.18% → 4.12% | 98.27% → 97.75% | 0% → 0% |

蹲起确实出现早期学习进展，后期才更多碰到Track终止；行走几乎一直在失握宽限出口失败。不能由32次更新断言15000次无用，但也不能仅以“和原始Track一样”推断已经具备可靠长训初始化。

TensorBoard实查存在102条分族Scalar，末更新step31，包括：

```
Env/stage1/{squat_stand,forward_carry}/completed_episodes
Env/stage1/{family}/completed/episode_length_s
Env/stage1/{family}/completed/contact_continuity
Env/stage1/{family}/completed/robot_tracking_error_m
Env/stage1/{family}/completed/object_tracking_error_m
Env/stage1/{family}/completed/torque_clip_fraction
Env/stage1/{family}/completed/termination/physical_failure/loss_of_grasp
Env/stage1/{family}/completed/termination/track_failure
Env/stage1/{family}/step/...
```

`completed/*`为本进程累计完成回合统计；`step/*`为当前控制步在该动作族中的均值。Clip自然结束也纳入完成回合，和物理失败分开记录。跨Checkpoint的诊断计数重新开始，不影响训练恢复。

## 6. 时间、坐标和奖励的一致性

NPZ根姿态为xyz+wxyz，q为后29列，qd为后29列（前6列根速度）。HMI Loader将body/object四元数转换为xyzw；Isaac Lab Object的wxyz在观测入口转换一次。位置添加env_origins，速度不添加平移；重新FK和loader检查通过。NPZ pelvis位置与q根位置误差0，角速度字段差最大约2.09e-6rad/s。

四维命令为 `[R_yaw(ref_root)^T*v_world 的x/y, ref_omega_world_z, pelvis_world_z-ground_z]`。这里yaw_rate是world-z角速度分量，不是机身坐标角速度，也不严格等于大倾斜时的Euler yaw导数。Actor实际速度也用yaw-heading系，actual yaw项同取root world-z角速度，因此定义一致。四维命令runtime与独立重算最大误差0，不依赖Terminal Goal。

行走参考并非严格直线：vx约0.293～0.787m/s，vy约-0.082～0.238m/s，world-z角速度约-2.053～1.434rad/s。Stage1按完整参考导出这些值，符合Track定义；不能将它误述为Stage1也强制vy/yaw=0。第一轮Gen的零横移/零转向约束属于后续Stage2。

实际Isaac Sim顺序：

```
Actor观测/参考k → action → 20×1ms物理推进
→ termination(k) → Robot/Object奖励(k) → 分族日志
→ 失败环境Reset → 未失败环境参考k+1 → 下一Actor观测
```

审查rollout逐步断言：termination看到的index等于动作前index，未失败环境随后恰好推进1帧，各Clip边界夹紧，没有跨Clip串读。Robot/Object奖励均使用同一个index，没有一个跟k、另一个跟k+1的混用。但是post-action状态与reference(k)比较存在20ms滞后；参考箱体单帧最大位移蹲起2.25mm、行走13.10mm，相比Object奖励sigma0.3m、Track终止0.3m较小，不能解释0.12秒失握的全部现象。

Robot全局参考位置/姿态奖励使用原HMI参考body；相对body奖励使用按参考body平移/偏航对齐的全身目标，body速度为world系。Object位置/姿态奖励使用带env_origin的绝对world参考，属于原HMI设计，而非与Robot完全相同的局部锚定。八项原始Robot/Object奖励、sigma和权重均未改；目标与命令同帧，但存在上述共同一帧时序偏差。

## 7. 上次失败能归因于termination太严格吗

1. **训练进程为什么停止**：旧最终报告记录 `Job timeout/budget reached: stage1_training`。那是外部训练管理停止原因，不是单个Episode的termination，也不等于达到15000次。新版单次训练入口已无该预算/切段机制，本次未改。
2. **早期回合为什么短**：当前新训练的行走约98%因loss_of_grasp在宽限出口结束，确实存在强烈的探索截断；不是Track误差0.4m/0.3m“太严格”造成。蹲起亦先失握，学会部分夹持后才更多触发Track检查。
3. **旧评估为什么极早失败**：旧首Reset在Actor接管前有20ms零动作，b0356f4已移除。本次旧模型在新版Reset能存活到单周期末尾，因此不能再把此前0/20完全解释为“Policy一点都没学会”，也不能据此声称它已满足最终精度/接触/滑移标准。
4. **不能排除的共同因素**：95%软限位对合法参考的隐式裁剪；从高位夹持q_default控制所有行走姿态导致的大动作偏移；探索/力矩裁剪；行走尚未物理认证以及纯位置目标缺少接触预紧。当前证据不支持把termination认定为唯一根因，也不支持偷偷放宽它来制造进展。

本次保持所有阈值和验收标准。正式训练前至少应单独审议并修复零噪声Reset的隐式裁剪，再用同一探针和短训练验证初始化与物理抓持。是否调整**训练期**失握宽限或接触判定，需要新的明确授权和可比实验；不等于降低最终验收。不得以这份报告为依据自动改增益、数据或启动Stage2。

## 8. 复现命令与测试

以下均为本机已执行的入口；输出目录必须全新，避免覆盖证据。短训练命令明确为32次，不是正式15000次训练。

```bash
cd /home/han/pyx/g1_carry_baseline_new/HMI
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV LD_LIBRARY_PATH
export PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
../envs/g1_hmi_carry/bin/python scripts/carry/audit_stage1_pretrain.py \
  --output ../artifacts/stage1_pretrain_audit/reproduce_static

../envs/g1_hmi_carry/bin/python scripts/carry/run_bounded.py \
  --name reproduce_runtime --output-root ../artifacts/stage1_pretrain_audit --timeout 420 \
  --require-result ../artifacts/stage1_pretrain_audit/reproduce_runtime_data/rollouts.json -- \
  ../envs/g1_hmi_carry/bin/python scripts/carry/audit_stage1_pretrain.py \
  --output ../artifacts/stage1_pretrain_audit/reproduce_runtime_data \
  --runtime --num-envs 64 --seconds 2 --seed 1000 \
  --policy ../artifacts/fullbody_goal_carry/stopped_stage1_policy_20261121/model_05500.onnx

../envs/g1_hmi_carry/bin/python scripts/carry/run_bounded.py \
  --name reproduce_short_train --output-root ../artifacts/stage1_pretrain_audit --timeout 600 \
  --require-result ../artifacts/stage1_pretrain_audit/reproduce_short_train_data/worker/worker_result.json -- \
  bash scripts/carry/train_stage1_joint.sh --num-envs 256 --iterations 32 --save-every 16 \
  --seed 42 --run-dir ../artifacts/stage1_pretrain_audit/reproduce_short_train_data

../envs/g1_hmi_carry/bin/python scripts/carry/run_bounded.py \
  --name reproduce_old_clips --output-root ../artifacts/stage1_pretrain_audit --timeout 600 \
  --require-result ../artifacts/stage1_pretrain_audit/reproduce_old_clips_data/rollouts.json -- \
  ../envs/g1_hmi_carry/bin/python scripts/carry/audit_stage1_pretrain.py \
  --output ../artifacts/stage1_pretrain_audit/reproduce_old_clips_data --runtime \
  --num-envs 16 --seconds 14 --seed 1001 --modes old_policy \
  --conditions squat_high squat_low walking_start repeated_start \
  --policy ../artifacts/fullbody_goal_carry/stopped_stage1_policy_20261121/model_05500.onnx

../envs/g1_hmi_carry/bin/python -m pytest tests/test_carry_interface.py \
  tests/test_carry_supervisor.py tests/test_fullbody_carry.py \
  tests/test_stage1_joint.py tests/test_stage1_pretrain_audit.py -q

../envs/g1_hmi_carry/bin/python -m tensorboard.main \
  --logdir ../artifacts/stage1_pretrain_audit --host 127.0.0.1 --port 6013
```

当前相关测试：**32 passed**。完整失败日志、原始NPZ rollout、按关节动作范围CSV、静态JSON、32次更新日志、Checkpoint、ONNX及TensorBoard均保存在本地证据目录。没有使用它们来宣称收敛或通过正式物理验收。
