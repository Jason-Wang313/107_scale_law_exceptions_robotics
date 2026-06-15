# Hostile Reviewer Response

Paper: 107 Scale-Law Exceptions in Robotics

## Strongest Technical Threats

- Scaling-law papers already show predictable neural loss improvements under data/model/compute scaling.
- Compute-optimal scaling already shows that scale must be balanced, not merely increased.
- RT-1, RT-2, RT-X, Open X-Embodiment, DROID, and Octo already provide strong robot-foundation-model scaling evidence.
- Ensemble uncertainty and conformal risk filtering already catch some deployment tails.
- A reviewer may argue that "scale fails on tails" is too obvious unless the paper isolates an embodied mechanism.

## ICLR Main Response

The v4 rebuild narrows the claim to embodied scale exceptions: cases where average scaling metrics improve while rare-failure recall, contact-boundary error, unsafe commitment, overtrust, or recovery scarcity regress. The local benchmark supports that narrower boundary. Proposed combined-exception success is `0.550 +/- 0.005` versus `0.407 +/- 0.006` for `conformal_risk_filter`; rare-failure recall improves by `0.138`; contact-boundary error drops by `0.058`; unsafe commitment and overtrust both decrease; and the strongest-baseline paired comparison is 7/7 seeds in favor of the proposed method.

## Remaining Hostile Review

A hostile reviewer would still be right to reject a main-track submission today if it claimed deployment readiness. The evidence is local and synthetic; the baselines are diagnostic executable models rather than external robot systems; and there is no real robot or independently validated high-fidelity simulator result.

## Honest Action

The paper is marked `STRONG_REVISE`. Continue only if the next version adds real robot or high-fidelity external validation, implemented learned baselines, and qualitative rollouts.
