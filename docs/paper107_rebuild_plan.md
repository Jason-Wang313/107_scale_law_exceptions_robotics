# Paper 107 Rebuild Plan: Scale-Law Exceptions in Robotics

Started: 2026-06-15 00:49:00 +0100

## Goal

Rebuild Paper 107 from a v3 archive into an honest ICLR-main-target evidence package if, and only if, the evidence supports it. The falsifiable claim is not that scaling laws are useless. The claim is narrower: embodied robot policies can show average loss/success scaling while still crossing the wrong failure boundary in contact-rich, partially observed, rare-tail, or recovery-critical regimes.

## Claimed Mechanism

The proposed method, `proposed_embodied_scale_exception_audit`, detects scale-law exceptions by separating:

- average imitation or prediction improvement;
- rare physical failure recall;
- contact-boundary error;
- out-of-distribution embodiment shift;
- intervention and overtrust cost;
- calibration error under rare tails;
- recoverability after a bad scaled-policy commitment.

It should identify when larger data/model settings improve global metrics but increase or hide safety-critical embodied failures.

## Benchmark To Build

Create a RAM-light executable benchmark with aggregate metrics rather than full trajectory storage. The benchmark will cover:

- 5 robot task families: contact insertion, deformable handling, mobile manipulation, bimanual handoff, and tool-use sequence.
- 7 scale-exception regimes: rare contact tail, occluded precondition, embodiment mismatch, long-horizon compounding, spurious visual shortcut, recovery-scarce failure, and mixed exception stress.
- 5 evaluation splits: nominal scaling, contact-tail shift, embodiment shift, shortcut shift, and combined exception stress.
- 9 methods: small behavior clone, large behavior clone, data-only scaling, model-only scaling, generic scaling-law extrapolator, ensemble uncertainty gate, conformal risk filter, proposed embodied scale-exception audit, and oracle exception selector.
- 7 random seeds with independent task/regime groups.
- 84 episodes per task/regime/split/method group.

## Evidence Requirements

The rebuild must produce:

- Task success, rare-failure recall, contact-boundary error, tail-risk rate, unsafe commitment, overtrust rate, calibration ECE, recovery success, intervention cost, data-efficiency proxy, and regret to oracle.
- Per-task/per-regime breakdowns.
- Pairwise seed-level tests against the strongest non-oracle baseline.
- Stress sweep over exception intensity.
- Ablations for rare-tail memory, contact-boundary factor, embodiment-shift detector, shortcut audit, and recoverability calibration.
- Failure cases showing where scaling works normally, where uncertainty alone is enough, and where the proposed audit is too conservative.
- Figures and LaTeX tables generated from CSVs.

## Terminal Gate

Mark `STRONG_REVISE` only if the proposed method:

- Beats the strongest non-oracle closed-loop baseline on combined exception stress by at least 0.030 success.
- Improves rare-failure recall by at least 0.050 or reduces contact-boundary error by at least 0.050.
- Does not buy success by increasing unsafe commitments, overtrust, or intervention cost beyond the configured tolerance.
- Wins paired seed comparisons against the strongest non-oracle baseline in at least 5/7 seeds.
- Survives core ablations: removing rare-tail memory, contact-boundary factor, embodiment-shift detector, shortcut audit, or recoverability calibration must not match the full method.
- States clearly that real robot/external benchmark validation is still missing.

Otherwise mark `KILL_ARCHIVE` with evidence.

## Execution Steps

1. Replace the shared v3 probability script with a paper-specific scale-exception robotics benchmark.
2. Generate metrics, seed metrics, per-task/per-regime tables, pairwise tests, stress sweep, ablations, failure cases, figures, and LaTeX tables.
3. Update repository docs to reflect the actual terminal gate.
4. Rewrite `paper/main.tex` as either a strong-revise evidence report or a negative archive report.
5. Compile and copy only `107.pdf` to `C:/Users/wangz/Downloads/107.pdf`.
6. Verify finite CSVs, py_compile, LaTeX log, PDF hash, no Desktop PDF, clean child repo, public GitHub push, and root report consistency.

## RAM Discipline

Use vectorized or aggregate group simulation and write summary tables directly. Keep all seeds, tasks, regimes, methods, stress levels, ablations, and failure cases; do not reduce experimental coverage to save memory.
