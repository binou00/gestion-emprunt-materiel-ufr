"""
Tests du module chatbot — focalisés sur le ChatService.

Lancer :
    cd backend/
    python manage.py test chatbot
"""
from unittest.mock import patch, Mock

from django.test import TestCase

from .services import ChatService, IAServiceError


class ChatServiceTests(TestCase):
    """Tests unitaires de ChatService avec mocks HTTP."""

    def setUp(self):
        self.service = ChatService(ia_url="http://localhost:8001", timeout=5)

    @patch("chatbot.services.requests.post")
    def test_repondre_succes(self, mock_post):
        """Réponse OK → on renvoie le texte du modèle."""
        mock_post.return_value = Mock(
            status_code=200,
            json=Mock(return_value={"response": "La Leica TS06 a une précision de 5\".", "mode": "real"}),
        )
        mock_post.return_value.raise_for_status = Mock()

        reponse = self.service.repondre("Précision Leica TS06 ?")
        self.assertIn("Leica", reponse)
        mock_post.assert_called_once()

        # Vérifie que le payload envoyé contient bien la question
        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["messages"][-1]["role"], "user")
        self.assertIn("Leica", kwargs["json"]["messages"][-1]["content"])

    @patch("chatbot.services.requests.post")
    def test_repondre_avec_historique(self, mock_post):
        """L'historique est bien transmis avant la nouvelle question."""
        mock_post.return_value = Mock(
            status_code=200,
            json=Mock(return_value={"response": "...", "mode": "real"}),
        )
        mock_post.return_value.raise_for_status = Mock()

        historique = [
            {"role": "user", "content": "Bonjour"},
            {"role": "assistant", "content": "Salut !"},
        ]
        self.service.repondre("Comment ça va ?", historique=historique)

        _, kwargs = mock_post.call_args
        msgs = kwargs["json"]["messages"]
        self.assertEqual(len(msgs), 3)  # 2 historique + 1 nouvelle
        self.assertEqual(msgs[0]["content"], "Bonjour")
        self.assertEqual(msgs[-1]["content"], "Comment ça va ?")

    @patch("chatbot.services.requests.post")
    def test_fallback_si_timeout(self, mock_post):
        """En cas de timeout, on utilise le fallback (pas d'exception)."""
        import requests
        mock_post.side_effect = requests.Timeout("timeout")

        reponse = self.service.repondre("Question test")
        self.assertIn("indisponible", reponse.lower())
        self.assertIn("Question test", reponse)

    @patch("chatbot.services.requests.post")
    def test_fallback_si_erreur_reseau(self, mock_post):
        """En cas d'erreur réseau, fallback aussi."""
        import requests
        mock_post.side_effect = requests.ConnectionError("connection refused")

        reponse = self.service.repondre("Question test")
        self.assertIn("indisponible", reponse.lower())

    @patch("chatbot.services.requests.post")
    def test_erreur_si_reponse_vide(self, mock_post):
        """Si le modèle renvoie une réponse vide, on tombe sur le fallback."""
        mock_post.return_value = Mock(
            status_code=200,
            json=Mock(return_value={"response": "   ", "mode": "real"}),
        )
        mock_post.return_value.raise_for_status = Mock()

        reponse = self.service.repondre("Question test")
        self.assertIn("indisponible", reponse.lower())

    @patch("chatbot.services.requests.get")
    def test_health_online(self, mock_get):
        """health() renvoie online=True quand le service répond."""
        mock_get.return_value = Mock(
            status_code=200,
            json=Mock(return_value={"status": "ok", "mode": "mock"}),
        )
        mock_get.return_value.raise_for_status = Mock()

        result = self.service.health()
        self.assertTrue(result["online"])
        self.assertEqual(result["mode"], "mock")

    @patch("chatbot.services.requests.get")
    def test_health_offline(self, mock_get):
        """health() renvoie online=False si erreur."""
        import requests
        mock_get.side_effect = requests.ConnectionError("down")

        result = self.service.health()
        self.assertFalse(result["online"])
        self.assertIn("error", result)


class IAServiceErrorTests(TestCase):
    """L'exception IAServiceError doit être levable et descriptive."""

    def test_creation(self):
        with self.assertRaises(IAServiceError) as ctx:
            raise IAServiceError("test")
        self.assertEqual(str(ctx.exception), "test")
