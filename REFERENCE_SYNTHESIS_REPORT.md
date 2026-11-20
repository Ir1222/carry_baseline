# P0 Whole-Body Continuous Side-Grasp Carry–Squat–Stand Reference

日期：2026-11-20。工作区：`/home/han/pyx/g1_carry_baseline_new`。分支：`reference/continuous-side-grasp-squat-stand`。

## 结果与验收范围

**本阶段通过：原始 LargeBox + 原始半球手 G1，在自由箱体、重力、真实接触、原始电机限制下完成单周期和连续双周期侧向摩擦夹持蹲起。** 最大已测试并通过的参考下降幅度为 **12 cm**；并未搜索超过12 cm的全局可达极限。全过程没有 pickup/place、重新抓取、箱体绑定、额外支撑物或运行时箱体/root位姿写入。没有启动 PPO 训练。

正式单周期为351帧、50 FPS、7 s：A站立1 s → B下蹲2 s → C低位1 s → D起立2 s → E站立1 s。双周期651帧、13 s。两条正式12 cm动作的物理执行均先在**同一 episode** 中进行2 s夹持预检，且只有预检通过才启动参考时钟，因此实际物理记录分别为9 s和15 s。Warmup最初约2 ms存在单手接触建立过程，全部保留在数据中；**正式A–E段双手接触率均为100%，无丢失或重抓**。

| 实测指标 | 单周期12 cm | 连续双周期12 cm |
|---|---:|---:|
| 完整时长（含2 s夹持预检） | 9.0000 s | 15.0000 s |
| 实际骨盆高度范围 | 12.1433 cm | 12.1436 cm |
| 最小箱底离地 | 53.1729 cm | 53.1729 cm |
| 最大手箱平移漂移 | 1.1360 mm | 1.1360 mm |
| 最大箱体位置跟踪误差 | 4.8322 mm | 4.8435 mm |
| 最大足部滑移 | 0.5025 mm | 0.5446 mm |
| 最大骨盆高度跟踪误差 | 2.7635 mm | 2.7635 mm |
| 最大关节跟踪误差 | 0.0579 rad | 0.0579 rad |
| 非手掌对箱体接触力 | 0.0000 N | 0.0000 N |
| 平均向上摩擦力/箱重 | 96.3684 % | 96.3615 % |

表中骨盆总范围包含reset最初约1.65 mm的沉降；正式A–E段范围为 **11.9873 cm**。双周期第二次下蹲/起立也分别约11.98 cm；两段低位保持的高度波动小于0.1 mm。左右手接触率100%，双脚接触率100%。双周期末左右手相对箱体的累计平移变化分别为 0.0085/0.0089 mm。

正式动作平均左右法向夹紧力为 27.038/26.798 N，向上摩擦力为 4.944/5.454 N；箱重10.791 N。侧接触法向的最大竖直分量比仅3.14%，接触位置始终至少高于箱底 11.96 cm，符合侧面摩擦夹持而非底部承托。非手掌接触为零。

实际施加力矩没有超过原始上限；最初夹持建立阶段少数时刻达到上限。0.1 s之后力矩饱和比例为 0.000000。正式A–E最大力矩/上限比为0.6669。关节位置越界最大仅2.79e-07 rad数值误差；全记录关节速度/上限最大比为0.4756，包括reset瞬态。

验证状态仅适用于本报告的确定性模型与控制器，不等价于原HMI PPO已学会该动作，也不验证硬件、随机质量、外推速度或更深蹲姿。

## 原始数据审计与保留

原始正向/镜像参考各325帧、50 FPS。原始两个NPZ、LargeBox URDF/OBJ、原始G1半球手URDF及手掌网格的SHA256保存在 `immutable_sources.json`；验证器已检查未改变。原始完整数据没有被覆盖。

