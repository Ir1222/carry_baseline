"""HMI PPO unchanged; publish only complete, stable checkpoint/export files."""
from pathlib import Path
from holosoma.carry.fullbody_ppo import FullBodyCarryPPO


class UnifiedCarryPPO(FullBodyCarryPPO):
    def save(self,path,infos=None):
        super().save(path,infos)
        for file in (Path(path),Path(path).with_suffix('.ready.json')):
            self.logging_helper.save_to_wandb(str(file))

    def _export_actor(self,path):
        # CarryPPO exports to a temporary name. W&B must see the final names,
        # after parity/checksums/atomic publication, rather than broken symlinks.
        upload=self.logging_helper.save_to_wandb
        self.logging_helper.save_to_wandb=lambda _:None
        try:
            super()._export_actor(path)
        finally:
            self.logging_helper.save_to_wandb=upload

    def export(self,onnx_file_path):
        super().export(onnx_file_path)
        path=Path(onnx_file_path)
        for file in (path,path.with_suffix('.actor.json'),path.with_suffix('.export.json')):
            self.logging_helper.save_to_wandb(str(file))
