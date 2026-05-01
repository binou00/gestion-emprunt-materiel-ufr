"""
train_lora.py — Fine-tuning LoRA du chatbot UFR SI sur Phi-3-mini.

Usage :
    python train_lora.py [--model microsoft/Phi-3-mini-4k-instruct] [--epochs 3]

Sortie : un dossier ./checkpoints/ufr-chatbot-lora/ avec les poids LoRA.

Note pédagogique : ce script illustre la méthodologie. L'exécution réelle
demande un GPU (idéalement >= 8 Go VRAM) ou beaucoup de patience sur CPU.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

# --- Imports HuggingFace ---
import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "dataset"
TRAIN_FILE = DATA_DIR / "train.jsonl"
VAL_FILE = DATA_DIR / "val.jsonl"
OUTPUT_DIR = ROOT / "training" / "checkpoints" / "ufr-chatbot-lora"


# === Format de prompt (style Phi-3 chat) ===
def formater_exemple(ex: dict) -> str:
    """Convertit un exemple JSONL au format chat de Phi-3."""
    system = ex.get("system", "Tu es un assistant utile.")
    instruction = ex["instruction"]
    output = ex["output"]
    return (
        f"<|system|>\n{system}<|end|>\n"
        f"<|user|>\n{instruction}<|end|>\n"
        f"<|assistant|>\n{output}<|end|>"
    )


def charger_jsonl(chemin: Path) -> Dataset:
    """Charge un fichier JSONL et le formate pour Phi-3."""
    items = []
    with chemin.open(encoding="utf-8") as f:
        for ligne in f:
            ex = json.loads(ligne)
            items.append({"text": formater_exemple(ex)})
    return Dataset.from_list(items)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tuning LoRA du chatbot UFR SI")
    parser.add_argument("--model", default="microsoft/Phi-3-mini-4k-instruct",
                        help="Modèle de base HuggingFace")
    parser.add_argument("--epochs", type=int, default=3, help="Nombre d'époques")
    parser.add_argument("--batch_size", type=int, default=2, help="Taille du batch")
    parser.add_argument("--lr", type=float, default=2e-4, help="Learning rate")
    args = parser.parse_args()

    print(f"[INFO] Modèle de base : {args.model}")
    print(f"[INFO] Données : {TRAIN_FILE}")

    # 1. Charger les données
    train_ds = charger_jsonl(TRAIN_FILE)
    val_ds = charger_jsonl(VAL_FILE)
    print(f"[OK] Datasets chargés : {len(train_ds)} train / {len(val_ds)} val")

    # 2. Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 3. Quantization 4-bit (économise la VRAM)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    # 4. Modèle
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    model = prepare_model_for_kbit_training(model)

    # 5. Configuration LoRA
    lora_config = LoraConfig(
        r=16,                 # rang de la décomposition
        lora_alpha=32,        # mise à l'échelle
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        # Phi-3 : modules d'attention
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()  # Affiche le % de params adaptés

    # 6. Arguments d'entraînement
    training_args = TrainingArguments(
        output_dir=str(OUTPUT_DIR),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=4,
        learning_rate=args.lr,
        warmup_ratio=0.1,
        logging_steps=5,
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=2,
        fp16=True,
        optim="paged_adamw_8bit",
        report_to="tensorboard",
    )

    # 7. SFTTrainer (Supervised Fine-Tuning de TRL)
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=tokenizer,
        dataset_text_field="text",
        max_seq_length=1024,
    )

    # 8. Entraînement
    print("[INFO] Début de l'entraînement...")
    trainer.train()

    # 9. Sauvegarde finale
    trainer.save_model(str(OUTPUT_DIR))
    tokenizer.save_pretrained(str(OUTPUT_DIR))
    print(f"[OK] Modèle LoRA sauvegardé dans : {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
