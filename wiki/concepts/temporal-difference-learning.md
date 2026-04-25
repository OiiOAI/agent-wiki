---
id: temporal-difference-learning
title: Temporal Difference Learning
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-25'
sources:
- '[raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean
  - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p1-401]'
- '[raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_
  Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]'
confidence: high
related:
  broader:
  - reinforcement-learning
  - prediction-error
  narrower:
  - actor-critic
  - q-learning
  adjacent:
  - actor-critic-model
  - reward-prediction-error
tags:
- reinforcement-learning
- temporal-difference
- prediction-error
- dopamine
- machine-learning
aliases: []
---

# Temporal Difference Learning

## Summary

Temporal Difference (TD) Learning is a reinforcement learning algorithm where the expected reinforcement signal is defined by temporally discounted reward from all future time steps. The idea of an adaptive critic forms the basis for TD learning, and the algorithm converts TD errors into synaptic weight changes. Early models aimed to understand patterns of dopaminergic neuron firing based on TD learning principles.

## Key facts

- The idea of an adaptive critic forms the basis for TD learning, in which the expected reinforcement signal is defined by temporally discounted reward from all future time steps. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p164]
- Early attempts in converting the TD learning algorithm into biophysical models aimed to understand the patterns of dopaminergic neuron firing. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p164]
- Evidence indicates that other mechanisms are required to capture the exact pattern of experimental data, including a long-lasting eligibility trace. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p164]
- TD learning updates value estimates according to V(St)new = V(St)old + η[rt + γV(St+1) - V(St)], where δ = rt + γV(St+1) - V(St) is the temporal difference prediction error. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p334]
- The temporal difference prediction error δ(t) is a natural error signal for improving estimates of value functions, reducing discrepancy between predicted and actual outcomes. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p335]
- TD learning was derived as a normative prediction learning rule related to dynamic programming methods. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p334]

## Inferences

- Inference: The TD learning algorithm solves the problem of learning without knowing the dynamics of the environment in advance, by using actual experienced rewards and state transitions as samples.
- Inference: The recursive relationship V(St) = Pr(St) + γΣ P(St+1|St)V(St+1) forms the consistency condition that TD learning seeks to satisfy.

## Uncertainties

- Uncertain: Whether the biological implementation of TD learning in dopamine neurons is exact or approximately TD is still being investigated.

## Related pages

- Broader: [[reinforcement-learning]]
- Broader: [[prediction-error]]
- Narrower: [[actor-critic]]
- Narrower: [[q-learning]]
- Adjacent: [[actor-critic-model]]
- Adjacent: [[reward-prediction-error]]
- Concepts: [[reinforcement learning]]
- Concepts: [[eligibility-trace]]
- Concepts: [[reinforcement-learning]]
- Concepts: [[prediction-error]]
- Concepts: [[reward-learning]]
- Concepts: [[actor-critic-model]]

## Provenance

- Primary source: [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p1-401]
- Additional source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]

## Change notes

- 2026-04-24 — page created by auto ingest.
- 2026-04-25 — merged contributions from `neuroeconomics-decision-making-and-the-brain-paul-w-glimcher`.
