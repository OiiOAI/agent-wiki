---
id: planning-as-inference
title: Planning as Inference
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- planning
- inference
- policy
- decision-making
- expected free energy
- bayesian
related:
  broader:
  - Active Inference
  - Bayesian brain hypothesis
  narrower:
  - expected free energy
  - policy
  - temporal depth
  - counterfactual simulation
  - exploration-exploitation
  adjacent:
  - reinforcement learning
  - Bellman equation
  - optimal control
  - decision theory
  - ideomotor theory
---


# Planning as Inference

## Summary

Planning as inference is the extension of the Active Inference framework that treats planning and decision-making as problems of Bayesian inference over policies (hypothesized courses of action). Rather than using value functions or utility functions, Active Inference scores alternative policies by their expected free energy. Policies are treated as random variables in the generative model, analogous to how hidden states are treated in perceptual inference. The prior over policies is set proportional to the negative expected free energy: policies associated with lower expected free energy (higher information gain and greater alignment with prior preferences) are assigned higher prior probability. Inferring a policy is then equivalent to forming a posterior belief about which course of action to pursue, which directly translates into an intention that is fulfilled through action.

## Key facts

- Active Inference treats planning as inference, where policies (sequences of actions) are scored by their expected free energy in the same way that hidden states are scored by variational free energy. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p31]
- A policy is a hypothesis about a way of behaving, analogous to how the apple/frog hypothesis was a hypothesis about the hidden state in the perceptual example. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p31]
- The prior probability of a policy is proportional to the negative expected free energy, effectively endowing the agent with the prior belief that it will pursue the least surprising course of action. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p32]
- Inferring a policy is equivalent to forming a posterior belief about which course of action to pursue, which directly translates into an intention fulfilled by action. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p38]
- Expected free energy scores policies by considering future observations they would generate, which requires temporal depth in the generative model. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p56]
- Planning as inference replaces the notion of value (from reinforcement learning) with the notion of prior belief about what the agent expects to do. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p53]

## Inferences

- Inference: Planning as inference eliminates the need for a separate value function or utility function because prior beliefs about preferred outcomes serve the same role as utility functions, unifying subjective preferences with objective probabilistic beliefs in a single framework.

## Related pages

- Broader: [[Active Inference]]
- Broader: [[Bayesian brain hypothesis]]
- Narrower: [[expected free energy]]
- Narrower: [[policy]]
- Narrower: [[temporal depth]]
- Narrower: [[counterfactual simulation]]
- Narrower: [[exploration-exploitation]]
- Adjacent: [[reinforcement learning]]
- Adjacent: [[Bellman equation]]
- Adjacent: [[optimal control]]
- Adjacent: [[decision theory]]
- Adjacent: [[ideomotor theory]]
- Concepts: [[expected free energy]]
- Concepts: [[policy]]
- Concepts: [[variational free energy]]
- Concepts: [[temporal depth]]
- Concepts: [[counterfactual simulation]]
- Concepts: [[exploration-exploitation]]
- Concepts: [[Bellman equation]]
- Concepts: [[value function]]
- Concepts: [[utility]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
