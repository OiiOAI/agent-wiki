---
id: hidden-markov-model-attention
title: Hidden Markov Model (HMM) in Attention
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/neuroscience/Neuroscience of Decision Making - Mandel, David R.,Vartanian,
  Oshin.pdf#p1-500]'
confidence: medium
tags:
- hmm
- bayesian
- attention
- computational-model
- uncertainty
related:
  broader: []
  narrower: []
  adjacent: []
---


# Hidden Markov Model (HMM) in Attention

## Summary

A Hidden Markov Model with Gaussian noise was used to computationally model sustained attention tasks. The model captures stimulus uncertainty through transition probabilities between signal-on and signal-off states. ACh level was identified with the posterior probability of signal presence, and manipulating ACh in the model reproduced pharmacological effects: depletion decreased hits while elevation decreased correct rejections.

## Key facts

- The HMM for sustained attention has a hidden stimulus variable (signal on/off) that undergoes transitions between two states controlled by a transition matrix. [raw/books/neuroscience/Neuroscience of Decision Making - Mandel, David R.,Vartanian, Oshin.pdf#p155]
- In the model, ACh depletion is equivalent to decreasing P(signal on|observations), causing underestimation of signal presence and decreased hit rate. [raw/books/neuroscience/Neuroscience of Decision Making - Mandel, David R.,Vartanian, Oshin.pdf#p162]
- The model reproduced the doubly dissociated effects of ACh manipulation: depletion spared CR while decreasing hits, elevation spared hits while decreasing CR. [raw/books/neuroscience/Neuroscience of Decision Making - Mandel, David R.,Vartanian, Oshin.pdf#p162]
- ACh level was identified with expected uncertainty, corresponding to the uncertainty associated with the predominant expectation of signal-off state. [raw/books/neuroscience/Neuroscience of Decision Making - Mandel, David R.,Vartanian, Oshin.pdf#p161]

## Inferences

- Inference: The HMM formulation may be overly simple, as performance on intermediate signal (50ms) trials was significantly worse than expected from model predictions at saturation.

## Related pages

- Concepts: [[bayesian-inference]]
- Concepts: [[uncertainty]]
- Concepts: [[sustained-attention]]
- Concepts: [[acetylcholine]]
- Topics: [[neuroscience-of-decision-making]]
- Entities: [[yu]]

## Provenance

- Primary source: [raw/books/neuroscience/Neuroscience of Decision Making - Mandel, David R.,Vartanian, Oshin.pdf#p1-500]

## Change notes

- 2026-04-24 — page created by auto ingest.
