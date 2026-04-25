---
id: dirichlet-distribution-learning
title: Dirichlet Distribution (Learning in POMDPs)
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- Dirichlet
- learning
- Bayesian
- variational inference
- POMDP
related:
  broader:
  - Variational Inference
  - Bayesian Learning
  narrower: []
  adjacent:
  - Categorical Distribution
  - Conjugate Prior
  - Free Energy Minimization
---


# Dirichlet Distribution (Learning in POMDPs)

## Summary

The Dirichlet distribution serves as the conjugate prior for categorical distributions in Active Inference, enabling tractable Bayesian learning of the parameters of generative models. When predictions are confirmed by outcomes, the associated Dirichlet parameters are augmented, providing a simple update rule that implements Bayesian parameter updating without requiring explicit computation of posterior distributions.

## Key facts

- The expectation of the log of a Dirichlet distributed variable equals the difference between two digamma functions: E_Q(D)[ln D] = ψ(d) − ψ(d0), where ψ is the derivative of the gamma function. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p254]
- The free energy minimum with respect to Dirichlet parameters yields the simple update: d = d0 + s1, meaning posterior parameters equal prior parameters plus the number of times the associated state was visited. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p254]
- Update rules for different probability distributions follow similar principles: a = a + Στ oτ ⊗ sτ for likelihoods, bπτ = bπτ + Σ sπτ ⊗ sπτ−1 for transitions, and c = c + Στ oτ for preferences. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p254]
- The interpretation is that when the thing predicted by a probability distribution term comes to pass, that element of the probability array is augmented to signal it is more likely to happen again in the future. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p254]

## Inferences

- Inference: The Dirichlet update rule provides a neurally plausible mechanism for learning, as counting occurrences and incrementing parameters can be implemented through simple synaptic modifications.

## Related pages

- Broader: [[Variational Inference]]
- Broader: [[Bayesian Learning]]
- Adjacent: [[Categorical Distribution]]
- Adjacent: [[Conjugate Prior]]
- Adjacent: [[Free Energy Minimization]]
- Concepts: [[Digamma Function]]
- Concepts: [[Gamma Distribution]]
- Concepts: [[Conjugate Prior]]
- Concepts: [[Parameter Learning]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
