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
- Terminal decision: STRONG_REVISE.

## v4.1 - Continuation Submission Audit

- Reran the v4 benchmark from source and rebuilt the numbered Downloads PDF.
- Preserved STRONG_REVISE with ICLR main ready: no.

## v5 - Expanded Submission Rebuild

- Added `docs/paper107_expanded_submission_plan_20260622.md`.
- Replaced the v4.1 runner with a CPU-only/RAM-light expanded benchmark.
- Added 8 tasks, 9 regimes, 8 splits, 16 methods, 10 seeds, 92,160 main cell rows, 43,200 stress cell rows, 46,080 fixed-risk cell rows, 7,200 ablation rows, and 24 failure cases.
- Added `scripts/generate_manuscript.py` and `scripts/validate_submission_artifacts.py`.
- Generated a 28-page ICLR-style manuscript with bright boxed clickable citations and full bibliography pressure set.
- Validated `C:/Users/wangz/Downloads/107.pdf` only, SHA256 `C89FA6CF361AB036F12378316CDD850EA7742B20E4649D91CC02A92E1FF691CD`.
- Visual-PDF QA passed on representative pages.
- Terminal decision: STRONG_REVISE; ICLR main ready: no.
