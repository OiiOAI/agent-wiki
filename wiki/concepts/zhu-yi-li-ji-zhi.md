---
id: zhu-yi-li-ji-zhi
title: 注意力机制
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/sociology/方正证券 - 计算机行业：解析ChatGPT背后的技术演进 - 230322.pdf#p1-40]'
confidence: high
tags:
- 注意力机制
- Attention
- 深度学习
- Transformer
related:
  broader:
  - 深度学习
  - 神经网络
  narrower:
  - 自注意力机制
  - 多头注意力机制
  - 交叉注意力机制
  adjacent:
  - Transformer
  - 循环神经网络
  - 卷积神经网络
---


# 注意力机制

## Summary

注意力（Attention）机制最早由Bengio团队在2014年提出，其思想来源于人类视觉注意力——先快速扫描全局，再聚焦重点区域。Attention在并行计算效率和解决长距离信息依赖能力上优于传统RNN和CNN，成为大语言模型的基石。

## Key facts

- 注意力机制最早由Bengio团队在2014年提出，随后广泛应用于深度学习各领域. [raw/books/sociology/方正证券 - 计算机行业：解析ChatGPT背后的技术演进 - 230322.pdf#p6]
- Attention在每一层计算中都考虑词与词之间的全连接关系，能够解决长距离信息依赖问题. [raw/books/sociology/方正证券 - 计算机行业：解析ChatGPT背后的技术演进 - 230322.pdf#p11]
- Attention模型是并行计算的，可大幅提升语言模型运行效率，契合现代GPU硬件架构. [raw/books/sociology/方正证券 - 计算机行业：解析ChatGPT背后的技术演进 - 230322.pdf#p11]
- CNN可看作有注意力范围的Attention，Attention则是实现了全连接的CNN. [raw/books/sociology/方正证券 - 计算机行业：解析ChatGPT背后的技术演进 - 230322.pdf#p12]
- 自注意力机制（Self-Attention）是Transformer大语言模型的核心组成部分. [raw/books/sociology/方正证券 - 计算机行业：解析ChatGPT背后的技术演进 - 230322.pdf#p13]

## Inferences

- Inference: Self-Attention通过Q、K、V三个向量序列进行计算，本质是对输入矩阵进行多次矩阵变换

## Related pages

- Broader: [[深度学习]]
- Broader: [[神经网络]]
- Narrower: [[自注意力机制]]
- Narrower: [[多头注意力机制]]
- Narrower: [[交叉注意力机制]]
- Adjacent: [[Transformer]]
- Adjacent: [[循环神经网络]]
- Adjacent: [[卷积神经网络]]
- Concepts: [[QKV向量]]
- Concepts: [[Softmax归一化]]

## Provenance

- Primary source: [raw/books/sociology/方正证券 - 计算机行业：解析ChatGPT背后的技术演进 - 230322.pdf#p1-40]

## Change notes

- 2026-04-24 — page created by auto ingest.
