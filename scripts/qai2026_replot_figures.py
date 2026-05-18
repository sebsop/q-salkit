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
from matplotlib import patches


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
        kwargs = {}
        if fmt == "pdf":
            kwargs["metadata"] = {
                "Creator": "q-salkit",
                "Producer": "q-salkit",
                "CreationDate": None,
                "ModDate": None,
            }
        fig.savefig(FIGURE_DIR / f"{name}.{fmt}", **kwargs)
    plt.close(fig)


def add_box(
    ax: plt.Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
    text: str,
    facecolor: str,
    edgecolor: str = "#263238",
    fontsize: int = 8,
    linewidth: float = 1.0,
) -> patches.FancyBboxPatch:
    box = patches.FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.035",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        linespacing=1.15,
    )
    return box


def add_arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float]) -> None:
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={
            "arrowstyle": "->",
            "color": "#263238",
            "linewidth": 1.2,
            "shrinkA": 2,
            "shrinkB": 2,
        },
    )


def plot_methodology_overview(data: dict, formats: tuple[str, ...]) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_facecolor("#fbfbfa")

    colors = {
        "data": "#dcebf2",
        "model": "#f3ead8",
        "saliency": "#dfeee2",
        "eval": "#f4ded5",
        "output": "#e7e1ef",
    }
    steps = [
        (0.04, "1. Data\nstandardize\nangle-scale"),
        (0.24, "2. Models\nVQC and HQNN\nQiskit"),
        (0.44, "3. Attributions\ngrad, SG, IG\nocclusion"),
        (0.64, "4. Evaluation\nfaithfulness\nrobustness"),
        (0.84, "5. Evidence\nfigures\ntables"),
    ]
    keys = ["data", "model", "saliency", "eval", "output"]
    for idx, ((x, label), key) in enumerate(zip(steps, keys)):
        add_box(ax, (x, 0.48), 0.14, 0.25, label, colors[key], fontsize=8)
        if idx < len(steps) - 1:
            add_arrow(ax, (x + 0.14, 0.605), (steps[idx + 1][0], 0.605))

    add_box(
        ax,
        (0.17, 0.17),
        0.30,
        0.19,
        "Explanation target\nVQC: expectation score z\nHQNN: selected logit or probability",
        "#f9f9f9",
        fontsize=7,
    )
    add_arrow(ax, (0.31, 0.48), (0.33, 0.36))
    add_box(
        ax,
        (0.53, 0.17),
        0.31,
        0.19,
        "Reported diagnostics\nDeletion, sensitivity, entropy\nrank stability, parameter knock-out",
        "#f9f9f9",
        fontsize=7,
    )
    add_arrow(ax, (0.71, 0.48), (0.70, 0.36))

    ax.text(
        0.5,
        0.92,
        "QNN Saliency Evaluation Framework",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
    )
    ax.text(
        0.5,
        0.05,
        "The workflow evaluates both feature-level explanations and internal parameter/gate sensitivity.",
        ha="center",
        va="bottom",
        fontsize=7,
        color="#455a64",
    )
    save(fig, "fig_methodology_overview", formats)


def draw_gate(
    ax: plt.Axes,
    x: float,
    y: float,
    width: float,
    height: float,
    label: str,
    facecolor: str,
    fontsize: int = 6,
) -> None:
    box = patches.FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width,
        height,
        boxstyle="round,pad=0.01,rounding_size=0.015",
        facecolor=facecolor,
        edgecolor="#263238",
        linewidth=0.8,
    )
    ax.add_patch(box)
    ax.text(x, y, label, ha="center", va="center", fontsize=fontsize, linespacing=1.05)


def draw_cx(ax: plt.Axes, x: float, y_control: float, y_target: float) -> None:
    ax.plot([x, x], [y_control, y_target], color="#263238", linewidth=1.0)
    ax.scatter([x], [y_control], s=18, color="#263238", zorder=3)
    target = patches.Circle((x, y_target), 0.016, facecolor="#fbfbfa", edgecolor="#263238", linewidth=0.9)
    ax.add_patch(target)
    ax.plot([x - 0.011, x + 0.011], [y_target, y_target], color="#263238", linewidth=0.8)
    ax.plot([x, x], [y_target - 0.011, y_target + 0.011], color="#263238", linewidth=0.8)


