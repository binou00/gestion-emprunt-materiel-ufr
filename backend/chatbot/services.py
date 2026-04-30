"""
Service IA — abstrait l'appel au modèle fine-tuné.

En Phase 5, on remplacera le mock par un vrai appel HTTP au service FastAPI.
Pour l'instant, on retourne une réponse factice — l'application reste fonctionnelle
même sans modèle entraîné.
"""
from django.conf import settings


class ChatService:
    """Interface unique pour discuter avec l'IA. Injecte le modèle au besoin."""

    def __init__(self, ia_url: str | None = None):
        self.ia_url = ia_url or settings.IA_SERVICE_URL

    def repondre(self, question: str, historique: list[dict]) -> str:
        """
        Appelle le service IA pour générer une réponse.
        En attendant le fine-tuning (Phase 5), on retourne un mock.
        """
        # TODO Phase 5 : appel HTTP réel
        # import requests
        # response = requests.post(f"{self.ia_url}/chat", json={"prompt": question, "history": historique}, timeout=30)
        # return response.json()["answer"]

        # Mock simple basé sur des mots-clés
        q = question.lower()
        if "station totale" in q:
            return ("Pour mettre en station une station totale Leica TS06 :\n"
                    "1. Centrer le trépied au-dessus du point ;\n"
                    "2. Caler grossièrement avec la nivelle sphérique ;\n"
                    "3. Caler finement avec la nivelle torique en jouant sur les vis ;\n"
                    "4. Vérifier le centrage optique.\n"
                    "(Réponse mock — sera remplacée par le modèle fine-tuné en Phase 5.)")
        if "gnss" in q or "gps" in q:
            return ("Avant tout levé GNSS : vérifier la batterie, la configuration RTK, "
                    "le masque d'élévation (10°) et le PDOP (< 5). "
                    "(Réponse mock — modèle fine-tuné à venir en Phase 5.)")
        if "niveau" in q:
            return ("Pour un nivellement direct : calez le niveau, lisez le fil moyen sur la mire, "
                    "puis pratiquez le double cheminement aller-retour. "
                    "(Mock — Phase 5 pour la vraie réponse.)")
        return ("Bonjour ! Je suis l'assistant matériel de l'UFR. "
                "Je serai pleinement opérationnel une fois le fine-tuning du modèle terminé (Phase 5). "
                "Pour l'instant je peux répondre à des questions sur les stations totales, GNSS et niveaux.")
