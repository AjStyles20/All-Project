"""A small hand-written science corpus (data governance, Pass 001/002).

Provenance: every fact and misconception below was written for this project (CC0, no
external source text, no teacher model), so the trained model depends on nothing larger.
Facts are simplified school-level statements; they are not an authoritative reference.

Two training conditions with the same token budget:
  exposition  — each fact stated in varied training templates
  contrast    — the same, plus misconception -> correction units (Pass 002, H2)
Evaluation uses templates that never appear in training.
"""
import random

FACTS = [
    ("the heart", "pumps blood around the body", "makes blood"),
    ("plants", "make their food from sunlight", "get their food from the soil"),
    ("the moon", "reflects light from the sun", "makes its own light"),
    ("the earth", "goes around the sun", "is the centre of the solar system"),
    ("a whale", "is a mammal", "is a fish"),
    ("a bat", "is a mammal", "is a bird"),
    ("a spider", "has eight legs", "is an insect"),
    ("water", "boils at one hundred degrees", "boils at fifty degrees"),
    ("ice", "floats on water", "sinks in water"),
    ("sound", "cannot travel through empty space", "travels fastest in empty space"),
    ("light", "travels faster than sound", "travels slower than sound"),
    ("a magnet", "attracts iron", "attracts all metals"),
    ("the lungs", "take in oxygen", "make oxygen"),
    ("bones", "are living tissue", "are dead and dry"),
    ("a seed", "needs water to grow", "needs no water to grow"),
    ("the sun", "is a star", "is a planet"),
    ("rust", "forms when iron meets water and air", "forms on all metals"),
    ("a circuit", "needs a closed loop", "works with a gap"),
    ("friction", "slows moving things down", "speeds moving things up"),
    ("evaporation", "turns liquid into gas", "turns gas into liquid"),
    ("a shadow", "forms when light is blocked", "is made of dark light"),
    ("the stomach", "breaks down food", "stores blood"),
    ("a fossil", "is the remains of an old living thing", "is a kind of rock crystal"),
    ("a volcano", "lets out melted rock", "is made by rain"),
    ("an insect", "has six legs", "has eight legs"),
    ("clouds", "are made of tiny water drops", "are made of smoke"),
    ("the brain", "controls the body", "pumps blood"),
    ("a thermometer", "measures temperature", "measures weight"),
    ("a lever", "helps move heavy loads", "makes things heavier"),
    ("salt", "dissolves in water", "never dissolves in water"),
    ("a penguin", "is a bird", "is a mammal"),
    ("a frog", "is an amphibian", "is a reptile"),
    ("gravity", "pulls things towards the earth", "pushes things away from the earth"),
    ("a battery", "stores chemical energy", "stores sound"),
    ("roots", "take in water for a plant", "make seeds for a plant"),
    ("a kidney", "cleans the blood", "digests food"),
    ("oxygen", "is needed for burning", "puts out fires"),
    ("a rainbow", "splits light into colours", "is painted by clouds"),
    ("the skin", "protects the body", "makes bones"),
    ("a compass", "points to the north", "points to the sun"),
]

TRAIN_TEMPLATES = ["{c} {f}.", "we know that {c} {f}.", "in science class we learn that {c} {f}.",
                   "remember: {c} {f}.", "it is true that {c} {f}."]
CONTRAST_TEMPLATES = ["some people think {c} {m}. that is wrong. {c} {f}.",
                      "a common mistake is to say {c} {m}. in fact {c} {f}."]
# Never used for training: evaluation only.
HELD_OUT_TEMPLATES = ["did you know {c} {f}?", "a teacher would say {c} {f}."]


def _normalise(text):
    return " ".join(text.lower().split())


def training_text(condition: str, seed: int, n_chars: int) -> str:
    """Shuffled training lines until the character budget is met (same budget in both conditions)."""
    rng = random.Random(f"{condition}:{seed}")
    lines, size = [], 0
    while size < n_chars:
        c, f, m = rng.choice(FACTS)
        if condition == "contrast" and rng.random() < 0.4:
            lines.append(rng.choice(CONTRAST_TEMPLATES).format(c=c, f=f, m=m))
        else:
            lines.append(rng.choice(TRAIN_TEMPLATES).format(c=c, f=f))
        size += len(lines[-1]) + 1
    return "\n".join(_normalise(line) for line in lines)[:n_chars]


def validation_text(seed: int = 999, n_chars: int = 6000) -> str:
    return training_text("exposition", seed, n_chars)


def eval_items():
    """Pairs (correct sentence, misconception sentence) in held-out templates."""
    items = []
    for c, f, m in FACTS:
        for t in HELD_OUT_TEMPLATES:
            items.append((_normalise(t.format(c=c, f=f)), _normalise(t.format(c=c, f=m))))
    return items


def recall_items():
    """Which subject does a fact belong to? (correct sentence, a sentence with another subject)."""
    rng = random.Random(7)
    items = []
    for i, (c, f, _) in enumerate(FACTS):
        other = FACTS[(i + rng.randint(1, len(FACTS) - 1)) % len(FACTS)][0]
        t = HELD_OUT_TEMPLATES[0]
        items.append((_normalise(t.format(c=c, f=f)), _normalise(t.format(c=other, f=f))))
    return items
