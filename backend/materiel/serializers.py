from rest_framework import serializers
from .models import Categorie, Materiel, Maintenance


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ("id", "libelle", "description")


class MaterielSerializer(serializers.ModelSerializer):
    categorie_libelle = serializers.CharField(source="categorie.libelle", read_only=True)
    est_disponible = serializers.SerializerMethodField()

    class Meta:
        model = Materiel
        fields = (
            "id", "nom", "categorie", "categorie_libelle",
            "numero_serie", "etat", "photo", "description",
            "date_acquisition", "quantite_disponible", "est_disponible",
        )

    def get_est_disponible(self, obj) -> bool:
        return obj.est_disponible()


class MaintenanceSerializer(serializers.ModelSerializer):
    materiel_nom = serializers.CharField(source="materiel.nom", read_only=True)

    class Meta:
        model = Maintenance
        fields = (
            "id", "materiel", "materiel_nom", "type", "description",
            "date_signalement", "date_resolution", "statut",
        )
