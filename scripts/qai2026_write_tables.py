"""Write QAI 2026 LaTeX table snippets."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = ROOT / "paper_artifacts" / "qai2026" / "tables"


TABLES = {
    "table_experimental_setup.tex": r"""\begin{table}[t]
\centering
\caption{Datasets and model configurations used in the experiments.}
\label{tab:experimental-setup}
\begin{tabular}{lcccc}
\toprule
Setting & Task & Features & Qubits & Split \\
\midrule
VQC Iris & Binary & 4 & 4 & 70/15/15 \\
VQC Cleveland & Binary & 8 selected & 8 & 70/15/15 \\
HQNN Iris & 3-class & 4 & 4 & 80/20 \\
HQNN Cleveland & Binary & 8 selected & 8 & 80/20 \\
\bottomrule
\end{tabular}
\end{table}
""",
    "table_hyperparameters.tex": r"""\begin{table*}[t]
\centering
\caption{Main training and explanation hyperparameters.}
\label{tab:hyperparameters}
\begin{tabular}{lcccccccc}
\toprule
Setting & Layers & Encoding & Optimizer & LR & Batch & Epochs/Iters & Shots & Seeds \\
\midrule
VQC Iris & 2 & $R_Y$ re-uploading + CNOT ring & SPSA & 0.06 & 24 & 350 iters & exact; 1000 stability & 5 \\
VQC Cleveland & 2 & $R_X/R_Y$ re-uploading + CZ ladder & SPSA & 0.10 & 32 & 200 iters & exact; 10 stability & 5 \\
HQNN Iris & 2 trainable blocks & plain/richer $R_Y/R_Z$ & Adam & 0.01 & 8 & 25 epochs & statevector & fixed seed \\
HQNN Cleveland & 2 trainable blocks & plain/richer $R_Y/R_Z$ & Adam & 0.01 & 8 & 20 epochs & statevector & 5 stability \\
\bottomrule
\end{tabular}
\end{table*}
""",
    "table_results_summary.tex": r"""\begin{table}[t]
\centering
\caption{Summary of predictive and explanation metrics.}
\label{tab:results-summary}
\begin{tabular}{lccc}
\toprule
Model & Accuracy & Key stability & Explanation note \\
\midrule
VQC Iris & 0.9375 & $\rho=[1,1,1,0.8]$ & petal width dominant \\
VQC Cleveland & 0.7826 & $\rho=0.381$--$0.595$ & AUDC $=0.428$ \\
HQNN Cleveland plain & 0.8197 & $\rho=0.554$ & sensitivity $=21.21$ \\
HQNN Cleveland richer & 0.8361 & $\rho=0.613$ & sensitivity $=44.39$ \\
\bottomrule
\end{tabular}
\end{table}
""",
}


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    for name, content in TABLES.items():
        path = TABLE_DIR / name
        path.write_text(content + "\n", encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
