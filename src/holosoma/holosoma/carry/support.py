"""Measured support transfer, independent of reference phase and task mode."""
import torch

PROTOCOL = "measured_support_v2"
DEFAULTS = dict(contact_threshold_n=.5, loss_of_grasp_s=.10, reset_grace_s=.10,
                support_confirm_s=.20, support_loss_s=.10, release_confirm_s=.50)
PRIVILEGED_FIELDS = (
    "left_hand_normal_n", "right_hand_normal_n", "bilateral_contact",
    "ground_support_weight_ratio", "upward_friction_weight_ratio",
    "continuous_no_contact_s", "grasp_acquired", "stable_support", "released",
    "support_required", "support_stable_s", "support_lost_s", "release_stable_s",
    "reset_grace_remaining_s", "nonhand_box_contact_n", "nonhand_upward_force_n",
    "hand_slip_speed_m_s", "box_clearance_m", "object_speed_m_s", "object_angular_speed")


def advance_contact_gap(gap, both, required, sim_dt):
    """Only the physics loop calls this; duty cycle never increments a timer."""
    return torch.where(both | ~required, 0., gap + sim_dt)


class SupportState:
    def __init__(self, n, device, **settings):
        self.settings = {**DEFAULTS, **settings}
        self.acquired = torch.zeros(n, device=device, dtype=torch.bool)
        self.stable = torch.zeros_like(self.acquired)
        self.required = torch.zeros_like(self.acquired)
        self.support_time = torch.zeros(n, device=device)
        self.lost_time = torch.zeros_like(self.support_time)
        self.release_time = torch.zeros_like(self.support_time)
        self.age = torch.zeros_like(self.support_time)

    def reset(self, ids):
        for name in ("acquired", "stable", "required", "support_time", "lost_time", "release_time", "age"):
            getattr(self, name)[ids] = 0

    def update(self, m, dt):
        cfg = self.settings
        self.age += dt
        sample = m["stable_support_sample"]
        departure = ((m["box_clearance_m"] > .08) | (m["object_speed_m_s"] > .8)
                     | (m["object_angular_speed"] > 3.))
        self.support_time = torch.where(sample, self.support_time + dt, 0.)
        self.lost_time = torch.where(sample, 0., self.lost_time + dt)
        self.stable = (self.stable | (self.support_time >= cfg["support_confirm_s"] - 1e-7)) & ~(
            departure | (self.lost_time >= cfg["support_loss_s"] - 1e-7))
        hands = (m["bilateral_contact"] > .5) & (m["upward_friction_weight_ratio"] >= .5)
        airborne = m["box_clearance_m"] > .03
        self.acquired |= hands & airborne
        required = ~self.stable & ~sample & (airborne | self.acquired)
        entered = required & ~self.required
        self.required = required
        released = ((m["left_hand_normal_n"] < cfg["contact_threshold_n"]) &
                    (m["right_hand_normal_n"] < cfg["contact_threshold_n"]))
        clean = m["nonhand_box_contact_n"] <= cfg["contact_threshold_n"]
        self.release_time = torch.where(self.stable & released & clean, self.release_time + dt, 0.)
        gap = torch.where(required & ~entered, m["continuous_no_contact_s"], 0.)
        grace_remaining = (cfg["reset_grace_s"] - self.age).clamp_min(0)
        m.update(grasp_acquired=self.acquired.float(), stable_support=self.stable.float(),
                 released=released.float(), support_required=required.float(),
                 support_transition=(sample & ~self.stable).float(),
                 support_stable_s=self.support_time.clone(), support_lost_s=self.lost_time.clone(),
                 release_stable_s=self.release_time.clone(), reset_grace_remaining_s=grace_remaining,
                 continuous_no_contact_s=gap,
                 putdown_stable_success=(self.release_time >= cfg["release_confirm_s"] - 1e-7).float())
        return (grace_remaining <= 1e-7) & required & (gap >= cfg["loss_of_grasp_s"] - 1e-7)
