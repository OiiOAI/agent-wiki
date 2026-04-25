---
id: hidden-monoliths
title: Hidden monoliths
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/business/Team_Topologies.epub#L1-L1]'
confidence: high
tags:
- software-architecture
- monolith
- anti-patterns
- coupling
related:
  broader:
  - software architecture
  narrower: []
  adjacent:
  - fracture plane
  - microservices
  - monolith
---


# Hidden monoliths

## Summary

Hidden monoliths are types of monolithic software that are hard to detect at first. Beyond the traditional application monolith, organizations may have joined-at-the-database monoliths (multiple applications coupled to the same database), monolithic builds (single CI build for entire codebase), monolithic releases (components bundled together), monolithic models (single domain language forced across contexts), monolithic thinking (one-size-fits-all standardization), and monolithic workplaces (standardized office layouts).

## Key facts

- A joined-at-the-database monolith is composed of several applications or services all coupled to the same database schema, making them difficult to change, test, and deploy separately. [raw/books/business/Team_Topologies.epub#L1271-L2183]
- A monolithic build uses one gigantic CI build to get a new version of a component instead of using standard dependency-management mechanisms between components. [raw/books/business/Team_Topologies.epub#L1271-L2183]
- A monolithic release is a set of smaller components bundled together for deployment, often because components can only be tested in a shared static environment. [raw/books/business/Team_Topologies.epub#L1271-L2183]
- Monolithic thinking is 'one size fits all' thinking for teams that leads to unnecessary restrictions on technology and implementation approaches, reducing learning and experimentation. [raw/books/business/Team_Topologies.epub#L1271-L2183]
- A distributed monolith results when organizations split a monolith into smaller services but create a complex system of interdependent services where almost all changes require updates to other services. [raw/books/business/Team_Topologies.epub#L1271-L2183]

## Related pages

- Broader: [[software architecture]]
- Adjacent: [[fracture plane]]
- Adjacent: [[microservices]]
- Adjacent: [[monolith]]
- Concepts: [[Conway's law]]
- Concepts: [[coupling]]
- Concepts: [[decoupling]]

## Provenance

- Primary source: [raw/books/business/Team_Topologies.epub#L1-L1]

## Change notes

- 2026-04-23 — page created by auto ingest.
