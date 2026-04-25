---
id: potential-outcomes
title: Potential Outcomes
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/strategy/The_Book_of_Why.epub#L1-L1]'
confidence: high
tags:
- causal-inference
- potential-outcomes
- statistics
- missing-data
related:
  broader:
  - causal-inference
  - counterfactuals
  narrower: []
  adjacent: []
---


# Potential Outcomes

## Summary

Potential outcomes (Neyman-Rubin causal model) express causal effects as the difference between outcomes that would have occurred under different treatment conditions. Developed by Jerzy Neyman in 1923 and expanded by Donald Rubin in the 1970s.

## Key facts

- A potential outcome Y_x(u) represents the value Y would have taken for individual u had X been assigned value x. [raw/books/strategy/The_Book_of_Why.epub#L2470-L2480]
- The fundamental problem of causal inference is that at most one potential outcome can be observed for any individual. [raw/books/strategy/The_Book_of_Why.epub#L2485-L2495]
- The ignorability assumption requires Y_x be independent of X given confounders Z. [raw/books/strategy/The_Book_of_Why.epub#L2515-L2525]
- Pearl argues that ignorability is difficult to assess without causal diagrams, as it requires speculating about potential outcomes to determine if they are independent of treatment. [raw/books/strategy/The_Book_of_Why.epub#L2525-L2540]

## Inferences

- Inference: The SCM approach and potential outcomes approach differ primarily in the use of causal diagrams for representing and testing causal assumptions.

## Uncertainties

- Uncertain: Whether ignorability holds in any given problem requires assumptions that are difficult to assess without additional causal structure.

## Related pages

- Broader: [[causal-inference]]
- Broader: [[counterfactuals]]
- Concepts: [[counterfactuals]]
- Concepts: [[structural-causal-models]]
- Concepts: [[ignorability]]
- Concepts: [[matching]]
- Entities: [[jerzy-neyman]]
- Entities: [[donald-rubin]]
- Entities: [[paul-holland]]

## Provenance

- Primary source: [raw/books/strategy/The_Book_of_Why.epub#L1-L1]

## Change notes

- 2026-04-25 — page created by auto ingest.