| 原始帧（闭区间） | 骨盆高度 m | 按真实旋转网格计算的箱底高度 m |
|---|---:|---:|
| 54–95 | 0.5110–0.7401 | 0.0265–0.5776 |
| 95–204 | 0.7231–0.7417 | 0.5680–0.6177 |
| 205–254 | 0.5664–0.7388 | 0.0244–0.5625 |

正向与镜像全部逐帧骨盆、箱底、实际半球手碰撞frame位置及手箱局部位置在 `audit_*.npz` 和 `source_audit.json`。这里记录的是手掌frame，不把它等同于实际物理接触点；实际接触点只取自PhysX。

原始 `largebox.obj` 的轴对齐尺寸约0.471×0.459×0.408 m，但网格自身的箱体侧面相对局部XYZ旋转、略有倾斜；其最小有向包围盒尺寸为 [0.33505318344443236, 0.3377126782442066, 0.3600858891291371] m。这是**同一个网格的坐标表达**，没有缩放/替换箱体。先前用AABB侧面安排手掌会产生悬空/穿模，最终优化改用真实凸包截面与有向侧面。

原始body数组相对本次实际使用的碰撞URDF，公共body FK位置最大差为10.158 mm。因此保留两份表达：`source_crops/` 是 `[95,205)` 所有原始字段的精确裁剪；`motions_kinematic/original_forward_carry*.npz` 保留原始全部29关节、root和object运动（仅float32存储量化），按原始碰撞URDF重算body FK与速度。没有冻结上半身。原始forward参考只有运动学验证，未冒充新控制器的物理通过结果。

## 模型与物理参数

- Robot：原始 `main_mesh_collision_halfspherehand.urdf`，29 DoF，保留双手原始半球碰撞网格、全身惯量、碰撞与自碰撞；不是小箱体掌心承托模型。
- Object：原始 `objects_largebox.urdf` + `largebox.obj`，比例1，自由动态刚体。
- URDF标称箱重0.1 kg。原HMI随机化调用使用 `operation="add"` 增加1–4 kg，因此实际质量范围是1.1–4.1 kg，而不是0.1–0.4 kg。本轮固定1.1 kg；PhysX读取值约1.100000024 kg。原对角惯量0.002按质量比11缩放为约0.022 kg·m²，三轴一致；没有启用惯量随机化。
- Robot静/动摩擦1.0/0.9；Box为0.6/0.6，均固定，回弹0。记录了PhysX实际材质张量，另记录USD材料定义及average组合模式，不能把USD默认材料标值误认为运行时override后的张量值。
- URDF中的非标准contact标签包含摩擦0.9、stiffness30000/damping1000；同原HMI的URDF导入路径没有把这两个柔顺标签应用成PhysX compliant material。实际导入材质的 compliant stiffness/damping为0，即硬接触TGS；完整读取在 `physics_model.json`，没有声称这些URDF标签已生效。
- 重力[0.0, 0.0, -9.81] m/s²，GPU PhysX TGS，1 ms物理与关节控制步长；全局位置迭代范围8–16、速度迭代范围4–8，G1 articulation配置16/8。原5 ms配合提高后的PD增益产生腕踝振荡，失败证据保留；最终稳定性不外推到5 ms控制。
- `physics_model.json` 含实际质量/惯量/材质、所有碰撞prim、碰撞启用状态、USD几何、刚体属性、关节名称和原始力矩上限。Object无任何关节，kinematic=False、rigid_body_enabled=True、disable_gravity=False。独立读取导入后的USD：LargeBox collider的实际MeshCollisionAPI为 **convexHull**、collisionEnabled=True，其子Mesh有13551个顶点，局部bounds与原始OBJ一致。原始半球手的导入碰撞也记录在 `evidence/repeated_12cm_001_data/import_geometry_audit.json`。早期logger仅按prim类型识别Mesh，会把Xform上的mesh collider误标为primitive；以独立审计实际API为准，当前logger已修正。这里验证了导入的几何、范围与碰撞近似配置，没有声称导出了PhysX内部cooked hull拓扑。

