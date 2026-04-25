---
id: decision-making-network
title: Decision-Making Network
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles
  of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1-1761]'
confidence: high
tags:
- decision-making
- neural-networks
- computational-neuroscience
- competition
- attractor-dynamics
related:
  broader:
  - theoretical-neuroscience
  narrower:
  - bistable-network
  - inhibition-stabilized-network
  adjacent:
  - recurrent-excitation
  - competitive-inhibition
  - attractor-networks
---


# Decision-Making Network

## Summary

A decision-making network is a computational model of neural circuits that enables organisms to make choices between two or more alternatives based on sensory evidence. The model, developed by X.J. Wang, consists of two populations of excitatory neurons that compete through inhibition from a shared inhibitory population, allowing sensory input to bias the network toward one of several stable states representing different decisions.

## Key facts

- A decision-making network must have a stable pattern of spontaneous activity corresponding to no decision when no relevant sensory stimuli are present. [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1665]
- A sensory stimulus requiring a decision should eliminate or destabilize the no-decision state and introduce two new stable firing patterns corresponding to the two possible actions. [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1665]
- Sensory stimuli should be capable of biasing the outcome so that one decision state is more likely to occur than the other. [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1665]
- The network consists of two excitatory populations representing unique decisions, each recurrently connected, both exciting a single inhibitory population that returns feedback inhibition to both. [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1665]
- The inhibitory population prevents the state in which both excitatory populations fire at high rates, which would correspond to making both decisions simultaneously. [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1666]
- When inputs to the two excitatory populations are equal, small random fluctuations in firing rates favor one group, resulting in each decision occurring approximately 50% of the time. [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1665]
- A biased stimulus generates larger input to one excitatory population than the other, causing its firing rate to rise and remain high while the other falls, with the favored decision reached almost 100% of the time. [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1665]
- Decision latency from stimulus onset to decision can be determined by examining the divergence between the firing rates of the two neuronal populations. [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1665]
- Decisions are made more rapidly when the stimulus is biased than when unbiased, similar to experimental observations in perceptual decision-making. [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1665]
- The model equations include differential equations for firing rates ra and rb of the two excitatory populations, with terms for recurrent excitation (wEE), inhibitory feedback (wEI), and external input (ha, hb). [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1667]
- In the absence of sensory stimuli (ha = hb = 0), the firing rates of the two excitatory populations are equal and low, representing the no-decision state. [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1667]
- Large enough equal inputs (ha = hb > 0) result in two stable states corresponding to the two decision states, with the previous no-decision outcome disappearing. [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1667]

## Related pages

- Broader: [[theoretical-neuroscience]]
- Narrower: [[bistable-network]]
- Narrower: [[inhibition-stabilized-network]]
- Adjacent: [[recurrent-excitation]]
- Adjacent: [[competitive-inhibition]]
- Adjacent: [[attractor-networks]]
- Concepts: [[neural-network-models]]
- Concepts: [[persistent-activity]]
- Concepts: [[population-coding]]
- Topics: [[computational-neuroscience]]
- Topics: [[perceptual-decision-making]]
- Entities: [[wang-xj]]
- Entities: [[shadlen-michael]]
- Entities: [[lateral-intraparietal-area]]

## Provenance

- Primary source: [raw/books/neuroscience/Principles of Neural Science, Fifth Edition (Principles of - Eric R_ Kandel; James H_ Schwartz; Thomas M_ Jessell; Steven.pdf#p1-1761]

## Change notes

- 2026-04-24 — page created by auto ingest.
