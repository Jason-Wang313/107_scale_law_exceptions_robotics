# Hostile Prior Work

The hostile set contains scaling laws, robot foundation models, generalist agents, open robot datasets, and uncertainty/safety filters. The strongest pressure comes from:

- Neural scaling-law work, which shows predictable loss improvements from data/model/compute scaling.
- Compute-optimal scaling work, which shows that larger is not the only scaling axis and that data/model balance matters.
- RT-1 and RT-2 style robot foundation models, which show real-world robot control gains from larger robot data and web-scale representations.
- Open X-Embodiment and RT-X style cross-embodiment training, which directly target robot generalization through larger shared robot datasets.
- Octo and other open generalist robot policies, which already make multi-embodiment robot-policy scaling concrete.
- Ensemble uncertainty and conformal risk filters, which already catch some tail failures without a new scale-exception mechanism.

The novelty boundary is therefore narrow. The contribution cannot be "scaling is useful", "bigger models fail sometimes", "uncertainty helps", or "robot data should be broader." The surviving claim is embodied scale-exception auditing: identifying when average scaling metrics improve while contact-boundary, rare-tail, shortcut, embodiment-shift, overtrust, or recoverability metrics regress.

The v4 local benchmark supports this boundary but does not close the external-validation gap.
