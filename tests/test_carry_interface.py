"""Fast invariants for the simulator-independent carry interface."""
import math
import torch
from holosoma.carry.observations import physical_frame, FRAME_DIM
from holosoma.carry.sampling import sample_commands, smooth_commands
from holosoma.utils.rotations import quat_apply, quat_mul


def states(n=8):
    root = torch.zeros(n, 13); root[:, 6] = 1; root[:, 2] = .735
    box = root.clone(); box[:, 0] = .35; box[:, 2] = .85
    q = torch.zeros(n, 29)
    c = torch.tensor([.1, -.07, .2, .735]).repeat(n, 1)
    return root, box, q, c


def test_actor_schema_and_heading_frame_invariance():
    root, box, q, c = states()
    root[:, 7] = .1; root[:, 8] = -.07; root[:, 12] = .2
    box[:, 7:10] = root[:, 7:10]
    a = physical_frame(root, q, q, q, q, box, c, torch.zeros(8))
    assert a.shape == (8, FRAME_DIM) and torch.equal(a[:, -4:], c)
    rotation = torch.tensor([0., 0., math.sin(.7/2), math.cos(.7/2)]).repeat(8, 1)
    for state in (root, box):
        state[:, :3] = quat_apply(rotation, state[:, :3], w_last=True)+torch.tensor([3., -4., 0.])
        state[:, 3:7] = quat_mul(rotation, state[:, 3:7], w_last=True)
        state[:, 7:10] = quat_apply(rotation, state[:, 7:10], w_last=True)
        state[:, 10:13] = quat_apply(rotation, state[:, 10:13], w_last=True)
    b = physical_frame(root, q, q, q, q, box, c, torch.zeros(8))
    torch.testing.assert_close(a, b, atol=1e-6, rtol=1e-6)


def test_independent_sampling_and_stationary_hold():
    torch.manual_seed(2)
    c = sample_commands(30000, 4, "cpu")
    moving = c[c[:, :3].abs().sum(-1) > 0]
    correlation = torch.corrcoef(moving.T)
    assert (correlation-torch.eye(4)).abs().max() < .03
    assert (c[:, 0] < 0).any() and (c[:, 0] > 0).any()
    assert ((c[:, 0] == 0) & (c[:, 1] == 0) & (c[:, 2] == 0)).float().mean() > .2
    hold = sample_commands(30, 0, "cpu")
    assert torch.equal(hold[:, :3], torch.zeros(30, 3))


def test_smooth_command_transition_and_independent_yaw_height():
    start = torch.tensor([[0., 0., 0., .735]])
    end = torch.tensor([[0., 0., .25, .715]])
    torch.testing.assert_close(smooth_commands(start, end, torch.tensor([0.])), start)
    torch.testing.assert_close(smooth_commands(start, end, torch.tensor([.5])), end)
    middle = smooth_commands(start, end, torch.tensor([.25]))
    torch.testing.assert_close(middle, (start+end)/2)
    assert (middle[:, :2] == 0).all()
