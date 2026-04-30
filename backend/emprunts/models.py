"""
Modèles d'emprunt : Demande, LigneDemande, Emplacement, Restitution.

Cœur du métier : cycle de vie EN_ATTENTE -> APPROUVEE -> EN_COURS -> RESTITUEE.
"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from materiel.models import Materiel, EtatMateriel


class StatutDemande(models.TextChoices):
    EN_ATTENTE = "EN_ATTENTE", "En attente"
    APPROUVEE = "APPROUVEE", "Approuvée"
    REFUSEE = "REFUSEE", "Refusée"
    EN_COURS = "EN_COURS", "En cours"
    RESTITUEE = "RESTITUEE", "Restituée"
    ANNULEE = "ANNULEE", "Annulée"


class Demande(models.Model):
    """
    Demande d'emprunt soumise par un utilisateur.
    Une demande peut contenir plusieurs LigneDemande (plusieurs matériels).
    """

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="demandes",
        verbose_name="demandeur",
    )
    date_demande = models.DateTimeField("date de la demande", auto_now_add=True)
    date_debut = models.DateField("date de début")
    date_fin = models.DateField("date de fin")
    statut = models.CharField(
        "statut",
        max_length=20,
        choices=StatutDemande.choices,
        default=StatutDemande.EN_ATTENTE,
    )
    motif = models.TextField(
        "motif / commentaire",
        blank=True,
        help_text="Justification de la demande ou motif de refus.",
    )
    valide_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="demandes_validees",
        verbose_name="validé par",
    )
    date_validation = models.DateTimeField("date de validation", null=True, blank=True)

    class Meta:
        verbose_name = "demande d'emprunt"
        verbose_name_plural = "demandes d'emprunt"
        ordering = ["-date_demande"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(date_fin__gte=models.F("date_debut")),
                name="date_fin_apres_date_debut",
            )
        ]

    def __str__(self) -> str:
        return f"Demande #{self.pk} — {self.utilisateur} ({self.get_statut_display()})"

    # --- Validation métier ---
    def clean(self):
        super().clean()
        if self.date_debut and self.date_fin and self.date_fin < self.date_debut:
            raise ValidationError("La date de fin doit être postérieure ou égale à la date de début.")

    # --- Méthodes du cycle de vie ---
    def valider(self, par_utilisateur):
        """Approuve la demande : décrémente le stock matériel."""
        if self.statut != StatutDemande.EN_ATTENTE:
            raise ValidationError("Seule une demande en attente peut être approuvée.")
        for ligne in self.lignes.all():
            mat = ligne.materiel
            if mat.quantite_disponible < ligne.quantite:
                raise ValidationError(
                    f"Stock insuffisant pour {mat.nom} "
                    f"(demandé : {ligne.quantite}, disponible : {mat.quantite_disponible})."
                )
            mat.quantite_disponible -= ligne.quantite
            if mat.quantite_disponible == 0:
                mat.etat = EtatMateriel.EMPRUNTE
            mat.save(update_fields=["quantite_disponible", "etat"])
        self.statut = StatutDemande.APPROUVEE
        self.valide_par = par_utilisateur
        self.date_validation = timezone.now()
        self.save()

    def refuser(self, par_utilisateur, motif: str):
        if self.statut != StatutDemande.EN_ATTENTE:
            raise ValidationError("Seule une demande en attente peut être refusée.")
        self.statut = StatutDemande.REFUSEE
        self.motif = motif
        self.valide_par = par_utilisateur
        self.date_validation = timezone.now()
        self.save()

    def marquer_en_cours(self):
        """À appeler quand l'étudiant a effectivement récupéré le matériel."""
        if self.statut != StatutDemande.APPROUVEE:
            raise ValidationError("La demande doit être approuvée avant de passer en cours.")
        self.statut = StatutDemande.EN_COURS
        self.save(update_fields=["statut"])

    def annuler(self):
        if self.statut not in {StatutDemande.EN_ATTENTE, StatutDemande.APPROUVEE}:
            raise ValidationError("Cette demande ne peut plus être annulée.")
        # Si elle était approuvée, on remet le stock
        if self.statut == StatutDemande.APPROUVEE:
            for ligne in self.lignes.all():
                mat = ligne.materiel
                mat.quantite_disponible += ligne.quantite
                mat.etat = EtatMateriel.DISPONIBLE
                mat.save(update_fields=["quantite_disponible", "etat"])
        self.statut = StatutDemande.ANNULEE
        self.save(update_fields=["statut"])


