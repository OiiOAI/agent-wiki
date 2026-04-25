---
id: epistemic-value
title: Epistemic Value
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- epistemic-value
- information-gain
- exploration
- curiosity
related:
  broader:
  - expected-free-energy
  - active-learning
  narrower:
  - salience
  - novelty
  - information-gain
  adjacent: []
---


# Epistemic Value

## Summary

Epistemic value is the drive toward information gathering in Active Inference, arising from the expected free energy. It comprises posterior predictive entropy (total uncertainty about what would be observed) minus expected ambiguity (irreducible uncertainty due to weak state-observation associations). Epistemic value explains why agents explore to resolve uncertainty.

## Key facts

- Epistemic value equals posterior predictive entropy minus expected ambiguity: I(π) = H[Q(o|π)] - E_Q(s|π)[H[P(o|s)]]. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p141]
- Posterior predictive entropy quantifies uncertainty about what would be observed if a given action were performed. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p143]
- Expected ambiguity quantifies the degree to which observations and states are independent, being maximal when there is no association between states and outcomes. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p143]
- The best saccades (or perceptual experiments) are those for which there is greatest uncertainty to resolve but only if that uncertainty can be resolved. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p143]

## Related pages

- Broader: [[expected-free-energy]]
- Broader: [[active-learning]]
- Narrower: [[salience]]
- Narrower: [[novelty]]
- Narrower: [[information-gain]]
- Concepts: [[expected-free-energy]]
- Concepts: [[exploration]]
- Concepts: [[information-theory]]
- Concepts: [[active-learning]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
