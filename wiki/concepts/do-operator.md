---
id: do-operator
title: The Do-Operator
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/strategy/The_Book_of_Why.epub#L1-L1]'
confidence: high
tags:
- do-calculus
- causal-inference
- notation
related:
  broader:
  - causal-inference
  - causal-calculus
  narrower:
  - adjustment-formula
  adjacent: []
---


# The Do-Operator

## Summary

The do-operator is a mathematical notation P(Y | do(X)) that represents the probability of outcome Y under an intervention where X is forcibly set to a specific value, as opposed to passive observation. It is fundamental to causal inference because it distinguishes 'doing' from 'seeing' and enables calculation of causal effects from observational data.

## Key facts

- P(L | do(D)) represents the probability of Lifespan L if patients are made to take Drug D, regardless of their choice. [raw/books/strategy/The_Book_of_Why.epub#L78]
- P(L | D) (conditional probability) may differ totally from P(L | do(D)) because observation does not account for confounding factors. [raw/books/strategy/The_Book_of_Why.epub#L79]
- Classical statistics had no operator comparable to do(D) before the Causal Revolution. [raw/books/strategy/The_Book_of_Why.epub#L88]
- The do-operator ensures that observed changes are due to the intervention itself and not confounded with other factors. [raw/books/strategy/The_Book_of_Why.epub#L79]

## Inferences

- Inference: The do-operator was mathematically defined during the Causal Revolution, enabling scientists to properly formulate causal questions that previously could not be asked scientifically.

## Related pages

- Broader: [[causal-inference]]
- Broader: [[causal-calculus]]
- Narrower: [[adjustment-formula]]
- Concepts: [[causal inference]]
- Concepts: [[intervention]]
- Concepts: [[observation]]
- Concepts: [[confounding]]
- Concepts: [[P(Y|do(X))]]
- Topics: [[statistics]]
- Topics: [[scientific-method]]

## Provenance

- Primary source: [raw/books/strategy/The_Book_of_Why.epub#L1-L1]

## Change notes

- 2026-04-25 — page created by auto ingest.
