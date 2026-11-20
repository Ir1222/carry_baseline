"""Forward/height commands derived from admitted references; simulator independent."""
import torch


def transition(start, target, elapsed, height_rate, velocity_duration=.8):
    # Cubic smoothstep peaks at 1.5 delta/T. Per-axis duration bounds dh/dt.
    duration = torch.full_like(start, velocity_duration)
    duration[:, 3] = torch.maximum(duration[:, 3], 1.5*(target[:, 3]-start[:, 3]).abs()/height_rate)
    t = (elapsed[:, None]/duration).clamp(0, 1)
    return start+(target-start)*t.square()*(3-2*t)


def sample(count, level, device, limits):
    """A-E explicit modes and later independent vx/h mixed sampling."""
    low, high = limits['height_low'], limits['height_high']
    mode = torch.multinomial(torch.tensor(
        [.30,.15,.25,.25,.05,0.] if level == 0 else
        [.20,.15,.20,.20,.20,.05] if level == 1 else
        [.15,.15,.15,.15,.25,.15], device=device), count, replacement=True)
    values = torch.zeros(count, 4, device=device)
    values[:, 3] = high
    values[(mode == 1) | (mode == 2), 3] = low
    forward = mode >= 4
    # These are independent random variates, conditional on mode.
    speed = torch.rand(count, device=device)*limits['vx_high']*min(1., .5+.25*level)
    height = low+torch.rand(count, device=device)*(high-low)
    values[forward, 0] = speed[forward]
    values[mode == 5, 3] = height[mode == 5]
    return values, mode


def validate_commands(value, limits):
    if not torch.isfinite(value).all() or value.shape[-1] != 4:
        raise ValueError('Expected finite [N,4] commands')
    if (value[:, 0] < 0).any() or (value[:, 1:3].abs() > 1e-7).any():
        raise ValueError('This experiment admits vx>=0, vy=0, yaw_rate=0 only')
    if (value[:, 0] > limits['vx_high']+1e-6).any():
        raise ValueError('Forward velocity exceeds admitted training range')
    if ((value[:, 3] < limits['height_low']-.005) | (value[:, 3] > limits['height_high']+.005)).any():
        raise ValueError('Height exceeds reference-derived range')
