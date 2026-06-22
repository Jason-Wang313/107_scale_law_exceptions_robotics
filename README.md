# 107 Scale-Law Exceptions in Robotics

Submission-hardening version: v5 expanded

Terminal decision: STRONG_REVISE for an ICLR-main-target paper, not ready to submit.

This rebuild replaces the six-page v4.1 artifact with a 28-page, source-generated, ICLR-style audit of boundary-aware scale-law exceptions in robotics. The central claim is narrow: average robot-policy scaling can improve while rare embodied failure boundaries remain under-covered, so scaling claims should be audited with boundary-conditioned metrics rather than average success alone.

The v5 benchmark is CPU-only and RAM-light. It uses compact cell-level rows rather than per-episode logs to stay below GitHub file-size limits while expanding the evidence surface to 8 task families, 9 exception regimes, 8 splits, 16 methods, 10 seeds, 6 episodes per cell, 92,160 main cells, 43,200 stress cells, 46,080 fixed-risk cells, 7,200 ablation cells, and 24 failure cases.

## Main Result

The strongest non-oracle baseline is `proposed_embodied_scale_exception_audit_v4`.

Hard-aggregate v5 metrics:

- success: `0.66184` versus `0.58707` for v4
- utility: `0.75598` versus `0.65560`
- rare-failure recall: `0.65069` versus `0.57725`
- contact-boundary error: `0.18075` versus `0.21372`
- unsafe commitment: `0.03975` versus `0.06290`
- overtrust rate: `0.02679` versus `0.05513`
- boundary coverage: `0.63452` versus `0.54074`
- strict fixed-risk coverage: `0.68370`

All frozen local empirical gates pass: success, diagnostic, safety, pairwise, ablation, stress, and fixed-risk. The scope gate fails because there is no real robot study, accepted high-fidelity benchmark, external benchmark split, calibrated deployment log, trained checkpoint, or rollout video. That is why the honest terminal decision remains STRONG_REVISE rather than ICLR-main-ready.

## Reproduce Evidence

```powershell
python src\run_experiment.py
python scripts\generate_manuscript.py
```

Generated artifacts include:

- `results/summary.json`
- `results/cell_metrics.csv`
- `results/hard_aggregate_metrics.csv`
- `results/hard_pairwise_stats.csv`
- `results/ablation_metrics.csv`
- `results/stress_sweep.csv`
- `results/fixed_risk_metrics.csv`
- `results/failure_cases.csv`
- `figures/scale_exception_*_v5.png`
- `paper/main.tex`

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local numbered PDF: `C:/Users/wangz/Downloads/107.pdf`

Validated PDF SHA256: `C89FA6CF361AB036F12378316CDD850EA7742B20E4649D91CC02A92E1FF691CD`

## Validate

```powershell
python scripts\validate_submission_artifacts.py
```

The validator checks row counts, finite CSV values, local gates, scope-gate honesty, bright boxed citation settings, 25+ page count, hash equality between `paper/main.pdf` and `Downloads/107.pdf`, and absence of visible Desktop/root numbered PDFs.
