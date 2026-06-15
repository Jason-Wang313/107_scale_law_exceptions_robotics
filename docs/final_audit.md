# Final Audit

1. Chosen thesis: robot scaling curves can improve average metrics while missing embodied failure boundaries in rare contact, shortcut, embodiment-shift, and recovery-scarce regimes.
2. ICLR-main decision: STRONG_REVISE.
3. Submission-hardening version: v4.
4. Evidence: 5 tasks x 7 scale-exception regimes x 5 splits x 9 methods, 7 seeds, 84 episodes/group.
5. Strongest non-oracle baseline: `conformal_risk_filter`.
6. Main result: proposed combined-exception success `0.550 +/- 0.005` vs strongest non-oracle `0.407 +/- 0.006`.
7. Diagnostic result: rare-failure recall `0.512` vs `0.375`; contact-boundary error `0.225` vs `0.283`.
8. Safety result: unsafe commitment `0.073` vs `0.086`; overtrust `0.069` vs `0.106`; intervention cost `0.217` vs `0.246`.
9. Ablation result: full model `0.554 +/- 0.006`; best removed component `minus_embodiment_shift_detector` at `0.503 +/- 0.007`.
10. Pairwise result: proposed beats the strongest non-oracle baseline in 7/7 seeds with `0.144 +/- 0.006` mean success difference.
11. Claim-validity status: mechanism supported locally; not submission-ready without external robot/high-fidelity validation.
12. Exact Downloads PDF path: `C:/Users/wangz/Downloads/107.pdf`.
13. GitHub URL: https://github.com/Jason-Wang313/107_scale_law_exceptions_robotics
14. Confirmation: no visible Desktop copy was requested or made.
