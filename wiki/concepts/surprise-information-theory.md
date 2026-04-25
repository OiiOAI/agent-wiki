---
id: surprise-information-theory
title: Surprise (Information Theory)
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- surprise
- information theory
- entropy
- model evidence
- bayesian
related:
  broader:
  - information theory
  - Active Inference
  - variational inference
  narrower:
  - surprisal
  - self-information
  - negative log evidence
  - model evidence
  - entropy
  - Bayesian surprise
  adjacent:
  - variational free energy
  - model comparison
  - KL-divergence
  - Jaynes maximum entropy principle
---


# Surprise (Information Theory)

## Summary

In Active Inference and information theory, surprise (also called surprisal or self-information) is defined as the negative log probability of an observation: ℑ(y) = -ln P(y). It measures how unlikely an observation is under a generative model. Surprise is a fundamental quantity in Active Inference because the central imperative is that living organisms must minimize the surprise of their sensory observations to survive. Surprising observations indicate a poor fit between the organism's generative model and reality. Surprise is related to but distinct from Bayesian surprise (the KL-divergence between prior and posterior), which measures belief updating rather than observation unlikelihood. Variational free energy is an upper bound on surprise, making it a tractable proxy for the purpose of minimization.

## Key facts

- Surprise is defined as the negative log probability of an observation: ℑ(y) = -ln P(y), measuring how unlikely the observation is under the organism's generative model. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p19]
- Surprise is used to compare models: a model that assigns higher probability to observed data has lower surprise and is a better model of those data. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p19]
- Bayesian surprise (KL-divergence between prior and posterior) measures the amount of belief updating following an observation, distinct from surprise which measures observation unlikelihood. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p20]
- Minimizing surprise mathematically equals maximizing model evidence P(y), the marginal probability of observations under the generative model. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p46]
- Entropy H[P(y)] equals the expected surprise over a distribution, and minimizing surprise over time is equivalent to minimizing entropy. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p48]

## Inferences

- Inference: Because exact Bayesian inference minimizes surprise directly, but this is computationally intractable, variational free energy provides a tractable upper bound that can be minimized efficiently. The gap between variational free energy and surprise is exactly the KL-divergence between the approximate and true posteriors.

## Related pages

- Broader: [[information theory]]
- Broader: [[Active Inference]]
- Broader: [[variational inference]]
- Narrower: [[surprisal]]
- Narrower: [[self-information]]
- Narrower: [[negative log evidence]]
- Narrower: [[model evidence]]
- Narrower: [[entropy]]
- Narrower: [[Bayesian surprise]]
- Adjacent: [[variational free energy]]
- Adjacent: [[model comparison]]
- Adjacent: [[KL-divergence]]
- Adjacent: [[Jaynes maximum entropy principle]]
- Concepts: [[surprise]]
- Concepts: [[model evidence]]
- Concepts: [[entropy]]
- Concepts: [[Bayesian surprise]]
- Concepts: [[KL-divergence]]
- Concepts: [[variational free energy]]
- Concepts: [[information theory]]
- Concepts: [[negative log probability]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
