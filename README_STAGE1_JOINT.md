# Stage 1：一个 Policy 联合跟踪抱箱蹲起和抱箱行走

2026-11-21修复了95%软限位Reset裁剪和一帧参考滞后，Stage1候选动作改为reference-free小增量位置目标；详见 [STAGE1_REPAIR_VALIDATION.md](STAGE1_REPAIR_VALIDATION.md)。Forward短训虽改善，但原始行走参考与侧向抓持姿态的几何差异尚未解决，**当前不建议直接启动下面的15000次长训**。此前审查保留在 [STAGE1_PRETRAIN_AUDIT.md](STAGE1_PRETRAIN_AUDIT.md)。

新入口：`exp:g1-29dof-carry-stage1-joint`。单次调用现有 HMI PPO，默认从头连续更新 **15000 次**，每500次保存 Checkpoint/ONNX。没有资源时间预算、评估停滞早停、2000次切段、自动resume、自动改奖励或自动进入Stage 2。单个Episode的真实失败仍会终止并正常Reset，PPO训练继续。

这次只修改、验证并交付训练入口，正式15000次训练由你手动开始。短训练验证不代表Policy已经收敛。

## 直接启动

本机使用现有环境，不必另开conda环境：

```bash
cd /home/han/pyx/g1_carry_baseline_new/HMI
bash scripts/carry/train_stage1_joint.sh --num-envs 8192 --iterations 15000
```

长时间运行建议手动在后台启动，关闭当前终端后继续运行：

```bash
cd /home/han/pyx/g1_carry_baseline_new/HMI
mkdir -p ../artifacts/fullbody_stage1_joint
stage1_log="../artifacts/fullbody_stage1_joint/console_$(date +%Y%m%d_%H%M%S).log"
nohup bash scripts/carry/train_stage1_joint.sh --num-envs 8192 --iterations 15000 \
  > "$stage1_log" 2>&1 &
echo "训练PID=$!，控制台日志=$stage1_log"
```

启动脚本直接使用 `../envs/g1_hmi_carry/bin/python`，清理冲突的Python/动态库环境变量。一个协作文件锁阻止重复启动Carry训练。没有监督器定时停止；操作系统、CUDA异常、非有限数等真实程序错误仍会报错退出，不会伪造训练完成。

## TensorBoard

另开终端执行：

```bash
cd /home/han/pyx/g1_carry_baseline_new/HMI
bash scripts/carry/tensorboard_stage1_joint.sh
```

浏览器打开 **http://127.0.0.1:6012**。该端口/目录用于新联合训练；旧实验的6011保持独立。

重点查看：原始HMI六项Robot模仿Reward、两项Object模仿Reward、夹持/滑移、Episode长度、各类Termination，以及 `track/family_fraction_squat_stand`、`track/family_fraction_forward_carry`、`track/env_fraction`、`track/gen_env_fraction`。两类动作均为Track，Gen比例必须为0。

## 数据、采样与准入

随代码提交的数据包：`datasets/fullbody_carry_track_v2/`，约1.6MB。三个NPZ均为原文件的逐字节副本，没有覆盖P0、旧参考或旧Checkpoint：

| Clip | 时长 | 物理验证状态 |
|---|---:|---|
| continuous_grasped_squat_stand | 7秒 | P0控制器验证通过 |
| repeated_grasped_squat_stand | 13秒 | P0控制器验证通过 |
| original_forward_carry | 2.18秒 | 运动学有效；先前控制器准入失败，**没有标记为物理验证通过** |

全部环境为Track。固定一半训练环境采样蹲起、一半采样行走，共享同一个Actor/Critic/PPO；蹲起内部两条Clip按40%/60%抽样。这样不会因为行走Clip较短，使行走在实际环境步数中的占比下降。保留各Clip内部的HMI自适应时间采样；50%的Reset从该Clip首帧开始，兼顾完整执行和随机帧训练。

本次按用户修订要求，把**HMI Track目标准入**与**控制器物理认证**分开：格式、全身FK、坐标/速度、原始资产一致的数据允许作为Track训练目标，不要求P0静态/轨迹控制器先成功执行完整行走。前进参考的物理失败证据保留。准入只表示可以参与学习，不表示参考或Policy已物理成功。完整Policy仍需按真实自由箱体验收。

```bash
# 校验已提交的数据，不改动源文件
../envs/g1_hmi_carry/bin/python scripts/carry/prepare_stage1_joint.py --verify-only

# 单元与回归检查
../envs/g1_hmi_carry/bin/python -m pytest \
  tests/test_carry_interface.py tests/test_carry_supervisor.py \
  tests/test_fullbody_carry.py tests/test_stage1_joint.py -q

# 只打印正式运行配置，不启动仿真或训练
bash scripts/carry/train_stage1_joint.sh --dry-run
```

