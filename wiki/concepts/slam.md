---
id: slam
title: SLAM (Simultaneous Localization and Mapping)
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/neuroscience/The Brain from Inside Out - György Buzsáki MD, PhD.pdf#p1-461]'
confidence: medium
tags:
- SLAM
- robot navigation
- autonomous
- mapping
- localization
related:
  broader:
  - robot navigation
  - spatial navigation
  narrower: []
  adjacent: []
---


# SLAM (Simultaneous Localization and Mapping)

## Summary

SLAM (Simultaneous Localization and Mapping) is a breakthrough approach in autonomous robot navigation that combines motor-driven path integration with sensor-dependent landmark detection. The robot's movement trajectory and locations of all landmarks are continuously estimated and updated without a priori knowledge. As the robot moves, spring-like correlations between landmarks increase, and estimated locations are corrected and propagated through the network. This process is analogous to how the hippocampal CA2/3 recurrent system may construct cognitive graphs.

## Key facts

- SLAM combines motor-driven path integration and sensor-dependent landmark detection, with the robot's trajectory and landmark locations continuously estimated without a priori knowledge. [raw/books/neuroscience/The Brain from Inside Out - György Buzsáki MD, PhD.pdf#p118]
- As the robot moves back and forth through the environment, spring stiffness or correlations between landmarks increase, and corrections are propagated through the spring network. [raw/books/neuroscience/The Brain from Inside Out - György Buzsáki MD, PhD.pdf#p118]
- The spring map model is reminiscent of the 'cognitive graph' idea where springs are replaced by synaptic strengths between hippocampal CA3 neurons. [raw/books/neuroscience/The Brain from Inside Out - György Buzsáki MD, PhD.pdf#p119]

## Inferences

- Inference: machines with few microprocessors or insects with tiny brains can solve the navigation problem, mammals may need a complicated navigation system because they need to flexibly combine and compare many environmental details.

## Related pages

- Broader: [[robot navigation]]
- Broader: [[spatial navigation]]
- Concepts: [[path integration]]
- Concepts: [[cognitive map]]
- Concepts: [[hippocampus]]

## Provenance

- Primary source: [raw/books/neuroscience/The Brain from Inside Out - György Buzsáki MD, PhD.pdf#p1-461]

## Change notes

- 2026-04-24 — page created by auto ingest.
