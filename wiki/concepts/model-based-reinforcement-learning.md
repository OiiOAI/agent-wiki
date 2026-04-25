---
id: model-based-reinforcement-learning
title: Model-Based Reinforcement Learning
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
- goal-directed
related:
  broader: []
  narrower: []
  adjacent:
  - model-free-reinforcement-learning
  - goal-directed-learning
  - reinforcement-learning
---


# Model-Based Reinforcement Learning

## Summary

Model-based reinforcement learning infers action values by first learning a model of the environment (transition and reward functions) and then using planning to compute values. This approach corresponds to goal-directed behavior as it requires knowledge of both action-outcome contingencies and the values of specific outcomes. Computationally, it requires estimating transition probabilities T(s,a,s') and reward function R(s), then applying value iteration.

## Key facts

- Model-based reinforcement learning estimates the transition function T(s,a,s') and reward function R(s) to form a model of the MDP, then computes action values using planning. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p359]
- Values derived from model-based RL are computationally analogous to goal values because the transition function embodies knowledge about how actions lead to outcomes, and the reward function represents the rewarding value of those outcomes. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p359]
- Decisions derived from model-based values are sensitive to outcome contingency and value changes. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p359]

## Inferences

- Inference: Hampton et al. (2006) found that vmPFC activity during probabilistic reversal learning reflected the structure of the decision problem, updating instantly following reversals rather than incrementally, consistent with model-based inference

## Related pages

- Adjacent: [[model-free-reinforcement-learning]]
- Adjacent: [[goal-directed-learning]]
- Adjacent: [[reinforcement-learning]]
- Concepts: [[reinforcement-learning]]
- Concepts: [[goal-directed-learning]]
- Concepts: [[markov-decision-process]]

## Provenance

- Primary source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]

## Change notes

- 2026-04-24 — page created by auto ingest.
