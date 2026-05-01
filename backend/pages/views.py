"""
Vues HTML — rendent les templates Django (pas l'API REST).
"""
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from materiel.models import Materiel, Categorie, EtatMateriel
from users.models import Utilisateur
from .forms import InscriptionForm


def home(request):
    """Page d'accueil avec statistiques."""
    stats = {
        "materiels": Materiel.objects.count(),
        "categories": Categorie.objects.count(),
        "disponibles": Materiel.objects.filter(etat=EtatMateriel.DISPONIBLE).count(),
        "utilisateurs": Utilisateur.objects.filter(is_active=True).count(),
    }
    return render(request, "home.html", {"stats": stats})


def register(request):
    """Inscription d'un nouvel utilisateur (étudiant par défaut)."""
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Bienvenue ! Votre compte a été créé.")
            return redirect("home")
    else:
        form = InscriptionForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def catalogue(request):
    """Catalogue du matériel — placeholder Phase 3 suite."""
    materiels = Materiel.objects.select_related("categorie").all()
    categories = Categorie.objects.all()
    return render(request, "materiel/catalogue.html", {
        "materiels": materiels,
        "categories": categories,
    })


@login_required
def mes_emprunts(request):
    """Historique des demandes de l'utilisateur courant."""
    demandes = request.user.demandes.all().prefetch_related("lignes", "emplacement")
    return render(request, "emprunts/mes_emprunts.html", {"demandes": demandes})


@login_required
def nouvelle_demande(request):
    """Formulaire de nouvelle demande avec carte Leaflet."""
    materiels = Materiel.objects.filter(etat=EtatMateriel.DISPONIBLE).select_related("categorie")
    return render(request, "emprunts/nouvelle_demande.html", {"materiels": materiels})


@login_required
def chat(request):
    """Interface du chatbot IA."""
    conversations = request.user.conversations.all()[:20]
    return render(request, "chatbot/chat.html", {"conversations": conversations})
