"""Seed QAI 2026 paper artifacts from current notebook outputs.

This script records the scalar/table values already present in the checked
notebooks. It does not train models.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "paper_artifacts" / "qai2026" / "data"


CURATED_RESULTS = {
    "metadata": {
        "source": "Values transcribed from executed notebook outputs.",
        "note": (
            "Curve-level artifacts are not present in the repository yet. "
            "Use notebook artifact-export cells for exact deletion/stability curves."
        ),
    },
    "vqc_cleveland": {
        "accuracy": 0.7826,
        "deletion": {
            "initial_confidence": 0.618,
            "all_features_removed_confidence": 0.475,
            "confidence_drop": 0.143,
            "audc": 0.428,
        },
        "average_sensitivity": 0.000652,
        "saliency_entropy": 0.3076,
        "saliency_sparseness_l1_l2": 5.3209,
        "spearman_vs_seed0": [0.524, 0.524, 0.381, 0.595],
        "feature_scores": {
            "features": [
                "thal",
                "cp",
                "ca",
                "exang",
                "slope",
                "oldpeak",
                "thalach",
                "chol",
            ],
            "ig_norm": [
                0.8459176,
                0.1540824,
                1.228999e-16,
                1.536779e-16,
                9.177773e-17,
                4.664701e-17,
                6.178409e-17,
                4.468437e-17,
            ],
            "gi_norm": [
                0.9692782,
                0.03072178,
                2.150320e-16,
                4.310064e-16,
                3.007523e-16,
                1.112506e-16,
                1.456848e-16,
                8.402043e-17,
            ],
            "ns_norm": [
                0.7810015,
                0.1476986,
                0.07129986,
                4.336135e-15,
                4.034348e-15,
                4.518355e-15,
                4.239921e-15,
                4.103585e-15,
            ],
            "occ_norm": [
                0.8818782,
                0.1104646,
                0.007657198,
                1.942452e-16,
                1.942452e-16,
                1.942452e-16,
                0.0,
                0.0,
            ],
            "mean_rank": [1.0, 2.0, 3.75, 4.25, 5.25, 5.75, 6.25, 7.75],
        },
    },
    "vqc_iris": {
        "accuracy": 0.9375,
        "spearman_vs_seed0": [1.0, 1.0, 1.0, 0.8],
    },
    "hybrid_cleveland": {
        "accuracy": {"plain": 0.8197, "richer": 0.8361},
        "stability_probe": {
            "epochs": 3,
            "plain_accuracy_mean": 0.593,
            "plain_accuracy_std": 0.145,
            "plain_spearman": 0.554,
            "richer_accuracy_mean": 0.475,
            "richer_accuracy_std": 0.0,
            "richer_spearman": 0.613,
        },
        "average_sensitivity": {"plain": 21.214615, "richer": 44.392387},
        "saliency_entropy": {"plain": 2.0726507, "richer": 2.0752678},
        "saliency_sparseness_l1_l2": {"plain": 13.425935, "richer": 14.305616},
        "overreliance_risk": {"plain": -0.6500894306177838, "richer": -0.6155564469983654},
        "minimum_efficacy": {
            "plain_auc_confidence": 0.7800,
            "plain_auc_saliency": 0.2473,
            "plain_saliency_gain": -0.5327,
            "richer_auc_confidence": 0.7333,
            "richer_auc_saliency": 0.4765,
            "richer_saliency_gain": -0.2569,
        },
        "wilcoxon": {
            "features": ["thal", "cp", "ca", "exang", "oldpeak", "chol", "thalach", "slope"],
            "statistic": [310.0, 531.0, 542.0, 557.0, 303.0, 560.0, 350.0, 440.0],
            "p_value": [0.0001, 0.0339, 0.0413, 0.0536, 0.0001, 0.0564, 0.0006, 0.0052],
        },
    },
    "hybrid_iris": {
        "accuracy_reported": {"plain": 1.0, "richer": 1.0},
        "accuracy_classification_report": {"plain": 0.97, "richer": 0.97},
        "average_sensitivity": {"plain": 105.03278, "richer": 123.172195},
        "saliency_entropy": {"plain": 1.3723845, "richer": 1.383727},
        "saliency_sparseness_l1_l2": {"plain": 8.548584, "richer": 9.246264},
    },
}


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DATA_DIR / "qai2026_curated_results.json"
    out_path.write_text(json.dumps(CURATED_RESULTS, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
