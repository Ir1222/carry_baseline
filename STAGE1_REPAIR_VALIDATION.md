# Stage 1 修复与短训练对照

> 本文件保留历史运行语义。2026-11-22新修复与当前执行状态以[Stage1支撑修复记录](STAGE1_SUPPORT_REPAIR_20261122.md)为准；历史full_training_ready或未训练策略成功率不作为开训门禁。

日期：2026-11-21。基线：`feature/fullbody-goal-carry-autotrain` / `d2281cf9c404c823cb4f457be6dd4e0fa8dcbd20`。本报告对应修复提交可由 `git log -1` 查询。

## 结论

**Reset BLOCKER及参考时序问题已修复，动作偏置问题有可用的参考无关参数化；Forward抓持兼容性仍未通过，本次不建议直接启动15000次正式训练。**

| 项目 | 结果 |
|---|---|
| P0：合法硬限位参考的精确Reset | PASS，真实Isaac Sim三Clip×四帧共12组，实际关节位置最大误差0rad |
| P1：消除固定q_default造成的±84动作偏置 | PASS，`joint_delta_v1`不改变增益、原动作尺度或探索std；显著降低Forward力矩裁剪 |
| P1：行走参考与P0侧向抓持几何一致 | **未通过**；腕姿态和半球朝向不同，采样帧右手顶点凸包signed-gap代理值达15.8mm（非精确网格间距离）；参考位置探针不能建立持续双手接触 |
| P2：post-action奖励/终止对齐下一帧 | PASS，首帧、普通帧、重复调用、Clip边界、真实自然结束均验证 |
| P3：同条件32次PPO更新、保存/导出/推理 | PASS训练链路；不是Policy物理成功 |
| 正式Policy验收 | 未通过，短模型三Clip各0/2；未启动正式长训或Stage2 |

Forward早期指标确有改善，并非完全没有学习：累计接触率4.59%→19.69%，最后8次更新的窗口接触率达到42.23%。但平均回合仍短、失握仍主导，不能将其标记为已解决真实侧向搬运。这里保留用户已批准的Track目标准入，不重新要求P0控制器先通过；只是明确记录尚未解决的抓持方式一致性问题，不擅自修改或替换行走数据。

## 保持不变的内容

三NPZ和Manifest、原始G1 29DoF、半球手、LargeBox几何、碰撞、重力、实际1.1kg质量、惯量和摩擦、PD gains、原effort/Kp action scales、力矩上限及裁剪、初始Policy std=0.3、50/50动作族、所有Reward函数/权重、termination与最终物理验收门槛均保持。PPO仍是原HMI共享Actor/Critic；Actor348D、Critic184D，四维命令不变，无Reference Pose/ID/Phase输入，无Gen或AMP训练。

所有模型与失败记录保存在新目录 `../artifacts/stage1_repair_validation/`；未覆盖旧Checkpoint、P0资产或d2281cf的审查证据。三NPZ原SHA256继续由Manifest校验。

## P0：Stage1专用精确Reset

原 `MotionCommand.reset()` 直接将参考初始化裁剪到 `simulator.dof_pos_limits`（95%软范围），即使噪声为零也改变合法姿态。现在用一个可覆盖的 `_prepare_reset_joint_positions()` Hook：基类默认行为仍是原软限位裁剪；只有 `Stage1TrackCommand` 改为校验后原样返回。

Stage1从PhysX实际资产读取硬限位，按实际DOF顺序与配置交叉检查，并在setup校验整个Motion Bank。Reset时再次校验所选参考和目标；若超出硬限位会报错，写入本次输出目录下 `stage1_failures/stage1_invalid_reference.json`，包括关节、行、数值和上下限，不静默修正。仅留1e-6rad的浮点序列化容差，**不做任何位置裁剪**。非零关节初始化扰动也不会被悄悄接受。

真实测试覆盖每条Clip的0、约1/4、约1/2、倒数第二帧，各16环境。检查实际q/qd、Robot根位置/四元数/线角速度、Object位置/四元数/线角速度与参考一致（比较容差2e-6）；q实测误差最大0rad。全局95%软限位数组前后完全不变。接触传感器、力阈值及子步平均方法不改。

证据：`reset_clock_delta_final_data/validation.json`；12组Reset、3次自然Clip结束全部通过，13.99秒、GPU峰值3228MiB。此前固定动作模式的同组测试也通过。

