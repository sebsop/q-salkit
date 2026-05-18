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
- adjustable summary figures from the JSON artifact
- temporary PNG previews extracted from embedded notebook outputs
- LaTeX table snippets for Overleaf

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
