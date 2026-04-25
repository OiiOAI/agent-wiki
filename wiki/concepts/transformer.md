---
id: transformer
title: Transformer
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-24'
sources:
- '[raw/books/sociology/方正证券 - 计算机行业：解析ChatGPT背后的技术演进 - 230322.pdf#p1-40]'
confidence: high
tags:
- Transformer
- Google
- 注意力机制
- 大语言模型
related:
  broader:
  - 深度学习
  - 注意力机制
  narrower:
  - 编码器
  - 解码器
  - 自注意力机制
  - 多头注意力机制
  adjacent:
  - GPT
  - BERT
  - 大语言模型
---


# Transformer

## Summary

Transformer是Google于2017年在论文《Attention is All You Need》中提出的模型架构，完全由Attention机制组成，没有使用传统CNN和RNN。Transformer由编码器和解码器两部分构成，编码器模拟语言理解，解码器模拟语言生成。Self-Attention是其最核心部分。

## Key facts

- 2017年Google机器翻译团队发布Transformer模型，抛弃传统CNN和RNN，完全由Attention机制组成. [raw/books/sociology/方正证券 - 计算机行业：解析ChatGPT背后的技术演进 - 230322.pdf#p6]
- Transformer由6个编码器和6个解码器堆叠而成，编码器-解码器结构模拟大脑理解自然语言的过程. [raw/books/sociology/方正证券 - 计算机行业：解析ChatGPT背后的技术演进 - 230322.pdf#p15]
- 编码器由Multi-head Attention和Feed Forward Neural Network两个子层组成，均加入Add&Norm层. [raw/books/sociology/方正证券 - 计算机行业：解析ChatGPT背后的技术演进 - 230322.pdf#p16]
- 解码器与编码器的最大不同是使用了带遮盖的自注意力机制（Masked Self-attention），只能依赖当前时刻以前的输出. [raw/books/sociology/方正证券 - 计算机行业：解析ChatGPT背后的技术演进 - 230322.pdf#p17]
- OpenAI的GPT使用解码器部分，Google的BERT使用编码器部分，二者技术路线不同. [raw/books/sociology/方正证券 - 计算机行业：解析ChatGPT背后的技术演进 - 230322.pdf#p18]
- Transformer在机器翻译、文本生成、问答系统等任务上性能均超过之前模型，训练速度快于RNN模型7倍. [raw/books/sociology/方正证券 - 计算机行业：解析ChatGPT背后的技术演进 - 230322.pdf#p19]

## Related pages

- Broader: [[深度学习]]
- Broader: [[注意力机制]]
- Narrower: [[编码器]]
- Narrower: [[解码器]]
- Narrower: [[自注意力机制]]
- Narrower: [[多头注意力机制]]
- Adjacent: [[GPT]]
- Adjacent: [[BERT]]
- Adjacent: [[大语言模型]]
- Concepts: [[残差连接]]
- Concepts: [[层标准化]]
- Concepts: [[前馈神经网络]]

## Provenance

- Primary source: [raw/books/sociology/方正证券 - 计算机行业：解析ChatGPT背后的技术演进 - 230322.pdf#p1-40]

## Change notes

- 2026-04-24 — page created by auto ingest.
