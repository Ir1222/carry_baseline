"""Independent command sampler and smooth transitions, with no simulator dependency."""
import torch


def sample_commands(count, level, device, nominal_height=0.735):
    # Each enabled axis uses its own random variate. 25% explicit stationary hold.
    limits = [
        (0., 0., 0., 0., 0.),
        (0., 0.12, 0., 0., 0.),
        (-0.10, 0.20, 0.08, 0., 0.),
        (-0.15, 0.25, 0.12, 0.25, 0.),
        (-0.15, 0.30, 0.15, 0.35, 0.025),
    ][max(0, min(int(level), 4))]
    low = torch.tensor([limits[0], -limits[2], -limits[3], nominal_height-limits[4]], device=device)
    high = torch.tensor([limits[1], limits[2], limits[3], nominal_height+limits[4]], device=device)
    result = low + torch.rand(count, 4, device=device)*(high-low)
    hold = torch.rand(count, device=device) < 0.25
    result[hold, :3] = 0
    return result


def smooth_commands(start, target, elapsed, duration=0.5):
    t = (elapsed/duration).clamp(0, 1).unsqueeze(-1)
    blend = t*t*(3-2*t)
    return start + blend*(target-start)
