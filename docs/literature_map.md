# Literature Map

Paper: 107 scale_law_exceptions_robotics

Field box: scaling laws, robot foundation models, cross-embodiment datasets, and robotics safety/reliability.

Thesis: average scaling curves can hide embodied failure-boundary regressions.

## Crowded Neighbor Clusters

- Scaling laws for neural models: predictable loss improvements from model size, data, and compute.
- Compute-optimal scaling: data/model balance and scaling efficiency.
- Robot foundation models: RT-1, RT-2, RT-X, Octo, and open robot datasets.
- Generalist agents: multi-task embodied policies that benefit from broad training.
- Risk filters: uncertainty, ensembles, and conformal prediction for safety gating.

## Hidden Assumptions Attacked

- Average loss or average success is enough to predict deployed robot safety.
- Larger robot datasets automatically cover rare physical tails.
- Web-scale representations solve embodiment mismatch.
- Conformal or ensemble gating catches all scale-law exceptions.
- Recovery scarcity can be treated as a generic tail-risk metric.

## Boundary

The project centers a mechanism-level change: audit scaling curves against embodied exception metrics, including rare-failure recall, contact-boundary error, unsafe commitment, overtrust, calibration under rare tails, recoverability, and regret to an oracle exception selector.
