"""View/test a policy-only ONNX actor in physics without loading any motion file."""
import argparse
from dataclasses import replace
import json
from pathlib import Path
import threading
import traceback

parser = argparse.ArgumentParser()
parser.add_argument("--policy", type=Path, required=True)
parser.add_argument("--steps", type=int, default=1500)
parser.add_argument("--num-envs", type=int, default=1)
parser.add_argument("--view", action="store_true")
parser.add_argument("--interactive", action="store_true")
parser.add_argument("--forbid-motion-loading", action="store_true", help="Fail if any reference loader is constructed")
parser.add_argument("--metrics", type=Path, required=True)
args = parser.parse_args()
if args.metrics.exists():
    raise FileExistsError(args.metrics)

from holosoma.carry.presets import g1_29dof_wbt_hybrid_carry as base, DATA
from holosoma.config_types.command import CommandManagerCfg, CommandTermCfg
from holosoma.config_types.env import get_tyro_env_config
from holosoma.config_types.observation import ObservationManagerCfg
from holosoma.config_types.termination import TerminationManagerCfg
from holosoma.train_agent import TrainingContext

target = "holosoma.carry.deployment:DeploymentCommand"
config = replace(base, training=replace(base.training, num_envs=args.num_envs, headless=not args.view),
    command=CommandManagerCfg(setup_terms={"motion_command": CommandTermCfg(func=target,
        params={"reset_pose_file": str(DATA / "verified_reset.json")})},
        reset_terms={"motion_command": CommandTermCfg(func=target)},
        step_terms={"motion_command": CommandTermCfg(func=target)}),
    observation=ObservationManagerCfg(groups={"actor_obs": base.observation.groups["actor_obs"]}),
    reward=replace(base.reward, terms={k:v for k,v in base.reward.terms.items()
        if k in ("velocity_tracking", "yaw_tracking", "height_tracking", "stable_carry", "hand_support", "box_orientation")}),
    termination=TerminationManagerCfg(terms={"physical_failure": base.termination.terms["physical_failure"]}))
context = TrainingContext(config)
context.__enter__()
try:
    import torch
    from holosoma.carry.environment import CarryEnv
    from holosoma.carry.inference import CarryActor
    from holosoma.carry.observations import simulator_box_state
    from holosoma.carry.rewards import task_errors, contact_quality
    if args.forbid_motion_loading:
        from holosoma.managers.command.terms import wbt
        def forbidden(*args, **kwargs):
            raise AssertionError("Reference motion loading is forbidden during deployment")
        wbt.MotionLoader.__init__ = forbidden
        wbt.MultiMotionLoader.__init__ = forbidden
    env = CarryEnv(get_tyro_env_config(config), device="cuda:0")
    env.reset_all()
    actor = CarryActor(args.policy, args.num_envs, "cuda:0")
    command = env.command_manager.get_state("motion_command")
    sequence = [[0,0,0,.735], [.12,0,0,.735], [0,0,0,.735], [-.08,0,0,.735],
                [0,.08,0,.735], [0,-.08,0,.735], [0,0,.2,.735], [0,0,-.2,.735],
                [0,0,0,.715], [0,0,0,.755]]
    pending = []
    if args.interactive:
        def read_commands():
            print("Enter vx vy yaw_rate pelvis_height (SI units), one command per line.", flush=True)
            while True:
                try:
                    values = list(map(float, input().split()))
                    if len(values) != 4:
                        raise ValueError("Expected four numbers")
                    pending.append(values)
                except EOFError:
                    return
                except ValueError as error:
                    print(error, flush=True)
        threading.Thread(target=read_commands, daemon=True).start()
    args.metrics.parent.mkdir(parents=True, exist_ok=True)
    with args.metrics.open("x") as output:
        for step in range(args.steps):
            if pending:
                command.set_command(pending.pop(0))
            elif not args.interactive and step % 150 == 0:
                command.set_command(sequence[(step//150) % len(sequence)])
            action = actor.act(env.simulator.robot_root_states[:], env.simulator.dof_pos, env.simulator.dof_vel,
                simulator_box_state(env), command.task_command, env.simulator.scene.env_origins[:,2])
            _, reward, done, info = env.step({"actions": action})
            assert torch.isfinite(action).all() and torch.isfinite(reward).all()
            actor.reset(torch.where(done)[0])
            output.write(json.dumps({"step": step, "command": command.task_command.tolist(),
                "errors": task_errors(env).tolist(), "contact_quality": contact_quality(env).tolist(),
                "root_height": env.simulator.robot_root_states[:,2].tolist(),
                "box_height": env.simulator._object.data.root_pos_w[:,2].tolist(), "done": done.tolist()})+"\n")
    print(f"Evaluation completed: {args.steps} physics steps; metrics: {args.metrics}", flush=True)
except BaseException:
    traceback.print_exc()
    raise
finally:
    context.__exit__(None, None, None)
