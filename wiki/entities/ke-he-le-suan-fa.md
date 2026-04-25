---
id: ke-he-le-suan-fa
title: 科赫勒算法
type: entity
status: draft
created: '2026-04-25'
updated: '2026-04-25'
sources:
- '[raw/books/economics/[诺贝尔经济学奖获奖者学术精品自选集]社会选择：个性与多准则·[美]肯尼思·约瑟夫·阿罗 著.pdf#p1-328]'
canonical: Kohler, G.
confidence: high
aliases:
- Kohler algorithm
- Kohler基本算法
- Kohler对偶算法
tags:
- 多准则决策
- 优序算法
- 科赫勒
related:
  concepts:
  - 优序方法
  - 谨慎序
  - 序贯独立性公理
  - 受控多数方法
  topics: []
  entities: []
---


# 科赫勒算法

## Summary

科赫勒算法是由法国格勒诺布尔大学应用数学系的科赫勒（G. Kohler）在1978年提出的一种多准则优序算法，用于从有限集合中选出最优或最差的对象。该算法通过逐次寻找优序矩阵行最小值中的最大值（或列最大值中的最小值），实现序贯的谨慎决策。

## Key facts

- 科赫勒基本算法（算法8.1）从当前优序矩阵的每一行中找出最小值，这些最小值中至少有一个大于其他的，如果有许多相同，则随意挑选出一个，这个最小值所在行对应的备择对象在多准则排序中会被排在第一位。. [raw/books/economics/[诺贝尔经济学奖获奖者学术精品自选集]社会选择：个性与多准则·[美]肯尼思·约瑟夫·阿罗 著.pdf#p257]
- 科赫勒对偶算法（算法8.2）从当前优序矩阵的每一列中找出最大值，这些最大值中至少有一个小于其他的，如果有许多相同，则随意挑选出一个，这个最大值所在列对应的备择对象在多准则排序中将被排在第(n-k+1)位。. [raw/books/economics/[诺贝尔经济学奖获奖者学术精品自选集]社会选择：个性与多准则·[美]肯尼思·约瑟夫·阿罗 著.pdf#p258]
- 即使常和特性不成立，解也不惟一，科赫勒算法仍产生在R_α内的一个序，并且相继的最大值中的最小值等于α。. [raw/books/economics/[诺贝尔经济学奖获奖者学术精品自选集]社会选择：个性与多准则·[美]肯尼思·约瑟夫·阿罗 著.pdf#p258]

## Inferences

- Inference: 科赫勒算法的设计体现了"急切的"排序策略——在每一步都试图尽快选出最好（或最差）的备择对象。
- Inference: 科赫勒基本算法与科赫勒对偶算法形成对偶关系，前者基于行最小值，后者基于列最大值。

## Related pages

- Concepts: [[优序方法]]
- Concepts: [[谨慎序]]
- Concepts: [[序贯独立性公理]]
- Concepts: [[受控多数方法]]

## Provenance

- Primary source: [raw/books/economics/[诺贝尔经济学奖获奖者学术精品自选集]社会选择：个性与多准则·[美]肯尼思·约瑟夫·阿罗 著.pdf#p1-328]

## Change notes

- 2026-04-25 — page created by auto ingest.
