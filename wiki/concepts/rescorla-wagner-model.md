---
id: rescorla-wagner-model
title: Rescorla-Wagner Model
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_
  Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]'
confidence: high
tags:
- learning-theory
- pavlovian-conditioning
- prediction-error
- associative-learning
related:
  broader:
  - pavlovian-conditioning
  - associative-learning
  narrower:
  - temporal-difference-learning
  adjacent: []
---


# Rescorla-Wagner Model

## Summary

The Rescorla-Wagner model is a classic error-correcting learning rule that explains Pavlovian conditioning phenomena such as blocking, overshadowing, and conditioned inhibition. It postulates that learning occurs only when events violate expectations, driven by the discrepancy between predicted and actual outcomes.

## Key facts

- The Rescorla-Wagner learning rule states: Vnew(CSi) = Vold(CSi) + η(CSi,US)[λ(US) - ΣiVold(CSi)], where learning is driven by the error between predicted and actual outcomes. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p333]
- The model explains blocking, where conditioning of a second stimulus fails when the first stimulus already fully predicts the unconditioned stimulus. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p333]
- Learning in the Rescorla-Wagner model occurs only when events are surprising, i.e., when actual outcomes exceed predictions. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p333]

## Inferences

- Inference: The Rescorla-Wagner model provided the foundation for temporal difference learning by introducing the error-correcting principle that learning depends on prediction errors.
- Inference: The two key assumptions of the model—that learning occurs only when predictions are violated and that predictions from multiple stimuli are summed—enabled parsimonious explanations of various conditioning phenomena.

## Uncertainties

- Uncertain: The model's assumption that conditional and unconditional stimuli are qualitatively different limits its ability to explain second-order conditioning.
- Uncertain: The discrete trial-based nature of the model does not fully account for temporal relationships within conditioning trials.

## Related pages

- Broader: [[pavlovian-conditioning]]
- Broader: [[associative-learning]]
- Narrower: [[temporal-difference-learning]]
- Concepts: [[blocking]]
- Concepts: [[overshadowing]]
- Concepts: [[conditioned-inhibition]]
- Concepts: [[prediction-error]]

## Provenance

- Primary source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]

## Change notes

- 2026-04-24 — page created by auto ingest.