## 合成与控制

从95–204帧中扫描95/140等源姿态。最终初始化源帧140，但双脚、骨盆、腰与手臂均经过约束优化，不能把原walking帧直接当作静态平衡姿态。稳定夹持扫描在1.1 kg自由物体上保持2 s；1 ms最终轮48组中20组通过当时全部门槛，后续正式动作还独立执行同episode预检。

Pinocchio FK + SciPy非线性最小二乘优化floating pelvis和完整29关节，约束双脚落地姿态、双手/箱体SE(3)关系、整体COM、关节上下限、躯干及全部非手掌上肢的原始碰撞网格。使用凸包真实侧面定位手掌；避碰优化采用保守有向包围体和确定性网格点，最终以完整导入模型的真实接触测试判定。动作种子采用五次平滑时间律，随后**每帧**重新优化整个Robot+Object状态，加入连续性和逐帧增量约束，进行重力/接触反力逆静力学检查。没有直接拼接pickup/place片段。

所有上半身关节都属于优化变量，没有固定的上半身块。12 cm参考中13个上半身关节的幅度大于0.001 rad；某些手腕在保持接触方向/关节限位下近乎恒定，这是优化结果，不是冻结上半身。膝、髋、踝、腰、躯干、双臂共同变化。完整每关节幅度、速度和加速度见 `format_validation.json`。

控制器仅用于P0验证：原始关节限制内的显式PD + 逆静力学重力/夹紧力前馈 + 通过双脚反力分配实现的root位置/姿态反馈。反馈最终转换为**关节力矩**，没有对root或箱体直接施力、没有kinematic位姿追踪、没有关节以外的执行器。运行时守卫禁止reset之后写入root/object状态。

## 物理测量、门槛与交叉核验

逐物理步保存法向力和切向摩擦力，均为object-filtered的作用在手上的世界坐标力；箱体受到的对应力取反。接触位置来自PhysX，手箱相对位姿来自实际刚体状态；箱底由原始OBJ顶点在实际箱体姿态下取最低Z。记录非手掌body接触、双脚地面法向力、关节实际力矩与速度。早期raw中 `normal_contact_count` 名称误指摩擦patch数量，已在 `rollout_field_definitions.json` 明确；该计数从未用于力/连续性验收，后续代码已改名为 `friction_contact_count`。

各门槛均未因失败放宽；后续还增加了更严格的侧面/底部位置、完整阶段、速度及力矩检查。接触0.5 N门槛高于数值噪声，允许20 ms局部丢失但总损失≤1%；正式通过动作实际为0损失。位置门槛按原始约33 cm有向箱宽和物理步长制定。原始大箱底部距离阈值3 cm、手箱漂移2.5 cm、脚滑3 cm、box跟踪4 cm、pelvis跟踪3 cm、root水平4 cm、root倾角0.25 rad。双脚各≥95%时间有>5 N法向接触。低位保持波动≤1.5 cm；每次下降和起立都需≥8 cm，而非只看全局高度极差。

| JSON门槛键 | 值 |
|---|---:|
| `min_box_clearance_m` | 0.03 |
| `max_box_tracking_error_m` | 0.04 |
| `max_hand_slip_m` | 0.025 |
| `max_foot_slip_m` | 0.03 |
| `max_root_tilt_rad` | 0.25 |
| `max_joint_tracking_error_rad` | 0.18 |
| `min_side_normal_n` | 0.5 |
| `min_upward_friction_weight_ratio` | 0.8 |
| `max_contact_gap_s` | 0.02 |
| `max_other_box_contact_n` | 0.5 |
| `max_joint_limit_violation_rad` | 0.005 |
| `min_squat_excursion_m` | 0.08 |
| `max_pelvis_tracking_error_m` | 0.03 |
| `max_root_horizontal_error_m` | 0.04 |
| `max_hand_relative_rotation_error_rad` | 0.2 |
| `max_box_rotation_error_rad` | 0.2 |
| `max_total_contact_loss_fraction` | 0.01 |
| `max_end_height_error_m` | 0.02 |
| `max_contact_side_error_m` | 0.025 |
| `max_normal_vertical_fraction` | 0.35 |
| `min_contact_height_above_box_bottom_m` | 0.05 |
| `max_torque_limit_fraction` | 1.0001 |
| `max_joint_velocity_limit_fraction` | 1.01 |

