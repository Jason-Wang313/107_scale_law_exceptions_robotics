# Submission Readiness Audit v4.1

Paper: 107 `scale_law_exceptions_robotics`

Audit date: 2026-06-15 17:17:13 +0100

Decision: STRONG_REVISE

ICLR main ready: no

## Regenerated Evidence

- Runner: `src/run_experiment.py`
- Rerun log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/107_scale_law_exceptions_robotics_continuation_rerun_20260615.log`
- Benchmark coverage: 5 tasks x 7 scale-exception regimes x 5 splits x 9 methods.
- Repeats: 7 seeds, 84 episodes per task/regime/split/method group.
- Strongest non-oracle baseline: `conformal_risk_filter`.
- Terminal decision emitted by runner: `STRONG_REVISE`.

## CSV Integrity

- `metrics.csv`: 45 rows, finite numeric fields.
- `per_task_regime_metrics.csv`: 1575 rows, finite numeric fields.
- `seed_task_regime_metrics.csv`: 11025 rows, finite numeric fields.
- `seed_split_metrics.csv`: 315 rows, finite numeric fields.
- `pairwise_stats.csv`: 8 rows, finite numeric fields.
- `ablation_metrics.csv`: 7 rows, finite numeric fields.
- `ablation_seed_metrics.csv`: 49 rows, finite numeric fields.
- `ablation_task_regime_seed_metrics.csv`: 1715 rows, finite numeric fields.
- `stress_sweep.csv`: 30 rows, finite numeric fields.
- `stress_sweep_seed_metrics.csv`: 7350 rows, finite numeric fields.
- `failure_cases.csv`: 8 rows, finite numeric fields.

## Main Result

On combined-exception stress, proposed embodied scale-exception auditing reaches `0.550 +/- 0.005` success versus `0.407 +/- 0.006` for `conformal_risk_filter`, a margin of `+0.144 +/- 0.006`. Proposed also improves rare-failure recall from `0.375` to `0.512`, reduces contact-boundary error from `0.283` to `0.225`, reduces unsafe commitment from `0.086` to `0.073`, reduces overtrust from `0.106` to `0.069`, and reduces intervention cost from `0.246` to `0.217`.

## Pairwise And Ablations

- Pairwise seed test against the strongest non-oracle baseline: `7/7` wins.
- Full ablation success: `0.554 +/- 0.006`.
- Best removed component: `minus_embodiment_shift_detector` at `0.503 +/- 0.007`.
- Ablation margin over best removed component: `+0.051`.

## Stress Sweep

Stress levels: `0.10`, `0.27`, `0.44`, `0.61`, `0.78`, `0.95`.

At maximum stress level `0.95`, proposed success is `0.539 +/- 0.007` versus `0.389 +/- 0.009` for the strongest non-oracle baseline and `0.699 +/- 0.006` for the oracle. Proposed also keeps higher rare-failure recall (`0.505` vs `0.355`), lower contact-boundary error (`0.224` vs `0.291`), lower tail risk (`0.135` vs `0.179`), lower unsafe commitment (`0.071` vs `0.092`), and lower overtrust (`0.072` vs `0.111`) than the strongest non-oracle baseline.

## Honest Submission Decision

The local evidence supports the mechanism and justifies continuing the project, but it does not make the paper ICLR-main-ready. A real submission needs real robot or independent high-fidelity simulator validation, external learned baselines, qualitative rollouts, and a stronger prior-work positioning section grounded in those external results.
