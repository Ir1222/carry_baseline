# Full-Body Goal-Conditioned Carry

这是独立的新实验 `exp:g1-29dof-fullbody-carry`。保留旧的小箱体 Carry 实验、P0 原文件和旧 Checkpoints。**当前是否获得可用 Policy，以 run 目录内的独立物理评估为准；Smoke Test 的模型不代表任务成功。**

本地工作区 `/home/han/pyx/g1_carry_baseline_new`，仓库在 `HMI/`。P0 保存提交 `ed106a7`，开发分支 `feature/fullbody-goal-carry-autotrain`。

## 环境与准入

```bash
cd /home/han/pyx/g1_carry_baseline_new
source /home/han/miniconda3/etc/profile.d/conda.sh
conda activate "$PWD/envs/g1_hmi_carry"
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV LD_LIBRARY_PATH
export PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
cd HMI
```

已生成的独立数据包：`../artifacts/fullbody_goal_carry/reference_v1`。需要重建时指定**新目录**，不要覆盖已有 bundle：

```bash
python scripts/carry/prepare_fullbody.py --output ../artifacts/fullbody_goal_carry/reference_reproduction
python -m pytest tests/test_carry_interface.py tests/test_carry_supervisor.py tests/test_fullbody_carry.py -q
python scripts/carry/preflight_fullbody.py --output ../artifacts/fullbody_goal_carry/physics_manual_new.json
```

`fresh_format_fk_validation.json` 保存本次对三条参考重新运行 `scripts/reference_synthesis/verify.py` 中 `verify_motion()` 的结果。原脚本的 main 还检查 P0 时受保护的训练代码哈希，所以新开发不应用它声称“训练代码未改动”。源 NPZ 的 SHA256、来源和采样权重在 `manifest.json`。

蹲起骨盆高度 `0.60688007–0.72688007m`，限速 `0.11247000m/s`，完整幅度 12cm。四维 Goal 保持 `[vx,vy,yaw_rate,pelvis_height]`，Actor 为 348D，Critic 为 184D。Gen 的 vy/yaw 恒为零，vx 非负。**原 Forward Carry 的物理准入失败，目前 vx 上限为 0；这不代表已实现正向搬运。** 前进参考保留在 `quarantine/`，不会被 MotionLoader 整目录误加载。

## 物理与控制

原始 29DoF 半球手 G1、原始 LargeBox URDF/OBJ、自由刚体、重力和自碰撞。URDF 质量 0.1kg 在启动时显式设置为 1.1kg，同时将惯量按质量比例改为对角约 0.022kg·m²；初期无物理随机化。Robot 摩擦 1.0/0.9，Box 摩擦 0.6/0.6，恢复系数零。

物理步长 1ms，PD 每物理步更新，Policy 50Hz，action decimation=20，Reference 50FPS。全局 TGS 位置迭代 8–16、速度 4–8；Robot 为 16/8。增益按 P0 的基础增益×4、阻尼×2，踝最低 250/12；力矩使用原 G1 限制。实际增益、力矩、action scale 在物理 Gate 和 ONNX Actor Metadata 中。

PPO 只输出关节位置偏移；没有调用 P0 逆静力学前馈或 WBC，没有箱体绑定、虚拟支撑或运行时写入箱体/root 位姿。运行中启用 virtual gantry 会报错。

## 自动训练与监控

完成 preflight 并自动选择环境数后运行。监督器先测试4096，再在显存允许时测试8192；每项4次预热、12次测量。正式 Stage 1 从头训练，最多15000 iterations/24小时；Stage 2 必须先通过 Stage 1 的10种子物理 Gate，最多20000 iterations/24小时。每500次保存及离线评估。训练和评估串行占用GPU。停滞时每阶段最多3次有证据的修正，所有阈值和物理约束不变。

```bash
bash scripts/carry/train_fullbody_auto.sh start
bash scripts/carry/train_fullbody_auto.sh status
bash scripts/carry/train_fullbody_auto.sh resume
# 需要显式停止时才运行：
bash scripts/carry/train_fullbody_auto.sh stop
```

使用独立的 `g1-fullbody-carry.service`，无无限自动重启。服务和子进程PID、完整命令、源码快照、配置、逐次耗时、GPU采样、TensorBoard、评估和失败原因都保存在：

```text
../artifacts/fullbody_goal_carry/current/
  config.json
  training_status.json
  source.tar
  jobs/*/{command.json,console.log,worker_result.json,iterations.jsonl,result.json}
  dashboard/
  evaluations/*/{evaluation.json,trials.json,*_rollout.npz}
  best_stage1/selection.json
  best_stage2/selection.json
  style_ablation.json
  autoresearch.jsonl
```

```bash
python -m tensorboard.main --logdir ../artifacts/fullbody_goal_carry --host 127.0.0.1 --port 6011
python scripts/carry/monitor_training.py --watch
journalctl --user -u g1-fullbody-carry.service -n 50 --no-pager
```

仪表板显示迭代、Episode、各Reward、Goal误差、实际侧向接触和摩擦力、滑移速度、箱底高度、失败分类、课程、GPU显存/吞吐及Checkpoint。50ms EMA 不用于新实验接触验收；实际物理子步接触连续率单独累计。

## 手动训练入口与 Resume

以下也是真实 HMI PPO 入口。长训建议使用上面的监督器，避免手动并发多个 Isaac 进程。

