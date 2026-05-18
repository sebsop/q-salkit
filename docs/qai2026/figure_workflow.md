# QAI 2026 Figure Workflow

The notebooks currently contain plotted outputs, but most underlying arrays are
not saved as reusable artifacts. The workflow is therefore split into two layers.

## Immediate layer

Run:

```bash
python scripts/qai2026_seed_artifacts.py
python scripts/qai2026_replot_figures.py
python scripts/qai2026_extract_notebook_images.py
python scripts/qai2026_write_tables.py
```

This creates:

- curated JSON data from existing notebook outputs
- adjustable methodology, architecture, and summary figures from the JSON artifact
- temporary PNG previews extracted from embedded notebook outputs
- LaTeX table snippets for Overleaf

Primary generated figures:

- `fig_methodology_overview.pdf`
- `fig_circuit_architectures.pdf`
- `fig_accuracy_summary.pdf`
- `fig_vqc_cleveland_global_importance.pdf`
- `fig_vqc_cleveland_mean_rank.pdf`
- `fig_vqc_cleveland_deletion_summary.pdf`
- `fig_hybrid_cleveland_metrics.pdf`

## Full artifact layer

For exact deletion curves, stability heatmaps, and parameter knock-out data,
add `np.savez` export cells to the Cleveland notebooks after the relevant cells
finish computing arrays:

- `notebooks/quantum/VQC_Cleveland.ipynb`
- `notebooks/hybrid/hybrid_qnn_saliency_cleveland.ipynb`

Save arrays into `paper_artifacts/qai2026/data/` and update
`scripts/qai2026_replot_figures.py` to prefer exact artifacts when present.

## Overleaf usage

Use `.pdf` figures for the paper and `.png` figures only for quick preview.
The `notebook_previews/` folder is useful for layout decisions, but final
figures should come from the replot script where possible.

Use `docs/qai2026/overleaf_snippets.tex` for figure placement and
`docs/qai2026/methodology_patch.tex` for the methodology text that clarifies
the HQNN saliency target and concentration metrics.
