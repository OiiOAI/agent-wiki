---
id: reward-prediction-error
title: Reward-Prediction Error
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-25'
sources:
- '[raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean
  - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p1-401]'
- '[raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_
  Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]'
confidence: high
tags:
- reward prediction error
- reinforcement learning
- dopamine
- prediction
- error signals
- reward
- learning
- prediction-error
- neuroscience
related:
  broader:
  - reinforcement learning
  - dopamine signaling
  - reward processing
  - reinforcement-learning
  - decision-neuroscience
  narrower:
  - temporal difference learning
  - eligibility traces
  - delta-rule
  - temporal-difference-learning
  adjacent:
  - dopamine neurons
  - ventral striatum
  - ventral tegmental area
  - dopamine-dependent-plasticity
  - temporal-difference-learning
  - actor-critic-model
  - temporal-difference-prediction-error-theory-of-dopamine
  - dopamine
  - reinforcement-learning
aliases: []
---

# Reward-Prediction Error

## Summary

The reward-prediction error (RPE) signal is a neural signal that reports the difference between received and predicted reward. This signal is a fundamental component of reinforcement learning models, encoding both positive errors (when reward exceeds prediction) and negative errors (when reward is worse than predicted or omitted).

## Key facts

- Dopamine neurons report reward-prediction errors through phasic increases in activity for positive errors and depressions for negative errors, occurring at latencies less than 100 ms and durations less than 200 ms. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p21]
- The Rescorla-Wagner model describes prediction error as the difference between received reward λ(t) and predicted reward V(t), expressed as PE(t) = λ(t) − V(t). [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p21]
- Temporal difference (TD) learning extends the Rescorla-Wagner model by incorporating the temporal progression of reward predictions across time steps within a trial. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p21]
- Dopamine RPE responses satisfy formal prediction error tests including blocking (where a stimulus is not learned when reward is fully predicted by another stimulus) and conditioned inhibition. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p22]
- Studies identified three novel properties of the dopamine RPE signal: an initial unselective response to salient events followed by specific reward-prediction error processing, subjective reward value and formal economic utility reflection, and compatibility with competitive decision models. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p21]
- The learning rule minimizes the difference between actual reward and the system's reward prediction; hence the error term is equivalent to the RPE. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p164]
- Dopaminergic neurons encode RPE signals that are both positive and negative values, whereas the neural response of DA neurons can only be positive. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p165]
- The RPE is used to update value functions in the critic circuit and action value functions in the actor circuit. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p164]
- Reward prediction error is defined as the difference between obtained and expected reward, driving learning via the delta rule. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p291]
- Midbrain dopamine neurons encode RPE parametrically—their firing rate scales with the magnitude of reward prediction error. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p294]
- fMRI correlates of RPE have been observed in the midbrain, striatum, and ventromedial prefrontal cortex. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p294]
- Psychosis patients show disrupted RPE signaling in the dopaminergic midbrain and attenuated responses in the ventral striatum. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p255]
- Methamphetamine administration in healthy volunteers disrupts striatal RPE-associated activity and induces mild psychotic symptoms. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p257]
- Dopamine neurons initially fired in response to juice but not to a tone that preceded it; once the monkey learned to associate tone with juice, dopamine responded to the tone but not to the juice. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p25]
- Once learning had taken place, if the tone was played but the monkey did not receive the juice, there was a pause or drop in the background level of dopamine activity. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p25]
- The RPE hypothesis states that dopamine responds to the difference between how rewarding an event is and how rewarding it was expected to be. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p25]
- The DRPE (dopaminergic reward prediction error) representation requires three properties: the reward function must represent the dopamine release function, respect dopaminergic dominance, and satisfy no surprise constancy. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p27]
- Dopamine neurons increase firing when reward is presented unexpectedly, decrease from baseline when reward is unexpectedly omitted, and respond initially at US time before learning but shift to CS time after learning is established. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p379]
- The temporal-difference prediction error δt = rt + γ V(st+1) - V(st) provides a signal theoretically appropriate for controlling learning. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p328]
- Pessiglione et al. (2006) provided causal evidence linking striatal prediction-error activity to learning: dopamine agonist boosted prediction-error signals and improved learning, while antagonist diminished both. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p380]

## Inferences

- Inference: The RPE signal follows a two-component structure, with an initial brief unselective activation followed by a specific reward-prediction error component that distinguishes this from simpler salience coding.
- Inference: Dopamine responses to punishers reflect physical impact rather than aversiveness when adequately controlled, suggesting the initial response component handles general salience detection.
- Inference: The RPE signal functions as an ideal teaching signal for updating decision variables and may have immediate effects on choice behavior.
- Inference: The finding that methamphetamine (which floods the striatum with dopamine) disrupts RPE signaling and induces psychotic symptoms suggests a causal link between RPE dysregulation and psychosis.
- Inference: The RPE theory revolutionized understanding of dopamine function by showing that dopamine signals are not simply hedonic rewards but encode learning signals about prediction errors.
- Inference: The axiomatic approach to testing RPE allows researchers to verify whether dopamine activity has the formal structure required by the theory without assuming specific parametric forms for how rewards and beliefs are formed.

## Uncertainties

- Uncertain: The exact cellular and molecular mechanisms by which dopamine RPE signals update synaptic weights remain partially characterized.
- Uncertain: Alternative hypotheses suggest dopamine encodes 'salience' or 'incentive salience' rather than reward prediction error; these competing views remain debated in the neuroscience community.

## Related pages

- Broader: [[reinforcement learning]]
- Broader: [[dopamine signaling]]
- Broader: [[reward processing]]
- Broader: [[reinforcement-learning]]
- Broader: [[decision-neuroscience]]
- Narrower: [[temporal difference learning]]
- Narrower: [[eligibility traces]]
- Narrower: [[delta-rule]]
- Narrower: [[temporal-difference-learning]]
- Adjacent: [[dopamine neurons]]
- Adjacent: [[ventral striatum]]
- Adjacent: [[ventral tegmental area]]
- Adjacent: [[dopamine-dependent-plasticity]]
- Adjacent: [[temporal-difference-learning]]
- Adjacent: [[actor-critic-model]]
- Adjacent: [[temporal-difference-prediction-error-theory-of-dopamine]]
- Adjacent: [[dopamine]]
- Adjacent: [[reinforcement-learning]]
- Concepts: [[temporal difference learning]]
- Concepts: [[utility prediction error]]
- Concepts: [[chosen value]]
- Concepts: [[eligibility traces]]
- Concepts: [[Rescorla-Wagner model]]
- Concepts: [[reinforcement learning]]
- Concepts: [[value-based decision-making]]
- Concepts: [[dopamine-and-reward]]
- Concepts: [[actor-critic-model]]
- Concepts: [[dopamine]]
- Concepts: [[reinforcement-learning]]
- Concepts: [[utility-estimation]]
- Concepts: [[neural-coding]]
- Concepts: [[temporal-difference]]
- Concepts: [[learning-signal]]
- Topics: [[neuroscience]]
- Topics: [[learning]]
- Entities: [[ventral-tegmental-area]]
- Entities: [[ventral-striatum]]
- Entities: [[wolfram-schultz]]
- Entities: [[peter-shizgal]]

## Provenance

- Primary source: [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p1-401]
- Additional source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]

## Change notes

- 2026-04-24 — page created by auto ingest.
- 2026-04-25 — merged contributions from `neuroeconomics-decision-making-and-the-brain-paul-w-glimcher`.
