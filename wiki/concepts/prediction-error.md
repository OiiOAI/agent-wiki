---
id: prediction-error
title: Prediction Error
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-25'
sources:
- '[raw/books/neuroscience/Anxious - Joseph LeDoux.pdf#p1-610]'
- '[raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_
  Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]'
confidence: high
related:
  broader:
  - learning
  - conditioning
  - reinforcement-learning
  - dopamine
  narrower:
  - temporal-difference-learning
  - rescorla-wagner-model
  adjacent:
  - extinction
  - reconsolidation
tags:
- prediction-error
- dopamine
- reinforcement-learning
- reward
aliases: []
---

# Prediction Error

## Summary

Prediction error is a mismatch between expected and actual outcomes that drives new learning. In the Rescorla-Wagner model of conditioning, learning occurs when an outcome is surprising or unexpected. During extinction, the absence of the expected US creates a prediction error that triggers new learning (CS–no US association). Creating greater expectancy violations during extinction should improve therapeutic outcomes, which is why cognitive interventions may be better applied after exposure rather than during it.

## Key facts

- Prediction errors have been shown to be a significant factor in Pavlovian threat conditioning, extinction, and reinforcement of instrumental responses. [raw/books/neuroscience/Anxious - Joseph LeDoux.pdf#p375]
- Prediction error triggers new learning during extinction when the absence of the US conflicts with learned expectations. [raw/books/neuroscience/Anxious - Joseph LeDoux.pdf#p375]
- In temporal difference learning, the prediction error δ(t) = rt + γV(St+1) - V(St) drives learning, with positive errors when outcomes exceed predictions and negative errors when outcomes fall short. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p324]
- Dopamine neurons show phasic bursts when rewards are better than predicted (positive prediction error), no response when predicted (no error), and pauses when worse than predicted (negative prediction error). [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p325]
- During conditioning, the dopamine response shifts from the unpredicted reward to the reward-predicting conditioned stimulus, consistent with back-propagating prediction errors. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p326]

## Inferences

- Inference: The close correspondence between dopamine neuron firing patterns and TD prediction errors suggests that dopamine encodes a teaching signal for learning.
- Inference: Prediction error signals allow efficient information processing by updating only the discrepancy rather than transmitting full information about states.

## Uncertainties

- Uncertain: Whether dopamine encodes pure prediction errors or also incorporates motivational or attention-related signals is still debated.

## Related pages

- Broader: [[learning]]
- Broader: [[conditioning]]
- Broader: [[reinforcement-learning]]
- Broader: [[dopamine]]
- Narrower: [[temporal-difference-learning]]
- Narrower: [[rescorla-wagner-model]]
- Adjacent: [[extinction]]
- Adjacent: [[reconsolidation]]
- Concepts: [[expectancy]]
- Concepts: [[surprise]]
- Concepts: [[dopamine]]
- Concepts: [[reinforcement-learning]]
- Concepts: [[learning-signal]]

## Provenance

- Primary source: [raw/books/neuroscience/Anxious - Joseph LeDoux.pdf#p1-610]
- Additional source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]

## Change notes

- 2026-04-24 — page created by auto ingest.
- 2026-04-25 — merged contributions from `neuroeconomics-decision-making-and-the-brain-paul-w-glimcher`.
