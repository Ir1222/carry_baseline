# Stage1 support repair — 2026-11-22

> 后续更新：Bool日志错误已修复，真实GPU容量、保存／导出、恢复与中断验证完成。见[最新验证记录](STAGE1_LOGGING_GPU_VALIDATION_20261122.md)。用户要求自行启动正式训练，当前未启动；下文早期沙箱阻塞状态保留为历史记录。

状态：旧任务已停止；代码和 CPU 验证已完成；PhysX 诊断、8192/4 容量验证和新正式训练尚未执行。不能据此宣称新训练已启动或 policy 可用。

基准：`60c91c1d8371037bc71fa002f5541e9001554fce`，分支 `feature/unified-hoi-stage1`。开始时 Git worktree clean，未 reset。上游 `c353731999b3578c41ad5a00f896415b45e6a9f5` 的共享 PPO、WBT tracking reward/termination 文件与当前逐文件 Git diff 相同。本轮仅 Unified 专用编排改变保存/停止；rollout、GAE、loss、KL 和 optimizer 数学仍调用原 PPO。

## 旧任务停训证据

- 从 /proc 核实 learner8170、controller8060，PPID8170→8060→user systemd3281，PGID/SID8060；两者 cwd 均为当前 HMI。
- unit `hmi-unified-stage1-resume02000.service`；读取 transient unit 的 `Restart=no`。定向对已确认 PGID8060 发 SIGTERM，随后 learner/controller/W&B8353/8370/monitor 均退出，transient unit 消失。未发现所属 timer；wrapper 未进入评估。
- 原始 run `../artifacts/unified_hoi_hmi_stage1/formal_8192_15000_003_resume02000_20261122/` 保持原位。console、events、W&B、resolved YAML、source archive 未移动。
- 已重新用 torch CPU 加载并校验最近完整 checkpoint：
  `../artifacts/unified_hoi_hmi_stage1/formal_8192_15000_002_save2000/training/logs/WholeBodyTracking/20261121_110128-unified_hoi_stage1-locomotion/model_02000.pt`。
  内部 iter2000，已完成2001次更新，7406198 bytes；
  SHA256 `f8a5447bb85dbca02e0fc8623dcd14c5d7e888c7d6c13b669b8b0a07323b9451`。
- 停止前最后日志 iteration2891。后续2001–2891共891次完整更新未保存，2892可能处于半次 update。源码无安全保存接口，因此没有声称 SIGTERM 保存了内存权重。
- 锁 /tmp/g1-carry-gpu0.lock 已实际非阻塞独占获取并释放。剩余 NVML compute PID3688是无关 gnome-remote-desktop-daemon，保留。旧训练没有继续占用 GPU。
- 原因记录在旧 run 的 `stop_reason.json`：**用户主动中断旧配置，进行Stage1修复**；原 status 为 stopped_or_failed，未写训练成功。

## 修改与物理语义

| 文件 | 修改原因 |
|---|---|
| fullbody_simulator.py | 手部法向/摩擦、双手占空比、地面支持和非手各 link 法向向量都聚合完整20个1ms子步；连续失接触每子步更新，双手恢复立即清零 |
| support.py / unified.py | 实测支撑责任、支撑转移、稳定地面支持和释放；稳定确认0.20s、丢失迟滞0.10s；真正离地>8cm、速度>0.8m/s或角速度>3rad/s撤销地面支持；reset宽限0.10s；失握容忍可配置0.10s |
| fullbody_termination.py / unified.py | 分开记录root_too_low、upside_down、deep_lean_without_foot_support。新增绝对低姿态门仅诊断；保留倒置、非有限、2cm严重穿透、0.9m分离，另保留明显失控速度保护。原tracking failure没有删除 |
| fullbody_rewards.py / unified.py | 新 pickup 接近/侧接触/预紧在地面上和向上摩擦为0时仍有效；承重后继续原摩擦抓握/滑移塑形；非手接触保持软惩罚 |
| unified.py / unified_presets.py | full sequence恢复原困难bin采样，限制eligible时用拒绝采样，不再按phase重写；uniform fallback也限制eligible；reset_all不清掉恢复的EMA及pending更新 |
| unified.py / fullbody_ppo.py / checkpoints.py / validators | actor357D不变；critic119+68+20=207D，实际观测项推导；Unified v2契约，旧v1/187D拒绝续训；旧ONNX允许诊断 |
| unified_ppo.py / checkpoints.py | 完整update后latest100、归档2000；latest不承担ONNX导出；原子写/checksum/完整性检查；latest和归档按验证后的内部进度排序；记录optimizer计数、RNG、完整任务契约 |
| train_unified_hmi_stage1.sh / train_unified_hoi.py / train_stage1_joint.py / presets | 默认4 minibatches；移除num_envs//64和latest=0覆盖；8192×24/4=49152 samples/minibatch，5epochs意味着actor/critic各20次step/update |
| train_unified_hmi_then_evaluate.sh | 中断130/143不会进入评估；源码归档包含patch和worktree快照；单次连续15000更新，不分段，不进入Stage2 |
| evaluate_unified_hoi.py / diagnose_support_repair.py | 使用新支持语义；旧判定只记录，保存每link向量和索引、旧/新触发与reference帧；旧checkpoint只诊断 |

