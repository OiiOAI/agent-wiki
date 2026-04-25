---
id: generalized-filtering
title: Generalized Filtering
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- continuous models
- predictive coding
- variational inference
- dynamic systems
related:
  broader:
  - Active Inference
  - Free Energy Principle
  - Predictive Coding
  narrower: []
  adjacent:
  - Laplace Approximation
  - Variational Inference
  - State-Space Models
---


# Generalized Filtering

## Summary

Generalized filtering extends Active Inference to continuous state-space models, using the Laplace approximation and generalized coordinates of motion to formulate variational inference in continuous time. This approach provides a general description of Active Inference for continuous systems, specifying how prediction errors drive updates in expectations about hidden states and how action minimizes free energy by modifying sensory input.

## Key facts

- Generalized filtering uses the Laplace approximation to express free energy under continuous models: F[q,~y] ≈ −1/2 ln(2π)Σk! − ln p(~y,~μ), where the approximate posterior is q(~x) = N(μ,~Σ) with Σ−1 = −∇x~T(∇x~ ln p(~y,~x)). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p262]
- The generative model in continuous time consists of: p(~y|~x,~v) = N(g(~x,~v),Πy), p(~x|~v) = N(D·i·f~(~x,~v),Πx), and p(~v) = N(η,Πv), where D is the matrix shifting generalized coordinates. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p262]
- The gradient descent equations for expected states include a moving frame of reference: μ~x − Dμ~x = ∇μ~xg~·i·Πyεy − D·i·Πxεx + ∇f~·i·Πxεx, ensuring that beliefs continue to move with velocity when free energy is minimized. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p263]
- These equations specify a predictive coding scheme in which prediction errors drive updates in expectations, resolving those errors through message passing between hierarchical levels. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p263]
- Action is determined by minimizing free energy with respect to sensory input: u~ = −∇u~y(u)~·i·Πyεy, providing a principled account of how motor commands arise from predictive processing. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p264]
- The framework can be extended to multiple hierarchical levels by duplicating the gradient equations with prediction errors from lower levels feeding into higher levels. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p263]

## Inferences

- Inference: Generalized filtering provides a bridge between discrete-time Active Inference and continuous-time neural dynamics, making it applicable to modeling brain imaging data using Dynamic Causal Modeling.
- Inference: The use of generalized coordinates enables biologically plausible gradient descent on free energy that naturally accounts for multiple orders of motion.

## Related pages

- Broader: [[Active Inference]]
- Broader: [[Free Energy Principle]]
- Broader: [[Predictive Coding]]
- Adjacent: [[Laplace Approximation]]
- Adjacent: [[Variational Inference]]
- Adjacent: [[State-Space Models]]
- Concepts: [[Generalized Coordinates of Motion]]
- Concepts: [[Prediction Error]]
- Concepts: [[Precision]]
- Concepts: [[Hierarchical Models]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
