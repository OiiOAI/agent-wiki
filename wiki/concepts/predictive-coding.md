---
id: predictive-coding
title: Predictive Coding
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- predictive coding
- neuroscience
- prediction error
- hierarchical
- message passing
- dopamine
related:
  broader:
  - Active Inference
  - Bayesian brain hypothesis
  - process theory
  - active-inference
  - message-passing
  narrower:
  - prediction error
  - prediction
  - precision
  - synaptic gain
  - dopamine
  - hierarchical message passing
  - prediction-error
  - hierarchical-message-passing
  adjacent:
  - Helmholtz machine
  - variational inference
  - predictive processing
  - neural coding
---


# Predictive Coding

## Summary

Predictive coding is a neuroscientific theory (Rao and Ballard 1999) positing that the brain constantly predicts incoming sensory stimuli at multiple hierarchical levels, with prediction errors propagating between levels. Under the Active Inference framework, predictive coding emerges as a specific process theory—specifically, the neural implementation of variational free energy minimization for continuous-time generative models. In this framework, predictions flow top-down while prediction errors (the difference between predicted and actual sensory input) flow bottom-up. Precision of predictions corresponds to synaptic gain of prediction error units; precision of policies corresponds to dopaminergic activity. The dynamics that emerge from the continuous-time generative models used in Active Inference closely correspond to established predictive coding models.

## Key facts

- Under Active Inference, prediction errors flow bottom-up between hierarchical levels while predictions flow top-down, minimizing the discrepancy between predictions and sensory data. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p10]
- Predictive coding emerges as the process theory of Active Inference, showing how the abstract computational principles of Active Inference map to specific neural computations. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p10]
- Precision of predictions (in predictive coding) corresponds to the synaptic gain of prediction error units, and precision of policies corresponds to dopaminergic activity. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p10]
- The dynamics from continuous-time generative models in Active Inference closely correspond to predictive coding and the Helmholtz machine as specific algorithmic implementations. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p10]
- In predictive coding, higher levels send descending predictions to lower levels, which compute errors in these predictions and pass these errors back up the hierarchy to update beliefs. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p91]
- Ascending messages—originating from error units—may be measurable in higher frequency bands than descending messages—originating from expectation units. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p97]
- Ascending connections are typically associated with gamma frequencies and descending connections with alpha or beta bands. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p97]
- Active Inference can be understood as predictive coding plus reflex arcs at the lowest level of the hierarchy. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p92]

## Inferences

- Inference: Because predictive coding and the Helmholtz machine both implement some form of approximate Bayesian inference, and Active Inference provides the normative framework that justifies these as implementations of variational free energy minimization, Active Inference can be seen as unifying these earlier neuroscientific theories under a first-principles justification.

## Related pages

- Broader: [[Active Inference]]
- Broader: [[Bayesian brain hypothesis]]
- Broader: [[process theory]]
- Broader: [[active-inference]]
- Broader: [[message-passing]]
- Narrower: [[prediction error]]
- Narrower: [[prediction]]
- Narrower: [[precision]]
- Narrower: [[synaptic gain]]
- Narrower: [[dopamine]]
- Narrower: [[hierarchical message passing]]
- Narrower: [[prediction-error]]
- Narrower: [[hierarchical-message-passing]]
- Adjacent: [[Helmholtz machine]]
- Adjacent: [[variational inference]]
- Adjacent: [[predictive processing]]
- Adjacent: [[neural coding]]
- Concepts: [[prediction error]]
- Concepts: [[prediction]]
- Concepts: [[precision]]
- Concepts: [[synaptic gain]]
- Concepts: [[dopamine]]
- Concepts: [[hierarchical message passing]]
- Concepts: [[variational free energy]]
- Concepts: [[Active Inference]]
- Concepts: [[generative model]]
- Concepts: [[active-inference]]
- Concepts: [[message-passing]]
- Concepts: [[hierarchical-inference]]
- Concepts: [[prediction-error]]
- Concepts: [[cortical-microcircuit]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
