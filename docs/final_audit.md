# Final Audit

Paper: 107 scale_law_exceptions_robotics

Audit date: 2026-06-22 23:07:28 +08:00

Submission-hardening version: v5 expanded

Terminal decision: STRONG_REVISE

ICLR main ready: no

## Evidence Rebuilt

- Runner: `src/run_experiment.py`
- Manuscript generator: `scripts/generate_manuscript.py`
- Validator: `scripts/validate_submission_artifacts.py`
- Main rows: 92,160 cell rows.
- Stress rows: 43,200 cell rows.
- Fixed-risk rows: 46,080 cell rows.
- Ablation rows: 7,200 cell rows.
- Failure cases: 24.
- PDF: `C:/Users/wangz/Downloads/107.pdf`
- PDF pages: 28.
- PDF SHA256: `C89FA6CF361AB036F12378316CDD850EA7742B20E4649D91CC02A92E1FF691CD`

## Gate Result

All frozen local empirical gates pass. V5 beats the strongest non-oracle baseline `proposed_embodied_scale_exception_audit_v4` by `0.07477` hard success and `0.10038` utility, improves rare-failure recall by `0.07345`, reduces contact-boundary error by `0.03297`, reduces unsafe commitment by `0.02315`, reduces overtrust by `0.02834`, clears the ablation/stress/fixed-risk gates, and remains below the oracle.

## Scope Result

The scope gate fails. The repository does not contain a real robot study, accepted high-fidelity benchmark, external benchmark split, calibrated deployment log, trained checkpoint, or rollout video. Therefore the paper is not ICLR-main-ready despite strong local evidence.

## Visual PDF QA

Rendered pages 1, 2, 5, 15, and 28. Title/abstract were readable, bright boxed citations were visible, tables and figures were not clipped, appendices were legible, and bibliography links rendered normally. Temporary render files were removed.
