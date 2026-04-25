---
id: simulated-annealing
title: Simulated Annealing
type: concept
status: draft
created: '2026-04-22'
updated: '2026-04-22'
sources:
- '[raw/books/strategy/Algorithms_to_Live_By.epub#L1-L1]'
confidence: high
tags:
- optimization
- algorithm
- randomness
- physics-metaphor
related:
  broader:
  - optimization-algorithms
  - randomized-algorithms
  narrower: []
  adjacent:
  - hill-climbing
  - metropolis-algorithm
  - random-restart-hill-climbing
---


# Simulated Annealing

## Summary

Simulated Annealing is an optimization algorithm that borrows from metallurgy's annealing process, where materials are heated and slowly cooled to achieve optimal crystalline structures. In computation, it applies gradual 'cooling'—reducing randomness over time—to escape local maxima and find near-optimal solutions to intractable problems like circuit chip layout.

## Key facts

- Simulated Annealing was developed by Scott Kirkpatrick and Dan Gelatt at IBM in the late 1970s and early 1980s. [raw/books/strategy/Algorithms_to_Live_By.epub#L1958-L1960]
- The algorithm starts at 'high temperature' by selecting solutions randomly, then slowly 'cools' by accepting fewer inferior moves as search continues. [raw/books/strategy/Algorithms_to_Live_By.epub#L1980-L1983]
- The paper by Kirkpatrick, Gelatt, and Vecchi has been cited over 32,000 times. [raw/books/strategy/Algorithms_to_Live_By.epub#L1989-L1990]
- Simulated annealing algorithms at IBM produced better chip layouts than the best human expert. [raw/books/strategy/Algorithms_to_Live_By.epub#L1987-L1988]

## Inferences

- Inference: The metaphor from metallurgy works because both physical annealing and algorithmic optimization involve finding global optima in complex, rugged landscapes with many local peaks.

## Uncertainties

- Uncertain: The book mentions initial skepticism from traditional optimization researchers but doesn't specify their specific objections beyond calling the approach 'messy' and 'analogy-based.'

## Related pages

- Broader: [[optimization-algorithms]]
- Broader: [[randomized-algorithms]]
- Adjacent: [[hill-climbing]]
- Adjacent: [[metropolis-algorithm]]
- Adjacent: [[random-restart-hill-climbing]]
- Concepts: [[hill-climbing]]
- Concepts: [[local-maxima]]
- Concepts: [[optimization]]
- Concepts: [[metropolis-algorithm]]
- Entities: [[scott-kirkpatrick]]
- Entities: [[dan-gelatt]]

## Provenance

- Primary source: [raw/books/strategy/Algorithms_to_Live_By.epub#L1-L1]

## Change notes

- 2026-04-22 — page created by auto ingest.
