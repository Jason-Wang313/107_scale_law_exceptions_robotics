# Submission Readiness Decision

Paper: 107 scale_law_exceptions_robotics

Decision date: 2026-06-22 23:07:28 +08:00

Decision: STRONG_REVISE

ICLR main ready: no

## Why It Is Stronger Than v4.1

The paper now has a 28-page generated manuscript, explicit theory, bright boxed clickable citations, stronger baselines, expanded tasks/regimes/splits, 10 seeds, paired tests, ablations, stress sweeps, fixed-risk budgets, failure cases, validation scripts, Downloads-only numbered PDF validation, and visual PDF QA.

## Why It Is Still Not Ready

The scope gate fails. No real robot study, accepted high-fidelity benchmark, external benchmark split, calibrated deployment log, trained checkpoint, or rollout video exists. The local evidence is useful for development, but it is not enough for a final ICLR-main robotics submission.

## Required Upgrade

Add external validation with trained robot policies, preserve the same gates, report failures honestly, and include qualitative rollouts. If the external result preserves the v5 pattern, the paper can move toward submission. If it does not, the method should be downgraded or archived.
