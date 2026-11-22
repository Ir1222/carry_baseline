# Bool 日志修复与 GPU 验证（2026-11-22）

当前状态：修复和必要 GPU 测试通过；依用户最新要求，**未启动正式训练，也未启动新 TensorBoard**。旧训练保持停止。

## 修复

原始 `stable_support_sample` 是 Bool，FullBodyCommand 将它原样转发给原 PPO 的 TensorAverageMeter，首次 update 后日志调用 mean() 报错。新增测试先在正式 HMI 环境复现同一异常，再修正指标出口：

- 每环境标量日志转为float；共享物理缓存的Bool判断保持原类型。
- 原始 `[env,link,xyz]` 力向量不进入标量日志缓存；UnifiedCarryEnv中已有每link具名力大小和xyz诊断保留。
- 不改变PPO数学、奖励、物理状态、actor357D／critic207D、4 minibatches或任何数据资产。

真实SIGTERM测试另发现：Isaac Kit关闭可以将Python SystemExit130变成进程退出0，旧wrapper因此进入完成验证并误标stopped_or_failed；完成验证拒绝缺失的最终checkpoint，未运行evaluation。新增小型 `run_status.py` 守卫，优先检查完整保存后原子写出的interrupted状态，再决定退出码。已用真实中断文件验证进程码0会转为130，并补齐5种退出状态回归。没有声称修改了上游Isaac关闭行为。

## 实测结果

正式解释器：`../envs/g1_hmi_carry/bin/python`。55项回归通过，含真实生产命令指标→原TensorAverageMeterDict聚合链。Python／shell语法及Git空白检查通过。

GPU任务全部串行：

| 项目 | 结果 |
|---|---|
| 环境／rollout／minibatches／epochs | 8192／24／4／5 |
| 初始化 | checkpoint=None，全新初始化 |
| 短测完成更新 | 3，actor与critic各60次optimizer step |
| logical minibatch | 49152条样本 |
| 初始std／LR／KL | 0.3可学习；actor/critic1e-4；adaptive/0.01 |
| 物理／策略步长 | 0.001／0.02s |
| 保存设置 | latest100，归档2000；短测最终同时保存latest和编号权重 |
| GPU整卡采样峰值 | 9946MiB，无OOM，不降级minibatches |
| TensorBoard与checkpoint | 有限值、完整性、checksum、W&B最终文件检查通过 |
| ONNX/PyTorch max absolute difference | 7.152557373046875e-7 |
| 恢复与中断 | 从3次完整更新恢复，正常完成至6次；actor/critic各累计120次step |
| 中断latest | 内部iter5、completed_updates6；即使没有邻接ONNX也能发现并验证 |
| 中断后evaluation | 没有启动；新守卫对真实状态返回130 |
| 退出后 | learner/controller退出，锁释放；GPU只剩无关远程桌面进程 |

容量checkpoint SHA256：
`aef184b6aae258751b6d30093b9d16036bf7dda2685506b1234642b47fc40af0`。
中断checkpoint SHA256：
`aec0a916e2bf76ce48808b824d879737789a913387f6c11eafad922b5f849d3f`。

未发现致命PhysX运行异常；原有辅助足部marker视觉引用和TGS velocity-iteration警告保留。测试是数值与运行链路验证，不是policy通过物理验收。

## 旧 policy 物理诊断

用户运行的五组串行诊断已完成，证据 `../artifacts/unified_hoi_hmi_stage1/diagnosis_20261122_190555/`，每组2个seed：

- frame0全序列在154／155帧因tracking failure结束。旧fall诊断152帧触发，继续几帧没有构成恢复或完整成功证明。
- 95帧边界片段两次到达102帧；205帧边界两次到达212帧，没有因固定mode边界直接硬终止。后者仍违反接触连续性／滑移等最终验收，torso接触峰值约0.818N，不能标为有效仅双手搬箱成功。
- putdown-support片段两次到304帧因tracking failure结束。
- release片段两次到324帧并达到稳定放置释放。这是该短入口的结果，不代表frame0完整取放能力。
- 本组没有复现旧loss_of_grasp触发，因此不能声称已经实验证明该旧规则造成了历史平台期。接触闪断与孤立地面坏样本的反例仍由生产状态机逻辑测试覆盖。

## 原始证据与使用

所有大文件在：
`../artifacts/unified_hoi_hmi_stage1/logging_fix_20261122111226/`

- `capacity.console.log`、`gpu_capacity.csv`、`capacity_resolved_summary.json`
- `capacity_validation.json`、`capacity_counts_memory.json`
- `recovery_interruption_validation.json`、`old_policy_diagnosis_summary.json`
- `capacity/logs/WholeBodyTracking/20261122_111235-unified_hoi_stage1-locomotion/`
- `resume_interrupt/training/logs/WholeBodyTracking/20261122_111548-unified_hoi_stage1-locomotion/`

用户先前失败的 `capacity_20261122_190555/` 原位保留，没有checkpoint；failure_reason.json说明替代测试位置。恢复测试权重禁止作为正式新实验初始化。

正式训练命令仍是原HMI入口的持久shell包装：`train_unified_hmi_then_evaluate.sh NEW_RUN_DIR`，不传checkpoint，从零连续15000更新，完成后串行10seed评估，无Stage2。TensorBoard对新run单独使用6016端口。用户最新要求自行启动，因此当前没有正式service/PID或新run。先前文档的沙箱阻塞及49项CPU结果保留为历史记录；本报告取代其当前未验证状态。
