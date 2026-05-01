# Module IA — Assistant chatbot UFR SI

Ce dossier contient tout ce qui concerne **l'assistant intelligent** du projet :
corpus, dataset de fine-tuning, scripts d'entraînement et service d'inférence.

## Structure

```
ia/
├── corpus/                 # Sources de connaissances brutes
│   ├── 01_materiels.md         # Fiches techniques du matériel UFR
│   ├── 02_procedures.md        # Règles, processus emprunt/restitution
│   ├── 03_topographie.md       # Notions techniques topo/géodésie
│   └── 04_faq.md               # Questions fréquentes étudiants
│
├── dataset/                # Paires Q/R prêtes pour entraînement
│   ├── build_dataset.py        # Script de génération JSONL
│   ├── train.jsonl             # Données d'entraînement (~80 %)
│   ├── val.jsonl               # Données de validation (~20 %)
│   └── examples_seed.json      # Paires Q/R initiales rédigées à la main
│
├── training/               # Scripts de fine-tuning (Phase 5)
│   └── (à venir)
│
└── service/                # Microservice d'inférence (Phase 5)
    └── (à venir)
```

## Périmètre du chatbot

Le chatbot répond à 4 grandes catégories de questions :

| Catégorie | Exemples |
|-----------|----------|
| **Matériel** | « Quelle est la précision d'une station Leica TS06 ? » |
| **Procédures** | « Comment faire une demande d'emprunt ? » |
| **Topographie** | « Différence entre nivellement direct et indirect ? » |
| **FAQ étudiants** | « Que faire si j'endommage le matériel ? » |

Le chatbot **n'est pas** un moteur de recherche général : hors-sujet, il oriente vers les ressources humaines (technicien, enseignant).

## Modèle cible

- **Base** : un petit LLM open-source (Mistral-7B-Instruct, Phi-3-mini, ou TinyLlama-1.1B selon ressources GPU)
- **Méthode** : LoRA (Low-Rank Adaptation) avec PEFT — efficace en VRAM
- **Format des données** : JSONL avec `{"instruction": ..., "input": ..., "output": ...}` (style Alpaca)

## Phases

- ✅ **Phase 4 (en cours)** — Construction du corpus + génération du dataset
- ⏳ **Phase 5** — Fine-tuning + microservice d'inférence FastAPI
