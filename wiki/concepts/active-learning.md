---
id: active-learning
title: Active Learning and Novelty Seeking
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- active-learning
- novelty
- curiosity
- bayesian-inference
related:
  broader:
  - learning
  - active-inference
  narrower:
  - dirichlet-priors
  - parameter-learning
  - structure-learning
  adjacent: []
---


# Active Learning and Novelty Seeking

## Summary

Active learning in Active Inference extends inference to include beliefs about model parameters (A, B, C, D, E matrices). Learning is cast as Bayesian inference about parameters, with Dirichlet priors enabling parametric learning. Novelty seeking emerges from the expected free energy when policies resolve uncertainty about parameters, driving agents to collect data that most change their beliefs.

## Key facts

- Including beliefs about parameters in the generative model permits treating learning as another form of Bayesian inference. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p141]
- Learning dynamics should lead to changes in intrinsic connectivity (transitions), while learning observation models should modify extrinsic connectivity (likelihoods). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p107]
- Novelty is the resolution of uncertainty about parameters, analogous to how salience is the resolution of uncertainty about states. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p144]
- Dirichlet distributions are conjugate priors for categorical distributions, enabling efficient Bayesian updating of beliefs about parameters. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p142]

## Related pages

- Broader: [[learning]]
- Broader: [[active-inference]]
- Narrower: [[dirichlet-priors]]
- Narrower: [[parameter-learning]]
- Narrower: [[structure-learning]]
- Concepts: [[bayesian-learning]]
- Concepts: [[novelty]]
- Concepts: [[curiosity]]
- Concepts: [[parameter-inference]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
