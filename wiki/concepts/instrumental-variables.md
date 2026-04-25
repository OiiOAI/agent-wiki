---
id: instrumental-variables
title: Instrumental Variables
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/strategy/The_Book_of_Why.epub#L1-L1]'
confidence: high
tags:
- causal-inference
- identification
- natural-experiment
- epidemiology
related:
  broader:
  - causal-inference
  - intervention
  narrower: []
  adjacent:
  - front-door-adjustment
  - mendelian-randomization
---


# Instrumental Variables

## Summary

Instrumental variables enable causal effect estimation when confounders cannot be measured, using a variable that affects the treatment but has no direct effect on the outcome except through the treatment. Dr. John Snow's water company study is the historical archetype.

## Key facts

- An instrumental variable Z must satisfy: (1) Z is independent of confounders, (2) no direct path from Z to Y, (3) Z affects X. [raw/books/strategy/The_Book_of_Why.epub#L2285-L2295]
- Dr. John Snow used water company as an instrumental variable to establish that contaminated water caused cholera, even without measuring the confounder 'miasma'. [raw/books/strategy/The_Book_of_Why.epub#L2265-L2285]
- Snow noted that districts served by both companies had different death rates despite no difference in miasma or poverty, as if a randomized experiment had been conducted. [raw/books/strategy/The_Book_of_Why.epub#L2295-L2310]
- Philip Wright (Sewall Wright's father) independently developed instrumental variables in 1928 for studying supply elasticity. [raw/books/strategy/The_Book_of_Why.epub#L2330-L2345]
- The formula b = r_ZY / r_ZX estimates the causal effect of X on Y using instrumental variable Z in linear models. [raw/books/strategy/The_Book_of_Why.epub#L2320-L2330]

## Inferences

- Inference: Snow's insight anticipated randomization by centuries, recognizing natural experiments where treatment assignment mimicked random allocation.

## Related pages

- Broader: [[causal-inference]]
- Broader: [[intervention]]
- Adjacent: [[front-door-adjustment]]
- Adjacent: [[mendelian-randomization]]
- Concepts: [[confounding]]
- Concepts: [[noncompliance]]
- Concepts: [[monotonicity]]
- Concepts: [[local-average-treatment-effect]]
- Entities: [[john-snow]]
- Entities: [[philip-wright]]
- Entities: [[sewall-wright]]

## Provenance

- Primary source: [raw/books/strategy/The_Book_of_Why.epub#L1-L1]

## Change notes

- 2026-04-25 — page created by auto ingest.
