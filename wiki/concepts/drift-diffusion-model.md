---
id: drift-diffusion-model
title: Drift-Diffusion Model
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-25'
sources:
- '[raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean
  - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p1-401]'
- '[raw/books/neuroscience/Eric Kandel PRINCIPLES OF NEURAL SCIENCE Sixth Edition
  - Eric R Kandel; John Koester; Sarah Mack; Steven Siegelbaum.pdf#p1-1695]'
confidence: high
tags:
- computational-neuroscience
- decision-making
- psychophysics
- models
- perceptual-decisions
- drift-diffusion
related:
  broader:
  - sequential-sampling-models
  - perceptual-decision-making
  - decision-making
  narrower:
  - leaky-competing-accumulator
  adjacent:
  - speed-accuracy-tradeoff
  - sequential-probability-ratio-test
aliases: []
---

# Drift-Diffusion Model

## Summary

The drift-diffusion model (DDM) is a sequential sampling model that describes perceptual decision-making as a noisy accumulation of sensory evidence toward a decision threshold. The model posits that decisions are made when the accumulated evidence reaches one of two boundaries, with the drift rate reflecting the quality of sensory evidence and boundary height controlling the speed-accuracy trade-off. The DDM and related bounded diffusion models have been used extensively to explain reaction time distributions and choice behavior in two-alternative forced choice tasks.

## Key facts

- Sequential sampling models assume that the decision process involves an integrative mechanism whereby the difference in sensory evidence supporting alternatives accumulates over time to a preset internal decision boundary. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p137]
- In the drift-diffusion model, response times are well described when exact log probabilities are replaced by a momentary input variable composed of signal and noise, with the drift rate reflecting relative evidence for one category over another. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p150]
- The height of the decision bound in the DDM controls the speed-accuracy trade-off; as the bound is raised, decisions become slower but more accurate. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p156]
- A key issue with bounded diffusion models is that they predict a long tail to the distribution of decision latencies that is rarely observed in empirical studies. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p157]
- The drift-diffusion model posits that evidence accumulates as a biased random walk until reaching one of two stopping bounds, which determines the decision outcome. [raw/books/neuroscience/Eric Kandel PRINCIPLES OF NEURAL SCIENCE Sixth Edition - Eric R Kandel; John Koester; Sarah Mack; Steven Siegelbaum.pdf#p1401]
- Sensitivity to weak sensory signals improves as the square root of viewing duration, consistent with the statistical prediction of averaging noisy samples. [raw/books/neuroscience/Eric Kandel PRINCIPLES OF NEURAL SCIENCE Sixth Edition - Eric R Kandel; John Koester; Sarah Mack; Steven Siegelbaum.pdf#p1401]
- Tight stopping bounds lead to fast but error-prone decisions, while distant bounds lead to slower but more accurate decisions. [raw/books/neuroscience/Eric Kandel PRINCIPLES OF NEURAL SCIENCE Sixth Edition - Eric R Kandel; John Koester; Sarah Mack; Steven Siegelbaum.pdf#p1401]
- Neurons in the lateral intraparietal area (LIP) represent the accumulation of evidence, with firing rates reaching a common threshold level just before a decision is executed. [raw/books/neuroscience/Eric Kandel PRINCIPLES OF NEURAL SCIENCE Sixth Edition - Eric R Kandel; John Koester; Sarah Mack; Steven Siegelbaum.pdf#p1406]
- Microstimulation of direction-selective neurons in area MT biases perceptual decisions in favor of the preferred direction of the stimulated neurons. [raw/books/neuroscience/Eric Kandel PRINCIPLES OF NEURAL SCIENCE Sixth Edition - Eric R Kandel; John Koester; Sarah Mack; Steven Siegelbaum.pdf#p1400]

## Inferences

- Inference: The DDM provides a computational framework linking neural activity (such as the buildup of firing rates in LIP) to behavioral parameters like drift rate and decision boundaries.

## Uncertainties

- Uncertain: The debate over whether decisions are driven by flat or collapsing bounds remains unresolved.
- Uncertain: The relationship between urgency signals and bounded diffusion processes is still being investigated.

## Related pages

- Broader: [[sequential-sampling-models]]
- Broader: [[perceptual-decision-making]]
- Broader: [[decision-making]]
- Narrower: [[leaky-competing-accumulator]]
- Adjacent: [[speed-accuracy-tradeoff]]
- Adjacent: [[sequential-probability-ratio-test]]
- Concepts: [[perceptual-decision-making]]
- Concepts: [[lateral-intraparietal-area-lip]]
- Concepts: [[signal-detection-theory]]
- Concepts: [[perceptual-decision]]
- Concepts: [[evidence-accumulation]]
- Concepts: [[lateral-intraparietal-area]]
- Entities: [[William Newsome]]
- Entities: [[Michael Shadlen]]

## Provenance

- Primary source: [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p1-401]
- Additional source: [raw/books/neuroscience/Eric Kandel PRINCIPLES OF NEURAL SCIENCE Sixth Edition - Eric R Kandel; John Koester; Sarah Mack; Steven Siegelbaum.pdf#p1-1695]

## Change notes

- 2026-04-24 — page created by auto ingest.
- 2026-04-25 — merged contributions from `kandel-neural-science-6e`.
