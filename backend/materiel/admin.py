from django.contrib import admin
from .models import Categorie, Materiel, Maintenance


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("libelle", "description")
    search_fields = ("libelle",)


@admin.register(Materiel)
class MaterielAdmin(admin.ModelAdmin):
    list_display = ("nom", "categorie", "numero_serie", "etat", "quantite_disponible", "date_acquisition")
    list_filter = ("categorie", "etat")
    search_fields = ("nom", "numero_serie", "description")
    list_editable = ("etat", "quantite_disponible")


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ("materiel", "type", "statut", "date_signalement", "date_resolution")
    list_filter = ("statut", "type")
    search_fields = ("materiel__nom", "type", "description")
    date_hierarchy = "date_signalement"
