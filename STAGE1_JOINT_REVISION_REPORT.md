# Stage 1 蹲起与行走联合训练修订记录

日期：2026-11-21。分支：`feature/fullbody-goal-carry-autotrain`。本次修订基于本地已有P0和旧自动训练代码；没有启动正式15000次训练。提交版本可由 `git log -1` 查看，每次正式启动也会记录到 `launch.json`。

## 交付行为

新实验 `g1_29dof_carry_stage1_joint` 在同一次原始HMI PPO训练中共享Actor和Critic，全部为Track环境。半数环境训练完整抱箱蹲起，半数训练抱箱行走；蹲起内部单周期/双周期按40%/60%采样。这样短行走Clip不会因频繁Reset而丢失环境步占比。保留原HMI自适应时间采样，50%从Clip首帧开始。

Stage 1只使用原HMI Robot/Object模仿奖励，以及动作正则和真实侧向抓持约束；没有Gen随机Goal或Gen速度/高度跟踪奖励。Actor348D、Critic184D，无Reference Pose、ID、Phase输入，无固定上半身。

`train_stage1_joint.sh`默认从头调用一次PPO `learn()`，目标15000次更新，每500次存盘，不按2000次切段，不自动resume，不因资源预算或评估停滞停止，不自动进入Stage 2。真实物理失败仍正常结束当前Episode并Reset；程序错误仍报错。旧实验及其自动管理入口保留，使用新入口即可避免旧预算机制。

## 准入、数据与物理

新数据包为 `datasets/fullbody_carry_track_v2`，所有NPZ均为P0原文件逐字节复制：

| 动作 | SHA256 | 状态 |
|---|---|---|
| continuous_grasped_squat_stand | `412681d73670e24c4a32401970710513ba9e3c2dd8b3205e2bf4c4a6a4f33a90` | P0控制器物理验证通过 |
| repeated_grasped_squat_stand | `d6238a97fa785d94cdf9579f82c002f2b088c34267ba35465e0ed350932ca835` | P0控制器物理验证通过 |
| original_forward_carry | `fe03f9072560cc75096c5a0cbcd1ae781a1fe9607c23fa8781ed257ebed98550` | 运动学有效、先前控制器物理准入失败 |

按本次用户要求，HMI Track训练目标的准入与P0控制器物理成功分开。行走允许参与学习，没有被改标为physics-validated；失败证据和所有旧实验保留。数据准入与训练结束均不能代替Policy物理验收。

原始29DoF半球手G1、原始LargeBox几何与重力保持。仿真读取的质量1.1000000238kg、惯量对角0.0220000017kg·m²，机器人摩擦1.0/0.9，箱体摩擦0.6/0.6。Physics/PD 1ms，Policy20ms，Reference50FPS，decimation20，保留原电机力矩限制。无绑定、托箱辅助、箱体位姿强制写入或P0控制器替代最终Actor。

保留现有FullBody PD设定：G1基础增益乘4，踝关节增益下限Kp250/Kd12，动作比例和实际增益由Checkpoint Metadata与实验配置保存。这是PPO关节位置偏移控制，不能等同P0的1ms跟踪控制器。

## 针对旧失败的检查和修改

旧自动运行的最终报告记录停止原因是 `Job timeout/budget reached: stage1_training`，其物理验收仍未通过。移除预算只能避免提前结束，不能证明旧失败只是迭代不足。

本次用旧模型比较了环境PyTorch输入和部署ONNX输入：确定性适配器路径348D历史误差为0，动作最大误差1.67e-6；使用环境输入驱动时历史最大误差1.43e-6。两条路径仍在5步内失败，因此该实验不支持“ONNX导出或历史顺序错误造成全部失败”的解释。诊断脚本为 `scripts/carry/audit_policy_inputs.py`。

发现首个Episode与普通Episode Reset时序不同：原 `reset_all()` 在首个Actor动作前推进20ms零动作。新Stage1返回Reset后的首个观测，交给Actor执行第一步，与普通Episode Reset一致。此修改有测试和短训练验证；尚不能断言它已经解决旧物理失败。

## 实测验证

本地完整证据目录：`../artifacts/fullbody_stage1_revision/`。短训练统一使用独立输出，未覆盖正式模型。

| 检查 | 结果 |
|---|---|
| 原Carry接口/管理器/FullBody回归及新增联合训练测试 | 28 passed，0.58秒 |
| 三NPZ哈希、完整Robot/Object字段、50FPS、四元数 | 通过 |
| 三参考完整FK与HMI Loader | 全部通过，最大位置误差1.17e-7m |
| 最终Reset版本64环境4次PPO更新、保存/导出 | 通过，`joint_track_reset_smoke*` |
| 可选手动恢复 | model_00003恢复到总更新目标5，仅执行1次更新，resume_verified=true |
| 8192环境2次更新容量检查 | 正常退出，107.53秒含启动，GPU峰值8768MiB，无OOM/Traceback |
| 8192最后一次更新性能 | 10968.73环境步/秒；rollout16.32秒，PPO更新1.61秒，simulation15.41秒 |
| 8192动作覆盖 | 蹲起环境0.5，行走环境0.5，Track1.0，Gen0.0 |
| 新Actor Metadata及三Clip离线评估入口 | 通过链路检查，2种子×3Clip均执行，complete_suite=true |
| 两次更新模型的实际Policy验收 | **未通过，三Clip分别0/2；不是收敛模型** |
| 新TensorBoard入口 | HTTP200，logdir指向fullbody_stage1_joint，端口6012 |

8192仅做短容量验证，不能当作长时间稳态吞吐基准或策略性能证据。短模型失去抓持的失败完整保存在 `joint_stage1_evaluation_data/evaluation.json` 和rollout NPZ。

## 长训和验收

可直接复制的手动启动、后台持久运行、TensorBoard、可选异常恢复及训练后评估指令见 [README_STAGE1_JOINT.md](README_STAGE1_JOINT.md)。正式训练未启动。

15000次完成后再离线评估，不在训练期间并发启动Isaac评估或截断训练。完整Stage1验收必须覆盖单周期、双周期和行走全部三条Clip，每条至少10个种子、各自成功率至少80%，满足原侧向抓持/滑移/离地/跟踪门槛。仅评估部分Clip不能触发完整Stage1通过。未修改这些物理成功门槛。

本次交付的是修订后的Stage1训练和评估入口，没有新收敛Stage1 Policy、Stage2 Policy或新的物理成功声明。15000次是本轮训练目标，是否收敛由训练后的真实验收决定。
