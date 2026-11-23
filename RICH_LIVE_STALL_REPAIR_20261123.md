# Rich Live 停滞修复与原版 HMI 对照（2026-11-23）

## 结论与责任范围

这次是修改后的训练集成回归。不能用“Rich 来自上游”或“任务在后台运行”回避新增日志负载的影响。

用户提供的只读 py-spy 栈确认：主线程 active+gil，停在 Console.render → Segment.split_and_crop_lines → LiveRender → Live.refresh → Live.stop → LoggingHelper.post_epoch_logging。W&B异步线程、TensorBoard写线程处于等待。iteration1301的TensorBoard数据已写出，控制台仍停在1300，完成状态文件为1301。

原版 HMI 与实际运行的35b483d，其train_agent.py、PPO、LoggingHelper代码逐字相同；当前新增了大量family/phase/link展开统计：实测2366个scalar，1440个为nonhand link展开；控制台每轮3406行。复用原有动态终端渲染处理这份负载，是需要修复的集成路径。调用栈确认卡点，但没有将一次采样夸大为已证明Rich库内部某个字符输入必然无限循环。

systemd服务没有退出，也没有训练时长限制触发。Restart=no只表示不自动重启；TimeoutStopSec=180只约束停止过程，并不是180秒运行期限。后台服务本身不等于训练会被中断。终端与重定向输出都应走安全日志路径。

## 代码修复

1. 共享PPO LoggingHelper移除Rich Live/Panel与refresh线程入口，改成一行有界纯文本进度。完整TensorBoard/W&B scalar、episode聚合不删减。即使是TTY也不恢复动态Rich。
2. Unified完整optimizer update结束后，先记录completed_updates、执行到点原子checkpoint保存，再执行外部日志。没有改变PPO loss、GAE、minibatch顺序、KL或optimizer数学。
3. 原生eval_agent使用可选load_for_evaluation。Unified推理仍校验v2 schema、actor/critic形状、数据manifest、控制/动作参数、PD/scales和reset协议；允许评估采样/展示差异，不加载optimizer或sampler。该实例禁止进入learn。训练load仍要求完整任务合同一致。
4. 修复play中Isaac Kit路径遮蔽websockets.asyncio的问题：Viser启用时在SimulationApp之前预加载已安装的兼容包。没有升级训练环境依赖，没有全局重写sys.path或删除模块。
5. 增加简单原生播放入口scripts/carry/play_unified_hoi.sh，复用eval_agent和carry GPU锁；训练占用GPU时明确拒绝并发play，不自动停训练，不修改资产/动作/终止。

## 原版与停滞时实际Stage1的区别

上游固定c353731999b3578c41ad5a00f896415b45e6a9f5；实际配置读取formal_repair_20261122_192144的holosoma_config.yaml，实际源码35b483d。

| 项目 | 原版HMI Object Stage1 | 当前Stage1实际 |
|---|---|---|
| PPO loss/GAE/optimizer算法 | 原HMI | 同一原实现 |
| rollout/minibatches/epochs | 24/4/5 | 24/4/5，当前不是128 minibatches |
| 初始actor/critic LR，schedule/KL | 1e-4，adaptive/0.01 | 相同 |
| 初始可学习std | 1.0 | 0.3；续训保留已学std |
| Actor任务条件 | 物体终点goal | 四维command＋额外3类任务意图，357D |
| Critic | 原privileged tracking观测 | 207D，含新增支撑/接触状态 |
| PD目标 | q_default+scale*a | q_at_policy_step+scale*a，20ms保持 |
| 物理dt/decimation/policy dt | 5ms/4/20ms | 1ms/20/20ms；PD/gains/scales亦有此前差异 |
| PhysX solver robot迭代 | 8/4 | 16/8 |
| 八项robot/object tracking奖励 | 原函数和参数 | 保留；另外有grasp、slip、nonhand、pickup、putdown |
| 硬终止 | 原tracking/proximity等 | 增加实测握持/支撑失败；root/body位置failure改用Z，object仍3D |
| Reset/参考时序 | 原软限位裁剪与时序、初始化扰动 | 硬限位有效精确reset、零扰动、首观测和post-action对齐 |
| Reference | movebox原始＋镜像两条 | 六条：完整原/镜像、加载原/镜像、单/重复蹲起 |
| Reset采样 | 原自适应时间bin，frame0=0.05 | family30/35/35＋自适应时间bin，frame0=0.25 |
| Episode设置 | 10s、随机初始episode age | 30s、初始age不随机 |
| 物理随机化 | 原任务随机化 | 当前固定1.1kg及既定材料/惯量；原G1/LargeBox资产保留 |
| Checkpoint | 归档3000、latest100且伴随导出 | 归档2000、latest100完整状态，低频独立导出 |
| 控制台诊断 | 原全局指标 | 新增大量family/phase/link统计，触发本次渲染集成问题 |

