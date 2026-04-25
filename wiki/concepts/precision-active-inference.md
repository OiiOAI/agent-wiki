---
id: precision-active-inference
title: Precision in Active Inference
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- precision
- attention
- variational inference
- prediction error
related:
  broader:
  - Active Inference
  - Variational Inference
  - Predictive Coding
  narrower: []
  adjacent:
  - Attention
  - Dopamine
  - Expected Free Energy
---


# Precision in Active Inference

## Summary

Precision in Active Inference refers to the inverse temperature parameter that controls the confidence or weight assigned to prediction errors or policies. It is modeled using gamma distributions, with separate precision parameters for likelihood (observations given states), transitions (state dynamics), and policies (action selection). Precision updates are derived from the gradient of free energy with respect to expected precision parameters, providing a mechanistic account of attention and dopaminergic signaling.

## Key facts

- Precision over policies is parameterized using a Gibbs measure where P(π|γ) = Cat(π0) with π0 = σ(−γG), allowing policies to be weighted by their expected free energy. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p255]
- The prior and approximate posterior distributions over precision parameters are gamma distributions: P(ζ) ∝ βζ exp(−βζζ), with expected precision ζ = E_Q(ζ)[ζ] = βζ−1. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p255]
- Update equations for precision parameters are given by gradient descent: βζ~ = Στ(oτζ − oτ)·i·ln A + βζ − βζ, where the first term reflects precision-weighted prediction errors. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p256]
- The dimensionality implies a row vector of precisions for the likelihood matrix A, where each column (state) has its own precision parameter. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p256]

## Inferences

- Inference: Precision in Active Inference provides a unified account of attentional modulation, with increased precision corresponding to enhanced weighting of prediction errors consistent with biased competition models of attention.
- Inference: Dopaminergic signaling may encode precision-weighted prediction errors, linking the mathematical formalism to neural implementation.

## Related pages

- Broader: [[Active Inference]]
- Broader: [[Variational Inference]]
- Broader: [[Predictive Coding]]
- Adjacent: [[Attention]]
- Adjacent: [[Dopamine]]
- Adjacent: [[Expected Free Energy]]
- Concepts: [[Gamma Distribution]]
- Concepts: [[Inverse Temperature]]
- Concepts: [[Prediction Error]]
- Concepts: [[Free Energy Minimization]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
