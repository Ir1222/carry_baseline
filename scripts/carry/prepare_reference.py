"""Crop actual carry frames, preserving source data; no pickup/place is claimed."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np
from scipy.spatial.transform import Rotation

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "src/holosoma/holosoma/data/motions/g1_29dof/whole_body_tracking"
DEFAULT_OUTPUT = ROOT.parent / "artifacts/carry_reference"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--start", type=int, default=95)
    parser.add_argument("--stop", type=int, default=205)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    motions = args.output / "motions"
    motions.mkdir()
    manifest = {"interval": [args.start, args.stop], "claims": "carry only; no pickup or place", "motions": []}
    for source in sorted((SOURCE / "movebox").glob("*.npz")):
        with np.load(source) as data:
            n = len(data["joint_pos"])
            assert 0 <= args.start < args.stop <= n
            crop = {k: data[k][args.start:args.stop].copy()
                    if data[k].ndim and data[k].shape[0] == n else data[k].copy() for k in data.files}
        i = crop["body_names"].tolist().index("pelvis")
        rot = Rotation.from_quat(crop["body_quat_w"][:, i, [1, 2, 3, 0]])
        heading = Rotation.from_euler("z", rot.as_euler("xyz")[:, 2])
        vel = heading.inv().apply(crop["body_lin_vel_w"][:, i])
        command = np.column_stack([vel[:, :2], crop["body_ang_vel_w"][:, i, 2], crop["body_pos_w"][:, i, 2]])
        assert np.isfinite(command).all() and crop["object_pos_w"][:, 2].min() > 0.7
        np.savez_compressed(motions / source.name, **crop)
        manifest["motions"].append({"source": str(source.relative_to(ROOT)),
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "frames": len(command),
            "fps": float(crop["fps"].item()), "command_min": command.min(axis=0).tolist(),
            "command_max": command.max(axis=0).tolist(), "box_z_min": float(crop["object_pos_w"][:, 2].min())})
    tree = ET.parse(SOURCE / "objects_largebox.urdf")
    tree.find(".//mass").set("value", "1.5")
    # Consistent cuboid inertia approximation for the supplied ~0.47 x 0.46 x 0.41 m mesh.
    inertia = tree.find(".//inertia")
    dx, dy, dz = 0.471, 0.459, 0.408
    for key, value in {"ixx": 1.5*(dy*dy+dz*dz)/12, "iyy": 1.5*(dx*dx+dz*dz)/12,
                       "izz": 1.5*(dx*dx+dy*dy)/12}.items():
        inertia.set(key, str(value))
    for mesh in tree.findall(".//mesh"):
        mesh.set("filename", str(SOURCE / "largebox.obj"))
    tree.write(args.output / "carry_box.urdf", encoding="unicode", xml_declaration=True)
    manifest["box_mass_kg"] = 1.5
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