## Stage 1训练目标与物理条件

复用原始HMI的全身Robot+Object Tracking Reward及Shared PPO。保留动作平滑、实际关节限位、侧向摩擦夹持、低手箱滑移和非手掌支撑检查。**不使用Gen随机Goal、速度/高度Goal Tracking Reward或Gen Style Reward**。四维观测命令仅从当前参考帧导出；Actor仍为348D物理历史，不输入Reference Pose、Motion ID或Phase，Critic仍为184D。

原始29DoF半球手G1与原始LargeBox，实际名义质量1.1kg、惯量对角约0.022kg·m²。固定Robot摩擦1.0/0.9、Box摩擦0.6/0.6；保留重力、自碰撞、原始电机力矩限制。物理/PD为1ms，Policy为20ms，Reference为50FPS，decimation=20。没有绑定箱体、虚拟支撑、前馈WBC或逐步写物体位姿。

与旧入口相比，还修正了初始Reset时序：旧 `reset_all()` 在Actor接管前先执行20ms零动作，新Stage1直接从初始化物理状态产生首个观测。合法硬限位内的参考关节角不再被95%软限位裁剪；post-action奖励/终止对齐k+1帧。默认 `joint_delta_v1` 目标是本次Policy调用时实测q加归一化动作乘原effort/Kp比例，在20个PD子步保持目标。Actor中的q_default仍用于观测居中。旧固定默认姿态动作可显式设置 `HMI_CARRY_ACTION_MODE=fixed`，两种模式不可混用Checkpoint。Checkpoint导出使用零张量示例输入，不Reset训练环境。

## 输出和可选恢复

每次启动创建独立目录：

```text
../artifacts/fullbody_stage1_joint/latest/
  launch.json                  # PID、命令、迭代目标、Git版本
  dataset_manifest.json
  source.tar
  worker/iterations.jsonl
  worker/worker_result.json
  tensorboard/WholeBodyTracking/<run>/
    holosoma_config.yaml
    train.log
    events.out.tfevents.*
    model_00000.pt ... model_14999.pt
    model_*.onnx / .actor.json / .ready.json / .export.json
```

迭代索引从0开始，`model_14999.pt`对应完成15000次更新。每500次保存只做文件写入/导出，不结束或重启训练进程。`worker_result.json` 中 `passed` 表示训练链路执行检查，不是物理验收结果。

仅当你主动中断或机器异常后需要恢复时，可手动指定**这版联合训练**的Checkpoint；不会自动调用：

```bash
bash scripts/carry/train_stage1_joint.sh --iterations 15000 \
  --resume /absolute/path/to/new_joint_stage1/model_05000.pt
```

15000是总更新目标，恢复会扣除已完成更新。旧的只训练蹲起的Checkpoint因Reference Manifest不同会被拒绝；d2281cf及更早的联合训练Checkpoint因Reset/时序协议不同也不能直接恢复本版训练。新训练默认从头开始。

## 训练后评估

`POLICY`指向这次联合训练导出的ONNX，程序会由Actor Metadata自动识别这版三Clip数据：

```bash
source /home/han/miniconda3/etc/profile.d/conda.sh
conda activate /home/han/pyx/g1_carry_baseline_new/envs/g1_hmi_carry
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV LD_LIBRARY_PATH
export PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
cd /home/han/pyx/g1_carry_baseline_new/HMI
POLICY=/absolute/path/to/new_joint_stage1/model_14999.onnx
python scripts/carry/evaluate.py --fullbody --suite stage1 --policy "$POLICY" \
  --seeds 10 --output "../artifacts/fullbody_stage1_joint/eval_$(date +%Y%m%d_%H%M%S)"
```

查看GUI时可用 `--seeds 1 --view --video`。完整Stage1验收必须覆盖三条Clip，其中包含行走；单独用 `--only clip_0` 查看某条动作不能触发完整Stage1通过。各Clip至少10个种子、各自成功率至少80%，同时满足原侧向摩擦抓持及Robot/Object Tracking门槛。评估不在训练过程中启动第二个Isaac进程，也不会提前截断本次15000次训练。

旧的 `train_fullbody_auto.sh` 是先前有24小时预算/停滞修正的历史入口，本次请使用本文件的 `train_stage1_joint.sh`。本入口不会自动开始Stage2。
