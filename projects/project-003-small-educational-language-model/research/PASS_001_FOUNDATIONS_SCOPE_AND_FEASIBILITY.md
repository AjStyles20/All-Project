# P003 Research Pass 001 — Foundations, Scope and Feasibility

## Status
DISCOVERY / FEASIBILITY SCREEN. No implementation approval and no novelty claim.

## Original concept
Build a small educational language model from first principles as a portfolio/research project. The phrase "from first principles" is treated strictly: the project should expose and implement the major learning pipeline rather than merely wrap an existing chat model.

## First-principles boundary
Candidate scope includes:
- corpus definition and licensing/provenance;
- text normalization and train/validation/test separation;
- tokenizer training and analysis;
- decoder-only Transformer implementation or a deliberately minimal equivalent;
- causal language-model objective;
- initialization, optimization, batching, checkpointing and reproducibility;
- controlled scaling experiments;
- intrinsic evaluation (loss/perplexity/tokenization behaviour);
- educational-domain capability evaluation;
- safety/data-quality limitations;
- optional later instruction tuning or retrieval, clearly separated from pretraining.

Using PyTorch/autograd/CUDA libraries does not invalidate "from first principles" if the architecture, data pipeline, objective and training/evaluation logic are implemented and explainable. Calling an API or only fine-tuning a pretrained model would not satisfy the core concept.

## Historical/technical baseline
Language-model scaling work established empirical power-law relationships between model loss, parameter count, data and compute. Kaplan et al. (2020) showed predictable scaling across orders of magnitude. Hoffmann et al. (2022, Chinchilla) later demonstrated that under a fixed training-compute budget, model size and training tokens should be scaled together much more aggressively than earlier practice; their experiments covered 70M–16B parameter models and 5B–500B training tokens.

TinyStories (Eldan & Li, 2023) is a major feasibility/prior-art reference. It showed that specially constrained synthetic data can train models below 10M parameters, even very shallow architectures, to produce coherent multi-paragraph English stories. Therefore "a tiny model can produce coherent language" is established prior art and cannot be P003 novelty.

## Immediate novelty threats
The following are NOT defensible novelty claims by themselves:
- training a small Transformer from scratch;
- building a tokenizer;
- making a mini-GPT;
- training on educational text;
- distilling a larger model into a smaller model;
- demonstrating coherent language in a tiny model;
- using synthetic curriculum-like data;
- comparing model sizes or tokenizers;
- making a small model run locally.

P003 must discover a sharper research question or remain an educational engineering project.

## Feasibility reality
AJ's primary laptop (Pentium N3710, 4 GB RAM, integrated graphics) is suitable for code development, tokenizer experiments, data preprocessing at modest scale, unit tests, and very small CPU training demonstrations. It is not a realistic machine for serious pretraining of a competitive tens/hundreds-of-millions parameter language model.

Therefore the project must be designed around two compute tiers:

### Tier A — Local proof system
Purpose: demonstrate understanding and correctness.
Possible order of magnitude: sub-million to low-single-digit-million parameters, small context, tightly bounded corpus, CPU-friendly tests/training.

### Tier B — Research experiment
Purpose: test the actual hypothesis at meaningful scale.
Requires rented/free cloud GPU or another GPU environment if the final experiment exceeds local feasibility. Exact model size is NOT approved yet; it must be derived from the hypothesis, corpus, training budget and pilot scaling measurements.

This prevents the common failure of choosing an arbitrary parameter count first and discovering later that data/compute are mismatched.

## Core research directions to investigate
### R1 — Educational data curriculum
Does structured sequencing of educational text (simple definitions/examples -> explanations -> exercises/reasoning) improve sample efficiency or targeted learning relative to an equal-token shuffled baseline for genuinely small models?

Threat: curriculum learning and data ordering are established fields. Novelty would require a precise educational mechanism and controlled evidence.

### R2 — Knowledge density vs general language breadth
Can a small model trained on a deliberately structured educational corpus acquire useful domain competence with less compute than a general-purpose corpus of equal token count, and what general-language capability is lost?

Threat: domain-specific pretraining is established. The contribution would need a careful trade-off/evaluation design rather than "domain data works better."

### R3 — Pedagogy-aware synthetic corpus design
Can training examples encode pedagogical transformations (definition -> worked example -> misconception -> correction -> independent question) in a way that measurably changes a small model's educational behaviour?

