"""Physical tensors + unchanged four goals + explicit intention. No motion imports."""
import numpy as np
import torch
from holosoma.carry.inference import CarryActor
from holosoma.carry.observations import physical_frame

class UnifiedActor(CarryActor):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.metadata.get('unified_schema')!=1:raise ValueError('Unified actor checkpoint required')
        self.history=torch.zeros(len(self.previous_action),3,119,device=self.previous_action.device)
    def act(self,root_xyzw,joint_pos,joint_vel,box_xyzw,commands,ground_height,task_mode):
        if isinstance(task_mode,str):
            if task_mode not in ('pickup','carry','putdown'):raise ValueError('Unknown task mode')
            task_mode=('pickup','carry','putdown').index(task_mode)
        raw=torch.as_tensor(task_mode,device=joint_pos.device)
        if not torch.isfinite(raw).all() or (raw!=raw.long()).any():raise ValueError('task_mode must be an integer intention')
        mode=raw.long().expand(len(joint_pos))
        if ((mode<0)|(mode>2)).any():raise ValueError('task_mode must be pickup=0, carry=1, putdown=2')
        frame=physical_frame(root_xyzw,joint_pos,joint_vel,self.default_joint_pos,self.previous_action,box_xyzw,commands,ground_height)
        frame=torch.cat([frame,torch.nn.functional.one_hot(mode,3).float()],-1).clamp(-100,100)
        self.history[:,:-1]=self.history[:,1:].clone();self.history[:,-1]=frame
        rows=self.history.flatten(1).detach().cpu().numpy().astype(np.float32)
        actions=np.concatenate([self.session.run(['action'],{'actor_obs':r[None]})[0] for r in rows])
        self.previous_action=torch.as_tensor(actions,device=joint_pos.device)
        return self.previous_action
