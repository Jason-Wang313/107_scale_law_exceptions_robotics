# Paper 107 Expanded-Submission Plan

Paper: `107_scale_law_exceptions_robotics`

Timestamp: 2026-06-22 22:21:29 +08:00

Target venue posture: ICLR-main-target, hostile-review standard.

Terminal honesty rule: do not optimize for pretty results. Optimize for results that survive hostile review. Freeze the protocol before interpreting the final numbers; report all predefined outcomes honestly. Mark ICLR-main ready only if the artifact contains real robot, accepted high-fidelity benchmark, external benchmark, calibrated deployment logs, trained-checkpoint, or rollout-video evidence. Otherwise mark `STRONG_REVISE` or `KILL_ARCHIVE`.

## Current Weakness

The v4.1 artifact is only 6 pages and uses a local synthetic diagnostic benchmark. It supports a narrow mechanism claim, but it is not a real submission because it lacks external robot evidence, trained policy checkpoints, deployment logs, high-fidelity simulation, and a full theory/related-work/error-analysis treatment.

## Scope Expansion

- Expand from the v4.1 suite to a heavier CPU-only benchmark with additional task families, exception regimes, scale regimes, methods, seeds, stress levels, fixed-risk budgets, ablations, and negative cases.
- Keep memory light by streaming raw rollout rows to CSV and aggregating seed-level summaries incrementally.
- Preserve the central claim: scaling can improve average metrics while leaving embodied failure-boundary risk non-identifiable or worse.
- Add a theory section proving why average scaling trends do not identify rare-contact, embodiment-shift, shortcut, or recoverability tails without boundary coverage.
- Include failure modes, falsification criteria, and decision gates before seeing final v5 results.

## Frozen Empirical Protocol

- Tasks: contact insertion, deformable handling, mobile manipulation, bimanual handoff, tool-use sequence, shelf retrieval, articulated-object opening, cable routing.
- Regimes: rare contact tail, occluded precondition, embodiment mismatch, long-horizon compounding, spurious visual shortcut, recovery-scarce failure, distribution-mixture aliasing, actuator-latency shift, mixed exception stress.
- Splits: nominal scaling, contact-tail shift, embodiment shift, shortcut shift, recovery scarcity, cross-robot morphology, held-out exception composition, combined exception stress.
- Methods: small/medium/large behavior cloning, data-only scaling, model-only scaling, compute-balanced scaling, generic scaling-law extrapolator, ensemble uncertainty gate, conformal risk filter, dropout risk filter, retrieval-augmented nearest-failure, invariance penalty, risk-sensitive CVaR policy, v4 proposed audit, v5 boundary-aware scale-exception audit, and oracle exception selector.
- Seeds: 10.
- Episodes per cell: 6, with enough cells to exceed the v4 evidence surface while keeping RAM usage low.
- Ablations: remove rare-tail memory, contact-boundary factor, embodiment-shift detector, shortcut audit, recoverability calibration, scale-slope residual, counterfactual coverage score, and boundary mixture model.
- Stress sweep: 10 exception-intensity levels.
- Fixed-risk budgets: 0.08, 0.12, 0.16, 0.20.
- Negative/falsification cases: include regimes where scaling should not help, where uncertainty gating should match the audit, and where the proposed method should abstain or lose to the oracle.

## Frozen Metrics

- Primary: success, rare-failure recall, contact-boundary error, unsafe commitment, overtrust rate, recovery success, tail-risk rate, calibration ECE, intervention cost, regret to oracle, and utility.
- Scaling diagnostics: average-scaling gain, boundary-risk slope, scale-exception gap, boundary coverage, shortcut reliance, morphology transfer gap, and recoverability deficit.
- Statistical checks: paired seed differences against the strongest non-oracle baseline, bootstrap-style CI over seeds, ablation margins, stress monotonicity, and fixed-risk coverage.

## Predefined Gates

- Local success gate: v5 beats the strongest non-oracle baseline by at least 0.03 success or 0.05 utility under combined exception stress.
- Diagnostic gate: v5 improves rare-failure recall by at least 0.05 or reduces contact-boundary error by at least 0.04.
- Safety gate: v5 does not increase unsafe commitment, overtrust, intervention cost, or tail-risk rate beyond predefined tolerances.
- Pairwise gate: v5 wins at least 8/10 paired seeds on success or utility against the strongest non-oracle baseline.
- Ablation gate: the full v5 method beats every removed-component variant on success or utility.
- Stress gate: v5 remains above the strongest non-oracle baseline at the highest stress level.
- Fixed-risk gate: v5 maintains useful coverage at the strictest feasible risk budget and beats the strongest non-oracle baseline on utility.
- Scope gate: fail unless real robot, accepted high-fidelity benchmark, external benchmark, calibrated deployment logs, trained checkpoint, or rollout-video evidence is present.

## Manuscript Expansion

- Generate a 25+ page ICLR-style manuscript from results, not hand padding.
- Add bright boxed clickable citation links with `hyperref` color boxes.
- Add sections for theory, benchmark design, baselines, metrics, results, stress tests, ablations, fixed-risk deployment, falsification cases, related-work pressure, reproducibility, limitations, and appendices.
- Keep all claims tied to generated evidence. If the scope gate fails, explicitly state that the paper remains `STRONG_REVISE` and is not ICLR-main-ready.

## Artifact Rules

- Canonical numbered PDF: `C:/Users/wangz/Downloads/107.pdf`.
- Do not copy PDFs to the visible Desktop.
- Do not leave `C:/Users/wangz/robotics_massive_pool_paper_factory/107.pdf`.
- Validate CSV finite values, PDF page count, citation/link settings, artifact placement, and stale documentation before commit.
- Render representative PDF pages to `tmp/pdfs/` for visual QA and delete temporary renders before final commit.
