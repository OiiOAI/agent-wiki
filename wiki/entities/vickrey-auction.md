---
id: vickrey-auction
title: Vickrey Auction
type: entity
status: draft
created: '2026-04-22'
updated: '2026-04-22'
sources:
- '[raw/books/strategy/Algorithms_to_Live_By.epub#L1-L1]'
canonical: vickrey-auction
confidence: high
aliases:
- second-price sealed-bid auction
- Vickrey auction
- Vickrey-Clarke-Groves auction
tags:
- auctions
- mechanism-design
- game-theory
- economics
related:
  concepts:
  - mechanism-design
  - auction-theory
  - dominant-strategy
  - strategy-proof
  topics: []
  entities:
  - william-vickrey
---


# Vickrey Auction

## Summary

The Vickrey auction, named after Nobel laureate William Vickrey, is a sealed-bid auction where the highest bidder wins but pays the second-highest bid amount rather than their own. This design has the remarkable property of making honesty the dominant strategy— bidders maximize expected value by bidding their true valuation. The Vickrey auction demonstrates that it is possible to design games where truth-telling is optimal, exemplifying the mechanism designer's goal of strategy-proofness.

## Key facts

- In a Vickrey auction, the winner pays not their own bid but the second-highest bid amount. [raw/books/strategy/Algorithms_to_Live_By.epub#L3010-L3012]
- In a Vickrey auction, honesty is the dominant strategy—no better strategy exists than bidding one's true value for the item. [raw/books/strategy/Algorithms_to_Live_By.epub#L3020-L3022]
- Revenue equivalence establishes that over time, the average expected sale price in a first-price auction converges to precisely the same as in a Vickrey auction. [raw/books/strategy/Algorithms_to_Live_By.epub#L3035-L3037]
- William Vickrey won the Nobel Prize in Economics in 1996 for his work on auction theory. [raw/books/strategy/Algorithms_to_Live_By.epub#L3005-L3007]

## Inferences

- Inference: The Vickrey auction's strategy-proof property means bidders don't need to recursively anticipate others' bidding behavior, eliminating the computational burden of mental simulation.

## Related pages

- Broader: [[auctions]]
- Broader: [[mechanism-design]]
- Narrower: [[revelation-principle]]
- Adjacent: [[mechanism-design]]
- Adjacent: [[dominant-strategy]]
- Adjacent: [[information-cascade]]
- Concepts: [[mechanism-design]]
- Concepts: [[auction-theory]]
- Concepts: [[dominant-strategy]]
- Concepts: [[strategy-proof]]
- Entities: [[william-vickrey]]

## Provenance

- Primary source: [raw/books/strategy/Algorithms_to_Live_By.epub#L1-L1]

## Change notes

- 2026-04-22 — page created by auto ingest.
