---
id: prediction-error
title: Prediction Error
type: concept
status: draft
created: '2026-04-24'
updated: '2026-04-25'
sources:
- '[raw/books/neuroscience/Anxious - Joseph LeDoux.pdf#p1-610]'
- '[raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_
  Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]'
- '[raw/books/neuroscience/The Experience Machine_ How Our Minds Pred - Andy Clark.pdf#p1-325]'
confidence: high
related:
  broader:
  - learning
  - conditioning
  - reinforcement-learning
  - dopamine
  - predictive processing
  narrower:
  - temporal-difference-learning
  - rescorla-wagner-model
  adjacent:
  - extinction
  - reconsolidation
tags:
- prediction-error
- dopamine
- reinforcement-learning
- reward
- prediction error
- sensory processing
- learning
aliases: []
---

# Prediction Error

## Summary

Prediction error is a mismatch between expected and actual outcomes that drives new learning. In the Rescorla-Wagner model of conditioning, learning occurs when an outcome is surprising or unexpected. During extinction, the absence of the expected US creates a prediction error that triggers new learning (CS–no US association). Creating greater expectancy violations during extinction should improve therapeutic outcomes, which is why cognitive interventions may be better applied after exposure rather than during it.

## Key facts

- Prediction errors have been shown to be a significant factor in Pavlovian threat conditioning, extinction, and reinforcement of instrumental responses. [raw/books/neuroscience/Anxious - Joseph LeDoux.pdf#p375]
- Prediction error triggers new learning during extinction when the absence of the US conflicts with learned expectations. [raw/books/neuroscience/Anxious - Joseph LeDoux.pdf#p375]
- In temporal difference learning, the prediction error δ(t) = rt + γV(St+1) - V(St) drives learning, with positive errors when outcomes exceed predictions and negative errors when outcomes fall short. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p324]
- Dopamine neurons show phasic bursts when rewards are better than predicted (positive prediction error), no response when predicted (no error), and pauses when worse than predicted (negative prediction error). [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p325]
- During conditioning, the dopamine response shifts from the unpredicted reward to the reward-predicting conditioned stimulus, consistent with back-propagating prediction errors. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p326]
- When the brain's best guessing misses the mark, the mismatch with the actual sensory signal carries crucial new information (prediction error) that can be used to try again—to make a better guess. [raw/books/neuroscience/The Experience Machine_ How Our Minds Pred - Andy Clark.pdf#p9]
- Prediction error signals encode sensory information that the brain didn't manage to predict, and these flow forward and sideways, pushing deeper into the brain where they generate new, improved attempts at guessing. [raw/books/neuroscience/The Experience Machine_ How Our Minds Pred - Andy Clark.pdf#p37]
- In multilevel processing arrangements, all that flows forward from sensory edges into the brain is news—deviations from what is expected. Prediction errors at every level signal only the unexpected. [raw/books/neuroscience/The Experience Machine_ How Our Minds Pred - Andy Clark.pdf#p25]
- Error signals push, pull, and probe to see if there is stuff the brain already knows that would generate a more successful prediction, one better able to match the actual sensory signal. [raw/books/neuroscience/The Experience Machine_ How Our Minds Pred - Andy Clark.pdf#p37]

## Inferences

- Inference: The close correspondence between dopamine neuron firing patterns and TD prediction errors suggests that dopamine encodes a teaching signal for learning.
- Inference: Prediction error signals allow efficient information processing by updating only the discrepancy rather than transmitting full information about states.

## Uncertainties

- Uncertain: Whether dopamine encodes pure prediction errors or also incorporates motivational or attention-related signals is still debated.

## Related pages

- Broader: [[learning]]
- Broader: [[conditioning]]
- Broader: [[reinforcement-learning]]
- Broader: [[dopamine]]
- Broader: [[predictive processing]]
- Narrower: [[temporal-difference-learning]]
- Narrower: [[rescorla-wagner-model]]
- Adjacent: [[extinction]]
- Adjacent: [[reconsolidation]]
- Concepts: [[expectancy]]
- Concepts: [[surprise]]
- Concepts: [[dopamine]]
- Concepts: [[reinforcement-learning]]
- Concepts: [[learning-signal]]
- Concepts: [[precision weighting]]
- Concepts: [[controlled hallucination]]
- Topics: [[perception]]
- Topics: [[learning]]

## Provenance

- Primary source: [raw/books/neuroscience/Anxious - Joseph LeDoux.pdf#p1-610]
- Additional source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]
- Additional source: [raw/books/neuroscience/The Experience Machine_ How Our Minds Pred - Andy Clark.pdf#p1-325]

## Change notes

- 2026-04-24 — page created by auto ingest.
- 2026-04-25 — merged contributions from `neuroeconomics-decision-making-and-the-brain-paul-w-glimcher`.
- 2026-04-25 — merged contributions from `the-experience-machine-how-our-minds-pred-andy-clark`.
