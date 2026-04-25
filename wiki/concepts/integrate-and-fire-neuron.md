---
id: integrate-and-fire-neuron
title: Integrate-and-Fire Neuron
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles
  of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1-1761]'
confidence: high
tags:
- computational-neuroscience
- neuron-model
- integrate-and-fire
related:
  broader: []
  narrower: []
  adjacent: []
---


# Integrate-and-Fire Neuron

## Summary

The integrate-and-fire model is a simplified mathematical model of a neuron consisting of a single compartment with linear membrane dynamics and a threshold-crossing rule for action potential generation. It captures essential features of neurons: membrane resistance, membrane capacitance, and action potential generation.

## Key facts

- The integrate-and-fire model consists of a single compartment with a linear relationship between membrane current and membrane potential, and fires action potentials through a threshold-crossing rule. [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1654]
- In the model the membrane potential obeys: Cm(dV/dt) = (Vrest - V)/Rm + I, where Cm is membrane capacitance, Rm is membrane resistance, and I is synaptic current. [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1654]
- Background synaptic input makes neurons more sensitive to small numbers of presynaptic spikes but less sensitive to spike synchrony. [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1655]
- Ongoing asynchronous background input raises the baseline membrane potential closer to threshold, increasing sensitivity to additional input. [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1655]

## Inferences

- Inference: The integrate-and-fire model provides a tractable framework for studying network dynamics while sacrificing biophysical detail like dendritic morphology and nonlinear conductances.

## Related pages

- Concepts: [[mcculloch-pitts-neuron]]
- Concepts: [[firing-rate-model]]
- Concepts: [[action-potential]]
- Topics: [[single-neuron-modeling]]
- Topics: [[network-dynamics]]

## Provenance

- Primary source: [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1-1761]

## Change notes

- 2026-04-24 — page created by auto ingest.