## P1：原因、几何诊断与参数化

### 固定默认姿态为什么产生±84动作

旧定义 `q_target=q_P0_default+scale*a`，其中 `scale=0.25*effort/Kp`。腕pitch/yaw scale约0.018625rad/action，力矩限幅5N·m。P0侧夹默认腕yaw约±1.614rad，Forward约±0.05rad；约1.56rad的姿态差被除以很小的scale，产生约84的原始动作。这不是Actor被限制为±1，也不是NPZ关节顺序错误。

| 腕姿态 | P0单/双周期蹲起 | Forward |
|---|---|---|
| 左roll | 约1.671～1.674rad | 约-0.100rad |
| 左pitch | 约-1.057～-1.052rad | 约0.198～0.300rad |
| 左yaw | 约1.614rad | 约0.032～0.050rad |
| 右roll | 约-1.630～-1.628rad | 约0.156～0.200rad |
| 右pitch | 约-1.040～-1.037rad | 约0.300rad |
| 右yaw | 约-1.614rad | 约-0.050rad |

对比仓库原始 `movebox/sub3_largebox_003_mj_w_obj_reframed.npz` 的95～204帧：Forward的完整joint_pos、Object位置、Object四元数最大差分别5.85e-8、5.85e-8、2.94e-8，属于float32舍入。其腕/臂姿态来自原始HMI，不是此次Loader意外变换。还比较了未reframe的原始 `sub3_largebox_003_mj_w_obj.npz`，几何趋势相同。

### 半球朝向与真实接触法向分别报告

使用实际URDF、完整半球网格与原LargeBox凸包做FK。几何方向/间隙按stride20及末帧采样；完整关节范围用全部帧。密集全帧网格SDF枚举曾因成本过高主动停止，未将未完成结果当作证据。采样帧列表和源文件SHA均保存在 `geometry_sampled.json`。

| 几何量（左/右） | 单周期 | 双周期 | Forward |
|---|---|---|---|
| 半球+z轴与目标侧面向内方向平均点积 | 0.99985 / 0.99986 | 0.99985 / 0.99986 | -0.0430 / -0.0530 |
| 半球+z轴竖直分量绝对值均值 | 0.0111 / 0.0103 | 0.0111 / 0.0103 | 0.7254 / 0.8257 |
| 半球顶点到箱凸包最大采样signed gap | -1.65 / -1.56mm | -1.65 / -1.56mm | -2.19 / +15.81mm |

负signed gap表示采样网格顶点进入箱体凸包，正值表示最近采样顶点仍在外部。这是几何诊断，不是物理成功证明，也不能由半球+z轴直接推断接触法向：半球侧缘仍可能产生水平法向。

真实参考位置探针的有效单手接触中，蹲起左右法向竖直占比约0.02；Forward约0.05～0.06，**并非测到了竖直承托法向**。但Forward首帧64环境的整个首次Episode双手同时接触率为0，全部约0.12秒失握。说明关键问题是持续双手几何/接触协调，不应把方向统计或单手有力误当作双手侧夹成功。

### 新动作定义

```
q_center = actual_joint_pos sampled once at policy-step start
q_target = q_center + original_action_scales * clipped_actor_action
tau = clip(Kp*(q_target-q_actual) - Kd*qd_actual, original_torque_limits)
```

`q_target`在20个1ms PD子步中保持，不能每个PD子步重新居中。没有Reference目标前馈、P0控制器、绑箱或物体位姿写入。只改变PD目标中心，原Kp/Kd/scales/std/torque clipping复用原实现。理想参考跟踪时，下一帧增量动作范围：单/双周期约[-0.13760,0.13760]，Forward约[-1.24298,2.46879]；不会再因两类动作的固定姿态差需要±84。实际偏离参考时的动作仍由PPO学习，不能把理想范围当作策略实测性能。

该定义只用实测q，对Track与未来reference-free Gen完全相同，不读取Goal、MotionLoader、Track/Gen mask或phase。`q_default`仍用于原348D物理观测居中，角色不再是该模式的PD目标中心。Actor输出仍29D，原动作差正则函数及权重不变，但其物理含义现在是关节增量变化，不能称作纯数值重标定。

