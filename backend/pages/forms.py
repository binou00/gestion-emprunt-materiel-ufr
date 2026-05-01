"""Formulaires HTML pour les vues."""
from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import Utilisateur, Role


class InscriptionForm(UserCreationForm):
    """Formulaire d'inscription d'un étudiant."""

    first_name = forms.CharField(label="Prénom", max_length=150, required=True)
    last_name = forms.CharField(label="Nom", max_length=150, required=True)
    email = forms.EmailField(label="E-mail", required=True)
    filiere = forms.CharField(label="Filière", max_length=100, required=False)
    niveau = forms.CharField(label="Niveau", max_length=20, required=False)
    telephone = forms.CharField(label="Téléphone", max_length=20, required=False)

    class Meta:
        model = Utilisateur
        fields = (
            "username", "email", "first_name", "last_name",
            "filiere", "niveau", "telephone",
            "password1", "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.filiere = self.cleaned_data.get("filiere", "")
        user.niveau = self.cleaned_data.get("niveau", "")
        user.telephone = self.cleaned_data.get("telephone", "")
        user.role = Role.ETUDIANT
        if commit:
            user.save()
        return user
