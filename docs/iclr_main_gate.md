# ICLR Main Gate

Paper: 107 scale_law_exceptions_robotics

Previous v3 decision: KILL_ARCHIVE

v4.1 continuation gate verdict: STRONG_REVISE

Evidence digest: scale-exception robotics benchmark with 5 tasks, 7 regimes, 5 splits, 9 methods, 7 seeds, 84 episodes/group.

Gate outcomes:

- success gate: pass, proposed beats strongest non-oracle by `0.144` success.
- diagnostic gate: pass, rare-failure recall improves by `0.138` and contact-boundary error falls by `0.058`.
- safety gate: pass, unsafe commitment, overtrust, and intervention cost fall relative to strongest non-oracle.
- pairwise gate: pass, proposed wins 7/7 paired seeds against strongest non-oracle.
- ablation gate: pass, full model beats the best removed component by `0.051`.
- stress gate: pass locally, at maximum stress level `0.95` proposed success is `0.539 +/- 0.007` versus `0.389 +/- 0.009`.
- external-validation gate: fail, no real robot or independent high-fidelity benchmark.

The only honest main-conference-safe decision is STRONG_REVISE: the mechanism is worth developing, but the paper is not yet submission-ready.
