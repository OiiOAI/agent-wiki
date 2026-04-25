---
id: backpropagation
title: Backpropagation
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/neuroscience/The astonishing hypothesis _ the scientific search for
  the - Crick, Francis.pdf#p1-335]'
tags:
- neuroscience
- machine learning
- algorithms
confidence: medium
related:
  broader: []
  narrower: []
  adjacent: []
---


# Backpropagation

## Summary

Backpropagation (backprop) is a supervised learning algorithm introduced in the PDP book of 1986 that allows multilayer neural networks to learn. It requires graded output units, uses error signals from the output layer to adjust weights going backward through hidden layers, and is mathematically differentiable and nonlinear. However, it is biologically implausible as written since it requires teaching signals to be sent back along the same pathways as forward signals.

## Key facts

- Backpropagation requires that units have a graded output, usually between 0 and 1, unlike binary units. [raw/books/neuroscience/The astonishing hypothesis _ the scientific search for the - Crick, Francis.pdf#p204]
- The typical relationship between summed input and output follows a sigmoid curve that is mathematically differentiable and nonlinear. [raw/books/neuroscience/The astonishing hypothesis _ the scientific search for the - Crick, Francis.pdf#p204]
- The backprop algorithm uses error information from upper layers to adjust weights of synapses coming from lower layers, backpropagating information to hidden layers. [raw/books/neuroscience/The astonishing hypothesis _ the scientific search for the - Crick, Francis.pdf#p205]
- Backpropagation, taken literally, requires that teaching information be rapidly sent back along exactly the same axons that carried forward operational information—this is most unlikely to happen in the brain. [raw/books/neuroscience/The astonishing hypothesis _ the scientific search for the - Crick, Francis.pdf#p210]
- David Zipser proposed that backprop is really a very good way of identifying the nature of the system under study, called 'neural system identification.'. [raw/books/neuroscience/The astonishing hypothesis _ the scientific search for the - Crick, Francis.pdf#p213]

## Inferences

- Inference: While biologically implausible, backpropagation can serve as a tool to discover what biological learning rules might accomplish, which must then be verified experimentally.

## Related pages

- Concepts: [[neural networks]]
- Concepts: [[PDP]]
- Concepts: [[Hebbian learning]]
- Entities: [[David Rumelhart]]
- Entities: [[David Zipser]]

## Provenance

- Primary source: [raw/books/neuroscience/The astonishing hypothesis _ the scientific search for the - Crick, Francis.pdf#p1-335]

## Change notes

- 2026-04-24 — page created by auto ingest.
