---
id: actor-critic-model
title: Actor-Critic Model
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean
  - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p1-401]'
confidence: high
related:
  broader:
  - reinforcement-learning
  narrower: []
  adjacent: []
tags: []
---


# Actor-Critic Model

## Summary

The Actor-Critic Model is a reinforcement learning architecture where a critic circuit learns the reward value associated with different states of the environment (V(s)), and an actor circuit learns reward value associated with taking different actions in a given state (Q(s,a)). The critic combines the reward signal and state-value output to compute the reward prediction error, which updates both circuits.

## Key facts

- In RL models, a subnetwork responsible for value estimation is often referred to as the 'critic', which can be implemented as a single neuron receiving synaptic connections from sensory circuits. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p164]
- The critic circuit learns the reward value associated with different states of the environment, V(s_n), and the actor circuit learns reward value associated with taking different actions (e.g., A1 and A2) in a given state, Q(s_n,a_n). [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p164]
- The RPE is used to update value functions in the critic circuit and the action value functions in the actor circuit. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p164]

## Related pages

- Broader: [[reinforcement-learning]]
- Concepts: [[temporal-difference-learning]]
- Concepts: [[reward-prediction-error]]

## Provenance

- Primary source: [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p1-401]

## Change notes

- 2026-04-24 — page created by auto ingest.
