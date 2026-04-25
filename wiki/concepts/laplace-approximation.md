---
id: laplace-approximation
title: Laplace Approximation
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- approximation
- variational-inference
- gaussian
related:
  broader:
  - variational-free-energy
  - generative-model
  narrower: []
  adjacent: []
---


# Laplace Approximation

## Summary

The Laplace approximation is a method for approximating probability densities by treating them as Gaussian. This is achieved through a quadratic (Taylor series) expansion around the posterior mode. Under this approximation, the only term in the free energy that depends on the mode is the negative log probability of the data given the mode.

## Key facts

- The Laplace approximation approximates free energy by a quadratic expansion around the posterior mode (μ). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p90]
- Assuming a quadratic expansion is sufficient is equivalent to treating probabilities as Gaussian (since the log of a Gaussian density is quadratic). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p90]
- Under quadratic assumptions, the posterior precision is the second derivative of the joint probability evaluated at the posterior mode. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p90]
- The approximate posterior takes the form q(x) ∝ e^(-1/2(x-μ)^T Σ^{-1}(x-μ)) where Σ^{-1} = -∂²x ln p(x,y)|x=μ. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p90]

## Related pages

- Broader: [[variational-free-energy]]
- Broader: [[generative-model]]
- Concepts: [[variational-free-energy]]
- Concepts: [[generative-model]]
- Concepts: [[gaussian-approximation]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
