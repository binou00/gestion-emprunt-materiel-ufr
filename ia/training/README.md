# Fine-tuning du chatbot UFR SI

## Prérequis

- Python 3.10+
- GPU NVIDIA avec >= 8 Go VRAM (recommandé) **OU** patience sur CPU
- ~10 Go d'espace disque (modèle + checkpoints)

## Installation

```bash
# Environnement virtuel séparé du backend Django
python -m venv venv-ia
source venv-ia/bin/activate           # Linux/Mac
# venv-ia\Scripts\activate            # Windows PowerShell

pip install -r requirements.txt
```

## Lancement

```bash
# 1. Vérifier que le dataset est bien généré
ls ../dataset/train.jsonl ../dataset/val.jsonl

# 2. Lancer l'entraînement (3 époques par défaut)
python train_lora.py

# Options :
python train_lora.py --epochs 5 --batch_size 4 --lr 1e-4
```

L'entraînement écrit ses checkpoints dans `./checkpoints/ufr-chatbot-lora/`
et ses logs TensorBoard dans `./checkpoints/ufr-chatbot-lora/runs/`.

## Suivi en temps réel

```bash
tensorboard --logdir checkpoints/ufr-chatbot-lora/runs
```

Ouvrir http://localhost:6006 dans le navigateur.

## Déploiement

Une fois l'entraînement terminé, le service d'inférence (`ia/service/`) charge
automatiquement les poids LoRA depuis `./checkpoints/ufr-chatbot-lora/`.

## Alternative : sans GPU

Si pas de GPU, utiliser un modèle plus petit :

```bash
python train_lora.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

Ou désactiver la quantization 4-bit dans `train_lora.py` (commenter `BitsAndBytesConfig`).
