---
id: pomdp
title: POMDP (Partially Observable Markov Decision Process)
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- POMDP
- discrete time
- generative model
- planning
- inference
- categorical
- message passing
related:
  broader:
  - generative model
  - Active Inference
  - discrete-time models
  - active-inference
  - hidden-markov-model
  narrower:
  - likelihood matrix A
  - transition matrix B
  - preference matrix C
  - initial state prior D
  - policy
  - hidden state
  - observation
  - variational message passing
  - categorical distribution
  - expected-free-energy
  - epistemic-value
  - policy-selection
  adjacent:
  - MDP
  - hidden Markov model
  - Bayesian networks
  - Kalman filter
  - reinforcement learning
  - optimal control
---


# POMDP (Partially Observable Markov Decision Process)

## Summary

A Partially Observable Markov Decision Process (POMDP) is one of the two main types of generative models used in Active Inference for discrete-time, categorical variable inference and planning. In the POMDP framework, hidden states evolve over time conditioned on policies (action sequences), and observations are generated probabilistically from states. The POMDP is specified by four probability matrices: the likelihood matrix A (mapping states to observations), transition matrices B parameterized by policies (mapping previous states to next states), preference matrix C (prior over preferred observations), and initial state prior D. The POMDP is solved in Active Inference by minimizing variational free energy through variational message passing, yielding posterior beliefs about states and posterior beliefs about policies.

## Key facts

- In a POMDP for Active Inference, the likelihood is specified by a categorical distribution P(o|s) = Cat(A), where A_ij = P(o=i | s=j). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p71]
- State transitions in the POMDP are conditioned on the policy being pursued: P(s_τ+1 | s_τ, π) = Cat(B_π_τ). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p71]
- The POMDP generative model for Active Inference includes prior preferences C over observations, which drive the pragmatic value component of expected free energy. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p73]
- Variational message passing for POMDPs updates beliefs about states by setting the rate of change of the log posterior equal to the negative gradient of free energy. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p75]
- Beliefs about policies are updated by softmax of the negative expected free energy: π = σ(-G - F), where F is the accumulated variational free energy for each policy. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p74]
- A POMDP extends a hidden Markov model by including policies (π) on which transition probabilities are conditioned, allowing alternative hypotheses about dynamics to be entertained as plans. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p129]
- The expected free energy decomposes into epistemic value (information gain) and pragmatic value (preference fulfillment). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p130]
- Policy selection in POMDPs equates to model comparison, where a policy is an explanatory variable for an observed sequence of self-generated sensations. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p130]
- POMDPs allow factorization of states and outcomes into separate modalities (e.g., 'what' and 'where' streams), avoiding costly representation of every possible combination. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p129]

## Inferences

- Inference: The POMDP framework naturally accommodates both discrete perceptual inference (where a single policy is assumed) and planning (where multiple policies are compared via expected free energy), unifying these cognitive functions within the same variational framework.

## Related pages

- Broader: [[generative model]]
- Broader: [[Active Inference]]
- Broader: [[discrete-time models]]
- Broader: [[active-inference]]
- Broader: [[hidden-markov-model]]
- Narrower: [[likelihood matrix A]]
- Narrower: [[transition matrix B]]
- Narrower: [[preference matrix C]]
- Narrower: [[initial state prior D]]
- Narrower: [[policy]]
- Narrower: [[hidden state]]
- Narrower: [[observation]]
- Narrower: [[variational message passing]]
- Narrower: [[categorical distribution]]
- Narrower: [[expected-free-energy]]
- Narrower: [[epistemic-value]]
- Narrower: [[policy-selection]]
- Adjacent: [[MDP]]
- Adjacent: [[hidden Markov model]]
- Adjacent: [[Bayesian networks]]
- Adjacent: [[Kalman filter]]
- Adjacent: [[reinforcement learning]]
- Adjacent: [[optimal control]]
- Concepts: [[likelihood matrix A]]
- Concepts: [[transition matrix B]]
- Concepts: [[preference matrix C]]
- Concepts: [[initial state prior D]]
- Concepts: [[policy]]
- Concepts: [[hidden state]]
- Concepts: [[observation]]
- Concepts: [[variational message passing]]
- Concepts: [[categorical distribution]]
- Concepts: [[softmax]]
- Concepts: [[expected free energy]]
- Concepts: [[variational free energy]]
- Concepts: [[active-inference]]
- Concepts: [[planning]]
- Concepts: [[decision-making]]
- Concepts: [[hidden-markov-model]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