保留为Stage1默认**候选** `joint_delta_v1`；显式 `HMI_CARRY_ACTION_MODE=fixed` 可复现实验中的旧解码。旧FullBody实验未设置该变量时仍用原固定中心；未来Gen可显式选用同一ActionTerm，不存在按动作族切换中心。没有运行Gen训练。

ONNX Metadata记录 `action_parameterization`、目标定义、动作裁剪及q_default角色，Viewer评估按Metadata选择同一解码。`CarryActor.joint_position_target()`可在无Reference时解码，必须每个Policy周期调用一次并保持目标。Checkpoint记录Reset/时序及动作协议，拒绝直接恢复d2281cf旧协议或跨fixed/delta恢复。

## P2：正确的参考时序

```
Reset reference(k), physical state(k), observation/command(k)
→ Actor(action_k) → 20×1ms physics → physical state(k+1)
→ advance reference to k+1, update reference-derived command/aligned body targets
→ termination(k+1), Robot/Object rewards(k+1), diagnostics
→ reset failed/finished environments only
→ observation(k+1); callback refreshes references without advancing again
```

采用Stage1专用pre-termination Hook，没有改变其他实验的BaseTask时序。每环境记录本Episode已对齐控制步，重复检查不重复推进；时钟跳步报错。最后一帧用于本次物理结果的跟踪检查后自然结束，不跨Clip、不瞬移续接。整个过程不增加Actor参考输入。

回归测试涵盖Reset首帧不推进、普通帧推进一次、重复callback不推进、边界夹紧、自然结束与非法时钟跳步。真实三个Clip从倒数第二帧各执行一步，捕获到末帧目标、正确timeout且没有物理失败；终态在自动Reset前捕获。

## P3：256环境×32更新，seed42

三组使用相同256环境、24步rollout、32更新、seed42、PPO epochs/minibatches、初始std0.3、固定物理、采样比例和Reward/termination。d2281cf为已保存的原始基线；两个修复试验均从头开始。单种子对照不提供统计显著性证明。

| 配置 | 动作族 | 回合秒 | 双手接触率 | 失握终止率 | Robot误差m | Object误差m | 力矩裁剪率 |
|---|---|---:|---:|---:|---:|---:|---:|
| d2281cf基线 | squat_stand | 0.17745 | 46.273% | 77.222% | 0.02768 | 0.04076 | 0.35168% |
| d2281cf基线 | forward_carry | 0.11875 | 4.595% | 97.836% | 0.06513 | 0.04991 | 8.42619% |
| Reset/time修复+fixed | squat_stand | 0.17408 | 47.652% | 77.958% | 0.02826 | 0.03805 | 0.51065% |
| Reset/time修复+fixed | forward_carry | 0.11834 | 4.567% | 97.574% | 0.06743 | 0.04616 | 8.51949% |
| Reset/time修复+delta | squat_stand | 0.16774 | 49.498% | 59.244% | 0.02121 | 0.04612 | 0.29204% |
| Reset/time修复+delta | forward_carry | 0.14323 | 19.693% | 84.788% | 0.02181 | 0.03729 | 0.00203% |

统计为每个已结束Episode先取均值、再在动作族内累计平均；loss与其他终止原因可能重叠。没有用尚未结束的长回合冒充已成功回合。

最后8次更新窗口：fixed的Forward回合0.11834秒、接触3.97%、失握97.64%；delta为0.18105秒、42.23%、63.55%。delta的Squat/Stand接触77.42%、失握21.03%，但Object误差约7.22cm，高于fixed约5.60cm。这一取舍保留，不能只展示接触改善而隐藏跟踪误差。

| 试验 | 正常完成更新 | 耗时含启动/导出 | GPU峰值 |
|---|---:|---:|---:|
| Reset/time修复，fixed | 32 | 250.94秒 | 3452MiB |
| Reset/time修复，delta | 32 | 266.12秒 | 3452MiB |

两组均无OOM、无非有限数错误、Checkpoint/ONNX保存正常。delta最终PyTorch/ONNX最大输出差9.54e-7。单独禁止导入命令/Reference Loader的进程仍可加载ONNX、用物理张量和四维Goal完成推理及关节目标解码；该测试只证明接口。

真实参考位置探针（64环境、seed1000、每条件最多2秒）使用真实自由箱体：

