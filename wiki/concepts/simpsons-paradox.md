---
id: simpsons-paradox
title: Simpson's Paradox
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/strategy/The_Book_of_Why.epub#L1-L1]'
confidence: high
tags:
- paradoxes
- causal-reasoning
- statistics
- confounding
related:
  broader:
  - causal-inference
  - paradoxes-in-causality
  - confounding
  - statistical-paradoxes
  narrower:
  - sure-thing-principle
  - confounding
  - mediator
  - collider-bias
  adjacent:
  - berksons-paradox
  - monty-hall-problem
  - birth-weight-paradox
  - lords-paradox
  - monty-hall-paradox
  - sure-thing-principle
---


# Simpson's Paradox

## Summary

Simpson's paradox occurs when a relationship between two variables reverses or disappears when data is aggregated across subgroups, yet reverses again when disaggregated. The paradox reveals a conflict between causal intuition (a drug cannot be bad for men, bad for women, but good overall) and statistical proportions. It is resolved by causal diagrams: the correct interpretation depends on whether a third variable is a confounder (requiring stratification) or a mediator (making aggregation appropriate). The paradox demonstrates why causal structure—not just data patterns—is needed to determine correct analysis.

## Key facts

- Simpson's reversal is a purely numerical fact: relative frequencies can reverse direction upon merging samples, even when they do not reverse within each subgroup. [raw/books/strategy/The_Book_of_Why.epub#L1760-L1770]
- A BBG (bad for men, bad for women, good for people) drug is causally impossible; the corrected sure-thing principle requires that an action cannot increase a probability in each subpopulation yet decrease it overall, provided the action does not change the composition of subpopulations. [raw/books/strategy/The_Book_of_Why.epub#L1810-L1825]
- Gender acts as a confounder in the drug–heart attack example because it affects both the decision to take the drug and the risk of heart attack; adjusting for gender (stratification) reveals Drug D is BBB (bad for both sexes and the population). [raw/books/strategy/The_Book_of_Why.epub#L1830-L1840]
- Blood pressure is a mediator in the blood-pressure-drug example, not a confounder; no back-door path exists between Drug and Heart Attack, so aggregating the data gives the correct conclusion that Drug B works. [raw/books/strategy/The_Book_of_Why.epub#L1850-L1860]
- The paradox cannot be resolved by data alone; one must examine the data-generating process through a causal diagram to determine whether aggregation or stratification is appropriate. [raw/books/strategy/The_Book_of_Why.epub#L1860-L1870]
- Simpson's paradox occurs in real-world medical data: open surgery appeared worse overall than endoscopic surgery for kidney stones despite being better for both small and large stones, because stone severity confounded the treatment choice. [raw/books/strategy/The_Book_of_Why.epub#L1875-L1885]
- Simpson's reversal is a qualitative change in the sign of an effect, harder to ignore than other signs of confounding. [raw/books/strategy/The_Book_of_Why.epub#L1792-L1798]
- The exercise-cholesterol example demonstrates Simpson's paradox: within each age group, more exercise correlates with lower cholesterol, but across the population, more exercise correlates with higher cholesterol. [raw/books/strategy/The_Book_of_Why.epub#L1805-L1820]
- Age is identified as a confounder of Exercise and Cholesterol, meaning Age causes both exercise habits and cholesterol levels. [raw/books/strategy/The_Book_of_Why.epub#L1822-L1830]
- Controlling for the confounder (Age) resolves Simpson's paradox and reveals the true causal effect of exercise being beneficial. [raw/books/strategy/The_Book_of_Why.epub#L1830-L1835]
- Simpson's paradox occurs when aggregated data shows a different trend than data broken down by subgroups. [raw/books/strategy/The_Book_of_Why.epub#L3670-3672]
- Pearl (2009, pp. 174–182) provides an extensive account of the history of Simpson's paradox, documenting attempts by statisticians and philosophers to resolve it without invoking causation. [raw/books/strategy/The_Book_of_Why.epub#L3670-3672]
- Pearl (2014) offers a more recent account of Simpson's paradox geared toward educators. [raw/books/strategy/The_Book_of_Why.epub#L3672-3673]
- Real-world examples of Simpson's paradox include baseball batting averages (Savage, 2009), kidney stone treatment outcomes (Julious and Mullee, 1994), and smoking and mortality data (Appleton, French, and Vanderpump, 1996). [raw/books/strategy/The_Book_of_Why.epub#L3674-3675]

## Inferences

- Inference: The reason Simpson's paradox surprises people is that humans possess an implicit causal calculus (the sure-thing principle) that rejects BBG drugs, yet this calculus was never formalized in classical statistics, leaving a gap between intuition and mathematical reasoning.
- Inference: Simpson's paradox reveals the fundamental difference between statistical association and causal effect, requiring domain knowledge to resolve.
- Inference: The bibliography suggests that traditional statistical approaches struggle to resolve Simpson's paradox, indicating the need for causal inference methods.
- Inference: Pearl's extensive treatment of Simpson's paradox across multiple publications (2009, 2014) indicates this is a central example in his causal inference framework.

## Related pages

- Broader: [[causal-inference]]
- Broader: [[paradoxes-in-causality]]
- Broader: [[confounding]]
- Broader: [[statistical-paradoxes]]
- Narrower: [[sure-thing-principle]]
- Narrower: [[confounding]]
- Narrower: [[mediator]]
- Narrower: [[collider-bias]]
- Adjacent: [[berksons-paradox]]
- Adjacent: [[monty-hall-problem]]
- Adjacent: [[birth-weight-paradox]]
- Adjacent: [[lords-paradox]]
- Adjacent: [[monty-hall-paradox]]
- Adjacent: [[sure-thing-principle]]
- Concepts: [[confounding]]
- Concepts: [[collider-bias]]
- Concepts: [[back-door-criterion]]
- Concepts: [[exchangeability]]
- Concepts: [[causal-diagram]]
- Concepts: [[lords-paradox]]
- Concepts: [[causal-diagrams]]
- Entities: [[judea-pearl]]

## Provenance

- Primary source: [raw/books/strategy/The_Book_of_Why.epub#L1-L1]

## Change notes

- 2026-04-25 — page created by auto ingest.
