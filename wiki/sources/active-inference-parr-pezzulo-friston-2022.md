---
id: active-inference-parr-pezzulo-friston-2022
title: 'Active Inference: The Free Energy Principle in Mind, Brain, and Behavior'
type: source
status: draft
created: '2026-04-23'
updated: '2026-04-23'
sources:
- '[raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain,
  - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]'
source_kind: book
source_path: raw/books/neuroscience/Active Inference _ The Free Energy Principle in
  Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf
source_date: '2022'
source_author: Thomas Parr; Giovanni Pezzulo; Karl J. Friston
reliability: high
tags:
- neuroscience
- cognitive science
- active inference
- bayesian
- free energy
- normative theory
- generative models
- predictive processing
---


# Active Inference: The Free Energy Principle in Mind, Brain, and Behavior

## Summary

This book, published by MIT Press in 2022, presents Active Inference as a normative framework to understand brain, mind, and behavior from first principles. Written by Thomas Parr, Giovanni Pezzulo, and Karl J. Friston, it is structured in two parts: the first (chapters 1–5) introduces the conceptual and formal foundations of Active Inference, while the second (chapters 6–10) illustrates practical computational models. The book motivates Active Inference through two complementary 'roads'—the low road (starting from Bayesian brain theory) and the high road (starting from the free energy principle and self-organization). Core constructs include variational free energy, expected free energy, generative models (POMDPs and continuous-time models), and message passing, with implications for perception, action, planning, and learning.

## Key facts

- The book 'Active Inference: The Free Energy Principle in Mind, Brain, and Behavior' was published by MIT Press in 2022. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p4]
- The three authors are Thomas Parr, Giovanni Pezzulo, and Karl J. Friston. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p3]
- The book is divided into two parts: Part I (chapters 1–5) covers theory and Part II (chapters 6–10) covers practice of Active Inference. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p5]
- Karl Friston was funded by a Wellcome Trust Principal Research Fellowship (Ref: 088130/Z/09/Z) during the preparation of this book. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p9]
- Part I comprises five chapters: Overview (ch. 1), The Low Road to Active Inference (ch. 2), The High Road to Active Inference (ch. 3), The Generative Models of Active Inference (ch. 4), and Message Passing and Neurobiology (ch. 5). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p5]
- Part II comprises five chapters covering a recipe for designing Active Inference models, discrete-time models, continuous-time models, model-based data analysis, and Active Inference as a unified theory. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p5]
- The book provides a normative approach explaining behavior, cognitive, and neural processes from first principles. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p106]
- The generative modeling approach in Active Inference assumes the generative model provides a complete description of a system of interest. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p106]
- The choice of generative model corresponds to specific predictions about both behavior and neurobiology. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p106]
- Appendix B derives update equations for learning in POMDP models using Dirichlet priors, where parameters are updated by augmenting elements when predicted outcomes occur. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p254]
- Precision parameters in Active Inference are parameterized using gamma distributions, with update rules derived for likelihood precision (ζ), transition precision (ω), and policy precision (γ). [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p255]
- Expected free energy decomposes into expected ambiguity (entropy of predicted outcomes) and risk (KL divergence between inferred and preferred states), acting as an upper bound on the expected free energy used throughout the book. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p257]
- Bayesian model reduction enables comparison of alternative models that differ only in their priors, using variational quantities to find model evidence and posterior probabilities under reduced priors without re-inverting the full model. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p260]
- Active Generalized Filtering extends Active Inference to continuous state-space models using the Laplace approximation and generalized coordinates of motion, specifying a predictive coding scheme where prediction errors drive updates in expectations. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p262]
- The MATLAB implementation in Appendix C uses SPM12 functions (spm_MDP_VB_X) to implement message passing and policy selection for a T-maze foraging example, with visualization routines spm_MDP_VB_trial and spm_MDP_VB_LFP. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p271]
- The book covers both discrete and continuous generative models and their applications in Active Inference. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p173]
- The book details how to design Active Inference models and use them for model-based data analysis and computational phenotyping. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p196]
- The mathematical appendices provide background on linear algebra, Taylor series approximation, variational calculus, and stochastic dynamics. [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p231]

## Inferences

- Inference: The book's two-part structure reflects a pedagogical strategy of moving from conceptual understanding to practical implementation, as the preface states the book is 'for people who want to use Active Inference to simulate and model sentient behavior, in the service of either scientific inquiry or, possibly, artificial intelligence'.

## Uncertainties

- Uncertain: The Library of Congress Classification is LCC BF311 .P31366 2022; the page layout indicates the book uses Stone Serif and Stone Sans typefaces set by Westchester Publishing Services.

## Related pages

- Broader: [[neuroscience]]
- Broader: [[cognitive science]]
- Broader: [[Bayesian brain]]
- Broader: [[free energy principle]]
- Narrower: [[active inference]]
- Narrower: [[variational free energy]]
- Narrower: [[expected free energy]]
- Narrower: [[generative model]]
- Narrower: [[predictive coding]]
- Narrower: [[markov blanket]]
- Narrower: [[POMDP]]
- Narrower: [[self-evidencing]]
- Narrower: [[planning as inference]]
- Narrower: [[perception as inference]]
- Narrower: [[message passing]]
- Concepts: [[active inference]]
- Concepts: [[variational free energy]]
- Concepts: [[expected free energy]]
- Concepts: [[generative model]]
- Concepts: [[predictive coding]]
- Concepts: [[Bayesian brain]]
- Concepts: [[free energy principle]]
- Concepts: [[self-evidencing]]
- Concepts: [[Markov blanket]]
- Concepts: [[planning as inference]]
- Concepts: [[perception as inference]]
- Concepts: [[message passing]]
- Concepts: [[Bayes theorem]]
- Concepts: [[variational inference]]
- Concepts: [[entropy]]
- Concepts: [[Hamiltonian principle]]
- Entities: [[Thomas Parr]]
- Entities: [[Giovanni Pezzulo]]
- Entities: [[Karl J. Friston]]
- Entities: [[MIT Press]]

## Provenance

- Primary source: [raw/books/neuroscience/Active Inference _ The Free Energy Principle in Mind, Brain, - Thomas Parr; Giovanni Pezzulo; Karl J Friston; MIT Press.pdf#p1-309]

## Change notes

- 2026-04-23 — page created by auto ingest.
