---
id: mediation-analysis
title: Mediation Analysis
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/strategy/The_Book_of_Why.epub#L1-L1]'
confidence: high
tags:
- causal-inference
- mechanism
- path-analysis
- statistics
related:
  broader:
  - causal-inference
  - counterfactuals
  narrower:
  - natural-direct-effect
  - natural-indirect-effect
  - controlled-direct-effect
  - mediation-formula
  adjacent: []
---


# Mediation Analysis

## Summary

Mediation analysis seeks to disentangle direct and indirect effects of a treatment on an outcome. A mediator transmits part of the treatment's effect through a causal pathway, while direct effects bypass the mediator.

## Key facts

- A mediator transmits the effect of treatment to outcome, as in Smoking → Tar → Cancer where Tar is the mediator. [raw/books/strategy/The_Book_of_Why.epub#L2555-L2565]
- Mediation analysis aims to determine whether an effect is entirely indirect (through mediator), entirely direct, or partially both. [raw/books/strategy/The_Book_of_Why.epub#L2565-L2575]
- Direct and indirect effects require counterfactual definitions and occupy the third rung of the Ladder of Causation. [raw/books/strategy/The_Book_of_Why.epub#L2575-L2583]
- If smoking causes cancer only through tar deposits, then eliminating tar (e.g., via e-cigarettes) would eliminate the excess cancer risk. [raw/books/strategy/The_Book_of_Why.epub#L2565-L2575]
- Mediation analysis decomposes the total effect of X on Y into direct and indirect effects. [raw/books/strategy/The_Book_of_Why.epub#L2800-L2810]
- The Baron-Kenny method, developed in 1986, was the dominant approach but is based on linear models and has significant limitations. [raw/books/strategy/The_Book_of_Why.epub#L2950-L2970]
- The Baron-Kenny article ranks 33rd among most frequently cited scientific papers of all time with over 73,000 citations. [raw/books/strategy/The_Book_of_Why.epub#L2960-L2965]
- The Mediation Formula allows estimation of natural direct and indirect effects from observational data under transparent assumptions. [raw/books/strategy/The_Book_of_Why.epub#L3100-L3120]
- In nonlinear models, the simple additivity equation Total Effect = Direct Effect + Indirect Effect does not always hold. [raw/books/strategy/The_Book_of_Why.epub#L2975-L2990]
- Conditioning on a mediator when estimating total effect introduces bias, a mistake called the Mediation Fallacy. [raw/books/strategy/The_Book_of_Why.epub#L2765-L2775]

## Inferences

- Inference: Understanding mediation has direct policy implications: targeting the mediator may be sufficient to intervene on the outcome without eliminating the original cause.
- Inference: The Mediation Formula represents a major advance because it connects rung-three counterfactual concepts to rung-one observational data, enabling practical estimation.
- Inference: The limitations of linear models for mediation analysis explain why the Baron-Kenny approach fails in many real-world applications.

## Related pages

- Broader: [[causal-inference]]
- Broader: [[counterfactuals]]
- Narrower: [[natural-direct-effect]]
- Narrower: [[natural-indirect-effect]]
- Narrower: [[controlled-direct-effect]]
- Narrower: [[mediation-formula]]
- Concepts: [[direct-effect]]
- Concepts: [[indirect-effect]]
- Concepts: [[mediator]]
- Concepts: [[path-analysis]]
- Concepts: [[confounding]]
- Concepts: [[collider-bias]]
- Entities: [[judea-pearl]]

## Provenance

- Primary source: [raw/books/strategy/The_Book_of_Why.epub#L1-L1]

## Change notes

- 2026-04-25 — page created by auto ingest.