| 下一帧参考位置目标 | 平均存活秒 | 双手接触率 | 主要失败 |
|---|---:|---:|---|
| 单周期高位首帧 | 0.26750 | 84.67% | 失握51/64，非手部接触13/64，另有重叠Track失败 |
| 单周期低位 | 0.14250 | 71.84% | 非手部接触64/64 |
| Forward首帧 | 0.12000 | 0% | 失握64/64 |
| 双周期首帧 | 0.26937 | 85.09% | 失握53/64，非手部接触11/64，另有重叠Track失败 |

当前帧/下一帧两个探针及训练Reset分布的完整结果保留在 `reference_probes_final_data/`，不只保存成功片段。探针不是最终Actor，未用参考控制器制造Policy通过。

另用delta短模型执行真实三Clip ONNX评估链路，每Clip2个种子，结果各0/2，`accepted_policy=false`。这是未收敛模型，绝不标为最终可用Policy；也不能用32次更新的失败证明15000次一定失败。

## 修改文件与验证入口

- `managers/command/terms/wbt.py`：提取Reset关节位置Hook，基类行为不变。
- `carry/stage1_command.py`、`stage1_environment.py`、`fullbody_environment.py`：精确硬限位校验、错误证据、post-action时钟、恢复协议及跨Track/Gen解码一致性保护。
- `managers/action/terms/joint_control.py`：默认位置中心Hook，原PD/裁剪实现不变。
- `carry/action.py`：共享参考无关小增量ActionTerm及解码定义。
- `carry/stage1_presets.py`、`fullbody_presets.py`：候选模式和显式共用接口，不改奖励或物理。
- `carry/fullbody_ppo.py`、`inference.py`、`evaluate_fullbody.py`：Metadata、无参考解码与匹配评估。
- `validate_stage1_repair.py`、`diagnose_carry_geometry.py`、更新审查脚本及测试：真实验证与诊断。
- `autoresearch.md/.sh/.jsonl`：有限试验与保留决策；README更新当前风险。

相关Carry与原HMI命令/终止/WBT测试合计101项通过。非法硬限位负例会生成错误记录，未改输入张量。测试还验证旧MotionCommand仍用原软范围、delta中心跨PD子步保持、继承力矩裁剪、独立部署解码一致及未来Gen误用另一解码时拒绝恢复。

```bash
cd /home/han/pyx/g1_carry_baseline_new/HMI
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV LD_LIBRARY_PATH
export PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1

# 全新目录，真实Reset/时钟验证；不会启动训练
HMI_CARRY_ACTION_MODE=joint_delta ../envs/g1_hmi_carry/bin/python \
  scripts/carry/validate_stage1_repair.py --output ../artifacts/stage1_repair_validation/reproduce_reset

# 有界短对照，各32次更新；不调用15000次长训
export HMI_STAGE1_REPAIR_OUTPUT="../artifacts/stage1_repair_reproduce_$(date +%Y%m%d_%H%M%S)"
bash autoresearch.sh fixed
bash autoresearch.sh joint_delta

# 观察本轮审查/短训日志
../envs/g1_hmi_carry/bin/python -m tensorboard.main \
  --logdir ../artifacts/stage1_repair_validation --host 127.0.0.1 --port 6013
```

新目录中 `train_joint_delta_data/tensorboard/WholeBodyTracking/20261121_085402-stage1_joint_squat_walk-locomotion/model_00031.pt` 及同名ONNX是本次32更新短模型，不是正式Stage1模型。`comparison.json`、`geometry_sampled.json`、`source_crop_comparison.json`、`delta_action_ranges.json`、`probe_summary.json` 和各原始运行目录提供可核查数据。

## 是否建议正式训练

目前建议**保留P0/P2修复和delta候选，暂不直接开始15000次长训**。极端动作偏置与初始化/时序代码问题已有实证修复，Forward的早期条件改善；但参考位置探针仍不能建立双手持续夹持，且Forward与P0侧夹参考存在已量化的姿态/几何差异。下一步应先审议如何保留原始数据并处理该抓持一致性，而非继续放大噪声/尺度、修改所有增益、放松终止或降低最终验收。

没有自动修正数据、自动追加训练或进入Stage2。所有失败和短模型保留，未把任何短模型标记为最终可用Policy。
