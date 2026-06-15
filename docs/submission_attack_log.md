# Submission Attack Log

Paper: 107 scale_law_exceptions_robotics

This v4 pass rebuilds the paper around a stronger local evidence package. The result is STRONG_REVISE, not main-track submission.

## Attack 1: Scaling laws already explain average improvement.

Verdict: True but not fatal locally.

Action: The paper narrows the claim to embodied exception metrics, not average loss scaling.

## Attack 2: Conformal and uncertainty gates already catch tails.

Verdict: Strong threat, addressed locally.

Action: `conformal_risk_filter` is the strongest non-oracle baseline. Proposed combined-exception success is `0.550 +/- 0.005` versus `0.407 +/- 0.006`, with lower unsafe commitment and overtrust.

## Attack 3: The method may just be more conservative.

Verdict: Addressed locally.

Action: Intervention cost decreases from `0.246` for the strongest baseline to `0.217` for the proposed method, while success increases.

## Attack 4: The method may trade success for rare-tail recall.

Verdict: Addressed locally.

Action: Both success and rare-failure recall improve. Rare-failure recall rises from `0.375` to `0.512`.

## Attack 5: Contact-boundary errors may be unchanged.

Verdict: Addressed locally.

Action: Contact-boundary error falls from `0.283` to `0.225`.

## Attack 6: Ablations may not support the mechanism.

Verdict: Passed locally.

Action: The full model reaches `0.554 +/- 0.006`; the best removed component, `minus_embodiment_shift_detector`, reaches `0.503 +/- 0.007`.

## Attack 7: The benchmark might be saturated.

Verdict: Not saturated.

Action: Oracle success remains higher at `0.710 +/- 0.010`, leaving a meaningful ceiling gap.

## Attack 8: No real robot or external simulator validates the result.

Verdict: Fatal for immediate submission.

Action: Mark STRONG_REVISE, not ready-to-submit. Require external validation before main-track submission.

## Terminal Condition

The paper earns continued development because the local gates pass, but it does not earn ICLR-main readiness. Terminal state for this pass: STRONG_REVISE.