实际夹持法向力约28 N/手，向上摩擦约占箱重96%。用自由箱体实测速度做额外牛顿定律检查：`m Δv/Δt` 与 `-Σ(hand_normal+hand_friction)+mg` 对比，正式A–E逐轴RMS残差为 [0.0001081822101362133, 1.2061814125861493e-05, 0.0006434023463318283] N，最大绝对残差为 [0.00024568289518356323, 3.221631050109863e-05, 0.001439026355745554] N。这个检查独立确认力的符号和摩擦支撑记录与真实动态加速度一致。

在真实通过轨迹上注入七类故障：无摩擦但箱子仍悬空、单手脱离100 ms、箱体触地、躯干支撑、足部滑移5 cm、关节超限、参考在动但实际骨盆不蹲。七项均被拒绝；记录在各通过trial的 `acceptance_fault_injection.json`。

## 状态、数据与失败证据

| 数据 | 最终状态 |
|---|---|
| `motions_kinematic/original_forward_carry.npz` | Kinematic only |
| `motions_kinematic/original_forward_carry_mirrored.npz` | Kinematic only |
| `motions_kinematic/continuous_grasped_squat_stand_10cm.npz` | Physics validation failed |
| `motions_kinematic/continuous_grasped_squat_stand_10cm_smooth.npz` | Physics validated |
| `motions_kinematic/continuous_grasped_squat_stand_12cm.npz` | Physics validated |
| `motions_kinematic/repeated_grasped_squat_stand_12cm.npz` | Physics validated |
| `validated_motions/continuous_grasped_squat_stand.npz` | Physics validated |
| `validated_motions/repeated_grasped_squat_stand.npz` | Physics validated |

`validated_motions/` 只含通过物理测试的12 cm单/双周期；`motions_kinematic/` 包含未经物理测试或失败的候选，禁止整目录投入训练。原始forward数据单独保留，方便后续同模型任务选择，但本次未验证其快速前进跟踪。

失败修正记录：

1. `hold_sweep_001/002/003/004/006`：Kit/Pinocchio绑定顺序、USD相对子层、惯量张量维度/候选文件依赖等基础链路问题；保留真实异常与runner退出记录。
2. `hold_sweep_005_data`：AABB手掌目标错误，夹持不足、躯干碰撞、箱体掉落。rollout已保存；当时汇总器/关闭挂起有错误，后续从原始数据重算，未据此声称通过。
3. `hold_sweep_007_data`：真实侧面改善后仍存在肩肘碰撞与脱手。
4. `hold_sweep_008_data`：加入全上肢避碰后出现持续双手接触，但5 ms/高PD导致脚踝/手腕振荡、脚滑和箱体漂移。没有降低门槛。
5. `hold_sweep_009_data`：改为1 ms控制，48组中20组达到2 s稳定夹持。
6. `squat_10cm_001_data`：完成蹲起且双手接触连续，但box跟踪约5.68 cm、root倾角约0.281 rad、水平误差约6.01 cm；判失败。
7. `squat_10cm_002_data`：平滑约束与全身足部反力反馈后通过。
8. `squat_12cm_001_data` 与 `repeated_12cm_001_data`：同episode稳定夹持预检、单周期和双周期全部通过。

每个runner目录保存 `command.json/console.log/result.json`；对应 `_data/` 保存完整 `rollout.npz`、`physics_model.json`、候选参数、代码快照及 `validation.json`。正式通过trial另有逐毫秒CSV、实际50 FPS NPZ、接触/高度/漂移/跟踪PNG/SVG和 `viewer.json`。

