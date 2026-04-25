---
id: attractor-network-model
title: Attractor network model
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_
  Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]'
confidence: high
tags:
- neural-circuit-model
- decision-making
- attractor
- spiking-network
- reward-learning
related:
  broader: []
  narrower: []
  adjacent: []
---


# Attractor network model

## Summary

The attractor network model is a biophysically realistic spiking neural circuit model for decision making that implements a two-stage mechanism: valuation via synaptic weights and action selection via winner-take-all competition. The network consists of two neural pools selective for choices A and B, with strong recurrent excitatory connections within pools and competitive inhibition between pools mediated by interneurons. Decision evidence is provided by inputs IA and IB; the recurrent excitation in interplay with inhibition creates multiple stable states. Reward-dependent Hebbian plasticity at input synapses modifies synaptic strengths cA and cB, allowing the network to learn adaptive choice behavior through melioration. The network produces softmax-like choice probabilities as an emergent property of stochastic spiking dynamics.

## Key facts

- The attractor network model consists of two pyramidal cell groups selective for options A and B, with strong recurrent excitation within pools and competition through feedback inhibition. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p492]
- Inputs IA and IB provide evidence for the two alternatives, and the network's choice probability follows a sigmoid function of the difference in synaptic strengths (cA minus cB). [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p493]
- Synaptic plasticity at input synapses is reward-dependent: synapses are potentiated only if the choice is rewarded and depressed otherwise. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p495]
- The model reproduces matching law behavior observed in monkey foraging tasks, with synaptic strengths converging toward returns (reward per choice) rather than income (reward per unit time). [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p496]
- The model shows 'under-matching' — the relative probability of choosing the more rewarding option is slightly smaller than the relative reward rate — a consequence of stochasticity in neural activity. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p497]
- During competitive games, the interaction between the decision circuit and the opponent forces synaptic variables toward equality, producing quasi-random behavior characteristic of Nash Equilibrium. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p498]

## Inferences

- Inference: Valuation may occur at the synaptic level in the form of returns, rather than being encoded as firing rates of LIP neurons — LIP activity reflects synaptic values but the primary substrate for valuation is the plastic synapse.

## Related pages

- Concepts: [[softmax-function]]
- Concepts: [[drift-diffusion-model]]
- Concepts: [[matching-law]]
- Concepts: [[reinforcement-learning]]
- Concepts: [[reward-dependent-plasticity]]

## Provenance

- Primary source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]

## Change notes

- 2026-04-24 — page created by auto ingest.
