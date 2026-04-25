---
id: collider-bias
title: Collider Bias
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/strategy/The_Book_of_Why.epub#L1-L1]'
confidence: high
tags:
- causal-reasoning
- bias
- selection-bias
- colliders
related:
  broader:
  - causal-junctions
  - causal-diagrams
  - bayesian-networks
  narrower:
  - birth-weight-paradox
  - berksons-paradox
  - monty-hall-problem
  - m-bias
  adjacent:
  - chain-junction
  - fork-junction
  - back-door-criterion
---


# Collider Bias

## Summary

Collider bias (also called collider bias, the explain-away effect, or Berkson bias) arises when two independent causes jointly influence a common effect. Conditioning on the collider (the common effect) creates a spurious dependence between its causes. This mechanism explains numerous counterintuitive phenomena including the birth-weight paradox, Berkson's paradox, the Monty Hall problem, and the apparent correlation between attractiveness and niceness among dates. It is a core building block of causal diagrams and is essential for understanding when statistical associations are misleading.

## Key facts

- In a collider structure A → B ← C, variables A and C are unconditionally independent, but become dependent when conditioned on B, due to the explain-away effect. [raw/books/strategy/The_Book_of_Why.epub#L1015-L1025]
- Collider bias is the mechanism behind the birth-weight paradox: among low-birth-weight babies, maternal smoking appears protective because Birth Weight is a collider on paths from Smoking and Birth Defect to Mortality. [raw/books/strategy/The_Book_of_Why.epub#L1670-L1685]
- Berkson's paradox states that two independent diseases can appear associated among hospitalized patients because Hospitalization is a collider (both diseases can contribute to hospitalization). [raw/books/strategy/The_Book_of_Why.epub#L1650-L1665]
- The Monty Hall problem arises because Door Opened is a collider: conditioning on which door Monty opens creates a spurious dependence between the player's initial choice and the car's location. [raw/books/strategy/The_Book_of_Why.epub#L1700-L1710]
- M-bias occurs when conditioning on a pre-treatment variable B that is a collider on a path X ← A → B ← C → Y creates confounding rather than eliminating it. [raw/books/strategy/The_Book_of_Why.epub#L1550-L1565]
- Controlling for descendants (proxies) of a variable partially replicates the effect of controlling for the variable itself; controlling for a descendant of a collider partially opens the pipe. [raw/books/strategy/The_Book_of_Why.epub#L1505-L1515]

## Inferences

- Inference: Reichenbach's common cause principle ('no correlation without causation') was too strong because it failed to account for collider structures created by data selection processes. Correlations can arise from conditioning on colliders without any causal connection.

## Related pages

- Broader: [[causal-junctions]]
- Broader: [[causal-diagrams]]
- Broader: [[bayesian-networks]]
- Narrower: [[birth-weight-paradox]]
- Narrower: [[berksons-paradox]]
- Narrower: [[monty-hall-problem]]
- Narrower: [[m-bias]]
- Adjacent: [[chain-junction]]
- Adjacent: [[fork-junction]]
- Adjacent: [[back-door-criterion]]
- Concepts: [[d-separation]]
- Concepts: [[causal-junctions]]
- Concepts: [[bayesian-networks]]
- Concepts: [[conditional-independence]]

## Provenance

- Primary source: [raw/books/strategy/The_Book_of_Why.epub#L1-L1]

## Change notes

- 2026-04-25 — page created by auto ingest.
