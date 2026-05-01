# Phase 4 — Méthodologie de construction du corpus et du dataset IA

**Auteure** : Bineta Hanne (Backend & IA)
**Branche Git** : `feat/ia`

## Objectif

Construire un assistant intelligent capable de répondre aux questions des étudiants
sur le matériel topographique de l'UFR SI et sur les procédures d'emprunt.
Cette phase prépare les **données** ; le fine-tuning lui-même est en Phase 5.

## Choix méthodologiques

### Pourquoi un fine-tuning et pas du RAG ?

Deux approches étaient possibles pour spécialiser le chatbot :

| Approche | Avantages | Inconvénients |
|----------|-----------|---------------|
| **RAG** (Retrieval-Augmented Generation) | Pas d'entraînement, base de connaissances modifiable | Dépendance à un LLM externe (coût API, latence, hors-ligne impossible) |
| **Fine-tuning** | Modèle autonome, hors-ligne, intégré au stack | Entraînement coûteux, données figées |

Pour un projet pédagogique avec un sujet bien borné (matériel UFR + procédures fixes),
le **fine-tuning** est plus instructif et démontre les concepts de POO et de ML.

### Format de données : Alpaca (JSONL)

Le format Alpaca est devenu le standard de fait pour le fine-tuning supervisé :

```json
{"instruction": "Question utilisateur", "input": "", "output": "Réponse attendue"}
```

On y ajoute deux champs pédagogiques :
- `categorie` : pour les statistiques et le split stratifié
- `system` : prompt système réutilisable à l'inférence

## Pipeline de construction

```
┌─────────────────┐
│  4 fichiers     │  Sources de connaissances rédigées à la main
│  corpus/*.md    │  (matériel, procédures, topographie, FAQ)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ examples_seed   │  25 paires Q/R rédigées à la main
│      .json      │  couvrant les 4 catégories
└────────┬────────┘
         │  build_dataset.py
         ▼
┌─────────────────┐
│  Augmentation   │  Paraphrase d'instruction (× 2-4 selon type)
│   (templates)   │  → 65 exemples
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Split stratifié │  80 % train / 20 % val
│  par catégorie  │  → 54 train / 11 val
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  train.jsonl    │  Prêt pour fine-tuning
│   val.jsonl     │  (Phase 5 avec LoRA)
└─────────────────┘
```

## Augmentation par paraphrase

Pour démultiplier les 25 paires seed, on applique une augmentation par templates
selon le type de question :

| Type détecté | Templates appliqués |
|--------------|---------------------|
| « Quelle est… » / « Qu'est-ce que… » | original, « Peux-tu m'expliquer », « Explique-moi », « Dis-moi » |
| « Comment… » / « Que faire… » | original, « Procédure : », « Pourrais-tu me dire » |
| « Pourquoi… » / « À quoi sert… » | original, « Justifie : », « À quoi sert : » |

**Effet** : facteur de multiplication ~2,6x → 65 exemples au total.
Cette technique reste basique mais évite le surapprentissage sur la formulation exacte.

## Split stratifié

Plutôt qu'un split aléatoire global (qui pourrait sous-représenter une catégorie),
on applique un **split stratifié par catégorie** :

```python
for cat, items in par_cat.items():
    random.shuffle(items)
    n_val = max(1, int(len(items) * 0.2))
    val.extend(items[:n_val])
    train.extend(items[n_val:])
```

Garantit qu'au moins **un exemple de validation par catégorie** est présent.

## Statistiques du dataset

| Catégorie | Nb exemples |
|-----------|-------------|
| materiel | 19 |
| procedures | 12 |
| topographie | 26 |
| faq | 8 |
| **Total** | **65** |

Split final : **54 train / 11 val**.

## Limites et améliorations futures

- **Taille modeste** : 65 exemples, c'est peu pour un fine-tuning robuste. Une vraie
  mise en production demanderait au moins 500-1000 exemples.
- **Pas de paraphrases sémantiques** : on ne fait que des reformulations syntaxiques.
  Une LLM-as-augmenter (ex : générer des paraphrases via Mistral) enrichirait le dataset.
- **Pas de hard negatives** : on devrait ajouter des questions hors-périmètre avec
  réponses du type « Je ne sais pas, demande à ton enseignant » pour améliorer
  le rejet des questions non pertinentes.
- **Pas d'évaluation automatique** : on n'a pour l'instant que la perplexité comme
  métrique. Une évaluation par BLEU/ROUGE ou par jury humain serait intéressante.

## Concepts OOP mobilisés

Cette phase reste très orientée scripts, mais on retrouve :
- **Encapsulation** : chaque fonction du script (`augmenter`, `split_train_val`,
  `ecrire_jsonl`) a une responsabilité unique et masque ses détails.
- **Abstraction** : `PARAPHRASE_TEMPLATES` est un registre extensible — ajouter un
  type de question revient à ajouter une entrée dans le dictionnaire.
- **Réutilisabilité** : le script peut être ré-exécuté à volonté ; il est
  déterministe grâce à `random.seed(42)`.

## Pour rejouer la génération

```bash
cd ia/dataset/
python build_dataset.py
```

Sortie attendue :
```
[OK] 25 exemples seed chargés.
[OK] 65 exemples après augmentation (facteur ~2.6x).
[STATS] Répartition par catégorie :
    - faq             : 8
    - materiel        : 19
    - procedures      : 12
    - topographie     : 26
[OK] Split : 54 train / 11 val
[OK] Écrits : train.jsonl et val.jsonl
```
