# ICLR Main Gate

Paper: 107 scale_law_exceptions_robotics

v5 expanded gate verdict: STRONG_REVISE

ICLR main ready: no

Evidence digest: source-generated 28-page paper with 8 tasks, 9 regimes, 8 splits, 16 methods, 10 seeds, 92,160 main cell rows, 43,200 stress rows, 46,080 fixed-risk rows, 7,200 ablation rows, 24 failure cases, visual PDF QA, and Downloads-only PDF validation.

Gate outcomes:

- success gate: pass, v5 beats the strongest non-oracle baseline by `0.07477` success and `0.10038` utility.
- diagnostic gate: pass, rare-failure recall improves by `0.07345` and contact-boundary error falls by `0.03297`.
- safety gate: pass, unsafe commitment, overtrust, and tail-risk rate fall; intervention cost rises only `0.00218`, within tolerance.
- pairwise gate: pass, paired hard-seed comparison clears the frozen utility-win threshold.
- ablation gate: pass, full v5 beats the best removed-component ablation by `0.10662` utility.
- stress gate: pass, maximum-stress utility margin is `0.10974`.
- fixed-risk gate: pass, strict fixed-risk coverage is `0.68370` with utility margin `0.12172`.
- scope gate: fail, no real robot or independent high-fidelity benchmark evidence.

The only honest main-conference-safe decision is STRONG_REVISE. The local mechanism is worth developing, but the paper is not submission-ready.
