---
id: estimand
title: Estimand
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/strategy/The_Book_of_Why.epub#L1-L1]'
confidence: high
tags:
- estimation
- causal-methodology
- statistics
related:
  broader:
  - causal-inference
  - statistical-estimation
  narrower: []
  adjacent: []
---


# Estimand

## Summary

An estimand is a mathematical formula (recipe) derived from a causal model that specifies how to calculate the answer to a causal query from data. It is computed before data are examined and is valid across any dataset compatible with the causal model's qualitative structure.

## Key facts

- The term 'Estimand' comes from Latin meaning 'that which is to be estimated'. [raw/books/strategy/The_Book_of_Why.epub#L119]
- The estimand tells how to combine statistical quantities like P(L | D, Z) into an expression equivalent to the causal query P(L | do(D)). [raw/books/strategy/The_Book_of_Why.epub#L120]
- Some queries may not be answerable under a given causal model even with unlimited data, making the estimand impossible to derive. [raw/books/strategy/The_Book_of_Why.epub#L121-L122]
- The estimand is computed prior to examining data, making causal inference adaptable across different populations. [raw/books/strategy/The_Book_of_Why.epub#L136-L137]

## Inferences

- Inference: The distinction between estimand (the quantity to estimate) and estimate (the computed result) reflects a key principle of causal inference: model specification should precede data analysis.

## Related pages

- Broader: [[causal-inference]]
- Broader: [[statistical-estimation]]
- Concepts: [[causal query]]
- Concepts: [[estimate]]
- Concepts: [[causal model]]
- Concepts: [[adaptability]]
- Topics: [[statistics]]
- Topics: [[methodology]]

## Provenance

- Primary source: [raw/books/strategy/The_Book_of_Why.epub#L1-L1]

## Change notes

- 2026-04-25 — page created by auto ingest.
