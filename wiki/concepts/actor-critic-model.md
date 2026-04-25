---
id: actor-critic-model
title: Actor-Critic Model
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
related:
  broader:
  - reinforcement-learning
  narrower:
  - q-learning
  - sarsa
  - temporal-difference-learning
  adjacent:
  - q-learning
  - temporal-difference-prediction-error-theory-of-dopamine
  - dorsal-striatum
tags:
- reinforcement-learning
- actor-critic
- basal-ganglia
- action-selection
aliases: []
---

# Actor-Critic Model

## Summary

The Actor-Critic Model is a reinforcement learning architecture where a critic circuit learns the reward value associated with different states of the environment (V(s)), and an actor circuit learns reward value associated with taking different actions in a given state (Q(s,a)). The critic combines the reward signal and state-value output to compute the reward prediction error, which updates both circuits.

## Key facts

- In RL models, a subnetwork responsible for value estimation is often referred to as the 'critic', which can be implemented as a single neuron receiving synaptic connections from sensory circuits. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p164]
- The critic circuit learns the reward value associated with different states of the environment, V(s_n), and the actor circuit learns reward value associated with taking different actions (e.g., A1 and A2) in a given state, Q(s_n,a_n). [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p164]
- The RPE is used to update value functions in the critic circuit and the action value functions in the actor circuit. [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p164]
- In Actor-Critic models, a critic module estimates state values V(S) using temporal difference learning, and the same prediction error δ(t) trains both the critic's values and the actor's policy π(S,a). [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p336]
- The actor updates policy according to π(S,a)new = π(S,a)old + ηπδ(t), where δ(t) is the temporal difference prediction error from the critic. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p336]
- Actor-Critic methods have been linked to action selection and prediction learning in the basal ganglia. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p336]
- In Actor/Critic models, the Critic learns to predict future rewards (state values) while the Actor learns a policy for action selection based on prediction errors. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p328]
- fMRI studies show correlates of prediction-error signals can be dissociated in dorsal and ventral striatum according to whether an action is required to obtain reward: for passive prediction-learning tasks the reward-prediction error is evident only in ventral striatum, while in active tasks it is evident in both ventral and dorsal striatum. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p329]
- Different computational algorithms (Actor/Critic, Q-learning, SARSA) make different predictions regarding the nature of cue-related prediction error, making electrophysiological evidence critical in constraining the algorithm actually used by the brain. [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p328]

## Inferences

- Inference: The Actor-Critic architecture solves the credit assignment problem by using the prediction error to assign credit or blame to actions at each timestep, even when external reinforcement is delayed.
- Inference: The dual-component structure allows for separate learning of what states are good (critic) and which actions lead to good states (actor).
- Inference: Morris et al. (2006) found that in catch trials where monkeys chose between two cues, cue-elicited prediction errors matched best the errors corresponding to the cue that would subsequently be chosen, contrary to Actor/Critic predictions but more in line with SARSA learning

## Uncertainties

- Uncertain: In the general case, Actor/Critic methods are not guaranteed to converge to optimal policies.
- Uncertain: The exact algorithm used by the brain remains uncertain as different studies favor different models

## Related pages

- Broader: [[reinforcement-learning]]
- Narrower: [[q-learning]]
- Narrower: [[sarsa]]
- Narrower: [[temporal-difference-learning]]
- Adjacent: [[q-learning]]
- Adjacent: [[temporal-difference-prediction-error-theory-of-dopamine]]
- Adjacent: [[dorsal-striatum]]
- Concepts: [[temporal-difference-learning]]
- Concepts: [[reward-prediction-error]]
- Concepts: [[basal-ganglia]]
- Concepts: [[policy-learning]]
- Concepts: [[value-learning]]
- Concepts: [[reinforcement-learning]]
- Concepts: [[model-free-learning]]
- Concepts: [[habit-learning]]

## Provenance

- Primary source: [raw/books/neuroscience/Decision Neuroscience _ An Integrative Perspective - Jean - Claude Dreher; Léon Tremblay; Institut de sciences.pdf#p1-401]
- Additional source: [raw/books/neuroscience/Neuroeconomics _ Decision Making and the Brain - Paul W_ Glimcher, Ernst Fehr, Colin Camerer, Antonio Rangel,.pdf#p1-507]

## Change notes

- 2026-04-24 — page created by auto ingest.
- 2026-04-25 — merged contributions from `neuroeconomics-decision-making-and-the-brain-paul-w-glimcher`.