承重责任不读取mode；95/205帧切换不会单独宣布夹持、离地或释放完成。reference正常推进。地面正在接管重量时暂停手部失握计时；确认稳定后用迟滞抵抗孤立坏样本，真正离开支持则重新要求手部承重。空中RSI不依赖acquired=True才能检测失握。

非手 `nonhand_contact` 是接触诊断；`nonhand_upward_load_proxy` 是箱体侧传感器向上法向载荷超过半箱重的代理，不能当作已经测全所有摩擦承重的证明。训练不再因瞬时0.5N非手接触立即截断。最终仅双手有效搬箱的验收门槛原样保留。足部5N诊断仍取末子步，并明确与手/地完整周期平均口径不同；它不再影响本轮姿态硬终止。

每控制周期状态只更新一次；奖励/终止/日志/critic读取同一份缓存，重复指标调用不会推进计时。reset清空对应环境的状态和接触缓存。恢复保存完整PPO、normalizer、可学习std、sampler和RNG；PhysX场景重新reset，不声称逐bit延续旧接触求解器状态。

## 奖励公式与量级

八项原robot/object tracking reward函数、权重、sigma未改。HOI实际项仍为 grasp2、hand_slip0.5、nonhand_contact−2、pickup1、putdown1，没有新增更多顶层项。

令 n=min(N_left,N_right)，N=max(N_left,N_right)，v为法向竖直比例，
S=exp(−v²/0.35²)，E=exp(−max(N−45,0)²/30²)，
A=mean(exp(−distance_to_box_AABB²/0.10²))：

- pickup = I_pickup × [0.3A + 0.3 clamp(n/5,0,1) S E + 0.4 clamp(n/20,0,1) S E]。
  不乘离地gate或向上摩擦；raw范围0–1，weight1，20ms步贡献0–0.02。
- grasp沿用 clamp(n/20,0,1) × 有效侧接触 × clamp(向上摩擦/箱重,0,1) × E × 离地gate；weight2，步贡献0–0.04。putdown确认地面支持后屏蔽。
- hand_slip沿用exp(−slip_speed²/0.1²)×离地gate及承重阶段意图；weight0.5，步贡献0–0.01。
- nonhand_contact=I_非手力>0.5N，weight−2，步惩罚0或−0.04。
- putdown=I_putdown × (稳定支持 + 稳定释放成功)，weight1，步贡献0–0.04。

这些是公式边界，尚非真实训练中的奖励分布。CPU测试实际调用pickup_reward，验证地面上且摩擦为0时接近/20N预紧均有奖励，200N过力奖励下降。没有把这一逻辑例子当作真实物理抓持证据。

## 新旧配置

旧实际YAML vs新preset目标：minibatches128→4、latest0→100、critic187→207、自适应full sequence恢复；失握规则/支撑/奖励按上文。其余8192、15000、24、5epochs、std0.3可学习、初始LR1e-4、adaptive/KL0.01、Track1.0、physics1ms/policy20ms、save2000、原PD/scales/joint_delta均保持。新run checkpoint必须为None。

actor仍是**四维command＋额外任务意图**，不是纯四维完整取放控制器。原六NPZ、manifest、原G1、1.1kg自由LargeBox不变。历史full_training_ready=False保留历史含义，不是开训门禁；随机policy物理成功率不是门槛。

