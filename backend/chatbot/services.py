"""
Service IA — abstrait l'appel au modèle fine-tuné via HTTP.

Le microservice FastAPI (ia/service/main.py) expose deux routes :
    POST /predict  → prompt simple
    POST /chat     → prompt avec historique

Si le service est injoignable, on retombe sur une réponse de secours
afin que l'application Django continue de fonctionner.
"""
from __future__ import annotations

import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class IAServiceError(Exception):
    """Erreur levée quand le microservice IA est injoignable ou répond mal."""


class ChatService:
    """Interface unique pour discuter avec l'IA.

    Encapsule l'appel HTTP au microservice FastAPI et fournit un fallback
    pour que l'app Django reste utilisable même si l'IA est down.
    """

    def __init__(self, ia_url: str | None = None, timeout: int = 30):
        self.ia_url = (ia_url or settings.IA_SERVICE_URL).rstrip("/")
        self.timeout = timeout

    # ------------------------------------------------------------------
    # API publique
    # ------------------------------------------------------------------
    def repondre(self, question: str, historique: list[dict] | None = None) -> str:
        """Renvoie la réponse du chatbot pour une question donnée.

        :param question: Question de l'utilisateur (str non vide).
        :param historique: Liste de messages précédents au format
            [{"role": "user"|"assistant", "content": "..."}, ...]
        """
        historique = historique or []
        try:
            return self._appeler_chat(question, historique)
        except IAServiceError as exc:
            logger.warning("IA injoignable, fallback. Cause : %s", exc)
            return self._fallback(question)

    def health(self) -> dict:
        """Renvoie le statut du microservice IA (utile pour /api/chat/health/)."""
        try:
            r = requests.get(f"{self.ia_url}/health", timeout=5)
            r.raise_for_status()
            return {"online": True, **r.json()}
        except (requests.RequestException, ValueError) as exc:
            return {"online": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Implémentation
    # ------------------------------------------------------------------
    def _appeler_chat(self, question: str, historique: list[dict]) -> str:
        """Effectue l'appel HTTP POST /chat sur le microservice IA."""
        # Construire la liste de messages : historique + nouvelle question
        messages = list(historique) + [{"role": "user", "content": question}]
        payload = {"messages": messages, "max_new_tokens": 256}

        try:
            r = requests.post(
                f"{self.ia_url}/chat",
                json=payload,
                timeout=self.timeout,
            )
            r.raise_for_status()
            data = r.json()
        except requests.Timeout as exc:
            raise IAServiceError(f"Timeout après {self.timeout}s") from exc
        except requests.RequestException as exc:
            raise IAServiceError(f"Erreur réseau : {exc}") from exc
        except ValueError as exc:
            raise IAServiceError("Réponse non JSON") from exc

        reponse = data.get("response", "").strip()
        if not reponse:
            raise IAServiceError("Réponse vide du modèle")
        return reponse

    def _fallback(self, question: str) -> str:
        """Réponse de secours quand le service IA est indisponible."""
        return (
            "L'assistant IA est momentanément indisponible. "
            "Je vous invite à reformuler plus tard, ou à contacter directement "
            "votre enseignant ou le technicien de l'UFR. "
            f"(Question reçue : « {question[:80]}{'…' if len(question) > 80 else ''} »)"
        )
