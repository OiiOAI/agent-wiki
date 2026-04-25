---
id: probability-weighting
title: Probability Weighting
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-25'
sources:
- '[raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_
  Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]'
- '[raw/books/strategy/Thinking, Fast and Slow (Cover Baru) - Daniel Kahneman.pdf#p1-655]'
confidence: high
tags:
- probability
- decision-weights
- behavioral-economics
- probability-weighting
- prospect-theory
- decision-making
- certainty-effect
related:
  broader:
  - prospect-theory
  adjacent:
  - value-function
  - loss-aversion
  - allais-paradox
aliases: []
---

# Probability Weighting

## Summary

Probability weighting is a key component of Prospect Theory describing how decision makers psychologically transform objective probabilities. The weighting function is typically inverse-S shaped: low probabilities are overweighted while moderate to high probabilities are underweighted. This distortion explains the Allais paradox and the fourfold pattern of risk attitudes.

## Key facts

- The weighting function is inverse-S shaped, concave near zero and convex near one, with w(0) = 0 and w(1) = 1. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p143]
- Decision weights of complementary probabilities sum to less than one (w(p) + w(1-p) < 1), a property known as subcertainty. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p149]
- The common parameterization w(p) = δp^γ / (δp^γ + (1-p)^γ) from Lattimore et al. (1992) has δ measuring elevation and γ measuring curvature. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p149]
- Prelec's (1998) weighting function w(p) = exp[-δ(-ln p)^γ] accommodates overweighting of low probabilities, subproportionality, and subadditivity of decision weights. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p150]
- Decision weights deviate from probabilities: a 2% chance has a decision weight of about 8.1—over four times its objective probability—demonstrating the possibility effect. [raw/books/strategy/Thinking, Fast and Slow (Cover Baru) - Daniel Kahneman.pdf#p407]
- The certainty effect is even stronger: a 2% chance of losing a reward reduces utility from 100 to 87.1, showing that near-certain outcomes receive disproportionately high decision weight. [raw/books/strategy/Thinking, Fast and Slow (Cover Baru) - Daniel Kahneman.pdf#p407]
- The asymmetry between the possibility effect and certainty effect creates low sensitivity to probability changes in the mid-range: probabilities between 5% and 95% map to decision weights of only 13.7 to 79.3, roughly two-thirds of the rational range. [raw/books/strategy/Thinking, Fast and Slow (Cover Baru) - Daniel Kahneman.pdf#p407]
- Richly described outcomes reduce the role of probability in evaluation: participants asked about a 21% or 84% chance of receiving a dozen red roses in a glass vase showed far less sensitivity to probability than when the same probabilities were attached to monetary outcomes. [raw/books/strategy/Thinking, Fast and Slow (Cover Baru) - Daniel Kahneman.pdf#p421]
- The denominator neglect (or ratio neglect) bias causes 30–40% of students to choose a jar with more winning marbles (8 out of 100) over one with a higher probability of winning (1 out of 10), because the salient winning marbles draw attention away from the total number of marbles. [raw/books/strategy/Thinking, Fast and Slow (Cover Baru) - Daniel Kahneman.pdf#p424]

## Uncertainties

- Uncertain: Measured weighting function parameters vary considerably across individuals, with γ estimates ranging from 0.15 to 0.89 in some samples.

## Inferences

- Inference: Probability weighting explains why risk communication often fails: a risk stated as '1 in 10,000' is more alarming than the same risk stated as '0.01%' because the frequency format evokes a concrete image that receives excessive decision weight.

## Related pages

- Broader: [[prospect-theory]]
- Adjacent: [[value-function]]
- Adjacent: [[loss-aversion]]
- Adjacent: [[allais-paradox]]
- Concepts: [[prospect-theory]]
- Concepts: [[cumulative-prospect-theory]]
- Concepts: [[value-function]]
- Concepts: [[possibility-effect]]
- Concepts: [[certainty-effect]]
- Concepts: [[framing-effect]]
- Concepts: [[availability-heuristic]]

## Provenance

- Primary source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]
- Additional source: [raw/books/strategy/Thinking, Fast and Slow (Cover Baru) - Daniel Kahneman.pdf#p1-655]

## Change notes

- 2026-04-24 — page created by auto ingest.
- 2026-04-25 — merged contributions from `thinking-fast-and-slow-cover-baru-daniel-kahneman`.
