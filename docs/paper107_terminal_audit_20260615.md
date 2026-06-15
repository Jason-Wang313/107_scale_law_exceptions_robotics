# Paper 107 Terminal Audit

Date: 2026-06-15 17:17:13 +0100

## Terminal Decision

STRONG_REVISE

## Why Not KILL_ARCHIVE

The regenerated full local benchmark clears the predefined mechanism gates. The proposed method beats the strongest non-oracle baseline on combined-exception success by `+0.144 +/- 0.006`, wins `7/7` paired seeds, improves rare-failure recall by `+0.138`, reduces contact-boundary error by `-0.058`, reduces unsafe commitment by `-0.013`, reduces overtrust by `-0.037`, and lowers intervention cost by `-0.029`. Core ablations remain below the full model.

## Necessary Caveat

The claim must stay narrow. The evidence does not show that scaling laws are useless; it shows that local embodied failure boundaries can be missed by average scaling metrics and by generic conformal/uncertainty gates.

## Why Not ICLR Main Ready

The evidence is still local and synthetic. The repo does not contain real-robot deployment, independent high-fidelity simulator validation, learned policy checkpoints, training curves, external benchmark comparisons, or rollout videos. The correct action is to preserve the paper as a strong-revise candidate, not to represent it as submission-ready.

## Required Next Evidence

- Real robot or independent high-fidelity simulator evaluation.
- Implemented learned baselines for scaled behavior cloning, robot foundation policies, conformal risk filtering, and ensemble uncertainty gating.
- Qualitative rollouts showing rare contact, shortcut, embodiment-shift, and recovery-scarce exceptions.
- External benchmark split such as LIBERO, RLBench, Meta-World, BridgeData, Open X-Embodiment, DROID, or a comparable hardware manipulation suite.
- A revised related-work section tied to those external results.
