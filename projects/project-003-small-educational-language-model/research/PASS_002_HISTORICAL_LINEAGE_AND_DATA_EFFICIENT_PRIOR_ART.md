# P003 Research Pass 002 — Historical Lineage and Data-Efficient Prior Art

## Status
DISCOVERY / PRIOR-ART PRESSURE / MORE RESEARCH.

## Purpose
This pass tests whether P003 can contribute anything beyond the already-established fact that small Transformer language models can be trained from scratch on constrained or high-quality corpora. It separates educational value from research novelty and narrows the next experiments.

## Historical lineage
P003 sits in a mature lineage: statistical and neural language modelling; attention and Transformers; scaling-law research; data/compute-optimal training; compact language models; synthetic high-quality corpora; knowledge distillation; curriculum/data ordering; and data-constrained pretraining challenges. Therefore neither a decoder-only Transformer, a custom tokenizer, a small parameter count, nor training from scratch is a novelty claim.

## Major prior-art pressure
### TinyStories
TinyStories demonstrated that deliberately simplified synthetic language can train models below 10M parameters, including very shallow Transformers, to produce coherent multi-paragraph stories. This directly falsifies any novelty claim based on 'a genuinely tiny model can learn coherent language from a carefully designed corpus.'

### Phi / textbook-quality data
Phi-1 showed that a 1.3B code model trained with about 6B tokens of filtered textbook-quality web/code data plus about 1B tokens of synthetic textbooks/exercises could achieve strong coding benchmark results. Phi-1.5 extended the textbook-quality synthetic-data idea to broader natural-language/common-sense reasoning. Therefore 'train a smaller model on educationally written or synthetic textbook data' is already crowded prior art.

### TinyLlama
TinyLlama showed that a 1.1B model using a Llama-family architecture/tokenizer can be pretrained on roughly trillion-token scale and outperform comparable open models. This reinforces that 'small Llama-like model' or efficient engineering alone is not enough.

### BabyLM
BabyLM explicitly studies sample-efficient pretraining under human-scale data budgets. The 2025 challenge report found that architecture/objective choices and teacher interaction could outperform baselines, while many curriculum-learning submissions were unsuccessful or only modestly beneficial. BabyLM 2026 continues with 100M-word Strict and 10M-word Strict-Small tracks. P003 therefore cannot assume that intuitive easy-to-hard educational sequencing will help; it must be experimentally falsified.

### Curriculum-learning research
Recent systematic pretraining experiments report that curriculum ordering can accelerate early/mid-training convergence and sometimes retain modest gains, depending on difficulty signal and training regime. This conflicts with the simplistic interpretation that 'curriculum learning does not work.' The correct conclusion is conditional: curriculum effects depend on ordering metric, pacing, objective, model/data scale and evaluation. P003 must compare pedagogical curricula against strong non-pedagogical curriculum baselines rather than random order alone.

### Synthetic-data diversity
Controlled experiments on 350M and 1.4B models report positive relationships between synthetic-data diversity and downstream performance. Therefore P003 must not attribute gains from a pedagogically structured synthetic corpus to pedagogy unless diversity, token budget, topic coverage and difficulty are controlled.

## Distinctions P003 must preserve
1. **From-scratch pretraining** — random model initialization; our strongest educational transparency route.
2. **Continual pretraining** — start from an existing pretrained model and add domain data.
3. **Supervised fine-tuning** — adapt an already pretrained model to tasks/instructions.
4. **Distillation** — transfer behavior/knowledge from a stronger teacher into a student.
5. **Synthetic-data generation** — teacher models may create training data even when the student itself is trained from random initialization.

A model can therefore be 'trained from scratch' while still depending epistemically on a larger teacher through synthetic data. P003 must report that dependency rather than presenting such a model as knowledge-independent.

## Novelty threats
### Threat T1 — Pedagogical curriculum is already curriculum learning
A Definition -> Explanation -> Worked Example -> Misconception -> Correction -> Independent Problem sequence is educationally meaningful, but curriculum learning and staged educational data are established. Novelty would require a sharper mechanism, metric or result.

### Threat T2 — Educational synthetic data is already textbook-quality synthetic data
Phi-family work strongly occupies this space. Merely generating textbook-like lessons is insufficient.

### Threat T3 — Small model + high-quality data is established
TinyStories, Phi, BabyLM and later SLM work make this a baseline, not a contribution.

