---
id: confounding-and-deconfounding
title: Confounding and Deconfounding
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/strategy/The_Book_of_Why.epub#L1-L1]'
confidence: high
tags:
- causal-inference
- confounding
- adjustment
- deconfounding
related:
  broader:
  - causal-inference
  - do-operator
  - causal-diagrams
  narrower:
  - back-door-criterion
  - m-bias
  - exchangeability
  - randomized-controlled-trial
  adjacent:
  - mediator
  - collider-bias
  - chain-junction
  - fork-junction
---


# Confounding and Deconfounding

## Summary

Confounding is any factor that causes a discrepancy between P(Y|X) (observational probability) and P(Y|do(X)) (causal/interventional probability). The Causal Revolution resolved confounding by transforming it from an ambiguous statistical concept into a precise causal one. The back-door criterion identifies which variables must be measured and adjusted for to deconfound an estimated causal effect. The key insight is that confounders and deconfounders are not necessarily the same set; controlling for wrong variables (mediators, colliders, or M-bias structures) can introduce bias rather than remove it.

## Key facts

- Confounding is defined as anything that leads to P(Y|X) ≠ P(Y|do(X)); randomization eliminates confounder bias by severing all incoming arrows to the treatment variable. [raw/books/strategy/The_Book_of_Why.epub#L1415-L1425]
- The back-door criterion states that X and Y are deconfounded if all back-door paths (paths starting with an arrow into X) are blocked, without blocking any causal paths. [raw/books/strategy/The_Book_of_Why.epub#L1515-L1525]
- The 'classical epidemiological definition' of a confounder (associated with both X and Y, and not on the causal path) is wrong: Z satisfying these conditions may be a mediator or a collider, and controlling for it increases bias. [raw/books/strategy/The_Book_of_Why.epub#L1475-L1488]
- Greenland and Robins (1986) introduced exchangeability: treatment and control groups are exchangeable if the percentage of doomed, causative, preventive, and immune individuals is the same in both groups. [raw/books/strategy/The_Book_of_Why.epub#L1480-L1490]
- Controlling for a mediator (Z on the path X → Z → Y) blocks part or all of the causal effect of X on Y, as demonstrated in the smoking–miscarriage example where adjusting for prior miscarriages underestimates smoking's effect. [raw/books/strategy/The_Book_of_Why.epub#L1530-L1545]
- M-bias shows that a variable satisfying the three-part confounder test is not a deconfounder; conditioning on B opens the M-shaped back-door path X ← A → B ← C → Y. [raw/books/strategy/The_Book_of_Why.epub#L1550-L1565]
- Randomization simulates the do-operator by erasing all arrows pointing into the treatment variable and ensuring no arrow from the randomization device to the outcome, making P(Y|X) = P(Y|do(X)). [raw/books/strategy/The_Book_of_Why.epub#L1405-L1415]

## Inferences

- Inference: The Causal Revolution replaced Fisher's intuitive confounder concepts with algorithmic criteria (back-door criterion, d-separation) that can be computed in nanoseconds, ending centuries of confusion about what variables to adjust for.

## Related pages

- Broader: [[causal-inference]]
- Broader: [[do-operator]]
- Broader: [[causal-diagrams]]
- Narrower: [[back-door-criterion]]
- Narrower: [[m-bias]]
- Narrower: [[exchangeability]]
- Narrower: [[randomized-controlled-trial]]
- Adjacent: [[mediator]]
- Adjacent: [[collider-bias]]
- Adjacent: [[chain-junction]]
- Adjacent: [[fork-junction]]
- Concepts: [[do-operator]]
- Concepts: [[back-door-criterion]]
- Concepts: [[exchangeability]]
- Concepts: [[d-separation]]
- Concepts: [[adjustment]]

## Provenance

- Primary source: [raw/books/strategy/The_Book_of_Why.epub#L1-L1]

## Change notes

- 2026-04-25 — page created by auto ingest.
