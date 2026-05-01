"""
main.py — Microservice d'inférence FastAPI pour le chatbot UFR SI.

Routes :
    GET  /              → message de bienvenue
    GET  /health        → ping de santé
    POST /predict       → génération d'une réponse à partir d'un prompt
    POST /chat          → génération avec historique de conversation

Lancement :
    uvicorn main:app --host 0.0.0.0 --port 8001 --reload

Variable d'env :
    USE_MOCK=1   → mode mock (sans charger le modèle), pour dev/CI
    MODEL_PATH=/chemin/vers/checkpoint  → poids LoRA
"""
from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


USE_MOCK = os.getenv("USE_MOCK", "1") == "1"  # Mode mock par défaut (sécurité)
MODEL_PATH = Path(
    os.getenv(
        "MODEL_PATH",
        str(Path(__file__).resolve().parent.parent / "training" / "checkpoints" / "ufr-chatbot-lora"),
    )
)
BASE_MODEL = os.getenv("BASE_MODEL", "microsoft/Phi-3-mini-4k-instruct")
SYSTEM_PROMPT = (
    "Tu es l'assistant IA de l'UFR Sciences de l'Ingénieur de l'Université "
    "Iba Der Thiam de Thiès. Tu aides les étudiants en topographie et géodésie "
    "à utiliser le matériel de l'UFR et à comprendre les procédures d'emprunt. "
    "Réponds en français, de manière claire, factuelle et concise. "
    "Si tu ne sais pas, dis-le et oriente vers un enseignant ou technicien."
)

# === Singleton modèle ===
class ModelHolder:
    """Encapsule le modèle et le tokenizer (chargés une seule fois)."""

    def __init__(self) -> None:
        self.model = None
        self.tokenizer = None
        self.charge = False

    def charger(self) -> None:
        if self.charge:
            return
        if USE_MOCK:
            print("[INFO] Mode MOCK activé — pas de chargement de modèle.")
            self.charge = True
            return

        # Import paresseux : torch n'est requis qu'en mode réel
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel

        print(f"[INFO] Chargement du modèle de base : {BASE_MODEL}")
        self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
        )

        if MODEL_PATH.exists():
            print(f"[INFO] Application des poids LoRA : {MODEL_PATH}")
            self.model = PeftModel.from_pretrained(base_model, str(MODEL_PATH))
        else:
            print(f"[WARN] Pas de checkpoint LoRA trouvé à {MODEL_PATH}, "
                  "utilisation du modèle de base.")
            self.model = base_model

        self.model.eval()
        self.charge = True
        print("[OK] Modèle prêt.")

    def generer(self, prompt: str, max_new_tokens: int = 256) -> str:
        if USE_MOCK:
            return self._mock_response(prompt)

        import torch
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # On ne renvoie que la partie après l'assistant
        if "<|assistant|>" in text:
            text = text.split("<|assistant|>")[-1]
        return text.replace("<|end|>", "").strip()

    def _mock_response(self, prompt: str) -> str:
        """Réponse de démo basée sur des règles simples (mode mock).

        Les règles plus spécifiques (matériel, technique) sont testées avant
        les règles génériques (procédure d'emprunt) pour éviter qu'une question
        sur le RTK ne soit interceptée par la règle « comment faire une demande ».
        """
        p = prompt.lower()
        # Matériel spécifique
        if "leica" in p or "ts06" in p:
            return ("La station totale Leica TS06 a une précision angulaire de 5 secondes "
                    "d'arc et une portée d'environ 3 500 m sur prisme. L'UFR en possède 8 unités.")
        if "rtk" in p or "gnss" in p or "i50" in p or "i73" in p:
            return ("Le mode RTK (Real-Time Kinematic) permet d'obtenir une précision "
                    "centimétrique en temps réel grâce à une station de référence qui "
                    "transmet des corrections au récepteur mobile. Les CHC i50 et i73 "
                    "de l'UFR fonctionnent en RTK.")
        if "nivellement" in p or "niveau optique" in p:
            return ("Le nivellement direct utilise un niveau optique et une mire. "
                    "On lit la mire posée sur le point de départ (lecture arrière), "
                    "puis sur le point d'arrivée (lecture avant). La dénivelée vaut "
                    "Δh = lecture arrière - lecture avant.")
        # Procédures (vient après le matériel pour ne pas l'intercepter)
        if "demande" in p and ("comment" in p or "faire" in p):
            return ("Pour faire une demande d'emprunt : connectez-vous, allez sur "
                    "« Nouvelle demande », choisissez les dates, le motif, les matériels "
                    "et leur quantité, puis localisez votre zone sur la carte. "
                    "La demande sera traitée sous 48 h.")
        return ("Je suis l'assistant UFR SI en mode démonstration. Le modèle fine-tuné "
                "n'est pas encore chargé sur ce serveur. Posez votre question à un "
                "enseignant ou technicien en attendant.")


holder = ModelHolder()


# === Lifespan : chargement du modèle au démarrage ===
@asynccontextmanager
async def lifespan(app: FastAPI):
    holder.charger()
    yield
    print("[INFO] Service arrêté.")


app = FastAPI(
    title="Chatbot UFR SI — Service d'inférence",
    description="Microservice FastAPI pour le chatbot fine-tuné LoRA.",
    version="1.0.0",
    lifespan=lifespan,
)


# === Schémas Pydantic ===
class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class PredictRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)
    max_new_tokens: int = Field(256, ge=16, le=1024)


class PredictResponse(BaseModel):
    response: str
    mode: Literal["mock", "real"]


class ChatRequest(BaseModel):
    messages: list[Message] = Field(..., min_length=1)
    max_new_tokens: int = Field(256, ge=16, le=1024)


# === Routes ===
@app.get("/")
def racine() -> dict:
    return {
        "service": "Chatbot UFR SI",
        "version": "1.0.0",
        "mode": "mock" if USE_MOCK else "real",
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_loaded": holder.charge, "mode": "mock" if USE_MOCK else "real"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> PredictResponse:
    """Génération simple à partir d'un prompt brut."""
    try:
        # On encapsule dans le format chat de Phi-3
        prompt = (
            f"<|system|>\n{SYSTEM_PROMPT}<|end|>\n"
            f"<|user|>\n{req.prompt}<|end|>\n"
            f"<|assistant|>\n"
        )
        reponse = holder.generer(prompt, req.max_new_tokens)
        return PredictResponse(
            response=reponse,
            mode="mock" if USE_MOCK else "real",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/chat", response_model=PredictResponse)
def chat(req: ChatRequest) -> PredictResponse:
    """Génération avec historique de conversation."""
    try:
        # Construit le prompt complet à partir des messages
        parts = []
        # Insère le system par défaut si absent
        if not any(m.role == "system" for m in req.messages):
            parts.append(f"<|system|>\n{SYSTEM_PROMPT}<|end|>")
        for m in req.messages:
            parts.append(f"<|{m.role}|>\n{m.content}<|end|>")
        parts.append("<|assistant|>\n")
        prompt = "\n".join(parts)

        reponse = holder.generer(prompt, req.max_new_tokens)
        return PredictResponse(
            response=reponse,
            mode="mock" if USE_MOCK else "real",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