Threat: synthetic data and textbook-quality data are established. Need mechanism-level prior-art attack.

### R4 — Tokenization for educational/code/math mixtures
Does a tokenizer optimized for the selected educational mixture materially improve effective context use, learning efficiency or error rate at very small model scales?

Threat: tokenizer optimization is established. Could be supporting experiment rather than core contribution.

### R5 — Capability emergence at tiny scale
Which educational behaviours emerge as model/data scale increases under a fixed architecture family and controlled curriculum?

Threat: scaling/emergence research is extensive. Potential value as a reproducible educational study, not assumed novelty.

## Candidate product/research distinction
Product/learning value: a transparent educational LM laboratory where AJ can inspect tokenizer behaviour, attention, logits, loss curves, checkpoints and generated outputs.

Research value: UNKNOWN. Must come from a bounded experiment such as curriculum/sample efficiency, knowledge-density trade-off, pedagogical synthetic data, or another gap found through prior-art research.

## Evaluation principles
Do not judge success only by "the generated text looks good." Candidate measurements:
- held-out cross-entropy/perplexity;
- tokenization efficiency;
- factual/educational QA accuracy on contamination-controlled items;
- worked-example completion;
- misconception discrimination/correction;
- transfer to unseen formulations;
- calibration where feasible;
- memorization/duplication checks;
- parameter/token/FLOP efficiency;
- inference latency and memory;
- qualitative generations only as supporting evidence.

## Data governance requirements
Before training on any corpus:
- identify source and license/terms;
- record provenance and preprocessing;
- remove or control test contamination;
- avoid private/sensitive data;
- document synthetic-data generator/model if used;
- preserve train/validation/test hashes/manifests;
- do not describe generated synthetic facts as authoritative educational content without verification.

## Security/safety scope
This is not initially an autonomous agent. Primary risks are dataset poisoning, malicious/untrusted files in preprocessing, dependency/supply-chain risk, checkpoint deserialization, accidental secret inclusion, unsafe generated content, misleading factual confidence, and later model-serving abuse. Use safe serialization where feasible, least privilege, bounded resource use and explicit model limitations.

## Initial architecture hypothesis — NOT approved
Python + PyTorch; custom tokenizer experiment (BPE or unigram/subword candidate); decoder-only Transformer; configuration-driven experiments; deterministic seeds where possible; local SQLite/JSONL/Parquet-style experiment metadata as appropriate; pytest; optional cloud GPU training while retaining reproducible local smoke tests.

No web application is required for the research kernel. A visualization/educational dashboard can be considered after the model laboratory works.

## First adversarial questions
1. What educational capability can a tiny LM meaningfully learn that is not merely memorization?
2. What is the strongest baseline: equal-token shuffled educational corpus, general corpus, pretrained small model, or retrieval system?
3. Is training from scratch scientifically justified, or mainly educationally valuable?
4. How small can the model be while still supporting the selected experiment?
5. Is the proposed contribution about the model, the data curriculum, the tokenizer, the evaluation framework, or the learning process?
6. Can the experiment be replicated within a realistic GPU budget?
7. Would a non-neural baseline or retrieval system outperform the tiny LM on the claimed educational task?
8. How will contamination and memorization be distinguished from learning/generalization?

## Pass 001 decision
MORE RESEARCH.

P003 is feasible as an educational engineering project. Research novelty is not established. Training a tiny Transformer from scratch is well precedented; therefore the next passes must aggressively investigate small-model prior art, educational/domain-specific pretraining, curriculum learning, synthetic textbook data, tokenization, BabyLM-style data-efficient training, knowledge distillation, evaluation and compute economics before choosing a contribution.

## Next pass
Pass 002 — Historical Lineage, Small-Model Prior Art and Data-Efficient Training Landscape.

Required comparison classes:
- early neural/statistical language modelling;
- Transformer/GPT lineage;
- scaling laws and compute-optimal training;
- TinyStories;
- BabyLM/data-efficient language modelling;
- TinyLlama and other open small models;
- domain/educational LMs;
- synthetic/textbook-quality data approaches;
- distillation and pruning/quantization (to distinguish training-small from compressing-large);
- tokenizer research;
- non-neural/RAG baselines where educational factuality matters.
