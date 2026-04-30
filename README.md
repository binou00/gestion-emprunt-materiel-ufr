# Gestion de l'Emprunt du Matériel — UFR Sciences de l'Ingénieur

> Application web Python avec assistant IA intégré pour la gestion des emprunts de matériel topographique et géodésique.

**Projet de Programmation Orientée Objet — Licence 2 Géomatique**
Encadrant : Dr Abdoulaye Diallo

---

## Binôme

| Rôle | Membre | Responsabilités |
|------|--------|----------------|
| Backend & IA | **Bineta Elimane Hanne** | Django, API REST, modèles, chatbot fine-tuné |
| Frontend & Cartographie | **Aminata Kounta** | HTML/CSS, Bootstrap, Leaflet.js, UX |

---

## Contexte

L'UFR met à disposition des étudiants un parc de matériel coûteux (stations totales, GNSS, télémètres). La gestion actuelle (papier/fichiers) pose des problèmes de traçabilité, double attribution, retards et perte d'historique. Ce projet développe une application web complète pour digitaliser ce processus.

## Objectifs

1. Gestion complète du cycle d'emprunt (demande → validation → sortie → retour).
2. Géolocalisation de l'utilisation du matériel sur le terrain.
3. Chatbot IA fine-tuné pour aider les étudiants à utiliser le matériel.
4. Tableau de bord administrateur en temps réel.

---

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Langage | Python 3.11+ |
| Backend | Django + Django REST Framework |
| Frontend | HTML5 / CSS3 / Bootstrap 5 / JavaScript |
| Base de données | SQLite (dev) — extensible PostGIS |
| Cartographie | Leaflet.js + OpenStreetMap |
| Chatbot IA | Hugging Face Transformers + PEFT (LoRA/QLoRA) |

## Structure du dépôt

```
.
├── backend/           # Projet Django (API + admin)
├── frontend/          # Templates, JS, CSS, assets
├── ia/                # Dataset, scripts fine-tuning, modèle
├── docs/
│   ├── conception/    # UML, MCD, MLD, architecture
│   └── manuels/       # Manuels utilisateur
└── README.md
```

## Phases du projet

| Phase | Tâches | Durée |
|-------|--------|-------|
| 1 | Conception (UML, MCD/MLD, architecture) | 2 j |
| 2 | Backend + base de données + API | 10 j |
| 3 | Frontend + intégration cartographie | 3 j |
| 4 | Collecte corpus IA + dataset | 3 j |
| 5 | Fine-tuning + évaluation + intégration chat | 6 j |

## Démarrage rapide

```bash
# Cloner le dépôt
git clone https://github.com/<ton-pseudo>/gestion-emprunt-materiel-ufr.git
cd gestion-emprunt-materiel-ufr

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate    # Windows : .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Licence

Projet académique — UFR Sciences de l'Ingénieur, 2026.
