from holosoma.carry.fullbody_ppo import FullBodyCarryPPO
class UnifiedCarryPPO(FullBodyCarryPPO):
    pass  # Reuse PPO, checkpoint integrity and ONNX parity; schema is supplied by the environment.
