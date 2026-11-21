# Joint Stage1 Track reference bundle

This versioned bundle contains byte-identical copies of the P0 squat/stand references and the original forward-carry crop. Original files remain in the local `artifacts/carry_reference_synthesized/` directory and were not overwritten.

All clips preserve 29 joints, root pose/velocities, body pose/velocities and object pose/velocities, at 50FPS, world Z-up, NPZ quaternions wxyz. The existing HMI loader converts runtime quaternions to xyzw. The two squat clips have P0 controller validation; the forward clip remains kinematic-only with failed prior controller admission. No forward physics certificate is asserted.

Admission into this **Stage1 Track training bundle** follows the user's revised instruction: format/FK/asset consistency is required, but prior successful reproduction by the P0 controller is not a prerequisite for learning a Track target. Policy physics acceptance is a separate requirement, unchanged by admission.

Half the training environments sample the squat family and half the forward family. Within the squat family the single/repeated clip weights are 40%/60%. All environments are Track, share one policy/critic and do not expose family IDs to the actor.

`manifest.json` records exact hashes and separate training/physics statuses. `provenance/` preserves original P0 audits; those reports describe their original validation scope and code version. They do not certify the current PPO policy. See `README_STAGE1_JOINT.md` for the manual uninterrupted 15000-update entry point and evaluation commands.
