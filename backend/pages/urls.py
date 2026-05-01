"""URLs des pages HTML (côté étudiant)."""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("inscription/", views.register, name="register"),
    path("catalogue/", views.catalogue, name="catalogue"),
    path("mes-emprunts/", views.mes_emprunts, name="mes_emprunts"),
    path("nouvelle-demande/", views.nouvelle_demande, name="nouvelle_demande"),
    path("chat/", views.chat, name="chat"),
]
