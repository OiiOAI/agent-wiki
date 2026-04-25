---
id: markov-blanket
title: Markov Blanket
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-25'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
- '[raw/books/neuroscience/The Hidden Spring - Mark Solms.pdf#p1-378]'
confidence: high
tags:
- markov blanket
- action-perception cycle
- conditional independence
- autonomy
- self-organization
- mathematics
- statistics
- self-organisation
- consciousness
- Friston
related:
  broader:
  - free energy principle
  - self-organization
  - active-inference
  - generative-model
  - self-organisation
  narrower:
  - sensory states
  - active states
  - internal states
  - external states
  - Markov blanket dynamics
  - sensory-states
  - active-states
  - self-evidencing
  - free energy minimisation
  adjacent:
  - action-perception cycle
  - conditional independence
  - Bayesian networks
  - graphical models
  - free-energy-principle
  - self-organisation
  - inference
  - Karl Friston
  - Mark Solms
aliases: []
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
- A Markov blanket separates two sets of states from each other—internal and external—insulating internal states from those external to the system. [raw/books/neuroscience/The Hidden Spring - Mark Solms.pdf#p152]
- A Markov blanket is partitioned into sensory states (causally dependent on external states) and active states (causally dependent on internal states). [raw/books/neuroscience/The Hidden Spring - Mark Solms.pdf#p152]
- External states influence internal ones via the sensory states of the blanket, while internal states couple back to external ones through its active states—creating circular causality. [raw/books/neuroscience/The Hidden Spring - Mark Solms.pdf#p152]
- Cells have membranes with the properties of a Markov blanket, as does the skin and musculoskeletal system of the body as a whole. [raw/books/neuroscience/The Hidden Spring - Mark Solms.pdf#p153]
- The brain possesses a Markov blanket—it is a meta-blanket surrounding all the other blankets in the body. [raw/books/neuroscience/The Hidden Spring - Mark Solms.pdf#p153]
- The very selfhood of a complex dynamical system is constituted by its blanket; self-organising systems come into being by separating themselves from everything else. [raw/books/neuroscience/The Hidden Spring - Mark Solms.pdf#p153]
- The insulated nature of systems with Markov blankets—only able to register the not-self world via sensory states of their own blankets—constitutes the elemental basis of subjectivity. [raw/books/neuroscience/The Hidden Spring - Mark Solms.pdf#p153]
- Any ergodic random dynamical system that possesses a Markov blanket will appear to actively maintain its structural and dynamical integrity. [raw/books/neuroscience/The Hidden Spring - Mark Solms.pdf#p158]
- A Markov blanket consists of sensory states, active states and internal states that separates what belongs to the system from what belongs to the external world. [raw/books/neuroscience/The Hidden Spring - Mark Solms.pdf#p257]
- Systems equipped with a Markov blanket can automatically model the world on the basis of sensory samples. [raw/books/neuroscience/The Hidden Spring - Mark Solms.pdf#p257]
- The Markov blanket enables a system to measure its own expected free energy and act accordingly. [raw/books/neuroscience/The Hidden Spring - Mark Solms.pdf#p257]
- According to Karl Friston, Markov blankets are the boundary conditions that separate internal from external states, making self-organisation possible. [raw/books/neuroscience/The Hidden Spring - Mark Solms.pdf#p257]

## Inferences

- Inference: Because the Markov blanket establishes conditional independence between internal and external states (given blanket states), it is what enables the organism to maintain autonomy from the environment—without this autonomy, there would be no 'self' to be surprised and no minimization problem to solve.
- Inference: The Markov blanket endows internal states with a capacity to represent hidden external states probabilistically, enabling the system to infer the hidden causes of its own sensory states—this capacity enables it to act purposively upon the external milieu [raw/books/neuroscience/The Hidden Spring - Mark Solms.pdf#p155]

## Related pages

- Broader: [[free energy principle]]
- Broader: [[self-organization]]
- Broader: [[active-inference]]
- Broader: [[generative-model]]
- Broader: [[self-organisation]]
- Narrower: [[sensory states]]
- Narrower: [[active states]]
- Narrower: [[internal states]]
- Narrower: [[external states]]
- Narrower: [[Markov blanket dynamics]]
- Narrower: [[sensory-states]]
- Narrower: [[active-states]]
- Narrower: [[self-evidencing]]
- Narrower: [[free energy minimisation]]
- Adjacent: [[action-perception cycle]]
- Adjacent: [[conditional independence]]
- Adjacent: [[Bayesian networks]]
- Adjacent: [[graphical models]]
- Adjacent: [[free-energy-principle]]
- Adjacent: [[self-organisation]]
- Adjacent: [[inference]]
- Adjacent: [[Karl Friston]]
- Adjacent: [[Mark Solms]]
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
- Concepts: [[subjectivity]]
- Concepts: [[self]]
- Concepts: [[Friston]]
- Concepts: [[active inference]]
- Concepts: [[precision]]
- Concepts: [[prediction error]]
- Topics: [[artificial consciousness]]
- Topics: [[predictive processing]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]
- Additional source: [raw/books/neuroscience/The Hidden Spring - Mark Solms.pdf#p1-378]

## Change notes

- 2026-04-23 — page created by auto ingest.
- 2026-04-25 — merged contributions from `the-hidden-spring-mark-solms`.
