# Backend Django — Gestion Emprunt Matériel UFR SI

## Prérequis

- Python 3.11+
- pip
- (Optionnel) Git Bash sous Windows

## Installation pas à pas

### 1) Créer un environnement virtuel

```bash
cd "C:\Users\binou\Documents\Projet POO\backend"
python -m venv .venv

# Activation (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# OU Windows CMD
.\.venv\Scripts\activate.bat

# OU Git Bash / Linux / macOS
source .venv/bin/activate
```

### 2) Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3) Créer les migrations et la base SQLite

```bash
python manage.py makemigrations users materiel emprunts chatbot
python manage.py migrate
```

### 4) Charger les données initiales (catégories + matériels)

```bash
python manage.py loaddata fixtures/01_categories.json fixtures/02_materiels.json
```

### 5) Créer un super-utilisateur (administrateur)

```bash
python manage.py createsuperuser
```

Renseigne :
- e-mail (obligatoire)
- nom d'utilisateur
- mot de passe

### 6) Lancer le serveur de dev

```bash
python manage.py runserver
```

Puis ouvre dans le navigateur :
- **Admin Django** : http://localhost:8000/admin
- **API navigable** : http://localhost:8000/api/
- **Catalogue matériel (API)** : http://localhost:8000/api/materiels/
- **Documentation auto DRF** : http://localhost:8000/api/auth/login/

## Architecture des apps

| App | Modèles | Rôle |
|-----|---------|------|
| `users` | `Utilisateur` | Authentification + rôles (étudiant, enseignant, technicien, admin) |
| `materiel` | `Categorie`, `Materiel`, `Maintenance` | Catalogue et maintenance |
| `emprunts` | `Demande`, `LigneDemande`, `Emplacement`, `Restitution` | Cycle d'emprunt complet |
| `chatbot` | `ConversationChat` | Conversations avec l'assistant IA |
| `api` | (router DRF) | Routage centralisé des endpoints REST |

## Endpoints API principaux

| Méthode | URL | Description |
|---------|-----|-------------|
| POST | `/api/auth/login/` | Authentification (renvoie un token JWT) |
| GET | `/api/materiels/` | Liste du catalogue matériel |
| GET | `/api/materiels/?categorie=2` | Filtre par catégorie |
| POST | `/api/demandes/` | Soumettre une demande d'emprunt |
| POST | `/api/demandes/{id}/valider/` | Valider une demande (admin) |
| POST | `/api/demandes/{id}/refuser/` | Refuser une demande (admin) |
| POST | `/api/demandes/{id}/annuler/` | Annuler |
| POST | `/api/chat/` | Créer une nouvelle conversation |
| POST | `/api/chat/{id}/envoyer/` | Envoyer un message à l'IA |

## Tests rapides

```bash
# Vérifier que tout démarre
python manage.py check

# Voir les modèles enregistrés
python manage.py inspectdb | head -30

# Shell interactif Django
python manage.py shell
```

Dans le shell :

```python
from materiel.models import Materiel
print(Materiel.objects.count())   # 23
for m in Materiel.objects.filter(etat="DISPONIBLE")[:5]:
    print(m, m.quantite_disponible)
```
