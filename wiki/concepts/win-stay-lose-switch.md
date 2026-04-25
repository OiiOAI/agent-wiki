---
id: win-stay-lose-switch
title: Win-stay-lose-switch strategy
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_
  Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]'
confidence: high
tags:
- learning-strategy
- choice-behavior
- game-theory
- reinforcement
related:
  broader: []
  narrower: []
  adjacent: []
---


# Win-stay-lose-switch strategy

## Summary

Win-stay-lose-switch (WSLS) is a simple behavioral strategy in which a subject repeats the same choice after a reward (win-stay) and switches to the alternative after no reward (lose-switch). In matching pennies games against non-exploitative computer opponents, monkeys show strong WSLS behavior with probability substantially above 0.5. However, when the opponent exploits this strategy (algorithm 2), WSLS is no longer profitable and monkeys reduce reliance on it. A reinforcement learning model (with value functions updated by reward) typically outperforms WSLS when opponents are competitive, though the two models perform comparably against non-exploitative opponents.

## Key facts

- In matching pennies games against algorithm 1 (non-exploitative), monkeys chose targets according to WSLS substantially more than 50% of trials, with WSLS probability reaching nearly 1 in some animals. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p467]
- When the computer opponent exploited the animal's WSLS tendency (algorithm 2), the probability of WSLS was significantly reduced in all animals. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p467]
- A reinforcement learning model performed better than the WSLS model in 63.9% of sessions against algorithm 2, showing that adaptive learning replaces WSLS when it becomes unprofitable. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p468]
- In Rock-Paper-Scissors games, monkeys showed a significant bias for the Cournot best response (analogous to WSLS in the three-alternative case) even against an exploiting opponent. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p469]
- An attractor network model with reinforcement learning can reproduce WSLS behavior as an emergent property of reward-dependent synaptic plasticity. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p497]

## Uncertainties

- Uncertain: The probability of WSLS in the attractor network model is limited to about 0.65, below the nearly 1.0 observed in some monkeys, suggesting additional learning mechanisms (such as belief-dependent learning affecting both chosen and unchosen synapses) may be required.

## Related pages

- Concepts: [[reinforcement-learning]]
- Concepts: [[matching-pennies]]
- Concepts: [[game-theory]]
- Concepts: [[softmax-function]]

## Provenance

- Primary source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]

## Change notes

- 2026-04-24 — page created by auto ingest.
