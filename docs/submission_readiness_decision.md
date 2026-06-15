# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

The v4 rebuild provides a paper-specific local benchmark for scale-law exceptions in robotics, with strong synthetic baselines, ablations, paired seed comparisons, stress sweeps, failure cases, finite CSV artifacts, and generated figures/tables. The evidence supports the mechanism: on combined exception stress, `proposed_embodied_scale_exception_audit` reaches `0.550 +/- 0.005` success versus `0.407 +/- 0.006` for the strongest non-oracle baseline, `conformal_risk_filter`.

Diagnostic evidence also supports the mechanism. Rare-failure recall improves from `0.375` to `0.512`; contact-boundary error falls from `0.283` to `0.225`; unsafe commitment falls from `0.086` to `0.073`; overtrust falls from `0.106` to `0.069`; and paired seed comparisons favor the proposed method over the strongest baseline in 7/7 seeds.

The honest terminal action is strong-revise, not submit. A submission-quality revival still requires real robot or independent high-fidelity simulator validation, implemented learned baselines, and external benchmark evidence.
