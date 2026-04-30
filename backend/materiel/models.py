"""
Modèles Matériel : Catégorie, Matériel, Maintenance.

Reflète directement le diagramme de classes Phase 1.
"""
from django.db import models


class Categorie(models.Model):
    libelle = models.CharField("libellé", max_length=100, unique=True)
    description = models.TextField("description", blank=True)

    class Meta:
        verbose_name = "catégorie"
        verbose_name_plural = "catégories"
        ordering = ["libelle"]

    def __str__(self) -> str:
        return self.libelle


class EtatMateriel(models.TextChoices):
    """Énumération des états possibles d'un matériel."""
    DISPONIBLE = "DISPONIBLE", "Disponible"
    EMPRUNTE = "EMPRUNTE", "Emprunté"
    EN_MAINTENANCE = "EN_MAINTENANCE", "En maintenance"
    HORS_SERVICE = "HORS_SERVICE", "Hors service"


class Materiel(models.Model):
    """
    Matériel topographique ou géodésique (station totale, GNSS, etc.).
    Le champ `quantite_disponible` permet de gérer plusieurs unités identiques
    sous une même référence (ex : 42 trépieds).
    """

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.PROTECT,
        related_name="materiels",
        verbose_name="catégorie",
    )
    nom = models.CharField("nom", max_length=200)
    numero_serie = models.CharField("numéro de série", max_length=100, unique=True)
    etat = models.CharField(
        "état",
        max_length=20,
        choices=EtatMateriel.choices,
        default=EtatMateriel.DISPONIBLE,
    )
    photo = models.ImageField("photo", upload_to="materiel/", blank=True, null=True)
    description = models.TextField("description", blank=True)
    date_acquisition = models.DateField("date d'acquisition", null=True, blank=True)
    quantite_disponible = models.PositiveIntegerField(
        "quantité disponible",
        default=1,
        help_text="Nombre d'unités physiques actuellement disponibles à l'emprunt.",
    )

    class Meta:
        verbose_name = "matériel"
        verbose_name_plural = "matériels"
        ordering = ["categorie", "nom"]

    # --- Méthodes métier (POO) ---
    def __str__(self) -> str:
        return f"{self.nom} [{self.numero_serie}]"

    def est_disponible(self) -> bool:
        return self.etat == EtatMateriel.DISPONIBLE and self.quantite_disponible > 0

    def marquer_en_panne(self):
        self.etat = EtatMateriel.EN_MAINTENANCE
        self.save(update_fields=["etat"])

    def remettre_en_service(self):
        self.etat = EtatMateriel.DISPONIBLE
        self.save(update_fields=["etat"])


class Maintenance(models.Model):
    """Suivi des interventions de maintenance sur un matériel."""

    class StatutMaintenance(models.TextChoices):
        SIGNALE = "SIGNALE", "Signalé"
        EN_COURS = "EN_COURS", "En cours"
        RESOLU = "RESOLU", "Résolu"
        ABANDONNE = "ABANDONNE", "Abandonné"

    materiel = models.ForeignKey(
        Materiel,
        on_delete=models.CASCADE,
        related_name="maintenances",
        verbose_name="matériel",
    )
    type = models.CharField("type", max_length=100, help_text="Ex : panne, calibration, vérification")
    description = models.TextField("description", blank=True)
    date_signalement = models.DateField("date de signalement", auto_now_add=True)
    date_resolution = models.DateField("date de résolution", null=True, blank=True)
    statut = models.CharField(
        "statut",
        max_length=20,
        choices=StatutMaintenance.choices,
        default=StatutMaintenance.SIGNALE,
    )

    class Meta:
        verbose_name = "maintenance"
        verbose_name_plural = "maintenances"
        ordering = ["-date_signalement"]

    def __str__(self) -> str:
        return f"{self.type} — {self.materiel.nom} ({self.get_statut_display()})"
