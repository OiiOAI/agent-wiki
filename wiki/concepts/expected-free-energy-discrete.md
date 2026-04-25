---
id: expected-free-energy-discrete
title: Expected Free Energy (Discrete Models)
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- Active Inference
- policy selection
- epistemic value
- Bayesian inference
related:
  broader:
  - Active Inference
  - Free Energy Principle
  - Variational Inference
  narrower: []
  adjacent:
  - Risk
  - Ambiguity
  - Epistemic Value
  - Information Gain
---


# Expected Free Energy (Discrete Models)

## Summary

Expected free energy is the quantity that defines prior beliefs about policies in Active Inference. It combines the expected ambiguity (entropy of predicted outcomes given hidden states) and risk (KL divergence between inferred states and preferred states), providing a principled bound on the pragmatic and epistemic value of alternative courses of action. This chunk derives the mathematical relationship between expected free energy and the information-theoretic quantities that motivate policy selection.

## Key facts

- Expected free energy for discrete POMDP models decomposes into expected ambiguity and risk: G(π) = EQ(sτ|π)[H[P(oτ|sτ)]] + DKL[Q(oτ|π) || P(oτ|C)], where the first term is expected outcome entropy and the second measures divergence from preferences. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p258]
- The expected information gain associated with hidden states (epistemic value or Bayesian surprise) is expressed as H[Q(oτ|π)] − EQ(sτ|π)[H[P(oτ|sτ)]], decomposing expected free energy into pragmatic and epistemic components. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p258]
- Parameter information gain (novelty) is computed using the KL divergence between posterior and prior Dirichlet distributions, with the expression simplifying to approximately (1/2aij − 1/2a0j) + ln(a0j/aij) + ψ(aij) − ψ(a0j). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p259]
- The expected free energy can be expressed computationally as Gπ = Στ Gπτ where Gπτ = H·i·sπτ + oπτ·i(ln oπτ − ln Cτ), enabling efficient computation using linear algebra. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p258]
- Preferences are specified in terms of observations (C vector of prior probabilities) rather than states, connecting expected free energy to preferences over outcomes rather than states. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p258]

## Inferences

- Inference: Expected free energy unifies goal-directed (pragmatic) and information-seeking (epistemic) behavior within a single variational framework.
- Inference: The parameter information gain term ensures novelty-seeking behavior in addition to goal-seeking, allowing the system to balance exploitation and exploration.

## Uncertainties

- Uncertain: The derivation assumes α = 1, implying a balanced exchange between the organism and its environment; the implications of deviations from this assumption are noted as an active research area.

## Related pages

- Broader: [[Active Inference]]
- Broader: [[Free Energy Principle]]
- Broader: [[Variational Inference]]
- Adjacent: [[Risk]]
- Adjacent: [[Ambiguity]]
- Adjacent: [[Epistemic Value]]
- Adjacent: [[Information Gain]]
- Concepts: [[Entropy]]
- Concepts: [[KL Divergence]]
- Concepts: [[Policy Selection]]
- Concepts: [[Precision]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
