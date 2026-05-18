"""Write QAI 2026 LaTeX table snippets."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = ROOT / "paper_artifacts" / "qai2026" / "tables"


TABLES = {
    "table_experimental_setup.tex": r"""\begin{table}[!t]
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
    "table_hyperparameters.tex": r"""\begin{table*}[!t]
\centering
\caption{Main model and training hyperparameters.}
\label{tab:hyperparameters}
\scriptsize
\begin{tabular}{@{}lccp{3.0cm}p{1.8cm}cccc@{}}
\toprule
Setting & Qubits & Trainable quantum params & Encoding/entanglement & Head/loss & Optimizer & LR & Batch & Budget \\
\midrule
VQC Iris & 4 & 16 & $R_Y$ re-uploading + CNOT ring & Pauli-$Z$/BCE & SPSA & 0.06 & 24 & 350 iters \\
VQC Cleveland & 8 & 32 & $R_X/R_Y$ re-uploading + CZ ladder & Pauli-$Z$/BCE & SPSA & 0.10 & 32 & 200 iters \\
HQNN Iris & 4 & 8 & $R_Y$ or $R_Y/R_Z$ + CX ladder & MLP/Cross-entropy & Adam & 0.01 & 8 & 25 epochs \\
HQNN Cleveland & 8 & 16 & $R_Y$ or $R_Y/R_Z$ + CX ladder & MLP/BCE-logits & Adam & 0.01 & 8 & 20 epochs \\
\bottomrule
\end{tabular}
\end{table*}
""",
    "table_explanation_hyperparameters.tex": r"""\begin{table*}[!t]
\centering
\caption{Explanation and robustness hyperparameters used for the reported diagnostics.}
\label{tab:explanation-hyperparameters}
\scriptsize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}lp{2.2cm}p{2.2cm}p{2.7cm}p{1.8cm}c@{}}
\toprule
Setting & Saliency target & IG / baseline & Stochastic diagnostics & Deletion baseline & Seeds \\
\midrule
VQC Iris & expectation score $z$ & 25 / mean encoded input & SmoothGrad $K=30,\sigma=0.1$; noise $K=50,\sigma=0.1$ & mean encoded input & 5 \\
VQC Cleveland & expectation score $z$ & 25 / mean encoded input & SmoothGrad $K=30,\sigma=0.1$; noise $K=50,\sigma=0.1$ & mean encoded input & 5 \\
HQNN Iris & class logit/probability & local gradients & input-gradient noise tests; $\delta=10^{-3}$ sensitivity & zero input & fixed \\
HQNN Cleveland & binary logit/probability & 50 / zero input & SmoothGrad $K=30,\sigma=0.1$; noise $K=50,\sigma=0.1$ & zero input & 5 \\
\bottomrule
\end{tabular}
\end{table*}
""",
    "table_results_summary.tex": r"""\begin{table*}[!t]
\centering
\caption{Summary of predictive and explanation metrics.}
\label{tab:results-summary}
\scriptsize
\setlength{\tabcolsep}{5pt}
\begin{tabular}{@{}lcp{3.0cm}p{6.0cm}@{}}
\toprule
Model & Accuracy & Key stability & Explanation note \\
\midrule
VQC Iris & 0.9375 & $\rho=[1,1,1,0.8]$ & petal width dominant \\
VQC Cleveland & 0.7826 & $\rho=0.381$--$0.595$ & AUDC $=0.428$ \\
HQNN Cleveland plain & 0.8197 & $\rho=0.554$ & sensitivity $=21.21$ \\
HQNN Cleveland richer & 0.8361 & $\rho=0.613$ & sensitivity $=44.39$ \\
\bottomrule
\end{tabular}
\end{table*}
""",
}


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    for name, content in TABLES.items():
        path = TABLE_DIR / name
        path.write_text(content.rstrip() + "\n", encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
