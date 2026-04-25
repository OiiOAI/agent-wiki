---
id: team-api
title: Team API
type: concept
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/business/Team_Topologies.epub#L1-L1]'
confidence: medium
tags:
- team-api
- team-interactions
- boundaries
- documentation
related:
  broader:
  - team-first-thinking
  narrower: []
  adjacent:
  - conways-law
  - team-boundaries
---


# Team API

## Summary

A team API extends the concept of application programming interfaces to entire team interactions. It includes code (runtime endpoints, libraries, UI), versioning practices, documentation, team practices and principles, communication approaches, and work information. The team API should explicitly consider usability by other teams and define clear boundaries that minimize coordination costs. Organizations like Pivotal Cloud Foundry maintain API-based separation between teams, avoiding shared codebases and using pull requests or cross-team pairing for changes.

## Key facts

- A team API includes code (runtime endpoints, libraries, clients, UI), versioning practices, documentation, practices and principles, communication approaches, and work information. [raw/books/business/Team_Topologies.epub#L983-L987]
- At Pivotal Cloud Foundry, more than fifty teams maintain contract-based, API-based separation of concerns and do not share codebases between teams. [raw/books/business/Team_Topologies.epub#L992-L994]
- At AWS, each team must assume every other team becomes a potential denial of service attacker requiring service levels, quotas, and throttling. [raw/books/business/Team_Topologies.epub#L1000-L1002]
- The team API should explicitly consider usability by other teams, including ease of getting onboarded to code and working practices. [raw/books/business/Team_Topologies.epub#L989-L991]
- Teams should define, advertise, test, and evolve their team API to ensure it is fit for purpose for consumers: other teams. [raw/books/business/Team_Topologies.epub#L991-L993]

## Related pages

- Broader: [[team-first-thinking]]
- Adjacent: [[conways-law]]
- Adjacent: [[team-boundaries]]
- Concepts: [[interface-design]]
- Concepts: [[team-interactions]]
- Concepts: [[documentation]]

## Provenance

- Primary source: [raw/books/business/Team_Topologies.epub#L1-L1]

## Change notes

- 2026-04-23 — page created by auto ingest.
