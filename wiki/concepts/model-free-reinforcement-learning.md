---
id: model-free-reinforcement-learning
title: Model-Free Reinforcement Learning
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_
  Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]'
confidence: high
tags:
- reinforcement-learning
- computational
- habit
related:
  broader: []
  narrower: []
  adjacent:
  - model-based-reinforcement-learning
  - actor-critic-model
  - habit-values
---


# Model-Free Reinforcement Learning

## Summary

Model-free reinforcement learning estimates action values directly by averaging samples of cumulative future rewards, without learning an explicit model of the environment. Algorithms like Q-learning use temporal-difference errors to update value estimates. This approach corresponds to habit values as it is grounded in history of reinforcement rather than prediction of specific outcomes, making it insensitive to outcome devaluation.

## Key facts

- Model-free RL estimates action values directly by averaging samples of the right-hand side of the Bellman equation, without estimating transition and reward functions. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p360]
- Q-learning uses the update rule Q(st,at) ← Q(st,at) + ηδt where δt = rt + γ max_a[Q(st+1,a)] - Q(st,at) is the temporal-difference prediction error. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p360]
- Model-free learned values are insensitive to changes in reward value because the learned function Q(s,a) is not grounded in information about the identities of future outcomes. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p360]

## Related pages

- Adjacent: [[model-based-reinforcement-learning]]
- Adjacent: [[actor-critic-model]]
- Adjacent: [[habit-values]]
- Concepts: [[reinforcement-learning]]
- Concepts: [[habit-learning]]
- Concepts: [[q-learning]]

## Provenance

- Primary source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]

## Change notes

- 2026-04-24 — page created by auto ingest.
