---
id: variational-inference
title: Variational Inference
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- variational inference
- approximate inference
- bayesian
- optimization
- message passing
- machine learning
related:
  broader:
  - Bayesian inference
  - approximate inference
  narrower:
  - variational free energy
  - approximate posterior
  - Jensen's inequality
  - mean field approximation
  - message passing
  - KL-divergence
  - ELBO
  adjacent:
  - sampling methods
  - expectation-maximization
  - mean field theory
  - statistical physics
---


# Variational Inference

## Summary

Variational inference is a method for performing approximate Bayesian inference that converts an intractable integration problem into an optimization problem by introducing an approximate posterior distribution Q(x) that approximates the true posterior P(x|y). It exploits Jensen's inequality to derive the variational free energy as a tractable bound on the log model evidence (surprise). The method minimizes the KL-divergence between the approximate posterior and the true posterior by minimizing variational free energy. In Active Inference, variational inference provides the link between the free energy principle and practical neural computation, with the approximate posterior corresponding to beliefs about hidden states held by the brain. The book identifies two types of variational inference: message passing schemes (variational message passing and belief propagation) that are local and biologically plausible.

## Key facts

- Variational inference converts the intractable problem of computing the posterior P(x|y) and model evidence P(y) into an optimization problem by introducing an approximate posterior Q(x). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p65]
- Jensen's inequality states that the log of an average is always greater than or equal to the average of a log, which is used to derive variational free energy as an upper bound on surprise. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p65]
- The key variational message passing update sets the rate of change of the log posterior equal to the negative gradient of free energy, driving belief updating. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p75]
- Belief propagation and variational message passing are two message passing schemes used for approximate inference that rely on the Markov blanket structure to make local computations feasible. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p76]
- Variational inference is necessary because exact Bayesian inference is computationally intractable or infeasible for complex real-world models due to analytically intractable integrals. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p27]

## Inferences

- Inference: The mean field approximation (which factorizes the joint approximate posterior into a product of factors) is the simplest form of variational inference used in Active Inference and underlies the additive form of free energy over time steps in POMDPs.

## Uncertainties

- Uncertain: The book notes that Appendix B provides a concise form of the most important equations used in Active Inference, suggesting the full variational message passing scheme is developed in more detail beyond this chunk.

## Related pages

- Broader: [[Bayesian inference]]
- Broader: [[approximate inference]]
- Narrower: [[variational free energy]]
- Narrower: [[approximate posterior]]
- Narrower: [[Jensen's inequality]]
- Narrower: [[mean field approximation]]
- Narrower: [[message passing]]
- Narrower: [[KL-divergence]]
- Narrower: [[ELBO]]
- Adjacent: [[sampling methods]]
- Adjacent: [[expectation-maximization]]
- Adjacent: [[mean field theory]]
- Adjacent: [[statistical physics]]
- Concepts: [[variational free energy]]
- Concepts: [[approximate posterior]]
- Concepts: [[Jensen's inequality]]
- Concepts: [[mean field approximation]]
- Concepts: [[message passing]]
- Concepts: [[KL-divergence]]
- Concepts: [[ELBO]]
- Concepts: [[Bayes theorem]]
- Concepts: [[model evidence]]
- Concepts: [[surprise]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
