"""
build_dataset.py — Construction du dataset de fine-tuning du chatbot UFR SI.

Lit les exemples seed (examples_seed.json), applique une data augmentation
par paraphrase d'instruction, ajoute un prompt système (mise en contexte du
chatbot), puis exporte deux fichiers JSONL au format Alpaca :

    train.jsonl   (~80 % des exemples)
    val.jsonl     (~20 % des exemples)

Format Alpaca :
{
  "instruction": "...",
  "input": "",
  "output": "..."
}

Utilisation :
    python build_dataset.py
"""
from __future__ import annotations

import json
import random
from pathlib import Path

# Reproductibilité
random.seed(42)

DATA_DIR = Path(__file__).parent
SEED_FILE = DATA_DIR / "examples_seed.json"
TRAIN_FILE = DATA_DIR / "train.jsonl"
VAL_FILE = DATA_DIR / "val.jsonl"

# === Prompt système : identité du chatbot ===
SYSTEM_PROMPT = (
    "Tu es l'assistant IA de l'UFR Sciences de l'Ingénieur de l'Université "
    "Iba Der Thiam de Thiès. Tu aides les étudiants en topographie et géodésie "
    "à utiliser le matériel de l'UFR et à comprendre les procédures d'emprunt. "
    "Réponds en français, de manière claire, factuelle et concise. "
    "Si tu ne sais pas, dis-le et oriente vers un enseignant ou technicien."
)

# === Templates de paraphrase pour augmenter le dataset ===
# Pour chaque type de question, on génère N reformulations équivalentes.
PARAPHRASE_TEMPLATES = {
    "quoi_que": [
        "{q}",
        "Peux-tu m'expliquer : {q}",
        "Explique-moi : {q}",
        "Dis-moi : {q}",
    ],
    "comment": [
        "{q}",
        "Procédure : {q}",
        "Pourrais-tu me dire {q}",
    ],
    "pourquoi": [
        "{q}",
        "Justifie : {q}",
        "À quoi sert : {q}",
    ],
    "default": [
        "{q}",
    ],
}


def detecter_type(question: str) -> str:
    """Catégorise grossièrement la question pour appliquer les bons templates."""
    q_lower = question.lower().strip()
    if q_lower.startswith(("qu'est-ce", "quelle est", "quel est", "qu'", "quelle ", "quel ")):
        return "quoi_que"
    if q_lower.startswith(("comment", "que faire", "que dois-je")):
        return "comment"
    if q_lower.startswith(("pourquoi", "à quoi sert")):
        return "pourquoi"
    return "default"


def augmenter(exemple: dict) -> list[dict]:
    """Renvoie l'exemple original + ses paraphrases."""
    type_q = detecter_type(exemple["instruction"])
    templates = PARAPHRASE_TEMPLATES.get(type_q, PARAPHRASE_TEMPLATES["default"])
    variantes = []
    for tpl in templates:
        instr = tpl.format(q=exemple["instruction"])
        variantes.append({
            "instruction": instr,
            "input": exemple.get("input", ""),
            "output": exemple["output"],
            "categorie": exemple.get("categorie", "general"),
            "system": SYSTEM_PROMPT,
        })
    return variantes


def split_train_val(exemples: list[dict], ratio_val: float = 0.2) -> tuple[list, list]:
    """Découpe stratifié par catégorie pour éviter le déséquilibre."""
    par_cat = {}
    for ex in exemples:
        par_cat.setdefault(ex["categorie"], []).append(ex)

    train, val = [], []
    for cat, items in par_cat.items():
        random.shuffle(items)
        n_val = max(1, int(len(items) * ratio_val))
        val.extend(items[:n_val])
        train.extend(items[n_val:])

    random.shuffle(train)
    random.shuffle(val)
    return train, val


def ecrire_jsonl(chemin: Path, items: list[dict]) -> None:
    """Écrit une liste d'objets en JSONL (une ligne par objet)."""
    with chemin.open("w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")


def main() -> None:
    # 1. Charger les graines
    with SEED_FILE.open(encoding="utf-8") as f:
        seeds = json.load(f)
    print(f"[OK] {len(seeds)} exemples seed chargés.")

    # 2. Augmenter
    augmentes = []
    for ex in seeds:
        augmentes.extend(augmenter(ex))
    print(f"[OK] {len(augmentes)} exemples après augmentation "
          f"(facteur ~{len(augmentes) / len(seeds):.1f}x).")

    # 3. Statistiques par catégorie
    stats = {}
    for ex in augmentes:
        stats[ex["categorie"]] = stats.get(ex["categorie"], 0) + 1
    print("[STATS] Répartition par catégorie :")
    for cat, n in sorted(stats.items()):
        print(f"    - {cat:15s} : {n}")

    # 4. Split train/val
    train, val = split_train_val(augmentes, ratio_val=0.2)
    print(f"[OK] Split : {len(train)} train / {len(val)} val")

    # 5. Écriture
    ecrire_jsonl(TRAIN_FILE, train)
    ecrire_jsonl(VAL_FILE, val)
    print(f"[OK] Écrits : {TRAIN_FILE.name} et {VAL_FILE.name}")


if __name__ == "__main__":
    main()