## 格式、原始数据与训练隔离

全部NPZ：50 FPS，world Z-up，四元数wxyz；Pinocchio内部xyzw只在边界转换。`joint_pos` 36列（root xyz+wxyz+29关节），`joint_vel` 35列（world线/角速度+29关节速度）。Body与Object姿态/速度齐全，所有命名和joint顺序与原G1一致。body FK最大位置误差在微米以下；实际HMI `MotionLoader` 已成功逐文件加载并验证维度，速度与姿态有限差分已核对。

`format_validation.json` 检查原始数据及受保护训练代码SHA256。本次没有修改PPO、Actor/Critic、Reward、Goal Sampler、已验收Stage1/2逻辑或旧reset。开始时存在训练相关未提交修改，全部保留；不要把这些既有dirty文件误认为本次改动。没有覆盖旧实验或checkpoint，没有push或启动训练。

本次新增文件：`scripts/reference_synthesis/` 下 `README.md`, `audit_imports.py`, `common.py`, `finalize.py`, `metrics.py`, `physics.py`, `prepare.py`, `review.py`, `run_pipeline.py`, `synthesize.py`, `test_acceptance.py`, `verify.py`, `view.py`，以及本报告。产物全部在 `/home/han/pyx/g1_carry_baseline_new/artifacts/carry_reference_synthesized`。

## 查看与复现

```bash
cd /home/han/pyx/g1_carry_baseline_new
source /home/han/miniconda3/etc/profile.d/conda.sh
conda activate "$PWD/envs/g1_hmi_carry"
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV LD_LIBRARY_PATH
export PYTHONNOUSERSITE=1 OMNI_KIT_ACCEPT_EULA=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1

# 查看保存的双周期实际物理轨迹，与参考并排/叠加
python HMI/scripts/reference_synthesis/view.py \
  --evidence artifacts/carry_reference_synthesized/evidence/repeated_12cm_001_data --port 8014

# 用原始G1/LargeBox真正重新执行物理；必须选择新目录
python HMI/scripts/reference_synthesis/physics.py \
  --output artifacts/carry_reference_synthesized/evidence/manual_repeat_data \
  --motion artifacts/carry_reference_synthesized/validated_motions/repeated_grasped_squat_stand.npz \
  --reset-state artifacts/carry_reference_synthesized/verified_side_grasp_reset.json \
  --gain 4 --balance 0 --dt .001 --wbc --view

# 从审计、夹持候选到单/双周期的有界重建，输出新目录
python HMI/scripts/reference_synthesis/run_pipeline.py \
  --output artifacts/carry_reference_synthesis_reproduction_001

python HMI/scripts/reference_synthesis/verify.py
```

浏览器打开 http://localhost:8014 。`Frame`逐帧，`Play`暂停/播放，`Play FPS`慢放。橙色箱体是保存的真实动态轨迹，蓝色是参考；接触标记和力线均来自实测。浏览器播放不是新的物理验证。Isaac Sim GUI由 `--view` 打开，实际重新执行自由箱体物理。

供后续Stage1/2的数据目录：`validated_motions/`，物理模型契约：`model_contract.json`，新侧向reset：`verified_side_grasp_reset.json`。当前已验收carry训练仍使用旧的小箱体/掌心承托模型；这里**没有**自动替换其HMI_CARRY_DATA或reset。后续需明确授权、匹配原始LargeBox模型及物理参数后再集成，不能只替换数据路径就宣称同等物理条件。

运行环境版本完整保存于 `runtime_versions.json`：Python 3.11.15，Isaac Sim 5.1.0.0，Isaac Lab 0.47.2，Torch 2.7.0+cu128，Pinocchio 2.7.0。CUDA/GPU与runner显存记录保留在实验日志中。
