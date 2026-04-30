from rest_framework import serializers
from .models import ConversationChat


class ConversationChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationChat
        fields = ("id", "utilisateur", "titre", "date_creation", "derniere_activite", "messages")
        read_only_fields = ("utilisateur", "date_creation", "derniere_activite", "messages")


class MessageInputSerializer(serializers.Serializer):
    """Payload pour POST /api/chat/{id}/envoyer/"""
    contenu = serializers.CharField(max_length=2000)
