from rest_framework import serializers
from django.db import transaction

from .models import Demande, LigneDemande, Emplacement, Restitution


class LigneDemandeSerializer(serializers.ModelSerializer):
    materiel_nom = serializers.CharField(source="materiel.nom", read_only=True)

    class Meta:
        model = LigneDemande
        fields = ("id", "materiel", "materiel_nom", "quantite")


class EmplacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emplacement
        fields = ("id", "libelle", "adresse", "latitude", "longitude")


class RestitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restitution
        fields = (
            "id", "demande", "date_retour", "etat_materiel",
            "observations", "receptionne_par",
        )


class DemandeSerializer(serializers.ModelSerializer):
    lignes = LigneDemandeSerializer(many=True)
    emplacement = EmplacementSerializer()
    utilisateur_nom = serializers.CharField(source="utilisateur.get_full_name", read_only=True)

    class Meta:
        model = Demande
        fields = (
            "id", "utilisateur", "utilisateur_nom",
            "date_demande", "date_debut", "date_fin", "statut",
            "motif", "valide_par", "date_validation",
            "lignes", "emplacement",
        )
        read_only_fields = ("date_demande", "valide_par", "date_validation", "statut")

    def validate(self, attrs):
        if attrs.get("date_fin") and attrs.get("date_debut") and attrs["date_fin"] < attrs["date_debut"]:
            raise serializers.ValidationError("La date de fin doit être >= date de début.")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        lignes_data = validated_data.pop("lignes", [])
        emplacement_data = validated_data.pop("emplacement", None)
        # L'utilisateur est injecté par la vue (request.user)
        demande = Demande.objects.create(**validated_data)
        for ligne in lignes_data:
            LigneDemande.objects.create(demande=demande, **ligne)
        if emplacement_data:
            Emplacement.objects.create(demande=demande, **emplacement_data)
        return demande
