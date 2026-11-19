# Measured static reset and initial-settling evidence

`verified_reset.json` is a static physical reset asset, not a motion trajectory or
policy. `initial_settling_64env.json.gz` contains the actual bounded replay output.
The JSON hash in the pose is the SHA256 of the **uncompressed** evidence file.

Test: 64 environments, fixed joint PD targets, free 0.5 kg cuboid of dimensions
0.28 × 0.40 × 0.30 m, G1 half-sphere hand collisions, gravity enabled, no attachment,
no balance feedback, no root/object pose updates after initialization. Gains are
included in the pose; original effort limits are unchanged. The acceptance window
is the first 0.2 s. Across all environments: maximum box drop 1.44 cm, minimum root
height 0.758 m, minimum individual hand force 1.44 N, minimum summed vertical hand
support 68.4% of weight. Forces use a 50 ms average of actual PhysX normal/friction
contacts. This validates initial contact settling, **not sustained open-loop
balance, convergence, or a successful carrying policy**. At 0.5 s, some candidates
already have up to 10.1 cm box drop. Longer diagnostic holds required ankle feedback.

Actual replay command (the candidate-generation sweep remains a diagnostic):

```bash
python scripts/carry/probe_settling.py \
  --replay ../artifacts/p2_mvp_palmup3.json --candidate 14 --steps 25 \
  --gain-scale 4 --ankle-stiffness 300 \
  --data ../artifacts/carry_reference_mvp --output ../artifacts/p2_reset_replay1.json
```

Use `finalize_reference.py` with the compressed evidence to reproduce the ready
reference directory. It reruns all 64 initial-settling acceptance assertions and
regenerates the reference transforms through FK. See `README_CARRY.md`.
