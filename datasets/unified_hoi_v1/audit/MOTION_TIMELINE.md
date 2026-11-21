# Full HMI motion timeline (kinematic candidates only)

Pinned upstream: c353731999b3578c41ad5a00f896415b45e6a9f5. All three local source files byte-identical.

## sub3_largebox_003_mj_w_obj.npz

FK mismatch before canonical export: 0.010158m. Box bottom minimum -0.0083m.

| Candidate phase | Frames [start,end) | Time seconds |
|---|---|---|
| approach_reach_candidate | 0–25 | 0.00–0.48 |
| contact_acquisition_candidate | 25–55 | 0.50–1.08 |
| lifting_candidate | 55–95 | 1.10–1.88 |
| loaded_carry_candidate | 95–205 | 1.90–4.08 |
| lowering_candidate | 205–271 | 4.10–5.40 |
| support_transfer_candidate | 271–285 | 5.42–5.68 |
| release_candidate | 285–325 | 5.70–6.48 |

Contact/lift/settle/release candidate frames: 25, 55, 271, 285. No force inference is certified by these labels.

## movebox/sub3_largebox_003_mj_w_obj_reframed.npz

FK mismatch before canonical export: 0.010158m. Box bottom minimum -0.0083m.

| Candidate phase | Frames [start,end) | Time seconds |
|---|---|---|
| approach_reach_candidate | 0–25 | 0.00–0.48 |
| contact_acquisition_candidate | 25–55 | 0.50–1.08 |
| lifting_candidate | 55–95 | 1.10–1.88 |
| loaded_carry_candidate | 95–205 | 1.90–4.08 |
| lowering_candidate | 205–271 | 4.10–5.40 |
| support_transfer_candidate | 271–285 | 5.42–5.68 |
| release_candidate | 285–325 | 5.70–6.48 |

Contact/lift/settle/release candidate frames: 25, 55, 271, 285. No force inference is certified by these labels.

## movebox/sub3_largebox_003_mj_w_obj_reframed_mirrored.npz

FK mismatch before canonical export: 0.010158m. Box bottom minimum -0.0107m.

| Candidate phase | Frames [start,end) | Time seconds |
|---|---|---|
| approach_reach_candidate | 0–27 | 0.00–0.52 |
| contact_acquisition_candidate | 27–55 | 0.54–1.08 |
| lifting_candidate | 55–95 | 1.10–1.88 |
| loaded_carry_candidate | 95–205 | 1.90–4.08 |
| lowering_candidate | 205–271 | 4.10–5.40 |
| support_transfer_candidate | 271–287 | 5.42–5.72 |
| release_candidate | 287–325 | 5.74–6.48 |

Contact/lift/settle/release candidate frames: 27, 55, 271, 287. No force inference is certified by these labels.
