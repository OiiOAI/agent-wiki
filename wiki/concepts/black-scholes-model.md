---
id: black-scholes-model
title: Black-Scholes模型
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p1-516]'
confidence: high
tags:
- Black-Scholes
- 期权估价
- 看涨期权
- 看跌期权
- 平价
- 波动率
related:
  broader:
  - 利息的随机处理
  narrower:
  - 期权估价
  - 波动率
  - 平价关系
  adjacent:
  - 资本资产定价模型
---


# Black-Scholes模型

## Summary

Black-Scholes期权估价模型建立了欧式看涨期权和看跌期权的解析定价公式。该模型假设股票收益率服从对数正态分布，基于无套利均衡思想。看涨期权公式为C=S·N(d_1)−E·e^{−rτ}·N(d_2)，其中d_1和d_2涉及股票价格、履行价格、时间、无风险利率和波动率等参数。

## Key facts

- Black-Scholes公式假设1+i_t服从对数正态分布，这恰与10.2和10.3节中对随机利率的对数正态假设相呼应. [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p408]
- 欧式看涨期权的Black-Scholes公式：C=S·N(d_1)−E·e^{−rτ}·N(d_2)，其中d_1和d_2如书中(10.39a)和(10.39b)式所定义. [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p408]
- 对于不支付红利的股票，早期履行不是最优选择，因此美国看涨期权价值等于欧式看涨期权价值. [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p409]
- 看跌期权-看涨期权平价关系为P+S=C+E·e^{−rτ}，表明四者（看跌期权、看涨期权、股票、国库券）中已知三者即可确定第四者. [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p405]

## Related pages

- Broader: [[利息的随机处理]]
- Narrower: [[期权估价]]
- Narrower: [[波动率]]
- Narrower: [[平价关系]]
- Adjacent: [[资本资产定价模型]]
- Concepts: [[Black-Scholes公式]]
- Concepts: [[期权]]
- Concepts: [[看涨期权]]
- Concepts: [[看跌期权]]
- Concepts: [[平价]]
- Concepts: [[波动率]]

## Provenance

- Primary source: [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p1-516]

## Change notes

- 2026-04-25 — page created by auto ingest.