### Threat T4 — Teacher-generated data can confound claims
If a frontier model generates the corpus, observed student capability may partly reflect teacher knowledge, style and benchmark contamination. We need provenance, generation prompts, filtering rules, deduplication and held-out evaluation.

### Threat T5 — Curriculum gains may actually be diversity/difficulty effects
A pedagogical sequence can change lexical diversity, repetition, document length, topic frequency and difficulty distribution. Controlled ablations are mandatory.

### Threat T6 — Parameter efficiency is not educational effectiveness
Lower perplexity or coherent generation does not prove the model teaches, explains misconceptions or supports learning.

## Candidate contribution hypotheses after Pass 002
These are hypotheses, not novelty claims.

### H1 — Pedagogical Structure Efficiency
Under a fixed model architecture, token budget, topic coverage and synthetic-data generator, does explicit pedagogical structure improve learning efficiency or transfer compared with shuffled, random, readability-based and information-theoretic curricula?

Status: PLAUSIBLE / NOVELTY UNKNOWN.

### H2 — Misconception-Contrast Pretraining
Does systematically pairing a misconception with diagnosis, contrastive correction and a near-transfer problem produce measurable gains in misconception discrimination and correction at tiny-model scale compared with equal-token conventional exposition?

Status: PROMISING / NEEDS DIRECT PRIOR-ART ATTACK.

### H3 — Educational Token Utility
Can corpus/tokenizer design improve useful educational capability per training token, not merely compression ratio? Candidate metrics include tokens required for concept definitions, equations/code identifiers, misconception pairs and worked-example structures.

Status: UNKNOWN / HIGH CONFOUND RISK.

### H4 — Transparent Capability Emergence Lab
A family of truly small from-scratch models and checkpoints could expose when educational micro-capabilities emerge as data/parameters/curriculum change.

Status: STRONG PROJECT/TEACHING VALUE; LIKELY WEAK AS STANDALONE RESEARCH NOVELTY.

## Proposed controlled experiment skeleton
Hold constant:
- decoder-only architecture and parameter count;
- tokenizer unless tokenizer is the independent variable;
- optimizer/schedule/seed policy;
- total training tokens;
- subject/topic coverage;
- train/validation/test boundaries;
- synthetic teacher and generation budget where used.

Compare corpora/orderings:
A. ordinary/random educational text;
B. shuffled version of the same pedagogical units;
C. readability easy-to-hard;
D. information-theoretic/difficulty curriculum where feasible;
E. explicit pedagogical sequence;
F. misconception-contrast enriched sequence.

Evaluate:
- validation loss/perplexity;
- sample efficiency / steps-to-threshold;
- held-out concept QA;
- misconception discrimination;
- correction quality;
- near and far transfer;
- calibration/confidence where measurable;
- generation coherence;
- compute time and memory;
- robustness across multiple seeds.

## Data governance requirements
Before corpus construction:
- record source/license/provenance for every real dataset;
- separate synthetic from human-authored data;
- retain teacher model/version and generation template for synthetic data;
- deduplicate against evaluation items where feasible;
- prevent test-set leakage;
- track topic/difficulty/diversity statistics;
- never label synthetic facts authoritative without verification;
- maintain dataset cards and experiment manifests.

## Hardware consequence
The local machine should be used for pipeline correctness, tokenizer/data inspection, tiny proof models and reproducibility tests. Serious comparative pretraining should use bounded external GPU compute only after experiment size is justified. A local-only constraint must not force scientifically meaningless model sizes, while cloud scale must not hide an irreproducible pipeline.

## Pass 002 decision
MORE RESEARCH.

P003 is feasible and valuable, but the broad idea remains heavily occupied. The strongest next research target is no longer 'can we train a small educational LM?' It is whether a carefully controlled **misconception-aware pedagogical data mechanism** improves useful educational capability per token/compute beyond strong data-ordering and high-quality-data baselines.

## Next pass
Pass 003 — Direct Prior-Art Attack on Pedagogical Curriculum and Misconception-Contrast Training.

Required searches:
- misconception-aware LM pretraining/fine-tuning;
- contrastive misconception/correction datasets;
- educational knowledge tracing vs generative LM training;
- curriculum learning for LM pretraining, including negative results;
- data difficulty/ordering methods;
- textbook/synthetic-data generation and diversity controls;
- educational/domain tokenizers;
- benchmark leakage and synthetic-data contamination.

Kill/demote H1-H3 where direct prior art already implements equivalent mechanisms.