def draw_cz(ax: plt.Axes, x: float, y_a: float, y_b: float) -> None:
    ax.plot([x, x], [y_a, y_b], color="#263238", linewidth=1.0)
    ax.scatter([x, x], [y_a, y_b], s=18, color="#263238", zorder=3)


def draw_wire_labels(ax: plt.Axes, ys: list[float]) -> None:
    for idx, y in enumerate(ys):
        ax.text(0.055, y, f"$q_{idx}$", ha="right", va="center", fontsize=7, color="#263238")
        ax.plot([0.07, 0.78], [y, y], color="#263238", linewidth=0.9)
    ax.text(0.055, 0.32, r"$\vdots$", ha="right", va="center", fontsize=8, color="#455a64")


def draw_circuit_panel(
    ax: plt.Axes,
    title: str,
    subtitle: str,
    kind: str,
) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    panel = patches.FancyBboxPatch(
        (0.015, 0.06),
        0.97,
        0.87,
        boxstyle="round,pad=0.012,rounding_size=0.025",
        facecolor="#fbfbfa",
        edgecolor="#c8c8c8",
        linewidth=0.8,
    )
    ax.add_patch(panel)
    ax.text(0.05, 0.86, title, ha="left", va="center", fontsize=11, fontweight="bold", color="#263238")
    ax.text(0.05, 0.78, subtitle, ha="left", va="center", fontsize=7, color="#455a64")

    ys = [0.66, 0.56, 0.46, 0.36]
    draw_wire_labels(ax, ys)

    add_box(ax, (0.075, 0.18), 0.15, 0.10, "classical input\n$x \\in \\mathbb{R}^{d}$", "#f9f9f9", fontsize=6)
    add_arrow(ax, (0.15, 0.28), (0.18, 0.41))

    if kind == "vqc":
        ax.text(0.24, 0.73, "angle encoding", ha="center", va="center", fontsize=7, color="#455a64")
        for idx, y in enumerate(ys):
            label = "$R_Y(x_i)$" if idx % 2 else "$R_X(x_i)$"
            draw_gate(ax, 0.24, y, 0.075, 0.055, label, "#dcebf2")

        ax.text(0.38, 0.73, "CX/CZ entangler", ha="center", va="center", fontsize=7, color="#455a64")
        draw_cx(ax, 0.34, ys[0], ys[1])
        draw_cx(ax, 0.39, ys[1], ys[2])
        draw_cz(ax, 0.44, ys[2], ys[3])

        ax.text(0.56, 0.73, "trainable block, $L=2$", ha="center", va="center", fontsize=7, color="#455a64")
        for idx, y in enumerate(ys):
            label = "$R_Y(\\theta)$" if idx % 2 else "$R_Z(\\theta)$"
            draw_gate(ax, 0.56, y, 0.083, 0.055, label, "#dfeee2")
        ax.plot([0.49, 0.63], [0.31, 0.31], color="#78909c", linestyle="--", linewidth=0.8)
        ax.text(0.56, 0.27, "data re-uploading", ha="center", va="center", fontsize=6, color="#455a64")

        draw_gate(ax, 0.72, ys[0], 0.075, 0.055, "$\\langle Z \\rangle$", "#f4ded5")
        add_arrow(ax, (0.76, ys[0]), (0.82, ys[0]))
        add_box(ax, (0.82, 0.57), 0.13, 0.17, "score $z$\n$p=(1+z)/2$", "#e7e1ef", fontsize=7)
        ax.text(
            0.52,
            0.13,
            "Prediction is read directly from the measured expectation value.",
            ha="center",
            va="center",
            fontsize=7,
            color="#455a64",
        )
    else:
        ax.text(0.24, 0.73, "angle encoding", ha="center", va="center", fontsize=7, color="#455a64")
        for y in ys:
            draw_gate(ax, 0.24, y, 0.078, 0.055, "$R_Y/R_Z$", "#dcebf2")

        ax.text(0.39, 0.73, "trainable quantum layer", ha="center", va="center", fontsize=7, color="#455a64")
        for y in ys:
            draw_gate(ax, 0.39, y, 0.078, 0.055, "$R_Y(\\theta)$", "#dfeee2")

        ax.text(0.53, 0.73, "CX ladder", ha="center", va="center", fontsize=7, color="#455a64")
        draw_cx(ax, 0.50, ys[0], ys[1])
        draw_cx(ax, 0.54, ys[1], ys[2])
        draw_cx(ax, 0.58, ys[2], ys[3])

        ax.text(0.68, 0.73, "observables", ha="center", va="center", fontsize=7, color="#455a64")
        for y in ys[:3]:
            draw_gate(ax, 0.68, y, 0.066, 0.052, "$O_r$", "#f4ded5")
        ax.text(0.72, 0.49, "$h_q(x)$", ha="left", va="center", fontsize=7, color="#263238")
        add_arrow(ax, (0.72, 0.56), (0.78, 0.56))
        add_box(ax, (0.79, 0.47), 0.105, 0.19, "classical\nMLP head", "#f4ded5", fontsize=7)
        add_arrow(ax, (0.895, 0.56), (0.915, 0.56))
        add_box(ax, (0.925, 0.50), 0.052, 0.12, "logits\nprob.", "#e7e1ef", fontsize=6)
        ax.text(
            0.52,
            0.13,
            "The circuit produces expectation-value features that are classified by a classical head.",
            ha="center",
            va="center",
            fontsize=7,
            color="#455a64",
        )


