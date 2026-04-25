---
id: hybrid-discrete-continuous-models
title: Hybrid (Discrete and Continuous) Models
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- generative-models
- hybrid-systems
- continuous-time
- discrete-time
related:
  broader: []
  narrower: []
  adjacent: []
---


# Hybrid (Discrete and Continuous) Models

## Summary

Hybrid or mixed generative models combine discrete POMDP models at higher levels with continuous state-space models at lower levels, enabling both sequential action planning and translation of decisions into continuous movements. This architecture decomposes continuous time into a discrete sequence of short continuous trajectories.

## Key facts

- Hybrid models combine a POMDP at the higher level with a continuous model at the lower level. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p173]
- The higher-level POMDP generates a continuous model at each discrete time step, decomposing continuous time into a discrete sequence of short continuous trajectories. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p173]
- Transforming decisions about discrete target locations into continuous eye movements requires each discrete target location to be associated with a distribution over continuous hidden causes. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p174]

## Inferences

- Inference: The Bayesian model average over discrete locations, weighted by POMDP-level inferences, provides a prior over continuous target coordinates.
- Inference: Mixed models require reciprocal interactions between higher and lower hierarchical levels.

## Related pages

- Concepts: [[POMDP]]
- Concepts: [[generative-model]]
- Concepts: [[predictive-coding]]
- Concepts: [[variational-free-energy]]
- Topics: [[active-inference]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
