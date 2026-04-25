---
id: stochastic-interest-theory
title: 利息的随机处理
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p1-516]'
confidence: high
tags:
- 随机利率
- 独立利率
- 相关利率
- AR过程
- 对数正态分布
- 自回归
related:
  broader:
  - 利息理论
  narrower:
  - 独立利率
  - 相关利率
  - AR过程
  - 对数正态分布
  adjacent:
  - 资本资产定价模型
  - Black-Scholes模型
---


# 利息的随机处理

## Summary

本章讨论将利率作为随机变量处理的理论。核心发现是期望积累值和期望现时值不一定等于按期望利率计算的积累值和现时值。书中介绍了独立利率情形和相关利率情形（AR(1)和AR(2)自回归过程），以及当假设对数正态分布时可直接得出概率描述而无需模拟。

## Key facts

- 期望积累值E[a(n)]=Π(1+E[i_t])仅在i_t独立同分布时成立；期望利率下的积累值(1+E[i])^n一般小于期望积累值. [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p381]
- 若假设对数正态分布（log(1+i_t)服从正态分布），则a(n)服从对数正态分布，可直接得出概率描述而不需模拟. [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p386]
- AR(1)自回归过程：i_t=δ+k(i_{t-1}−δ)+ε_t，其中常数k∈(0,1)是赋予长期平均利率和上一期利率的相对权因子. [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p392]
- AR(2)自回归过程引入两个参数k1和k2，使利率同时依赖于前两期利率. [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p395]

## Related pages

- Broader: [[利息理论]]
- Narrower: [[独立利率]]
- Narrower: [[相关利率]]
- Narrower: [[AR过程]]
- Narrower: [[对数正态分布]]
- Adjacent: [[资本资产定价模型]]
- Adjacent: [[Black-Scholes模型]]
- Concepts: [[随机利率]]
- Concepts: [[独立利率]]
- Concepts: [[相关利率]]
- Concepts: [[AR过程]]
- Concepts: [[对数正态分布]]
- Concepts: [[期望积累值]]

## Provenance

- Primary source: [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p1-516]

## Change notes

- 2026-04-25 — page created by auto ingest.
