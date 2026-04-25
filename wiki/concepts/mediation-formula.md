---
id: mediation-formula
title: Mediation Formula
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/strategy/The_Book_of_Why.epub#L1-L1]'
confidence: high
tags:
- mediation
- formula
- identification
related:
  broader:
  - mediation-analysis
  - causal-mediation-analysis
  narrower: []
  adjacent:
  - natural-direct-and-indirect-effects
  - mediation-fallacy
---


# Mediation Formula

## Summary

The Mediation Formula is a mathematical expression derived by Judea Pearl that allows estimation of natural direct and indirect effects from observational data without requiring experimental intervention. It translates counterfactual definitions into expressions involving only standard conditional probabilities. The formula makes no assumptions about the functional form of relationships between variables, generalizing beyond the linear models that earlier methods required.

## Key facts

- The Mediation Formula translates NDE and NIE from counterfactual notation to expressions that can be estimated from rung-one data. [raw/books/strategy/The_Book_of_Why.epub#L3100-L3115]
- The formula requires assumptions about confounding that are transparently displayed in causal graphs. [raw/books/strategy/The_Book_of_Why.epub#L3105-L3115]
- For natural indirect effect: NIE = Σ_m [P(M=m|X=1) - P(M=m|X=0)] × P(Y=1|X=0, M=m). [raw/books/strategy/The_Book_of_Why.epub#L3115-L3125]
- The Mediation Formula makes mediation analysis applicable to nonlinear, numerical or logical relationships. [raw/books/strategy/The_Book_of_Why.epub#L3105-L3110]
- The Mediation Formula was introduced by Pearl (2001). [raw/books/strategy/The_Book_of_Why.epub#L3888-L3889]
- The formula provides a method for computing natural direct and indirect effects. [raw/books/strategy/The_Book_of_Why.epub#L3888-L3889]
- Pearl's work on the Mediation Formula legitimized the use of natural direct and indirect effects. [raw/books/strategy/The_Book_of_Why.epub#L3888-L3889]

## Inferences

- Inference: The Mediation Formula solved a problem that William Kruskal once called 'perhaps insoluble' regarding which variables to control for in mediation analysis.

## Related pages

- Broader: [[mediation-analysis]]
- Broader: [[causal-mediation-analysis]]
- Adjacent: [[natural-direct-and-indirect-effects]]
- Adjacent: [[mediation-fallacy]]
- Concepts: [[counterfactuals]]
- Concepts: [[do-calculus]]
- Concepts: [[causal-identification]]
- Entities: [[judea-pearl]]

## Provenance

- Primary source: [raw/books/strategy/The_Book_of_Why.epub#L1-L1]

## Change notes

- 2026-04-25 — page created by auto ingest.
