# Submission Readiness Audit v5

Paper: 107 `scale_law_exceptions_robotics`

Audit date: 2026-06-22 23:07:28 +08:00

Decision: STRONG_REVISE

ICLR main ready: no

## Regenerated Evidence

- Runner: `src/run_experiment.py`
- Benchmark coverage: 8 tasks x 9 regimes x 8 splits x 16 methods.
- Repeats: 10 seeds, 6 episodes per cell.
- Main cell rows: 92,160.
- Stress cell rows: 43,200.
- Fixed-risk cell rows: 46,080.
- Ablation cell rows: 7,200.
- Failure cases: 24.
- Strongest non-oracle baseline: `proposed_embodied_scale_exception_audit_v4`.
- Terminal decision emitted by runner: STRONG_REVISE.

## Main Result

V5 reaches hard success `0.66184` versus `0.58707` for the strongest non-oracle baseline and utility `0.75598` versus `0.65560`. Rare-failure recall improves from `0.57725` to `0.65069`; contact-boundary error falls from `0.21372` to `0.18075`; unsafe commitment falls from `0.06290` to `0.03975`; overtrust falls from `0.05513` to `0.02679`; and boundary coverage improves from `0.54074` to `0.63452`.

## Pairwise, Ablation, Stress, and Fixed-Risk

- Pairwise gate: pass.
- Ablation utility margin over the best removed component: `0.10662`.
- Maximum-stress utility margin: `0.10974`.
- Strict fixed-risk coverage: `0.68370`.
- Strict fixed-risk utility margin: `0.12172`.

## Artifact Audit

- `paper/main.pdf`: 28 pages.
- Downloads PDF: `C:/Users/wangz/Downloads/107.pdf`.
- SHA256: `C89FA6CF361AB036F12378316CDD850EA7742B20E4649D91CC02A92E1FF691CD`.
- Validator passed.
- Visual PDF QA passed.
- No visible Desktop numbered PDF.
- No factory-root or child-root numbered PDF.

## Honest Submission Decision

The local evidence supports the mechanism and justifies continued development, but it does not make the paper ICLR-main-ready. A real submission needs external robot or high-fidelity validation, trained baselines, deployment logs, checkpoints, rollout videos, and manual related-work validation.
