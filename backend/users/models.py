"""
Modèle Utilisateur — hérite d'AbstractUser pour ajouter rôle, filière, niveau, téléphone.

Application directe du diagramme de classes (Phase 1).
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    """Énumération des rôles — correspond à l'enum Role du diagramme de classes."""
    ETUDIANT = "ETUDIANT", "Étudiant"
    ENSEIGNANT = "ENSEIGNANT", "Enseignant"
    TECHNICIEN = "TECHNICIEN", "Technicien"
    ADMINISTRATEUR = "ADMINISTRATEUR", "Administrateur"


class Utilisateur(AbstractUser):
    """
    Utilisateur de l'application — étudiant, enseignant, technicien ou admin.
    Hérite d'AbstractUser : on garde username, email, password, first_name, last_name.
    On ajoute : role, filiere, niveau, telephone.
    """

    # email obligatoire et unique
    email = models.EmailField("adresse e-mail", unique=True)
    role = models.CharField(
        "rôle",
        max_length=20,
        choices=Role.choices,
        default=Role.ETUDIANT,
    )
    filiere = models.CharField("filière", max_length=100, blank=True)
    niveau = models.CharField("niveau", max_length=20, blank=True, help_text="L1, L2, L3, M1, M2…")
    telephone = models.CharField("téléphone", max_length=20, blank=True)

    # Login par email plutôt que par username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"
        ordering = ["last_name", "first_name"]

    # --- Méthodes métier (POO) ---
    def __str__(self) -> str:
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    def est_administrateur(self) -> bool:
        return self.role == Role.ADMINISTRATEUR or self.is_superuser

    def peut_emprunter(self) -> bool:
        """Tout utilisateur authentifié peut emprunter sauf si désactivé."""
        return self.is_active and self.role in {
            Role.ETUDIANT, Role.ENSEIGNANT, Role.TECHNICIEN, Role.ADMINISTRATEUR
        }

    def peut_valider_demandes(self) -> bool:
        return self.role in {Role.ADMINISTRATEUR, Role.TECHNICIEN} or self.is_superuser
