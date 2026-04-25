---
id: divisive-normalization
title: Divisive Normalization
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean
  - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p1-401]'
confidence: high
tags:
- neuroscience
- computation
- normalization
- neural-circuits
related:
  broader:
  - neural-computation
  - efficient-coding
  narrower: []
  adjacent:
  - gain-control
  - contextual-modulation
---


# Divisive Normalization

## Summary

Divisive normalization is a nonlinear gain control algorithm that describes how neural responses are modulated by the pooled activity of a larger neuronal population. Originally developed to describe response properties in primary visual cortex, it has been observed across multiple sensory modalities and brain regions. In the context of value coding, divisive normalization implements a relative value code where activation by a target's value is scaled by the summed value of all available alternatives, including the target itself.

## Key facts

- Divisive normalization describes how the response of neuron i depends on both the direct input to that neuron and the inputs to a more broadly tuned pool of neurons, with the direct drive divisively scaled by a term that sums over inputs to the larger pool. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p129]
- In LIP, relative value coding is implemented via divisive normalization where neural responses depend on rewards associated with both RF and extra-RF target values. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p129]
- Model comparison in LIP studies showed that divisive normalization far outperformed alternative relative value algorithms based on value difference or simple fractional value in characterizing the nonlinear relationship between LIP activity and option values. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p129]
- Normalized value coding produces a compressive saturating value function that ensures the neural representation of rewards does not exceed the finite dynamic range of spiking neurons. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p129]
- Divisive normalization contributes to efficient coding by decorrelating neural responses despite significant redundancies in original sensory information. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p130]

## Inferences

- Inference: Compressive utility functions produced by divisive normalization may underlie risk-averse choice behavior seen in most human subjects.
- Inference: The dynamic normalization model predicts time-varying aspects of value coding where modulation by RF target value is strongest early during the initial phasic transient.

## Uncertainties

- Uncertain: Whether divisive normalization is implemented identically across different brain regions and different computational contexts remains to be determined.

## Related pages

- Broader: [[neural-computation]]
- Broader: [[efficient-coding]]
- Adjacent: [[gain-control]]
- Adjacent: [[contextual-modulation]]
- Concepts: [[value-coding]]
- Concepts: [[lateral-intraparietal-area-lip]]
- Concepts: [[efficient-coding-hypothesis]]

## Provenance

- Primary source: [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p1-401]

## Change notes

- 2026-04-24 — page created by auto ingest.
