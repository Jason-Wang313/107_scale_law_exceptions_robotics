# Claims

- Mechanism claim: average robot-policy scaling can improve while rare embodied boundary risk remains under-covered.
- Evidence claim: the v5 local benchmark evaluates 8 task families, 9 exception regimes, 8 splits, 16 methods, 10 seeds, stress sweeps, fixed-risk budgets, ablations, and failure cases.
- Method claim: `boundary_aware_scale_exception_audit_v5` improves hard success, utility, rare-failure recall, contact-boundary error, unsafe commitment, overtrust, and boundary coverage relative to the strongest non-oracle baseline `proposed_embodied_scale_exception_audit_v4`.
- Theory claim: average scaling gain is not sufficient to identify boundary-conditioned risk without measuring boundary coverage and scale-exception gap.
- Scope claim: results support a local mechanism audit only, not real-robot deployment readiness.
- Unsupported claim explicitly avoided: no claim of ICLR-main readiness, hardware state of the art, or superiority over trained robot foundation models on external benchmarks.
