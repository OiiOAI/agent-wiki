---
id: controlled-direct-effect
title: Controlled Direct Effect (CDE)
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/strategy/The_Book_of_Why.epub#L1-L1]'
confidence: high
tags:
- mediation
- direct-effect
- do-calculus
related:
  broader:
  - mediation-analysis
  narrower: []
  adjacent: []
---


# Controlled Direct Effect (CDE)

## Summary

The Controlled Direct Effect (CDE) measures the effect of X on Y when the mediator M is held constant at a specific value. Unlike the natural direct effect, CDE can be expressed using do-operators and estimated using do-calculus. However, CDE can take different values depending on what value the mediator is held at, and forcing everyone to the same mediator value may create unnatural scenarios.

## Key facts

- CDE is defined by 'wiggling' X while holding M at a fixed value for everyone. [raw/books/strategy/The_Book_of_Why.epub#L2815-L2825]
- CDE can be expressed as a do-expression: CDE(0) = P(Y=1 | do(X=1), do(M=0)) - P(Y=1 | do(X=0), do(M=0)). [raw/books/strategy/The_Book_of_Why.epub#L2820-L2828]
- CDE requires specifying which value to hold M at, leading to different versions CDE(0), CDE(1), etc. [raw/books/strategy/The_Book_of_Why.epub#L2825-L2835]
- In nonlinear models, CDE depends on the chosen value of M, unlike in linear models. [raw/books/strategy/The_Book_of_Why.epub#L3000-L3015]

## Related pages

- Broader: [[mediation-analysis]]
- Concepts: [[direct-effect]]
- Concepts: [[do-calculus]]
- Concepts: [[natural-direct-effect]]

## Provenance

- Primary source: [raw/books/strategy/The_Book_of_Why.epub#L1-L1]

## Change notes

- 2026-04-25 — page created by auto ingest.
