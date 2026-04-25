---
id: variational-message-passing
title: Message Passing (Variational)
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- message passing
- variational inference
- neural implementation
- predictive coding
- bayesian
- belief propagation
related:
  broader:
  - Active Inference
  - variational inference
  - process theory
  narrower:
  - prediction error
  - prediction
  - precision
  - synaptic gain
  - hierarchy
  - generalized coordinates
  - POMDP message passing
  adjacent:
  - predictive coding
  - Helmholtz machine
  - loopy belief propagation
  - neural networks
  - graphical models
---


# Message Passing (Variational)

## Summary

Variational message passing refers to the local update rules derived from variational free energy minimization that allow biologically plausible implementations of Bayesian inference. In the Active Inference framework, message passing is the process theory that links abstract free energy minimization to neural computation. The update rules are derived from the Markov blanket structure: for a variable x, its new belief depends on messages from its parents (top-down predictions) and its children (bottom-up prediction errors). Two main schemes are discussed: variational message passing (VMP) and belief propagation (BP). In continuous-time generative models, message passing corresponds to predictive coding—top-down predictions and bottom-up prediction errors flowing between hierarchical levels. In discrete-time POMDPs, message passing updates beliefs about states and policies across time steps and policy branches.

## Key facts

- Variational message passing updates beliefs about a variable using messages from all constituents of its Markov blanket: parents (via conditional probability) and children (via prediction errors). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p76]
- Belief propagation uses a recursive definition of messages where each message to a variable depends on all other messages to that variable except the one from the sending variable. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p76]
- In the belief updating scheme for POMDPs, prediction errors drive updates in beliefs about states at each time step, and gradients of expected free energy drive updates in beliefs about policies. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p77]
- The message passing scheme can be expanded hierarchically, where higher-level networks predict states at lower levels and use these to infer context. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p77]
- The book states 'every­thing that changes in the brain must minimize free energy' (Friston 2009), meaning that all neural dynamics are interpretable as variational message passing. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p9]

## Inferences

- Inference: Because message passing can be implemented with local computations (each node only needs information from its Markov blanket neighbors), it provides a biologically plausible mechanism for Bayesian inference in neural tissue, where long-range connections exist but global coordination is limited.

## Related pages

- Broader: [[Active Inference]]
- Broader: [[variational inference]]
- Broader: [[process theory]]
- Narrower: [[prediction error]]
- Narrower: [[prediction]]
- Narrower: [[precision]]
- Narrower: [[synaptic gain]]
- Narrower: [[hierarchy]]
- Narrower: [[generalized coordinates]]
- Narrower: [[POMDP message passing]]
- Adjacent: [[predictive coding]]
- Adjacent: [[Helmholtz machine]]
- Adjacent: [[loopy belief propagation]]
- Adjacent: [[neural networks]]
- Adjacent: [[graphical models]]
- Concepts: [[prediction error]]
- Concepts: [[prediction]]
- Concepts: [[precision]]
- Concepts: [[Markov blanket]]
- Concepts: [[variational inference]]
- Concepts: [[hierarchy]]
- Concepts: [[generalized coordinates]]
- Concepts: [[POMDP]]
- Concepts: [[predictive coding]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
