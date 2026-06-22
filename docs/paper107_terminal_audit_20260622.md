# Paper 107 Terminal Audit

Date: 2026-06-22 23:07:28 +08:00

## Terminal Decision

STRONG_REVISE

## Why Not KILL_ARCHIVE

The expanded local benchmark clears every frozen local empirical gate. The proposed v5 audit beats the strongest non-oracle baseline by `0.07477` hard success and `0.10038` utility, improves rare-failure recall by `0.07345`, reduces contact-boundary error by `0.03297`, reduces unsafe commitment by `0.02315`, reduces overtrust by `0.02834`, beats all removed-component ablations on utility, survives maximum stress, and maintains useful strict fixed-risk coverage.

## Why Not ICLR Main Ready

The evidence is still local. The repo does not contain real-robot deployment, accepted high-fidelity simulator validation, trained learned policy checkpoints, external benchmark comparisons, deployment logs, or rollout videos. The correct action is to preserve the paper as a strong-revise candidate, not to represent it as submission-ready.

## Required Next Evidence

- Real robot or accepted high-fidelity simulator evaluation.
- Implemented learned baselines for scaled behavior cloning, robot foundation policies, conformal risk filtering, ensemble uncertainty, and v4/v5 audits.
- Qualitative rollouts showing rare contact, shortcut, embodiment shift, latency shift, and recovery-scarce exceptions.
- External benchmark split such as LIBERO, RLBench, Meta-World, BridgeData, Open X-Embodiment, DROID, or a comparable hardware manipulation suite.
- Manual related-work validation.
