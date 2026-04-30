from django.contrib import admin
from .models import ConversationChat


@admin.register(ConversationChat)
class ConversationChatAdmin(admin.ModelAdmin):
    list_display = ("id", "utilisateur", "titre", "date_creation", "derniere_activite")
    search_fields = ("utilisateur__email", "titre")
    readonly_fields = ("date_creation", "derniere_activite", "messages")
    date_hierarchy = "date_creation"
