---
id: bayesian-model-reduction
title: Bayesian Model Reduction
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- Bayesian methods
- model comparison
- variational inference
- Active Inference
related:
  broader:
  - Variational Inference
  - Free Energy Principle
  narrower: []
  adjacent:
  - Model Evidence
  - Free Energy Minimization
  - Structure Learning
---


# Bayesian Model Reduction

## Summary

Bayesian model reduction is a technique used in Active Inference to compare alternative models that differ only in their priors. It enables efficient computation of model evidence and posterior probabilities under reduced (simplified) priors without requiring full model inversion for each alternative. The technique uses variational quantities to derive expressions for the free energy difference between models, with closed-form solutions for normal and Dirichlet distributions commonly used in generative models.

## Key facts

- Bayesian model reduction exploits the fact that when models differ only in their priors, the likelihood terms cancel when taking ratios of joint probabilities. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p260]
- The free energy difference between full and reduced models is given by: F[P(θ)] − F[~P(θ)] = ln E_Q(θ)[~P(θ)/P(θ)], allowing model evidence computation using results from inverting a full model. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p261]
- For normal distributions, Bayesian model reduction yields a precision update (C~−1 = P + Π) and mean update (μ~ = C~(Pμ + Πη~ − Πη)), with free energy change ΔF expressed in terms of covariance and mean differences. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p261]
- For Dirichlet distributions, the reduced concentration parameters are computed as a~ = a + a~ − a, with free energy change ΔF = ln B(a) − ln B(~a) + ln B(~a) − ln B(a), where B denotes the beta function. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p261]
- Bayesian model reduction has been applied to simulate synaptic pruning during sleep by pruning elements in probability matrices (Friston, Lin et al. 2017). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p261]
- In mixed models with continuous and categorical components, Bayesian model reduction enables efficient evaluation of evidence for each categorical outcome's associated continuous prior without inverting each model in turn. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p261]

## Inferences

- Inference: Bayesian model reduction enables structure learning by comparing hypotheses about the structure of generative models, particularly useful when evaluating which connections or states should be retained or pruned.
- Inference: The computational efficiency of Bayesian model reduction makes it suitable for hierarchical model comparison and random model selection in large-scale generative models.

## Related pages

- Broader: [[Variational Inference]]
- Broader: [[Free Energy Principle]]
- Adjacent: [[Model Evidence]]
- Adjacent: [[Free Energy Minimization]]
- Adjacent: [[Structure Learning]]
- Concepts: [[Dirichlet Distribution]]
- Concepts: [[Normal Distribution]]
- Concepts: [[KL Divergence]]
- Concepts: [[Variational Free Energy]]
- Entities: [[SPM12]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
