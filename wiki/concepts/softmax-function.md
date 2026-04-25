---
id: softmax-function
title: Softmax function
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_
  Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]'
confidence: high
tags:
- decision-making
- action-selection
- probabilistic-choice
- softmax
related:
  broader: []
  narrower: []
  adjacent: []
---


# Softmax function

## Summary

The softmax function is the most commonly used probabilistic action selection mechanism in neuroeconomics, converting putative decision variables (subjective desirability values) into concrete predictions about choice by transforming them into probabilities via an exponential function. It takes the form p_chose(i) = exp(κ D_i) / Σ_j exp(κ D_j), where κ describes the steepness of the relationship between desirability and probability. Steep κ values approximate deterministic 'choose-the-best' behavior, while lower κ values introduce modest biases. The softmax function serves as the action selection stage in both reinforcement learning models and attractor network models of decision making.

## Key facts

- The softmax function computes the probability of choosing option i as p_chose(i) = exp(κ D_i) / Σ_j exp(κ D_j), where κ controls steepness. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p456]
- High κ values (steep sigmoid) make the softmax approximate deterministic argmax behavior, effectively always choosing the most desirable option. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p456]
- Low κ values (shallow sigmoid) introduce only modest biases in favor of the more desirable option, even for large differences in desirability. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p456]
- Probabilistic models with very steep decision criteria subsume deterministic models, accommodating behavior even when data are best described by a nearly perfect mapping from desirability to choice. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p456]
- The softmax rule is widely used as the action selection stage in reinforcement learning models of monkey choice behavior, selected after comparing a variety of rules using maximum likelihood techniques. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p460]
- A recurrent neural circuit model can produce a softmax-style decision criterion as an emergent property of stochastic spiking dynamics, where the probability of choosing A versus B is a sigmoid function of the difference in synaptic strengths cA minus cB. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p492]

## Inferences

- Inference: The universality of the softmax across behavioral models (reinforcement learning, attractor networks) suggests it may reflect a fundamental computational principle of the brain's choice circuitry rather than an arbitrary mathematical convenience.

## Uncertainties

- Uncertain: The neurobiological implementation of κ (steepness parameter) — whether it arises from synaptic properties, network architecture, or neuromodulation — remains unspecified.

## Related pages

- Concepts: [[drift-diffusion-model]]
- Concepts: [[action-selection]]
- Concepts: [[reinforcement-learning]]
- Concepts: [[subjective-value]]
- Concepts: [[attractor-network]]
- Concepts: [[win-stay-lose-switch]]

## Provenance

- Primary source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]

## Change notes

- 2026-04-24 — page created by auto ingest.
