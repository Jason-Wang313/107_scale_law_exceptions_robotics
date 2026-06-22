# Reproducibility Checklist

## What Reproduces

- [x] `python -m py_compile src\run_experiment.py`
- [x] `python src\run_experiment.py`
- [x] `python -m py_compile scripts\generate_manuscript.py scripts\validate_submission_artifacts.py`
- [x] `python scripts\generate_manuscript.py`
- [x] `results/summary.json`
- [x] `results/cell_metrics.csv`
- [x] `results/main_group_metrics.csv`
- [x] `results/seed_metrics.csv`
- [x] `results/hard_aggregate_metrics.csv`
- [x] `results/hard_pairwise_stats.csv`
- [x] `results/ablation_metrics.csv`
- [x] `results/stress_sweep.csv`
- [x] `results/fixed_risk_metrics.csv`
- [x] `results/failure_cases.csv`
- [x] `figures/scale_exception_hard_utility.png`
- [x] `figures/scale_exception_diagnostics_v5.png`
- [x] `figures/scale_exception_ablation_v5.png`
- [x] `figures/scale_exception_stress_sweep_v5.png`
- [x] `figures/scale_exception_fixed_risk_v5.png`
- [x] `figures/scale_exception_gap_v5.png`
- [x] `paper/main.tex`
- [x] `paper/main.pdf`
- [x] Canonical PDF: `C:/Users/wangz/Downloads/107.pdf`
- [x] `python scripts\validate_submission_artifacts.py`

## What Does Not Yet Reproduce

- [ ] Real robot results.
- [ ] Independent high-fidelity benchmark runs.
- [ ] Trained learned policy checkpoints.
- [ ] External robot-system baselines.
- [ ] Deployment logs or rollout videos.

This is reproducible as a local expanded STRONG_REVISE evidence package, not as a final ICLR-main empirical robotics submission.
