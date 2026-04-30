from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ConversationChat
from .serializers import ConversationChatSerializer, MessageInputSerializer
from .services import ChatService


class ConversationChatViewSet(viewsets.ModelViewSet):
    """
    Endpoints :
      - GET    /api/chat/                : conversations de l'utilisateur courant
      - POST   /api/chat/                : crée une nouvelle conversation
      - POST   /api/chat/{id}/envoyer/   : envoie un message et reçoit la réponse de l'IA
    """
    serializer_class = ConversationChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ConversationChat.objects.filter(utilisateur=self.request.user)

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

    @action(detail=True, methods=["post"])
    def envoyer(self, request, pk=None):
        conv = self.get_object()
        ser = MessageInputSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        message = ser.validated_data["contenu"]

        # 1) on enregistre le message utilisateur
        conv.ajouter_message("user", message)

        # 2) appel au service IA
        service = ChatService()
        reponse = service.repondre(message, historique=conv.historique_pour_llm())

        # 3) on enregistre la réponse
        conv.ajouter_message("assistant", reponse)

        return Response({"reponse": reponse, "conversation": ConversationChatSerializer(conv).data})
