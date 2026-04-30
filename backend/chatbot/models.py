"""
Conversation avec le chatbot IA.

Stockage simple en JSON pour la liste des messages —
permet d'évoluer sans migration à chaque changement de format.
"""
from django.conf import settings
from django.db import models
from django.utils import timezone


class ConversationChat(models.Model):
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversations",
        verbose_name="utilisateur",
    )
    titre = models.CharField("titre", max_length=200, blank=True)
    date_creation = models.DateTimeField("date de création", auto_now_add=True)
    derniere_activite = models.DateTimeField("dernière activité", default=timezone.now)
    messages = models.JSONField(
        "messages",
        default=list,
        help_text="Liste de dicts {role: 'user'|'assistant', content: str, ts: ISO8601}",
    )

    class Meta:
        verbose_name = "conversation"
        verbose_name_plural = "conversations"
        ordering = ["-derniere_activite"]

    def __str__(self) -> str:
        return f"Conversation #{self.pk} — {self.utilisateur} ({len(self.messages)} msg)"

    # --- Méthodes métier (POO) ---
    def ajouter_message(self, role: str, contenu: str):
        """Ajoute un message à la conversation. role ∈ {'user', 'assistant'}."""
        if role not in {"user", "assistant", "system"}:
            raise ValueError("role doit être 'user', 'assistant' ou 'system'")
        self.messages.append({
            "role": role,
            "content": contenu,
            "ts": timezone.now().isoformat(),
        })
        self.derniere_activite = timezone.now()
        # Auto-titre depuis le premier message utilisateur
        if not self.titre and role == "user":
            self.titre = (contenu[:60] + "…") if len(contenu) > 60 else contenu
        self.save()

    def historique_pour_llm(self, limite: int = 10) -> list:
        """Retourne les N derniers messages au format attendu par un LLM."""
        return [
            {"role": m["role"], "content": m["content"]}
            for m in self.messages[-limite:]
        ]
