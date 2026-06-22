# Hostile Reviewer Response

Paper: 107 Scale-Law Exceptions in Robotics

## Strongest Technical Threats

- Scaling-law and robot-foundation-model work already shows broad gains from more data, parameters, and compute.
- RT-1, RT-2, RT-X, Octo, DROID, and related systems already provide strong robot scaling evidence.
- Ensemble uncertainty, conformal prediction, retrieval of failures, invariance penalties, and CVaR risk sensitivity already address parts of the tail-risk problem.
- A reviewer may argue that the benchmark generator favors the proposed boundary-aware audit.
- A reviewer may reject the paper because it has no real robot/high-fidelity validation.

## v5 Response

The v5 rebuild narrows the claim to boundary-conditioned scale exceptions, not generic scaling failure. The benchmark includes 16 methods and makes the strongest non-oracle comparator the previous v4 audit, not a weak straw baseline. V5 improves hard success from `0.58707` to `0.66184`, utility from `0.65560` to `0.75598`, rare-failure recall from `0.57725` to `0.65069`, contact-boundary error from `0.21372` to `0.18075`, unsafe commitment from `0.06290` to `0.03975`, overtrust from `0.05513` to `0.02679`, and strict fixed-risk coverage to `0.68370`.

## Remaining Hostile Review

A hostile reviewer would still be right to reject a main-track submission today if it claims deployment readiness. The evidence is local; the baselines are diagnostic executable models rather than external trained robot systems; and no real robot, accepted high-fidelity simulator, external benchmark, deployment logs, checkpoint, or rollout video is present.

## Honest Action

Mark the paper `STRONG_REVISE`. Continue only if the next version adds external robot/high-fidelity validation, trained baselines, qualitative rollouts, and manual related-work validation.
