---
id: probability-weighting
title: Probability Weighting
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_
  Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]'
confidence: high
tags:
- probability
- decision-weights
- behavioral-economics
related:
  broader:
  - prospect-theory
  narrower: []
  adjacent:
  - value-function
  - loss-aversion
  - allais-paradox
---


# Probability Weighting

## Summary

Probability weighting is a key component of Prospect Theory describing how decision makers psychologically transform objective probabilities. The weighting function is typically inverse-S shaped: low probabilities are overweighted while moderate to high probabilities are underweighted. This distortion explains the Allais paradox and the fourfold pattern of risk attitudes.

## Key facts

- The weighting function is inverse-S shaped, concave near zero and convex near one, with w(0) = 0 and w(1) = 1. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p143]
- Decision weights of complementary probabilities sum to less than one (w(p) + w(1-p) < 1), a property known as subcertainty. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p149]
- The common parameterization w(p) = δp^γ / (δp^γ + (1-p)^γ) from Lattimore et al. (1992) has δ measuring elevation and γ measuring curvature. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p149]
- Prelec's (1998) weighting function w(p) = exp[-δ(-ln p)^γ] accommodates overweighting of low probabilities, subproportionality, and subadditivity of decision weights. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p150]

## Uncertainties

- Uncertain: Measured weighting function parameters vary considerably across individuals, with γ estimates ranging from 0.15 to 0.89 in some samples.

## Related pages

- Broader: [[prospect-theory]]
- Adjacent: [[value-function]]
- Adjacent: [[loss-aversion]]
- Adjacent: [[allais-paradox]]
- Concepts: [[prospect-theory]]
- Concepts: [[cumulative-prospect-theory]]
- Concepts: [[value-function]]

## Provenance

- Primary source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]

## Change notes

- 2026-04-24 — page created by auto ingest.
