"""Replot QAI 2026 paper figures from saved JSON artifacts."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "paper_artifacts" / "qai2026" / "data" / "qai2026_curated_results.json"
FIGURE_DIR = ROOT / "paper_artifacts" / "qai2026" / "figures"
MPLCONFIG_DIR = ROOT / "paper_artifacts" / "qai2026" / ".matplotlib"
FONT_CACHE_DIR = ROOT / "paper_artifacts" / "qai2026" / ".cache"
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIG_DIR))
os.environ.setdefault("XDG_CACHE_HOME", str(FONT_CACHE_DIR))
MPLCONFIG_DIR.mkdir(parents=True, exist_ok=True)
FONT_CACHE_DIR.mkdir(parents=True, exist_ok=True)

import matplotlib.pyplot as plt


def setup_style(font_size: int) -> None:
    plt.rcParams.update(
        {
            "font.size": font_size,
            "axes.labelsize": font_size,
            "axes.titlesize": font_size + 1,
            "xtick.labelsize": font_size - 1,
            "ytick.labelsize": font_size - 1,
            "legend.fontsize": font_size - 1,
            "figure.dpi": 160,
            "savefig.bbox": "tight",
        }
    )


def save(fig: plt.Figure, name: str, formats: tuple[str, ...]) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    for fmt in formats:
        fig.savefig(FIGURE_DIR / f"{name}.{fmt}")
    plt.close(fig)


def plot_vqc_feature_importance(data: dict, formats: tuple[str, ...]) -> None:
    scores = data["vqc_cleveland"]["feature_scores"]
    features = scores["features"]
    methods = [
        ("IG", np.array(scores["ig_norm"])),
        ("Grad x Input", np.array(scores["gi_norm"])),
        ("Noise sens.", np.array(scores["ns_norm"])),
        ("Occlusion", np.array(scores["occ_norm"])),
    ]
    x = np.arange(len(features))
    width = 0.19

    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    for idx, (label, values) in enumerate(methods):
        ax.bar(x + (idx - 1.5) * width, values, width=width, label=label)
    ax.set_ylabel("Normalized importance")
    ax.set_title("VQC Cleveland: Global Feature Importance")
    ax.set_xticks(x)
    ax.set_xticklabels(features, rotation=35, ha="right")
    ax.legend(ncols=2, frameon=False)
    ax.grid(axis="y", alpha=0.25)
    save(fig, "fig_vqc_cleveland_global_importance", formats)


def plot_accuracy_summary(data: dict, formats: tuple[str, ...]) -> None:
    labels = ["VQC\nCleveland", "Hybrid plain\nCleveland", "Hybrid richer\nCleveland", "VQC\nIris"]
    values = [
        data["vqc_cleveland"]["accuracy"],
        data["hybrid_cleveland"]["accuracy"]["plain"],
        data["hybrid_cleveland"]["accuracy"]["richer"],
        data["vqc_iris"]["accuracy"],
    ]
    colors = ["#3d5a80", "#98c1d9", "#ee6c4d", "#7a9e7e"]

    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    bars = ax.bar(labels, values, color=colors, edgecolor="black", linewidth=0.6)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Test accuracy")
    ax.set_title("Predictive Performance Summary")
    ax.grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.025, f"{value:.3f}", ha="center", va="bottom")
    save(fig, "fig_accuracy_summary", formats)


def plot_hybrid_metrics(data: dict, formats: tuple[str, ...]) -> None:
    hybrid = data["hybrid_cleveland"]
    metric_groups = [
        ("Sensitivity", hybrid["average_sensitivity"]),
        ("Entropy", hybrid["saliency_entropy"]),
        ("Sparseness", hybrid["saliency_sparseness_l1_l2"]),
        ("Rank stability", {
            "plain": hybrid["stability_probe"]["plain_spearman"],
            "richer": hybrid["stability_probe"]["richer_spearman"],
        }),
    ]

    fig, axes = plt.subplots(1, 4, figsize=(8.0, 2.7))
    for ax, (title, vals) in zip(axes, metric_groups):
        y = [vals["plain"], vals["richer"]]
        ax.bar(["Plain", "Richer"], y, color=["#98c1d9", "#ee6c4d"], edgecolor="black", linewidth=0.6)
        ax.set_title(title)
        ax.grid(axis="y", alpha=0.25)
        for i, value in enumerate(y):
            ax.text(i, value, f"{value:.2f}", ha="center", va="bottom", fontsize=8)
    fig.suptitle("Hybrid Cleveland: Explanation Metrics", y=1.06)
    save(fig, "fig_hybrid_cleveland_metrics", formats)


def plot_vqc_deletion_summary(data: dict, formats: tuple[str, ...]) -> None:
    deletion = data["vqc_cleveland"]["deletion"]
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    ax.plot([0, 8], [deletion["initial_confidence"], deletion["all_features_removed_confidence"]], marker="o")
    ax.set_xticks([0, 8])
    ax.set_xticklabels(["Original", "All masked"])
    ax.set_ylim(0, 0.75)
    ax.set_ylabel("Mean true-class confidence")
    ax.set_title(f"VQC Cleveland Deletion Summary\nAUDC = {deletion['audc']:.3f}")
    ax.grid(axis="y", alpha=0.25)
    save(fig, "fig_vqc_cleveland_deletion_summary", formats)


def plot_vqc_rank_summary(data: dict, formats: tuple[str, ...]) -> None:
    scores = data["vqc_cleveland"]["feature_scores"]
    features = scores["features"]
    mean_rank = np.array(scores["mean_rank"])
    order = np.argsort(mean_rank)

    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.barh(np.array(features)[order], mean_rank[order], color="#3d5a80", edgecolor="black", linewidth=0.6)
    ax.invert_yaxis()
    ax.set_xlabel("Mean rank across methods (lower is better)")
    ax.set_title("VQC Cleveland: Consensus Feature Ranking")
    ax.grid(axis="x", alpha=0.25)
    save(fig, "fig_vqc_cleveland_mean_rank", formats)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--font-size", type=int, default=10)
    parser.add_argument("--formats", nargs="+", default=["pdf", "png"], choices=["pdf", "png", "svg"])
    args = parser.parse_args()

    setup_style(args.font_size)
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    formats = tuple(args.formats)

    plot_vqc_feature_importance(data, formats)
    plot_accuracy_summary(data, formats)
    plot_hybrid_metrics(data, formats)
    plot_vqc_deletion_summary(data, formats)
    plot_vqc_rank_summary(data, formats)
    print(f"Wrote figures to {FIGURE_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
