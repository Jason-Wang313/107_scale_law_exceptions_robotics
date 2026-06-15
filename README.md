# 107 Scale-Law Exceptions in Robotics

Submission-hardening version: v4.1

Terminal decision: STRONG_REVISE for an ICLR-main-target paper, not ready-to-submit.

This rebuild replaces the v3 archive with a paper-specific scale-exception robotics benchmark. The 2026-06-15 continuation audit reran the full benchmark from source and preserved the terminal decision. The central claim is narrow: scaling data or model size can improve average behavior-cloning or prediction metrics while still missing embodied failure boundaries in rare contact tails, occluded preconditions, embodiment mismatch, long-horizon compounding, spurious visual shortcuts, and recovery-scarce failures.

The local evidence supports the mechanism. On combined exception stress, `proposed_embodied_scale_exception_audit` reaches `0.550 +/- 0.005` success versus `0.407 +/- 0.006` for the strongest non-oracle baseline, `conformal_risk_filter`. Rare-failure recall improves from `0.375` to `0.512`; contact-boundary error falls from `0.283` to `0.225`; unsafe commitment falls from `0.086` to `0.073`; overtrust falls from `0.106` to `0.069`; intervention cost falls from `0.246` to `0.217`; and paired seed comparisons favor the proposed method in 7/7 seeds.

At maximum stress level `0.95`, proposed success is `0.539 +/- 0.007` versus `0.389 +/- 0.009` for conformal risk filtering, with higher rare-failure recall and lower contact-boundary error, unsafe commitment, and overtrust.

The honest limitation is still material: this is a local executable diagnostic benchmark, not real robot or independently validated high-fidelity simulator evidence. The paper should be revised with external robot validation before main-track submission.

## Reproduce Evidence

```powershell
python src\run_experiment.py
```

Generated artifacts:

- `results/metrics.csv`
- `results/pairwise_stats.csv`
- `results/ablation_metrics.csv`
- `results/stress_sweep.csv`
- `results/failure_cases.csv`
- `figures/scale_exception_*.png`
- `paper/main.tex`

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/107.pdf`
