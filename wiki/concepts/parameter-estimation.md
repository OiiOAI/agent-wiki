---
id: parameter-estimation
title: Parameter estimation
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_
  Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]'
confidence: high
tags:
- parameter-estimation
- model-fitting
- likelihood
- behavioral-data
related:
  broader: []
  narrower: []
  adjacent: []
---


# Parameter estimation

## Summary

Parameter estimation in neuroeconomic models involves optimizing an objective function that measures goodness of fit between the model and observed behavioral data. The two most common techniques are maximum likelihood (ML), which maximizes the likelihood of the data given the model's predictions, and minimum squared error (MSE), which minimizes the squared error between predictions and data. ML is considered the most natural measure of fit for probabilistic models, while MSE can accommodate both deterministic and probabilistic models. When comparing models with different numbers of parameters, Bayesian Information Criterion (BIC) or Akaike's Information Criterion (AIC) are used to penalize additional parameters.

## Key facts

- Parameter estimation is done by optimizing an objective function — a measure of goodness of fit between the model and the data — comparing actual decisions to model-predicted decisions. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p456]
- Maximum likelihood estimation maximizes L = Π_t p_chose_t(x_t), where p_chose_t(x) is the model's predicted probability of choosing option x on trial t. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p456]
- Minimum squared error estimation minimizes E = Σ_t (1 - p_chose_t(x_t))^2, where p_chose_t(x) is the model's predicted probability. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p456]
- ML and MSE parameter estimates are often very similar, and rarely is there a strong case against using either method. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p456]
- MSE estimates are often easy to compute and can accommodate both deterministic and probabilistic models. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p456]
- For comparing models with different numbers of parameters, BIC or AIC can be used to augment the log-likelihood with a penalty term for additional parameters. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p457]
- BIC and AIC are only rough heuristics for correcting for additional parameters, not precise criteria. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p458]

## Uncertainties

- Uncertain: BIC and AIC are described as 'rough heuristics,' suggesting more principled model comparison methods may exist but are not yet standard in the field.

## Related pages

- Concepts: [[softmax-function]]
- Concepts: [[model-validation]]
- Concepts: [[maximum-likelihood]]
- Concepts: [[bayesian-information-criterion]]

## Provenance

- Primary source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]

## Change notes

- 2026-04-24 — page created by auto ingest.