class LigneDemande(models.Model):
    """Une ligne = un matériel demandé dans une demande, avec une quantité."""

    demande = models.ForeignKey(
        Demande,
        on_delete=models.CASCADE,
        related_name="lignes",
        verbose_name="demande",
    )
    materiel = models.ForeignKey(
        Materiel,
        on_delete=models.PROTECT,
        related_name="lignes_demande",
        verbose_name="matériel",
    )
    quantite = models.PositiveIntegerField("quantité", default=1)

    class Meta:
        verbose_name = "ligne de demande"
        verbose_name_plural = "lignes de demande"
        unique_together = ("demande", "materiel")  # un même matériel ne peut apparaître qu'une fois par demande

    def __str__(self) -> str:
        return f"{self.quantite} × {self.materiel.nom}"


class Emplacement(models.Model):
    """Localisation GPS d'utilisation du matériel sur le terrain."""

    demande = models.OneToOneField(
        Demande,
        on_delete=models.CASCADE,
        related_name="emplacement",
        verbose_name="demande",
    )
    libelle = models.CharField("libellé", max_length=200, blank=True)
    adresse = models.CharField("adresse", max_length=500, blank=True)
    latitude = models.FloatField("latitude")
    longitude = models.FloatField("longitude")

    class Meta:
        verbose_name = "emplacement"
        verbose_name_plural = "emplacements"

    def __str__(self) -> str:
        return f"{self.libelle or 'Emplacement'} ({self.latitude:.5f}, {self.longitude:.5f})"


class Restitution(models.Model):
    """Restitution du matériel à la fin de l'emprunt."""

    class EtatRetour(models.TextChoices):
        BON = "BON", "Bon état"
        ENDOMMAGE = "ENDOMMAGE", "Endommagé"
        PERDU = "PERDU", "Perdu"

    demande = models.OneToOneField(
        Demande,
        on_delete=models.CASCADE,
        related_name="restitution",
        verbose_name="demande",
    )
    date_retour = models.DateTimeField("date de retour", default=timezone.now)
    etat_materiel = models.CharField(
        "état du matériel",
        max_length=20,
        choices=EtatRetour.choices,
        default=EtatRetour.BON,
    )
    observations = models.TextField("observations", blank=True)
    receptionne_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="restitutions_receptionnees",
        verbose_name="réceptionné par",
    )

    class Meta:
        verbose_name = "restitution"
        verbose_name_plural = "restitutions"
        ordering = ["-date_retour"]

    def __str__(self) -> str:
        return f"Restitution demande #{self.demande_id} — {self.get_etat_materiel_display()}"

    def save(self, *args, **kwargs):
        """Lors de l'enregistrement, on remet le matériel en stock et on clôt la demande."""
        super().save(*args, **kwargs)
        for ligne in self.demande.lignes.all():
            mat = ligne.materiel
            if self.etat_materiel == self.EtatRetour.BON:
                mat.quantite_disponible += ligne.quantite
                mat.etat = EtatMateriel.DISPONIBLE
            elif self.etat_materiel == self.EtatRetour.ENDOMMAGE:
                mat.etat = EtatMateriel.EN_MAINTENANCE
            # PERDU : on ne réincrémente pas la quantité
            mat.save(update_fields=["quantite_disponible", "etat"])
        self.demande.statut = StatutDemande.RESTITUEE
        self.demande.save(update_fields=["statut"])
