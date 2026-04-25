---
id: exponential-backoff
title: Exponential Backoff
type: concept
status: draft
created: '2026-04-22'
updated: '2026-04-22'
sources:
- '[raw/books/strategy/Algorithms_to_Live_By.epub#L1-L1]'
confidence: high
tags:
- networking
- algorithm
- retry
- justice-reform
related:
  broader:
  - networking-protocols
  - retry-strategies
  narrower: []
  adjacent:
  - tcp
  - alohanet
---


# Exponential Backoff

## Summary

Exponential Backoff is an algorithm for handling network congestion and transmission failures by doubling the wait time after each failed attempt. Originally developed for the ALOHAnet in the 1970s, it is now embedded in TCP/IP protocols and has been adopted in fields from security (password lockout) to criminal justice (the HOPE probation program).

## Key facts

- Exponential Backoff was invented at the ALOHAnet in 1971 to prevent network collisions from cascading into permanent failure. [raw/books/strategy/Algorithms_to_Live_By.epub#L2137-L2141]
- After a failed transmission, a sender waits 1-2 turns; after two failures, 1-4 turns; after three failures, 1-8 turns, and so on. [raw/books/strategy/Algorithms_to_Live_By.epub#L2137-L2141]
- Exponential Backoff is now used in TCP/IP for all network failure handling and in security for account lockout after failed password attempts. [raw/books/strategy/Algorithms_to_Live_By.epub#L2146-L2149]
- The HOPE probation program in Hawaii applies Exponential Backoff principles: immediate, predefined punishments that increase after each violation, starting with one day in jail. [raw/books/strategy/Algorithms_to_Live_By.epub#L2175-L2179]
- HOPE probationers were 72% less likely to use drugs and half as likely to be rearrested compared to regular probationers. [raw/books/strategy/Algorithms_to_Live_By.epub#L2180-L2181]

## Inferences

- Inference: The algorithm embodies 'finite patience and infinite mercy'—never completely giving up while avoiding endless wasted effort.

## Related pages

- Broader: [[networking-protocols]]
- Broader: [[retry-strategies]]
- Adjacent: [[tcp]]
- Adjacent: [[alohanet]]
- Concepts: [[congestion-control]]
- Concepts: [[flow-control]]
- Concepts: [[packet-switching]]
- Entities: [[alohanet]]
- Entities: [[hope-probation]]
- Entities: [[norman-abramson]]

## Provenance

- Primary source: [raw/books/strategy/Algorithms_to_Live_By.epub#L1-L1]

## Change notes

- 2026-04-22 — page created by auto ingest.
