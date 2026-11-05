# P002 technology selection (PROJECT_RULES §21)

| Item | Choice | Why |
|---|---|---|
| Platform | Command-line lab | Pass 001: "No web application is required for the research kernel." |
| Language | Python 3.11+ | Project OS default. |
| Numerics | NumPy only, with every backward pass written by hand | Pass 001 allowed PyTorch; NumPy was chosen because (1) it makes "from first principles" literal: attention, LayerNorm, GELU and cross-entropy gradients are all visible code, checked against finite differences; (2) PyTorch is a heavy install on a 4 GB laptop. |
| Tokenizer | Byte-pair encoding trained from scratch, saved as JSON | Part of the first-principles pipeline. |
| Model | Decoder-only Transformer: 2 layers, 4 heads, width 64, context 32, tied embeddings (about 120,000 parameters) | Tier A: sized for a Pentium N3710 CPU. |
| Optimiser | AdamW with warm-up and cosine decay, gradient clipping | Standard; implemented by hand. |
| Checkpoints | NumPy `.npz`, loaded with `allow_pickle=False` | A checkpoint can only hold arrays, never code (Pass 001 safety). |
| Threads | Single-threaded BLAS | Measured 3× faster than four threads on the development laptop. |
| Tier B (GPU) | Not used | Would need cloud compute; not justified until a sharper research question exists. |
