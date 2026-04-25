---
id: variational-free-energy
title: Variational Free Energy
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
- bayesian inference
- free energy
- information theory
- surprise minimization
related:
  broader:
  - free energy principle
  - Active Inference
  - variational inference
  - active-inference
  - variational-inference
  narrower:
  - surprise
  - model evidence
  - Bayesian surprise
  - complexity
  - accuracy
  - energy
  - entropy
  - KL-divergence
  - variational posterior
  - approximate posterior
  - prediction-error
  - laplace-approximation
  adjacent:
  - expected free energy
  - surprise
  - model evidence
  - KL-divergence
  - ELBO
  - Jensen's inequality
---


# Variational Free Energy

## Summary

Variational free energy is the central quantity that Active Inference agents minimize through perception and action. It is a mathematically derived upper bound on surprise (negative log model evidence), defined as F[Q,y] = D_KL[Q(x)||P(x|y)] - ln P(y). The term was adopted from statistical physics and provides a tractable proxy for the otherwise intractable quantity of surprise. Minimizing variational free energy is equivalent to maximizing model evidence and minimizing surprise, provided the KL-divergence between the approximate posterior Q(x) and the true posterior P(x|y) approaches zero. It decomposes into complexity cost (KL-divergence between prior and posterior, i.e., Bayesian surprise) and accuracy (expected log likelihood).

## Key facts

- Variational free energy is an upper bound on surprise (negative log model evidence), defined as F[Q,y] = D_KL[Q(x)||P(x|y)] - ln P(y). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p28]
- When the approximate posterior Q matches the exact posterior P(x|y), the KL-divergence term becomes zero and variational free energy equals surprise exactly. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p29]
- Variational free energy can be decomposed into an energy term (expected joint log probability) and a negative entropy term of the approximate posterior. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p28]
- Variational free energy also decomposes into complexity (KL-divergence between prior and posterior) and accuracy (expected log likelihood of observations under the generative model). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p28]
- Perception minimizes variational free energy by updating the approximate posterior Q(x) to reduce the KL-divergence, without changing sensory observations. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p52]
- Action minimizes variational free energy by changing sensory observations to increase model evidence, thereby reducing the evidence term while keeping the divergence term fixed. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p52]
- The term 'free energy' originates from statistical physics; in Active Inference it refers specifically to variational free energy as used in machine learning and approximate Bayesian inference. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p50]
- Free energy for a generative model in continuous time can be written as F[μ, y] = −ln p(y, μ̃x, μ̃v). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p88]
- Under the Laplace approximation, all probability densities are treated as Gaussian, which is equivalent to assuming operation near the mode of the distribution. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p89]
- The free energy can be expressed in terms of squared precision-weighted prediction errors. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p89]
- The posterior precision under the Laplace approximation is simply the second derivative of the joint probability evaluated at the posterior mode. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p90]

## Inferences

- Inference: Because variational free energy can be computed without knowing the exact posterior (which is intractable), it provides a computationally tractable objective for biological systems with limited computational resources.

## Related pages

- Broader: [[free energy principle]]
- Broader: [[Active Inference]]
- Broader: [[variational inference]]
- Broader: [[active-inference]]
- Broader: [[variational-inference]]
- Narrower: [[surprise]]
- Narrower: [[model evidence]]
- Narrower: [[Bayesian surprise]]
- Narrower: [[complexity]]
- Narrower: [[accuracy]]
- Narrower: [[energy]]
- Narrower: [[entropy]]
- Narrower: [[KL-divergence]]
- Narrower: [[variational posterior]]
- Narrower: [[approximate posterior]]
- Narrower: [[prediction-error]]
- Narrower: [[laplace-approximation]]
- Adjacent: [[expected free energy]]
- Adjacent: [[surprise]]
- Adjacent: [[model evidence]]
- Adjacent: [[KL-divergence]]
- Adjacent: [[ELBO]]
- Adjacent: [[Jensen's inequality]]
- Concepts: [[surprise]]
- Concepts: [[model evidence]]
- Concepts: [[Bayesian surprise]]
- Concepts: [[complexity]]
- Concepts: [[accuracy]]
- Concepts: [[energy]]
- Concepts: [[entropy]]
- Concepts: [[KL-divergence]]
- Concepts: [[variational posterior]]
- Concepts: [[expected free energy]]
- Concepts: [[variational inference]]
- Concepts: [[ELBO]]
- Concepts: [[Jensen's inequality]]
- Concepts: [[approximate Bayesian inference]]
- Concepts: [[active-inference]]
- Concepts: [[variational-inference]]
- Concepts: [[prediction-error]]
- Concepts: [[laplace-approximation]]
- Concepts: [[generative-model]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
