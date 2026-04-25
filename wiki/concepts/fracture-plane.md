---
id: fracture-plane
title: Fracture plane
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/business/Team_Topologies.epub#L1-L1]'
confidence: high
tags:
- software-architecture
- team-design
- bounded-context
- domain-driven-design
related:
  broader:
  - team-first software boundaries
  narrower: []
  adjacent:
  - bounded context
  - monolith
  - microservices
---


# Fracture plane

## Summary

A fracture plane is a natural seam in a software system that allows it to be split easily into two or more parts, analogous to how stonemasons split rocks along their natural fracture planes. Fracture planes help identify natural split points that lead to software boundaries aligned with team capabilities. The primary fracture plane should map to business-domain bounded contexts, with other fracture planes including regulatory compliance, change cadence, team location, risk, performance isolation, technology, and user personas.

## Key facts

- A fracture plane is a natural seam in the software system that allows the system to be split easily into two or more parts. [raw/books/business/Team_Topologies.epub#L1271-L2183]
- Most fracture planes should map to business-domain bounded contexts as introduced in Eric Evans' book Domain-Driven Design. [raw/books/business/Team_Topologies.epub#L1271-L2183]
- Types of fracture planes include business domain bounded context, regulatory compliance, change cadence, team location, risk, performance isolation, technology, and user personas. [raw/books/business/Team_Topologies.epub#L1271-L2183]
- Splitting off parts of the system that change at different speeds allows each part to change more quickly, with business needs driving the speed of change rather than a monolith imposing a fixed pace. [raw/books/business/Team_Topologies.epub#L1271-L2183]
- The regulatory compliance fracture plane allows splitting subsystems subject to specific regulations (like PCI DSS) from the rest of the system to simplify auditing and reduce blast radius of regulatory oversight. [raw/books/business/Team_Topologies.epub#L1271-L2183]

## Related pages

- Broader: [[team-first software boundaries]]
- Adjacent: [[bounded context]]
- Adjacent: [[monolith]]
- Adjacent: [[microservices]]
- Concepts: [[domain-driven design]]
- Concepts: [[conway's law]]
- Concepts: [[cognitive load]]
- Entities: [[Eric Evans]]

## Provenance

- Primary source: [raw/books/business/Team_Topologies.epub#L1-L1]

## Change notes

- 2026-04-23 — page created by auto ingest.
