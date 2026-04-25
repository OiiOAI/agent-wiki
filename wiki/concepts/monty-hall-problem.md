---
id: monty-hall-problem
title: The Monty Hall Problem
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/strategy/The_Book_of_Why.epub#L1-L1]'
confidence: high
tags:
- probability
- paradoxes
- decision-theory
- causal-reasoning
related:
  broader:
  - paradoxes-in-probability
  - collider-bias
  narrower: []
  adjacent:
  - simpsons-paradox
  - berksons-paradox
  - birth-weight-paradox
---


# The Monty Hall Problem

## Summary

The Monty Hall problem is a probability puzzle that exposes the conflict between causal and probabilistic reasoning. A player chooses one of three doors; Monty Hall (who knows what is behind each door) opens a different door revealing a goat. The puzzle asks whether the player should switch. Switching doubles the probability of winning from 1/3 to 2/3 in the standard game, because the player's initial door and the car's location are unconditionally independent but become dependent upon conditioning on the opened door—a collider. When the game's rules change (Monty opens a door at random), the advantage disappears. The puzzle demonstrates that the data-generating process (not just the data) determines correct inference.

## Key facts

- In the standard Monty Hall game, switching doors wins with probability 2/3 while staying wins with probability 1/3, because Monty is constrained to open a door without a car, making the car location and the player's initial choice conditionally dependent. [raw/books/strategy/The_Book_of_Why.epub#L1690-L1705]
- If Monty opens a door at random (the 'Let's Fake a Deal' variant), the probability is 1/2 for both strategies because Monty could have opened the door with the car, making the game fundamentally different despite identical observed data. [raw/books/strategy/The_Book_of_Why.epub#L1715-L1725]
- Door Opened is a collider (affected by both Your Door and Car Location), and conditioning on a collider creates a spurious causal-like dependence between its parents—the source of the paradox. [raw/books/strategy/The_Book_of_Why.epub#L1700-L1710]
- Marilyn vos Savant's solution (switching) provoked over 10,000 letters of disagreement, including from PhDs in mathematics and statistics, because the solution requires accounting for the data-generating process rather than just the data. [raw/books/strategy/The_Book_of_Why.epub#L1685-L1695]
- The key insight is that Door 2 was vulnerable to refutation (Monty could have opened it) while Door 1 was not, so Door 2 becomes more likely as the car location after Monty opens Door 3. [raw/books/strategy/The_Book_of_Why.epub#L1725-L1735]

## Inferences

- Inference: The Monty Hall paradox reveals that human brains are wired for causal reasoning but not for probabilistic reasoning; our causal wiring produces systematic probabilistic mistakes, just like optical illusions. Persi Diaconis noted 'our brains are just not wired to do probability problems very well.'

## Related pages

- Broader: [[paradoxes-in-probability]]
- Broader: [[collider-bias]]
- Adjacent: [[simpsons-paradox]]
- Adjacent: [[berksons-paradox]]
- Adjacent: [[birth-weight-paradox]]
- Concepts: [[collider-bias]]
- Concepts: [[bayesian-reasoning]]
- Concepts: [[conditional-probability]]
- Concepts: [[causal-reasoning-vs-probabilistic]]

## Provenance

- Primary source: [raw/books/strategy/The_Book_of_Why.epub#L1-L1]

## Change notes

- 2026-04-25 — page created by auto ingest.
