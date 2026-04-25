---
id: expected-free-energy
title: Expected Free Energy
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- planning
- expected free energy
- active inference
- policy selection
- epistemic
- exploration-exploitation
related:
  broader:
  - Active Inference
  - planning as inference
  - variational free energy
  narrower:
  - information gain
  - pragmatic value
  - risk
  - ambiguity
  - epistemic value
  - exploitation
  - exploration
  - policy
  - Hamiltonian principle
  adjacent:
  - variational free energy
  - Bellman equation
  - KL control
  - expected Bayesian surprise
  - intrinsic motivation
  - entropy
---


# Expected Free Energy

## Summary

Expected free energy (G) is the quantity used in Active Inference to score alternative policies (plans or courses of action) during prospective planning. Unlike variational free energy which depends on present and past observations, expected free energy considers future, policy-dependent observations. It decomposes into information gain (epistemic value, resolving uncertainty about states) and pragmatic value (exploitation, aligning with preferred outcomes). It can also be expressed as risk (expected complexity of outcomes) plus expected ambiguity. Expected free energy furnishes a prior over policies: policies with lower expected free energy are assigned higher probability.

## Key facts

- Expected free energy extends Active Inference to prospective planning by considering future, policy-dependent observations that would result from executing each policy. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p31]
- The log probability of a policy is set proportional to the negative expected free energy of that policy: P(π) = σ(-G), where σ is the softmax function. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p32]
- Expected free energy decomposes into information gain (epistemic value, how much uncertainty a policy resolves) and pragmatic value (how well outcomes align with prior preferences). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p33]
- Expected free energy also decomposes into risk (expected complexity of outcomes, analogous to the complexity term in variational free energy) and expected ambiguity (expected inaccuracy due to ambiguous state-outcome mappings). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p35]
- Expected free energy provides a self-consistent prior over policies, effectively equating prior beliefs about what one will do with preferences for what one wants to happen. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p53]
- Minimizing expected free energy corresponds to inferring the most likely course of action, analogous to Hamilton's principle of least action in physics. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p53]
- By minimizing expected free energy, Active Inference automatically balances exploration (information gain) and exploitation (pragmatic value), unlike reinforcement learning schemes that consider these separately. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p33]

## Inferences

- Inference: Expected free energy is mathematically distinct from variational free energy because the expectation is taken over future outcomes rather than present observations, and the KL-divergence term changes sign, making expected free energy minimized by policies that maximize information gain rather than minimize it.

## Related pages

- Broader: [[Active Inference]]
- Broader: [[planning as inference]]
- Broader: [[variational free energy]]
- Narrower: [[information gain]]
- Narrower: [[pragmatic value]]
- Narrower: [[risk]]
- Narrower: [[ambiguity]]
- Narrower: [[epistemic value]]
- Narrower: [[exploitation]]
- Narrower: [[exploration]]
- Narrower: [[policy]]
- Narrower: [[Hamiltonian principle]]
- Adjacent: [[variational free energy]]
- Adjacent: [[Bellman equation]]
- Adjacent: [[KL control]]
- Adjacent: [[expected Bayesian surprise]]
- Adjacent: [[intrinsic motivation]]
- Adjacent: [[entropy]]
- Concepts: [[information gain]]
- Concepts: [[pragmatic value]]
- Concepts: [[risk]]
- Concepts: [[ambiguity]]
- Concepts: [[epistemic value]]
- Concepts: [[exploitation]]
- Concepts: [[exploration]]
- Concepts: [[policy]]
- Concepts: [[variational free energy]]
- Concepts: [[planning as inference]]
- Concepts: [[Hamiltonian principle]]
- Concepts: [[KL control]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
