# Submission Version Log

## v1 - Generated Draft

- Original continuation-batch generated paper and toy single-seed experiment.

## v2 - Submission Hardening

- Added hostile reviewer attack log and response docs.
- Added multi-seed synthetic diagnostics.
- Terminal decision: WORKSHOP_ONLY.

## v3 - ICLR Main Gate Archive

- Applied stricter ICLR-main-conference standard.
- Determined that missing real-robot/high-fidelity evidence, template-generated experiments, and unresolved novelty threats were not recoverable from local artifacts.
- Terminal decision: KILL_ARCHIVE.

## v4 - Paper-Specific Evidence Rebuild

- Replaced the shared template script with a scale-exception robotics benchmark.
- Added 5 tasks, 7 exception regimes, 5 splits, 9 methods, 7 seeds, and 84 episodes/group.
- Added success, rare-failure recall, contact-boundary error, tail risk, unsafe commitment, overtrust, calibration ECE, recovery success, intervention cost, data-efficiency proxy, regret, paired tests, ablations, stress sweeps, failure cases, figures, and LaTeX tables.
- Rewrote docs and manuscript around the actual evidence.
- Terminal decision: STRONG_REVISE.

## v4.1 - Continuation Submission Audit

- Added `docs/paper107_iclr_submission_execution_plan_20260615.md`.
- Reran `src/run_experiment.py` from source with the full benchmark and logged the run at `logs/107_scale_law_exceptions_robotics_continuation_rerun_20260615.log`.
- Verified expected CSV coverage and finite numeric outputs.
- Reconfirmed the strongest non-oracle baseline as `conformal_risk_filter`.
- Preserved the narrow claim that scaling can miss embodied failure boundaries, not that scaling is useless.
- Added terminal audit docs and rebuilt the numbered Downloads PDF.
- Terminal decision: STRONG_REVISE; ICLR main ready: no.
