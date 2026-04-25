---
id: unknown-interest-rate-problems
title: 未知利率问题
type: concept
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p1-516]'
confidence: high
tags:
- 利率
- 迭代法
- Newton-Raphson
related:
  broader: []
  narrower: []
  adjacent: []
---


# 未知利率问题

## Summary

本章讨论当利率i为未知时如何求解年金值问题。介绍了三种求解方法：代数方法、利息表线性插值法、以及逐次逼近法（迭代法）。其中Newton-Raphson迭代法收敛速度快，效果最佳。

## Key facts

- 第一种方法是用代数方法解n次多项式，仅当n值很小时才实用. [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p93]
- 第二种方法是在利息表中用线性插值. [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p94]
- 第三种也是最好的方法是逐次逼近法，可以达到任意要求的精度. [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p94]
- Newton-Raphson迭代公式(3.28)用于求解延付年金的未知利率，收敛速度很快. [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p95]
- 初始值可用利息表中线性插值方法或近似公式(3.29)得到. [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p95]
- 例3.8：用Newton-Raphson方法经过3次迭代就达到七位小数的精度，而ad hoc方法经过15次迭代后甚至还达不到五位小数的精度. [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p97]

## Inferences

- Inference: 公式(3.29)类似于7.6节中给出的计算近似债券收益的常用公式
- Inference: 对于积累值，Newton-Raphson迭代公式为(3.30)，类似公式为(3.31)

## Related pages

- Concepts: [[未知时间问题]]
- Concepts: [[Newton-Raphson迭代法]]
- Concepts: [[线性插值]]
- Topics: [[年金理论]]

## Provenance

- Primary source: [raw/books/economics/[保险精算丛书]利息理论·[美]S.G.凯利森 著.pdf#p1-516]

## Change notes

- 2026-04-25 — page created by auto ingest.