```bash
# Stage 1：从头训练
export CARRY_WORKER_OUTPUT="$PWD/../artifacts/fullbody_goal_carry/manual_stage1_worker"
python scripts/carry/train_worker.py exp:g1-29dof-fullbody-carry logger:disabled \
  --training.num-envs=4096 --training.headless=True \
  --logger.base-dir=../artifacts/fullbody_goal_carry/manual_stage1 \
  --algo.config.num-mini-batches=64 --algo.config.save-interval=500 \
  --algo.config.num-learning-iterations=15000 \
  --command.setup-terms.motion-command.params.motion-config.hybrid.track-ratio=1.0

# Stage 2 / Resume：MODEL 必须是新实验通过物理评估的 Stage 1 Checkpoint
export MODEL=/absolute/path/to/validated/new/stage1/model.pt
export CARRY_WORKER_OUTPUT="$PWD/../artifacts/fullbody_goal_carry/manual_stage2_worker"
python scripts/carry/train_worker.py exp:g1-29dof-fullbody-carry logger:disabled \
  --training.num-envs=4096 --training.headless=True --training.checkpoint="$MODEL" \
  --logger.base-dir=../artifacts/fullbody_goal_carry/manual_stage2 \
  --algo.config.num-mini-batches=64 --algo.config.save-interval=500 \
  --algo.config.num-learning-iterations=20000 \
  --command.setup-terms.motion-command.params.motion-config.hybrid.track-ratio=0.5
```

`MODEL` 是用户选择Checkpoint的变量，不能指向旧掌心承托实验。Checkpoint校验包括Actor/Critic、优化器、归一化、Reference Manifest、Goal范围、课程状态和自适应采样器。`num-learning-iterations` 是本次新增更新量。

## 评估、Viewer、交互和导出

训练时自动导出纯 Actor ONNX，含归一化和历史观测。单帧116D、历史3帧，无Reference/Motion ID/Phase输入。`CarryActor.act()` 接收实际root、关节、box状态和四维Goal；静态物理资产及reset仍是仿真所需。

```bash
export POLICY=/absolute/path/to/new/experiment/model.onnx
# Track评价：每条参考从首帧开始，多个随机种子的reset关节扰动
python scripts/carry/evaluate.py --fullbody --suite stage1 --policy "$POLICY" \
  --seeds 10 --output ../artifacts/fullbody_goal_carry/manual_track_new

# 10类Goal，同一episode连续切换；执行器禁止构造MotionLoader
python scripts/carry/evaluate.py --fullbody --suite goal --policy "$POLICY" \
  --seeds 10 --seconds 24 --output ../artifacts/fullbody_goal_carry/manual_grid_new

# Isaac Viewer，显示Goal及实际vx/h；stdin输入四维命令
python scripts/carry/evaluate.py --fullbody --suite goal --only standing \
  --policy "$POLICY" --seeds 1 --seconds 120 --view --interactive \
  --output ../artifacts/fullbody_goal_carry/interactive_new

# 无Isaac/无Reference文件的CPU重导出及32个输入的PyTorch/ONNX一致性检查
python scripts/carry/export_fullbody.py --checkpoint "$MODEL" \
  --output ../artifacts/fullbody_goal_carry/export_new/policy.onnx
```

交互示例：`0 0 0 0.60688` 蹲下，`0 0 0 0.72688` 起立；命令切换不reset。前进参考未准入时正向命令会被明确拒绝。`--video` 启用原框架录制器；需要可用的渲染环境。所有输出目录必须使用新名称。

## Reward 与验收

Track 复用 HMI 全身/物体模仿奖励。Gen 包含速度3、yaw1、高度3、侧向摩擦夹持3、相对箱体稳定1、箱体相对姿态1、低手箱滑移1，以及可关闭的Style0.5；非手掌托箱惩罚−2，保留动作平滑及实际关节限位奖励。具体权重以每次保存的 `holosoma_config.yaml` 为准。

Style 用高度、升降趋势、正向速度和匹配时间连续性选Reference姿态，匹配29DoF与手箱协同。越出Reference分布时降低权重。它只影响训练Reward，部署不加载Reference。Stage 1通过后自动执行同初始Checkpoint、同seed、同128次更新预算的开/关对照；未完成对照时不得宣称Style改善了动作。

真实失败包括箱底距地<3cm、跌倒、双手接触中断超过20ms（初始100ms接触建立单独记录）、非手掌支撑及非有限状态。验收还检查向上摩擦支撑/箱重≥0.8、法向竖直分量≤0.35、接触点高于箱底≥5cm、手箱漂移≤2.5cm；不能以掌心承托替代侧向夹持。合法低位不因固定箱体中心高度被误判。失败优先于Timeout。评估读取自动reset之前的物理状态，保留所有失败种子。

启动脚本同时启动有限等待的报告监督服务。训练正常结束或有证据阻塞后，会重新生成包含实际指标的 `FULLBODY_GOAL_CARRY_FINAL_REPORT.md` 并自动commit；不会自动push。报告在 RUNNING 状态下是进度报告。

最终文件和能力以 `FULLBODY_GOAL_CARRY_FINAL_REPORT.md` 及run内评估为准。未通过的最佳模型只保存在 `best_stage*/`，不标记为最终可用Policy。Forward准入失败的完整数据在 `forward_probe_001_data` 和 `forward_hold_diagnosis_003_data`；后者9组均未通过，不能通过增加夹紧力或只看接触率将其准入。
