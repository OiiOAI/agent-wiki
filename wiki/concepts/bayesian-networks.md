---
id: bayesian-networks
title: Bayesian Networks
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/strategy/The_Book_of_Why.epub#L1-L1]'
confidence: high
tags:
- artificial-intelligence
- probabilistic-models
- uncertainty-reasoning
related:
  broader:
  - artificial-intelligence
  - probabilistic-reasoning
  - probabilistic-graphical-models
  - causal-inference
  narrower:
  - belief-propagation
  - conditional-probability
  - likelihood-ratio
  - conditional-probability-table
  - d-separation
  - causal-diagrams
  adjacent:
  - causal-diagrams
  - path-analysis
  - chain-junction
  - fork-junction
  - collider-bias
---


# Bayesian Networks

## Summary

Bayesian networks are probabilistic graphical models that represent variables and their conditional dependencies via a directed acyclic graph. They were the first tool allowing computers to reason with uncertainty ("shades of gray"), and they encapsulate much of the mathematical foundation of causal diagrams.

## Key facts

- Bayesian networks were the first tool that allowed computers to think in "shades of gray". [raw/books/strategy/The_Book_of_Why.epub#L243]
- Bayesian networks remain a very important tool for AI. [raw/books/strategy/The_Book_of_Why.epub#L243]
- Bayesian networks encapsulate much of the mathematical foundation of causal diagrams. [raw/books/strategy/The_Book_of_Why.epub#L243]
- Bayesian networks use message-passing architecture where nodes send conditional probabilities in one direction and likelihood ratios in the other. [raw/books/strategy/The_Book_of_Why.epub#L620-L635]
- Bayesian networks can compute inverse probabilities efficiently through belief propagation, solving the computational problems that made full probabilistic approaches impractical. [raw/books/strategy/The_Book_of_Why.epub#L620-L635]
- A causal diagram is a Bayesian network in which every arrow signifies a direct causal relation or possibility of one in that direction. [raw/books/strategy/The_Book_of_Why.epub#L530-L545]
- Bayesian networks inhabit a world where all questions are reducible to degrees of association and cannot ascend to the second or third rungs of the Ladder of Causation without causal augmentation. [raw/books/strategy/The_Book_of_Why.epub#L505-L520]
- Two extensions to Bayesian networks enabled them to climb the causal ladder: the graph-surgery idea for handling interventions (1991) and capability for counterfactuals (1994). [raw/books/strategy/The_Book_of_Why.epub#L520-L535]
- A Bayesian network represents a joint probability distribution compactly: each node's probability depends only on its parents, and missing arrows between nodes indicate conditional independence given the parents. [raw/books/strategy/The_Book_of_Why.epub#L1105-L1115]
- Belief propagation allows Bayesian networks to update beliefs at every node when new evidence is entered at any point in the network, propagating information throughout. [raw/books/strategy/The_Book_of_Why.epub#L1230-L1240]
- The 'baggage' example demonstrates a Bayesian network with three nodes (Bag on Plane, Time Waited, Bag on Carousel) and a conditional probability table showing how the probability of seeing a bag decreases nonlinearly over time. [raw/books/strategy/The_Book_of_Why.epub#L1145-L1165]
- Turbo codes in every cell phone use belief propagation on Bayesian networks; Claude Berrou discovered this empirically in 1993 without knowing he was using Bayesian networks, and David MacKay later connected it to the belief propagation framework. [raw/books/strategy/The_Book_of_Why.epub#L1255-L1275]
- Bonaparte, used by the Netherlands Forensic Institute, converts DNA pedigree information into Bayesian networks to identify victims of mass disasters by propagating DNA evidence through family relationships. [raw/books/strategy/The_Book_of_Why.epub#L1200-L1215]
- The three elementary junctions (chain, fork, collider) in isolation, together with d-separation, are sufficient for reading off all conditional independences implied by any Bayesian network, regardless of complexity. [raw/books/strategy/The_Book_of_Why.epub#L1030-L1040]
- The key difference between Bayesian networks and causal diagrams lies in construction and interpretation: a causal diagram requires asking which variables each node 'listens' to, and missing arrows mean independence after holding parents constant. [raw/books/strategy/The_Book_of_Why.epub#L1280-L1295]

## Inferences

- Inference: Bayesian networks were once considered the key to unlocking AI, but Pearl came to believe this assessment was incorrect, leading him to pursue causal reasoning instead.
- Inference: The mathematical framework of Bayesian networks laid groundwork for causal diagrams, suggesting a connection between probabilistic and causal modeling.
- Inference: The discovery that turbo codes (used in all cell phones) operate via belief propagation on Bayesian networks demonstrates that Bayesian networks had been discovered independently multiple times in different fields, unifying coding theory and probabilistic inference.

## Related pages

- Broader: [[artificial-intelligence]]
- Broader: [[probabilistic-reasoning]]
- Broader: [[probabilistic-graphical-models]]
- Broader: [[causal-inference]]
- Narrower: [[belief-propagation]]
- Narrower: [[conditional-probability]]
- Narrower: [[likelihood-ratio]]
- Narrower: [[conditional-probability-table]]
- Narrower: [[d-separation]]
- Narrower: [[causal-diagrams]]
- Adjacent: [[causal-diagrams]]
- Adjacent: [[path-analysis]]
- Adjacent: [[chain-junction]]
- Adjacent: [[fork-junction]]
- Adjacent: [[collider-bias]]
- Concepts: [[bayes-rule]]
- Concepts: [[causal-diagrams]]
- Concepts: [[probability]]
- Concepts: [[causal-inference]]
- Concepts: [[ladder-of-causation]]
- Concepts: [[d-separation]]
- Concepts: [[belief-propagation]]
- Concepts: [[conditional-independence]]
- Entities: [[judea-pearl]]
- Entities: [[thomas-bayes]]

## Provenance

- Primary source: [raw/books/strategy/The_Book_of_Why.epub#L1-L1]

## Change notes

- 2026-04-25 — page created by auto ingest.
