---
id: markov-blanket
title: Markov Blanket
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
confidence: high
tags:
- markov blanket
- action-perception cycle
- conditional independence
- autonomy
- self-organization
related:
  broader:
  - free energy principle
  - self-organization
  - active-inference
  - generative-model
  narrower:
  - sensory states
  - active states
  - internal states
  - external states
  - Markov blanket dynamics
  - sensory-states
  - active-states
  adjacent:
  - action-perception cycle
  - conditional independence
  - Bayesian networks
  - graphical models
---


# Markov Blanket

## Summary

A Markov blanket is a statistical construct that formally separates an adaptive system (e.g., a brain or organism) from its environment. It comprises sensory states and active states, which mediate all statistical interactions between internal and external states. Formally, a Markov blanket for a variable comprises its parents, children, and the other parents of its children. The Markov blanket is a precondition for any adaptive system, as it provides the separation and autonomy from the environment that makes surprise minimization meaningful. Internal and external states acquire a form of synchrony through sharing a Markov blanket, enabling internal states to represent (model) external states on average.

## Key facts

- A Markov blanket comprises sensory states and active states that statistically separate internal states (of the organism/brain) from external states (of the environment). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p43]
- Internal states cannot directly change external states but can do so vicariously by changing active states; external states cannot directly change internal states but can do so indirectly by changing sensory states. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p43]
- A Markov blanket for a variable comprises its parents, its children, and the other parents of its children, defining the set of variables that mediate all interactions with the rest of the system. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p43]
- Through sharing a Markov blanket, internal and external states acquire a form of synchrony on average, enabling internal states to represent external states. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p45]
- Markov blankets can be nested within one another: for example, brains, organisms, dyads, and communities can each be conceived as having distinct Markov blankets nested hierarchically. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p44]
- A Markov blanket may be subdivided into sensory states (mediating influence of external world on internal states) and active states (mediating influence of internal states on the external world). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p108]
- The adaptive system only affects the environment by performing actions (via active states) and the environment only affects the adaptive system by producing observations (via sensory states). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p108]
- Defining the Markov blanket ensures we know what is being inferred (external states) and what is doing the inferring. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p109]

## Inferences

- Inference: Because the Markov blanket establishes conditional independence between internal and external states (given blanket states), it is what enables the organism to maintain autonomy from the environment—without this autonomy, there would be no 'self' to be surprised and no minimization problem to solve.

## Related pages

- Broader: [[free energy principle]]
- Broader: [[self-organization]]
- Broader: [[active-inference]]
- Broader: [[generative-model]]
- Narrower: [[sensory states]]
- Narrower: [[active states]]
- Narrower: [[internal states]]
- Narrower: [[external states]]
- Narrower: [[Markov blanket dynamics]]
- Narrower: [[sensory-states]]
- Narrower: [[active-states]]
- Adjacent: [[action-perception cycle]]
- Adjacent: [[conditional independence]]
- Adjacent: [[Bayesian networks]]
- Adjacent: [[graphical models]]
- Concepts: [[sensory states]]
- Concepts: [[active states]]
- Concepts: [[internal states]]
- Concepts: [[external states]]
- Concepts: [[action-perception cycle]]
- Concepts: [[conditional independence]]
- Concepts: [[self-evidencing]]
- Concepts: [[free energy principle]]
- Concepts: [[active-inference]]
- Concepts: [[generative-model]]
- Concepts: [[action-perception-loop]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
