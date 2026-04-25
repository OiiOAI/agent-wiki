---
id: markov-decision-process
title: Markov Decision Process
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
- framework
related:
  broader: []
  narrower: []
  adjacent:
  - reinforcement-learning
  - model-based-reinforcement-learning
  - model-free-reinforcement-learning
---


# Markov Decision Process

## Summary

The Markov Decision Process (MDP) is the standard formal framework for reinforcement learning. An MDP is defined by states s, actions a, a transition function T(s,a,s') = P(st+1 = s' | st = s, at = a) specifying state dynamics, and a reward function R(s). The agent's goal is to select actions to maximize cumulative expected reward, requiring evaluation of actions based on their long-term consequences.

## Key facts

- An MDP is defined by the transition function T(s,a,s') = P(st+1 = s' | st = s, at = a) specifying the probability distribution over next states given the current state and action. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p358]
- The state-action value function Q(s,a) is defined as the expected cumulative reward following action a in state s: Q(s,a) = E[rt + rt+1 + rt+2 + ... | st = s, at = a]. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p359]
- The Bellman equation for Q-values is Q(s,a) = R(s) + Σ_s' T(s,a,s') max_a' [Q(s',a')]. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p359]

## Related pages

- Adjacent: [[reinforcement-learning]]
- Adjacent: [[model-based-reinforcement-learning]]
- Adjacent: [[model-free-reinforcement-learning]]
- Concepts: [[bellman-equation]]
- Concepts: [[value-iteration]]
- Concepts: [[q-learning]]

## Provenance

- Primary source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]

## Change notes

- 2026-04-24 — page created by auto ingest.
