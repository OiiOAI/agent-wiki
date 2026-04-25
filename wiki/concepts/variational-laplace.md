---
id: variational-laplace
title: Variational Laplace
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- inference-scheme
- variational-methods
- laplace
related:
  broader: []
  narrower: []
  adjacent: []
---


# Variational Laplace

## Summary

Variational Laplace is an inference scheme based on the same principles as predictive coding that can be used with generic likelihood functions. It enables parameter estimation and model comparison by maximizing a free energy approximation to model evidence.

## Key facts

- Variational Laplace evaluates the log likelihood of an observed sequence of actions as a function of parameters, the model, and stimuli presented during an experiment. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p183]
- A softmax temperature parameter accounts for randomness in behavior not accounted for by the model. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p183]
- Equipped with Gaussian priors over parameters, the Laplace assumption expresses a free energy approximation to model evidence. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p184]

## Related pages

- Concepts: [[variational-inference]]
- Concepts: [[laplace-approximation]]
- Concepts: [[predictive-coding]]
- Concepts: [[free-energy]]
- Topics: [[model-based-data-analysis]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
