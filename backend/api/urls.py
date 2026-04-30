"""Routage central de l'API REST."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UtilisateurViewSet
from materiel.views import CategorieViewSet, MaterielViewSet, MaintenanceViewSet
from emprunts.views import DemandeViewSet, RestitutionViewSet
from chatbot.views import ConversationChatViewSet


router = DefaultRouter()
router.register(r"utilisateurs", UtilisateurViewSet, basename="utilisateur")
router.register(r"categories", CategorieViewSet, basename="categorie")
router.register(r"materiels", MaterielViewSet, basename="materiel")
router.register(r"maintenances", MaintenanceViewSet, basename="maintenance")
router.register(r"demandes", DemandeViewSet, basename="demande")
router.register(r"restitutions", RestitutionViewSet, basename="restitution")
router.register(r"chat", ConversationChatViewSet, basename="chat")


urlpatterns = [
    path("", include(router.urls)),
    # JWT auth (login)
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Browsable API login
    path("auth/", include("rest_framework.urls")),
]
