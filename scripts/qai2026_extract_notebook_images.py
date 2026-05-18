"""Extract selected embedded notebook figures as temporary paper previews.

These PNGs are useful for placement decisions. They are not a substitute for
the replot workflow because font and figure sizes are baked into the notebook
outputs.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "paper_artifacts" / "qai2026" / "figures" / "notebook_previews"

FIGURE_MAP = {
    "notebooks/quantum/VQC_Cleveland.ipynb": {
        8: ["preview_vqc_cleveland_circuit"],
        43: ["preview_vqc_cleveland_multi_method_importance"],
        45: ["preview_vqc_cleveland_gate_knockout_topk", "preview_vqc_cleveland_gate_knockout_summary"],
        51: ["preview_vqc_cleveland_deletion_curve"],
    },
    "notebooks/hybrid/hybrid_qnn_saliency_cleveland.ipynb": {
        17: ["preview_hybrid_cleveland_circuit"],
        51: ["preview_hybrid_cleveland_global_plain", "preview_hybrid_cleveland_global_richer"],
        53: ["preview_hybrid_cleveland_deletion_curve"],
        75: ["preview_hybrid_cleveland_parameter_knockout"],
    },
}


def image_payloads(cell: dict) -> list[str]:
    payloads: list[str] = []
    for output in cell.get("outputs", []):
        data = output.get("data", {})
        if "image/png" in data:
            value = data["image/png"]
            payloads.append("".join(value) if isinstance(value, list) else value)
    return payloads


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for notebook_rel, cell_map in FIGURE_MAP.items():
        notebook_path = ROOT / notebook_rel
        nb = json.loads(notebook_path.read_text(encoding="utf-8"))
        for cell_idx, names in cell_map.items():
            payloads = image_payloads(nb["cells"][cell_idx])
            for name, payload in zip(names, payloads):
                out_path = OUT_DIR / f"{name}.png"
                out_path.write_bytes(base64.b64decode(payload))
                written.append(out_path)
    for path in written:
        print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