因此，沿用HMI PPO和八项tracking不意味着训练条件与原版等价。动作、观测、PD、时序、数据、采样和物理判定均有明确差异；本轮只修运行/播放集成，不据此继续做控制或网络消融，也不声称已解释所有学习平台与回退。

机器对照：/home/han/pyx/g1_carry_baseline_new/artifacts/unified_hoi_hmi_stage1/rich_live_repair_20261123080108/upstream_vs_actual_config.json。

## 保全与停训

旧learner1821536/controller1821298及所属hmi-stage1-20261122_192144.service已重新核实。首先正常停止，Rich循环无法走到安全保存点，随后仅终止该unit的剩余进程；未注入调试代码。GPU与/tmp/g1-carry-gpu0.lock已释放。

保全checkpoint内部iter1299、completed_updates1300，SHA256：
3ce8f01b9805e4c8619734459c32cfc5ec203ad538979f6a664814c43c21a5a1。

不可变副本：/home/han/pyx/g1_carry_baseline_new/artifacts/unified_hoi_hmi_stage1/rich_live_repair_20261123080108/retained/model_01299.pt。
原始checkpoint、console、events、W&B原位保留，停止原因写入旧run/stop_reason.json。1300之后仅存在于内存或日志的更新不计入恢复进度；没有声称TERM保存了Rich循环中的权重。

## 验证证据

- CPU相关回归覆盖大指标集、TTY/文件两种输出、完整TensorBoard/W&B保留、保存先于日志、10000步原生policy循环、严格续训与仅推理加载隔离、Viser预加载、play GPU互斥。
- 真实GPU恢复：8192环境、24 rollout、4 minibatches、5epochs，1300→1303三次完整更新；每轮纯文本输出，保存/数值/导出验证通过，ONNX/PyTorch最大差4.291534423828125e-6。
- 原生eval_agent+Viser：2环境连续200步，HTTP200；机器人/箱体/参考可视化已加载，actor normalizer冻结，动态Rich日志入口不存在。测试是播放链路验证，不是policy物理成功验收。
- 早期play尝试的加载合同和websocket失败均保留日志；没有把进程退出0或后台策略循环当作网页播放成功。

证据目录：/home/han/pyx/g1_carry_baseline_new/artifacts/unified_hoi_hmi_stage1/rich_live_repair_20261123080108/。关键文件resume_smoke_validation.json、native_play_verified.json、native_play_http.json、logging_payload_counts.json、stall_and_retention.json。

## 恢复与播放

首次运行故障修复时从保全的1300权重继续，配置剩余13700更新达到总15000；短测1303分支不用作正式初始化。输出：/home/han/pyx/g1_carry_baseline_new/artifacts/unified_hoi_hmi_stage1/formal_recovery_1300_richfix_20261123080108；unit：hmi-stage1-richfix-20261123080108.service。实际PID、resolved config与完成更新数由恢复后的runtime_verified.json记录。旧曲线单独保留，不拼接未保全更新。

后续学习退化诊断在2010、2014、2021完整update后安全保存并串行测量，当前正式进程从2021状态恢复。最新service、run目录、std变化、配对结果与尚未解决的均值策略回退见[最新学习退化报告](STAGE1_LEARNING_REGRESSION_20261123.md)。上述1300恢复点与unit保留为历史证据。

完成训练或安全停止训练后，原生play：
```bash
cd /home/han/pyx/g1_carry_baseline_new/HMI
bash scripts/carry/play_unified_hoi.sh /absolute/path/to/verified/model.pt
```

默认Viser http://127.0.0.1:8012；可以追加--training.max-eval-steps=1000做有界播放。不要使用ONNX路径作为本入口checkpoint；ONNX独立评估入口继续保留。普通play和终端关闭不再使用Rich动态渲染；这不承诺排除OOM、驱动或其他无关故障。
