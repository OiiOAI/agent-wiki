---
id: overfitting
title: Overfitting
type: concept
status: draft
created: '2026-04-22'
updated: '2026-04-22'
sources:
- '[raw/books/strategy/Algorithms_to_Live_By.epub#L1-L1]'
confidence: high
tags:
- machine-learning
- statistics
- optimization
- cognitive-bias
related:
  broader:
  - machine-learning
  - decision-making
  narrower:
  - regularization
  - cross-validation
  - early-stopping
  adjacent: []
---


# Overfitting

## Summary

Overfitting is a fundamental problem in machine learning and decision-making where a model becomes too sensitive to the specific data it was trained on, reducing its ability to generalize to new situations. It occurs when models with too many factors fit noise rather than underlying patterns, leading to worse predictions despite better fit to training data.

## Key facts

- Including more factors in a model always makes it a better fit for existing data, but not necessarily for prediction. [raw/books/strategy/Algorithms_to_Live_By.epub#L1717-L1720]
- The nine-factor marriage satisfaction model produces wild undulations when data varies, while simpler one- and two-factor models remain stable. [raw/books/strategy/Algorithms_to_Live_By.epub#L1714-L1716]
- Overfitting is described as a form of 'idolatry of data'—worshipping what we can measure rather than what actually matters. [raw/books/strategy/Algorithms_to_Live_By.epub#L1730-L1732]
- Overfitting explains why foods that taste best are often unhealthy: taste is a proxy metric for nutrition that can be manipulated beyond its original purpose. [raw/books/strategy/Algorithms_to_Live_By.epub#L1743-L1747]
- In business, 'it really is true that the company will build whatever the CEO decides to measure,' leading to perverse optimization of wrong metrics. [raw/books/strategy/Algorithms_to_Live_By.epub#L1761-L1764]
- Police officers have been documented taking time during gunfights to pocket spent casings—good firing range etiquette that becomes deadly in real combat. [raw/books/strategy/Algorithms_to_Live_By.epub#L1775-L1779]

## Inferences

- Inference: The gap between data we have and predictions we want exists in virtually all human decisions, from financial forecasting to personal choices, making overfitting a universal risk.
- Inference: The solution to overfitting involves balancing model complexity against fit quality, which is the basis for regularization techniques.

## Related pages

- Broader: [[machine-learning]]
- Broader: [[decision-making]]
- Narrower: [[regularization]]
- Narrower: [[cross-validation]]
- Narrower: [[early-stopping]]
- Concepts: [[regularization]]
- Concepts: [[cross-validation]]
- Concepts: [[early-stopping]]
- Concepts: [[lasso]]
- Concepts: [[occams-razor]]

## Provenance

- Primary source: [raw/books/strategy/Algorithms_to_Live_By.epub#L1-L1]

## Change notes

- 2026-04-22 — page created by auto ingest.