机器记录：`../artifacts/unified_hoi_hmi_stage1/repair_20261122/target_preset_config.json`、
`config_diff_pending_runtime.json`。它们明确是目标preset，不冒充新进程实际holosoma_config.yaml。

## 验证与剩余工作

已完成49项CPU回归、Python语法、shell语法和git diff --check。CPU使用可执行的mjlab CPython3.11.15/PyTorch2.10，附加本地HMI依赖路径，未启动Isaac。
新状态机、接触gap函数、真实UnifiedFailure、困难bin sampler和保存选择均直接调用生产代码；安全中断测试在actor optimizer后发送SIGTERM，确认critic仍完成、随后保存并以130退出。

**未完成**：旧checkpoint逐帧PhysX诊断、8192/4真实rollout/backprop/optimizer容量、真实保存/恢复/ONNX parity、新正式训练、TensorBoard新实验。这不是随机policy表现阻塞。宿主沙箱报错 `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`，HMI Python与systemctl无法运行；提权请求被会话策略 `sandbox_approval=false` 拒绝。当前工具不能调整会话权限。49项CPU通过不替代这些必要运行验证。

## 可复用命令（需先恢复本任务执行环境）

在HMI根目录，先串行旧policy诊断：
```bash
../envs/g1_hmi_carry/bin/python scripts/carry/diagnose_support_repair.py \
  --policy ../artifacts/unified_hoi_hmi_stage1/formal_8192_15000_002_save2000/training/logs/WholeBodyTracking/20261121_110128-unified_hoi_stage1-locomotion/model_02000.onnx \
  --output ../artifacts/unified_hoi_hmi_stage1/repair_20261122/old_policy_physics
bash scripts/carry/train_unified_hmi_stage1.sh \
  ../artifacts/unified_hoi_hmi_stage1/repair_20261122/capacity8192_4 3
../envs/g1_hmi_carry/bin/python scripts/carry/validate_unified_hmi_run.py \
  --run ../artifacts/unified_hoi_hmi_stage1/repair_20261122/capacity8192_4 \
  --updates 3 --output ../artifacts/unified_hoi_hmi_stage1/repair_20261122/capacity.json
```

技术验证通过后，从头连续训练并在自然完成后串行10seed评估：
```bash
systemd-run --user --unit=hmi-stage1-repair-v2 \
  --property=WorkingDirectory=/home/han/pyx/g1_carry_baseline_new/HMI \
  --property=Restart=no --property=TimeoutStopSec=180 \
  /bin/bash /home/han/pyx/g1_carry_baseline_new/HMI/scripts/carry/train_unified_hmi_then_evaluate.sh \
  /home/han/pyx/g1_carry_baseline_new/artifacts/unified_hoi_hmi_stage1/formal_repair_v2_8192_15000_20261122
systemd-run --user --unit=hmi-stage1-repair-v2-tensorboard \
  /home/han/pyx/g1_carry_baseline_new/envs/g1_hmi_carry/bin/python -m tensorboard.main \
  --logdir /home/han/pyx/g1_carry_baseline_new/artifacts/unified_hoi_hmi_stage1/formal_repair_v2_8192_15000_20261122/training \
  --host 127.0.0.1 --port 6016 --load_fast=false
```

计划TensorBoard http://127.0.0.1:6016 尚未启动；旧6015服务仍保留对照。正式run目录尚未创建。持久systemd服务不依赖对话框存活，配置Restart=no，无reward平台或随机policy失败自动停训。

显式恢复（只接受新v2 checkpoint，不将旧2000或容量权重作为正式初始化）：
```bash
../envs/g1_hmi_carry/bin/python -c 'from holosoma.carry.checkpoints import newest_valid; print(newest_valid("/absolute/NEW_V2_RUN")[0])'
bash scripts/carry/train_unified_hmi_then_evaluate.sh /absolute/NEW_RECOVERY_RUN /absolute/VERIFIED_V2_CHECKPOINT.pt
```

独立评估（训练结束后，至少10seed）：
```bash
../envs/g1_hmi_carry/bin/python scripts/carry/evaluate_unified_hoi.py \
  --policy /absolute/model_14999.onnx --seeds 10 --output /absolute/NEW_EVALUATION
```

README和修复提交只含源码/文档/测试。大checkpoint、完整日志和源快照保留原artifacts，不进入Git。
