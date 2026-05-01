# Microservice d'inférence — Chatbot UFR SI

API FastAPI exposant le chatbot fine-tuné. Communique avec le backend Django
en HTTP JSON sur le port **8001**.

## Lancement (mode mock — pour développement)

```bash
cd ia/service/
pip install -r requirements.txt    # Installer fastapi + uvicorn + pydantic au minimum
USE_MOCK=1 uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

Le mode mock évite de charger le modèle (utile pour tester l'intégration Django).

## Lancement (mode réel — avec modèle fine-tuné)

```bash
cd ia/service/
pip install -r requirements.txt    # Installe aussi torch, transformers, peft

# Variables d'environnement
export USE_MOCK=0
export MODEL_PATH=../training/checkpoints/ufr-chatbot-lora
export BASE_MODEL=microsoft/Phi-3-mini-4k-instruct

uvicorn main:app --host 0.0.0.0 --port 8001
```

## Routes

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/` | Infos du service |
| GET | `/health` | Statut |
| GET | `/docs` | Documentation OpenAPI interactive (Swagger UI) |
| POST | `/predict` | Génération simple à partir d'un prompt |
| POST | `/chat` | Génération avec historique de messages |

## Test rapide

```bash
# Health
curl http://localhost:8001/health

# Prédiction simple
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Quelle est la précision de la Leica TS06 ?"}'

# Chat avec historique
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Comment faire une demande ?"},
      {"role": "assistant", "content": "Allez sur Nouvelle demande..."},
      {"role": "user", "content": "Et combien de temps à l'avance ?"}
    ]
  }'
```
