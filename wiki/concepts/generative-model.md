---
id: generative-model
title: Generative Model
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- generative models
- bayesian
- hidden states
- POMDP
- continuous time
- hierarchical models
related:
  broader:
  - Active Inference
  - Bayesian brain hypothesis
  narrower:
  - POMDP
  - continuous-time model
  - generalized coordinates of motion
  - likelihood
  - prior
  - hidden state
  - latent variable
  - policy
  - hierarchical model
  - deep temporal model
  adjacent:
  - variational inference
  - approximate Bayesian inference
  - predictive coding
  - Kalman-Bucy filter
  - factor graph
---


# Generative Model

## Summary

A generative model in Active Inference is a probabilistic model that defines how unobservable (hidden) causes in the world generate observable sensory consequences. It is formulated as the joint probability P(y,x) of observations y and hidden states x, decomposed into a prior P(x) and a likelihood P(y|x). Generative models used in Active Inference are of two main types: discrete-time POMDPs (for categorical variables and sequential decisions) and continuous-time dynamical models (for continuous sensory and motor variables). The book treats the generative model as the central challenge—getting it right as an apt explanation for any experimental subject or creature is the big challenge of Active Inference.

## Key facts

- A generative model is formulated as the joint probability P(y,x) of observations y and hidden states x, decomposed into a prior P(x) and a likelihood P(y|x). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p24]
- Active Inference uses two main types of generative models: Partially Observable Markov Decision Processes (POMDPs) for discrete time and categorical variables, and continuous-time dynamical models using stochastic differential equations for continuous variables. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p69]
- The book identifies getting the generative model right as 'the big challenge' of Active Inference, because the generative model determines what the agent finds surprising and therefore its behavior. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p8]
- In POMDPs, the generative model includes a likelihood matrix A, transition matrices B parameterized by policies, prior preferences C, and prior over initial states D. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p71]
- The organism's generative model and the true generative process of the environment are not necessarily the same; the model is a construct used to draw inferences, not a copy of reality. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p23]
- Generative models in Active Inference may be hierarchical, with higher levels encoding slower-changing context that modulates faster-changing lower-level states. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p56]

## Inferences

- Inference: Because a policy is itself a variable in the generative model, prior beliefs about policies are expressed in the same probabilistic framework as beliefs about hidden states, unifying inference and planning under one formalism.

## Uncertainties

- Uncertain: The book notes that continuous-time models are formulated using generalized coordinates of motion (position, velocity, acceleration, and higher derivatives), but the full mathematical treatment of these models is developed further in chapter 4 beyond the scope of this chunk.

## Related pages

- Broader: [[Active Inference]]
- Broader: [[Bayesian brain hypothesis]]
- Narrower: [[POMDP]]
- Narrower: [[continuous-time model]]
- Narrower: [[generalized coordinates of motion]]
- Narrower: [[likelihood]]
- Narrower: [[prior]]
- Narrower: [[hidden state]]
- Narrower: [[latent variable]]
- Narrower: [[policy]]
- Narrower: [[hierarchical model]]
- Narrower: [[deep temporal model]]
- Adjacent: [[variational inference]]
- Adjacent: [[approximate Bayesian inference]]
- Adjacent: [[predictive coding]]
- Adjacent: [[Kalman-Bucy filter]]
- Adjacent: [[factor graph]]
- Concepts: [[POMDP]]
- Concepts: [[continuous-time model]]
- Concepts: [[generalized coordinates of motion]]
- Concepts: [[likelihood]]
- Concepts: [[prior]]
- Concepts: [[hidden state]]
- Concepts: [[latent variable]]
- Concepts: [[policy]]
- Concepts: [[variational inference]]
- Concepts: [[predictive coding]]
- Concepts: [[Markov blanket]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
