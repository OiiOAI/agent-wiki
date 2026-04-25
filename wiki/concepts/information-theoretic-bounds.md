---
id: information-theoretic-bounds
title: Information-theoretic bounds on predictive performance
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_
  Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]'
confidence: high
tags:
- information-theory
- model-validation
- predictive-performance
- upper-bound
related:
  broader: []
  narrower: []
  adjacent: []
---


# Information-theoretic bounds on predictive performance

## Summary

Information theory provides a rigorous upper bound on the predictive performance of behavioral models. For any model M using inputs X to predict choices C, the mutual information between the model's predictions and actual choices cannot exceed the mutual information between X and C: I(M(X); C) ≤ I(X; C). This means models cannot add Shannon information — they can only distill it. The upper bound I(X; C) can be computed given particular inputs, setting the maximum achievable performance. A lower bound can be established by comparing model performance against random predictions.

## Key facts

- I(M(X); C) ≤ I(X; C): the mutual information between model predictions and actual choices cannot exceed the mutual information between model inputs and choices. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p458]
- Models cannot add Shannon information; they can only distill information already present in the inputs. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p458]
- If a subject behaves consistently (similar choices for repeated identical option sets), the upper bound I(X; C) is high, approaching perfect prediction; if behavior is erratic, the upper bound is lower. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p458]
- In dynamic foraging experiments, reward and choice history contained approximately 0.50 bits of predictive information about the next choice, setting the upper bound for models using those inputs. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p459]
- Mechanistic models retained between 50% (worst models) and 90% (best models) of the available information in I(X; C). [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p459]
- A practical limitation is that the data set required to estimate I(C; X) is typically much larger than can be gathered from individual human subjects, limiting the generality of this approach. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p459]

## Uncertainties

- Uncertain: The data requirements for computing I(X; C) are prohibitive for most human fMRI studies, limiting practical application despite theoretical importance.

## Related pages

- Concepts: [[model-validation]]
- Concepts: [[generative-performance]]
- Concepts: [[predictive-performance]]
- Concepts: [[mutual-information]]

## Provenance

- Primary source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]

## Change notes

- 2026-04-24 — page created by auto ingest.
