---
id: back-door-adjustment
title: Back-Door Adjustment
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/strategy/The_Book_of_Why.epub#L1-L1]'
confidence: high
tags:
- causal-inference
- adjustment
- confounding
- statistics
related:
  broader:
  - causal-inference
  - intervention
  narrower: []
  adjacent: []
---


# Back-Door Adjustment

## Summary

The back-door adjustment is a method for estimating causal effects by controlling for confounders. It uses the back-door criterion to identify which variables must be controlled to block all non-causal pathways between treatment and outcome.

## Key facts

- The back-door adjustment formula computes the average causal effect by taking a weighted average of stratum-specific causal effects, weighting by the prevalence of each stratum in the population. [raw/books/strategy/The_Book_of_Why.epub#L1950-L1965]
- The back-door criterion guarantees that the causal effect in each stratum equals the observed trend in that stratum. [raw/books/strategy/The_Book_of_Why.epub#L1965-L1975]
- In linear models, partial regression coefficients perform back-door adjustment implicitly without explicit stratification. [raw/books/strategy/The_Book_of_Why.epub#L2000-L2010]
- Regression coefficients only represent causal effects when the adjusted variables satisfy the back-door criterion, not merely because they are adjusted. [raw/books/strategy/The_Book_of_Why.epub#L2010-L2020]

## Inferences

- Inference: The back-door criterion and back-door adjustment formula are two sides of the same coin—one identifies what to control, the other performs the deconfounding.

## Related pages

- Broader: [[causal-inference]]
- Broader: [[intervention]]
- Concepts: [[back-door-criterion]]
- Concepts: [[front-door-adjustment]]
- Concepts: [[do-calculus]]
- Concepts: [[confounding]]
- Concepts: [[partial-regression]]
- Topics: [[mount-intervention]]

## Provenance

- Primary source: [raw/books/strategy/The_Book_of_Why.epub#L1-L1]

## Change notes

- 2026-04-25 — page created by auto ingest.
