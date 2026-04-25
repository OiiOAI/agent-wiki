---
id: bufferbloat
title: Bufferbloat
type: concept
status: draft
created: '2026-04-22'
updated: '2026-04-22'
sources:
- '[raw/books/strategy/Algorithms_to_Live_By.epub#L1-L1]'
confidence: high
tags:
- networking
- latency
- buffers
- performance
related:
  broader:
  - networking
  - queueing-theory
  narrower: []
  adjacent:
  - tcp
  - aimd
  - latency
---


# Bufferbloat

## Summary

Bufferbloat is a phenomenon where network buffers become excessively large, causing high latency while maintaining high throughput. It was discovered by Jim Gettys in 2010 and affects virtually all networking devices from modems to smartphones. The problem arises because buffers designed to smooth traffic bursts end up creating massive queues that delay all packets, including time-sensitive acknowledgments.

## Key facts

- Jim Gettys discovered bufferbloat in 2010 when analyzing why his home network was slow during file transfers. [raw/books/strategy/Algorithms_to_Live_By.epub#L2266-L2270]
- Bufferbloat affects modems, routers, laptops, smartphones, and the infrastructure of the Internet itself. [raw/books/strategy/Algorithms_to_Live_By.epub#L2277-L2279]
- The problem emerged when cheap memory allowed manufacturers to include gigabytes of RAM, creating buffers thousands of times too large for their actual throughput. [raw/books/strategy/Algorithms_to_Live_By.epub#L2319-L2322]
- Large buffers prevent TCP's congestion control from working properly because they hide packet loss, which is the signal that triggers bandwidth reduction. [raw/books/strategy/Algorithms_to_Live_By.epub#L2311-L2314]
- The fundamental principle of buffers is that they only work correctly when routinely emptied to zero. [raw/books/strategy/Algorithms_to_Live_By.epub#L2307-L2308]

## Inferences

- Inference: Bufferbloat illustrates a broader principle that optimizing for one metric (throughput) can worsen another (latency), and that 'better never than late' applies to interactive communications.
- Inference: The human parallel is being 'always buffered' rather than 'always connected'—the difference between processing information in real-time versus accumulating it indefinitely.

## Related pages

- Broader: [[networking]]
- Broader: [[queueing-theory]]
- Adjacent: [[tcp]]
- Adjacent: [[aimd]]
- Adjacent: [[latency]]
- Concepts: [[throughput]]
- Concepts: [[latency]]
- Concepts: [[tail-drop]]
- Concepts: [[queue-management]]
- Entities: [[jim-gettys]]
- Entities: [[van-jacobson]]

## Provenance

- Primary source: [raw/books/strategy/Algorithms_to_Live_By.epub#L1-L1]

## Change notes

- 2026-04-22 — page created by auto ingest.
