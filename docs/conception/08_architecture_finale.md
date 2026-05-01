# Phase 5 — Architecture finale & intégration chatbot

## Vue d'ensemble

```
┌──────────────────────┐         HTTP            ┌──────────────────────┐
│                      │  ◄───────────────────►  │                      │
│   Navigateur (HTML)  │     /api/chat/...       │   Django (port 8000) │
│   - Bootstrap 5      │     /api/materiels/...  │   - REST API (DRF)   │
│   - Leaflet (carte)  │     /catalogue, ...     │   - Pages HTML       │
│                      │                         │   - Auth, sessions   │
└──────────────────────┘                         └──────────┬───────────┘
                                                            │ HTTP JSON
                                                            ▼
                                                ┌──────────────────────┐
                                                │  FastAPI (port 8001) │
                                                │  - /predict          │
                                                │  - /chat             │
                                                │  - Phi-3 + LoRA      │
                                                └──────────────────────┘
                                                            │
                                                            ▼
                                                ┌──────────────────────┐
                                                │  Modèle fine-tuné    │
                                                │  (LoRA / PEFT)       │
                                                └──────────────────────┘
```

## Découpage en 3 services

| Service | Rôle | Port | Stack |
|---------|------|------|-------|
| **Django** | Pages HTML + API REST métier (matériels, demandes, users, conversations) | 8000 | Django 5 + DRF + SQLite |
| **FastAPI** | Inférence du modèle fine-tuné | 8001 | FastAPI + Transformers + PEFT |
| **Frontend** | Templates servis par Django, JS vanilla pour appeler l'API | (idem 8000) | Bootstrap 5 + Leaflet |

Pourquoi cette séparation ? Découpler **métier** et **IA** :
- Le modèle peut être redéployé sans toucher au Django
- L'IA peut tomber sans casser le reste de l'app (fallback dans `ChatService`)
- On peut héberger le modèle sur une machine GPU séparée

## Flux : envoi d'un message dans le chat

```
Étudiant tape une question
     │
     ▼
[chat.html JS] → POST /api/chat/<id>/envoyer/  (avec CSRF)
     │
     ▼
[ConversationChatViewSet.envoyer]
     │
     ├── conv.ajouter_message("user", message)  ← persistance JSONField
     │
     ▼
[ChatService.repondre(message, historique)]
     │
     ├── try : POST http://localhost:8001/chat
     │       └── Phi-3 + LoRA génère la réponse
     │
     └── except IAServiceError : _fallback("...")
     │
     ▼
[ConversationChatViewSet.envoyer]
     │
     ├── conv.ajouter_message("assistant", reponse)
     │
     ▼
[chat.html JS] → affiche la bulle bot
```

## Concepts OOP mobilisés (Phase 5)

- **Abstraction** : `ChatService` masque la complexité de l'appel HTTP, du fallback,
  du formatage des messages. La vue ne voit qu'une méthode `repondre(...)`.
- **Encapsulation** : `ModelHolder` (FastAPI) encapsule le modèle, le tokenizer, le
  flag `charge`. Le reste du service ne manipule que les méthodes publiques `charger()`
  et `generer()`.
- **Polymorphisme** : `ChatService` peut basculer entre mode mock et mode réel
  uniquement via la variable d'env `USE_MOCK`, sans changer le code des appelants.
- **Gestion d'erreurs propre** : exception métier dédiée `IAServiceError` plutôt
  que de laisser remonter des `requests.RequestException` techniques.

## Démarrage complet (3 terminaux)

### Terminal 1 — Microservice IA (mode mock pour démo)

```powershell
cd ia/service/
pip install fastapi uvicorn[standard] pydantic
$env:USE_MOCK="1"
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### Terminal 2 — Backend Django

```powershell
cd backend/
python manage.py migrate
python manage.py loaddata fixtures/01_categories.json fixtures/02_materiels.json
python manage.py createsuperuser     # une seule fois
python manage.py runserver
```

### Terminal 3 — Tests

```powershell
cd backend/
python manage.py test chatbot
```

Puis ouvrir http://127.0.0.1:8000 et naviguer vers **Assistant IA**.

## Pour passer en mode réel (avec modèle fine-tuné)

```powershell
cd ia/training/
pip install -r requirements.txt
python train_lora.py --epochs 3        # ~30 min sur GPU 8 Go

cd ../service/
$env:USE_MOCK="0"
$env:MODEL_PATH="../training/checkpoints/ufr-chatbot-lora"
uvicorn main:app --port 8001
```

## Limites & extensions futures

- **Pas de streaming** : la réponse est renvoyée d'un bloc. Une version
  Server-Sent Events ou WebSocket améliorerait l'UX.
- **Pas de rate limiting** : un étudiant peut spammer le chat.
  Ajouter `django-ratelimit` ou un middleware côté FastAPI.
- **Pas de cache** : les questions identiques re-déclenchent l'inférence.
  Un cache Redis sur (question, historique[-1]) serait pertinent.
- **Modèle figé** : pour de nouvelles connaissances, il faut re-fine-tuner.
  Une approche RAG complémentaire serait élégante (matériel récemment ajouté
  → recherche vectorielle plutôt que ré-entraînement).
