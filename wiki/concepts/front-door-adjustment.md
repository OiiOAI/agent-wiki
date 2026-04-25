---
id: front-door-adjustment
title: Front-Door Adjustment
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/strategy/The_Book_of_Why.epub#L1-L1]'
confidence: high
tags:
- causal-inference
- mediator
- unmeasured-confounding
- statistics
related:
  broader:
  - causal-inference
  - intervention
  narrower: []
  adjacent:
  - back-door-adjustment
  - instrumental-variables
---


# Front-Door Adjustment

## Summary

Front-door adjustment enables estimation of causal effects even when confounders are unmeasured, by exploiting a shielded mediator on the causal pathway. It was published by Pearl and provides an estimand that does not involve the unmeasured confounder.

## Key facts

- Front-door adjustment requires: (1) a causal effect mediated by variable(s) M, (2) no unblocked back-door paths from treatment to M, (3) M shielded from the effects of confounders. [raw/books/strategy/The_Book_of_Why.epub#L2050-L2065]
- The smoking-tar-cancer example demonstrates front-door adjustment: even without data on a smoking gene (confounder), the effect of smoking on cancer can be estimated through tar deposits. [raw/books/strategy/The_Book_of_Why.epub#L2035-L2050]
- Glynn and Kashin applied front-door adjustment to the JTPA Study, finding estimates that matched randomized controlled trial benchmarks much better than back-door estimates. [raw/books/strategy/The_Book_of_Why.epub#L2100-L2120]
- The front-door formula successfully deconfounds an unmeasured variable without needing any data on it. [raw/books/strategy/The_Book_of_Why.epub#L2070-L2085]

## Inferences

- Inference: Front-door adjustment represents a 'miracle' for statisticians of Fisher's generation, as it eliminates confounder effects without observing the confounder.

## Related pages

- Broader: [[causal-inference]]
- Broader: [[intervention]]
- Adjacent: [[back-door-adjustment]]
- Adjacent: [[instrumental-variables]]
- Concepts: [[front-door-criterion]]
- Concepts: [[mediator]]
- Concepts: [[shielded-mediator]]
- Concepts: [[do-calculus]]
- Entities: [[adam-glynn]]
- Entities: [[konstantin-kashin]]

## Provenance

- Primary source: [raw/books/strategy/The_Book_of_Why.epub#L1-L1]

## Change notes

- 2026-04-25 — page created by auto ingest.
