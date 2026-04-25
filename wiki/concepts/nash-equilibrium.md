---
id: nash-equilibrium
title: Nash Equilibrium
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-25'
sources:
- '[raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_
  Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]'
- '[raw/books/strategy/Algorithms_to_Live_By.epub#L1-L1]'
confidence: high
tags:
- game-theory
- equilibrium
- decision-theory
- economics
- algorithms
related:
  broader:
  - game-theory
  - algorithmic-game-theory
  narrower:
  - subgame-perfect-equilibrium
  - trembling-hand-equilibrium
  - quantal-response-equilibrium
  adjacent:
  - dominant-strategy
  - prisoners-dilemma
  - price-of-anarchy
aliases: []
---

# Nash Equilibrium

## Summary

Nash Equilibrium is a solution concept in game theory where no player can improve their expected payoff by unilaterally changing their strategy. It is defined as a strategy profile where each player's strategy is a best response to the other players' strategies.

## Key facts

- A Nash Equilibrium of a game is a strategy pair (x*, y*) such that P(x*, y*) >= P(x, y*) for all x in X and Q(x*, y*) >= Q(x*, y) for all y in Y. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p46]
- Nash (1950) demonstrated that every strategic game with a finite number of players with von Neumann-Morgenstern preferences and a finite number of strategies has a Nash Equilibrium. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p48]
- John Nash proved in 1951 that every two-player game has at least one equilibrium, earning the 1994 Nobel Prize in Economics. [raw/books/strategy/Algorithms_to_Live_By.epub#L2685-L2687]
- Finding Nash equilibria has been proved computationally intractable by Christos Papadimitriou and colleagues from 2005 to 2008. [raw/books/strategy/Algorithms_to_Live_By.epub#L2715-L2717]
- The predictive abilities of Nash equilibria only matter if those equilibria can actually be found by the players. [raw/books/strategy/Algorithms_to_Live_By.epub#L2727-L2729]
- In rock-paper-scissors, the Nash equilibrium is to choose each option at random, each roughly one-third of the time. [raw/books/strategy/Algorithms_to_Live_By.epub#L2665-L2667]

## Inferences

- Inference: Nash Equilibrium generalizes the concept of scalar optimization to multi-player settings where each player's payoff depends on others' choices.
- Inference: The existence of Nash equilibrium does not guarantee players can reach or discover it, undermining its practical utility as a behavior prediction tool.
- Inference: Nash equilibria may not represent socially optimal outcomes—they are stable but not necessarily good.

## Uncertainties

- Uncertain: The exact computational complexity class of finding Nash equilibria remains an area of ongoing research.

## Related pages

- Broader: [[game-theory]]
- Broader: [[algorithmic-game-theory]]
- Narrower: [[subgame-perfect-equilibrium]]
- Narrower: [[trembling-hand-equilibrium]]
- Narrower: [[quantal-response-equilibrium]]
- Adjacent: [[dominant-strategy]]
- Adjacent: [[prisoners-dilemma]]
- Adjacent: [[price-of-anarchy]]
- Concepts: [[pure-strategy]]
- Concepts: [[mixed-strategy]]
- Concepts: [[best-response]]
- Concepts: [[game-theory]]
- Concepts: [[equilibrium]]
- Concepts: [[algorithmic-game-theory]]
- Concepts: [[recursion]]
- Entities: [[john-nash]]
- Entities: [[christos-papadimitriou]]

## Provenance

- Primary source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]
- Additional source: [raw/books/strategy/Algorithms_to_Live_By.epub#L1-L1]

## Change notes

- 2026-04-24 — page created by auto ingest.
- 2026-04-25 — merged contributions from `algorithms-to-live-by`.
