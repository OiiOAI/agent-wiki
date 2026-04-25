---
id: do-calculus
title: Do-Calculus
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/strategy/The_Book_of_Why.epub#L1-L1]'
confidence: high
tags:
- causal-inference
- axiomatic-system
- do-operator
- identification
related:
  broader:
  - causal-inference
  - intervention
  narrower: []
  adjacent: []
---


# Do-Calculus

## Summary

Do-calculus is an axiomatic system with three rules that enables the transformation of do-expressions (intervention queries) into see-expressions (observational queries). It determines whether a causal effect can be estimated from observational data.

## Key facts

- Do-calculus consists of three rules: (1) addition/deletion of observations, (2) intervention/observation swapping, (3) addition/deletion of interventions. [raw/books/strategy/The_Book_of_Why.epub#L2155-L2170]
- The front-door formula was derived using do-calculus and presented as a challenge ('napkin problem') at Berkeley in 1993 with a $100 prize. [raw/books/strategy/The_Book_of_Why.epub#L2175-L2190]
- The completeness of do-calculus was proved independently by Yiming Huang and Marco Valtorta, and by Ilya Shpitser in 2006. [raw/books/strategy/The_Book_of_Why.epub#L2220-L2235]
- If do-calculus cannot find a way to estimate P(Y|do(X)) from observational data, then no solution exists without additional experiments. [raw/books/strategy/The_Book_of_Why.epub#L2235-L2245]
- Ilya Shpitser developed a polynomial-time algorithm to decide whether a causal effect is estimable. [raw/books/strategy/The_Book_of_Why.epub#L2245-L2255]

## Inferences

- Inference: Do-calculus enables researchers to systematically explore all possible routes to estimating causal effects without physical experimentation.

## Related pages

- Broader: [[causal-inference]]
- Broader: [[intervention]]
- Concepts: [[back-door-adjustment]]
- Concepts: [[front-door-adjustment]]
- Concepts: [[do-operator]]
- Concepts: [[d-separation]]
- Entities: [[judea-pearl]]
- Entities: [[ilya-shpitser]]
- Entities: [[james-robins]]
- Entities: [[sander-greenland]]

## Provenance

- Primary source: [raw/books/strategy/The_Book_of_Why.epub#L1-L1]

## Change notes

- 2026-04-25 — page created by auto ingest.