def plot_circuit_architectures(data: dict, formats: tuple[str, ...]) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 5.4), constrained_layout=True)
    draw_circuit_panel(
        axes[0],
        "Fully Quantum VQC",
        "8 qubits in Cleveland; 4 qubits in Iris",
        "vqc",
    )
    draw_circuit_panel(
        axes[1],
        "Hybrid QNN",
        "8 qubits in Cleveland; 4 qubits in Iris",
        "hybrid",
    )
    save(fig, "fig_circuit_architectures", formats)


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
    labels = ["VQC", "Hybrid\nplain", "Hybrid\nricher"]
    values = [
        data["vqc_cleveland"]["accuracy"],
        data["hybrid_cleveland"]["accuracy"]["plain"],
        data["hybrid_cleveland"]["accuracy"]["richer"],
    ]
    colors = ["#3d5a80", "#98c1d9", "#ee6c4d"]

    fig, ax = plt.subplots(figsize=(4.8, 3.0))
    bars = ax.bar(labels, values, color=colors, edgecolor="black", linewidth=0.6)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Test accuracy")
    ax.set_title("Cleveland Test Accuracy")
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

    fig, axes = plt.subplots(1, 4, figsize=(8.0, 3.0), constrained_layout=True)
    for ax, (title, vals) in zip(axes, metric_groups):
        y = [vals["plain"], vals["richer"]]
        bars = ax.bar(["Plain", "Richer"], y, color=["#98c1d9", "#ee6c4d"], edgecolor="black", linewidth=0.6)
        ymax = max(y)
        ax.set_ylim(0, ymax * 1.18 if ymax > 0 else 1.0)
        ax.set_title(title)
        ax.grid(axis="y", alpha=0.25)
        ax.bar_label(bars, labels=[f"{value:.2f}" for value in y], padding=3, fontsize=8)
    fig.suptitle("Hybrid Cleveland: Explanation Metrics")
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

    plot_methodology_overview(data, formats)
    plot_circuit_architectures(data, formats)
    plot_vqc_feature_importance(data, formats)
    plot_accuracy_summary(data, formats)
    plot_hybrid_metrics(data, formats)
    plot_vqc_deletion_summary(data, formats)
    plot_vqc_rank_summary(data, formats)
    print(f"Wrote figures to {FIGURE_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
