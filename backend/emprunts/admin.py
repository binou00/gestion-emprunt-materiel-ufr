from django.contrib import admin
from .models import Demande, LigneDemande, Emplacement, Restitution


class LigneDemandeInline(admin.TabularInline):
    model = LigneDemande
    extra = 1


class EmplacementInline(admin.StackedInline):
    model = Emplacement
    extra = 0
    max_num = 1


@admin.register(Demande)
class DemandeAdmin(admin.ModelAdmin):
    list_display = ("id", "utilisateur", "date_demande", "date_debut", "date_fin", "statut", "valide_par")
    list_filter = ("statut", "date_debut")
    search_fields = ("utilisateur__email", "utilisateur__last_name", "motif")
    date_hierarchy = "date_demande"
    inlines = [LigneDemandeInline, EmplacementInline]
    readonly_fields = ("date_demande", "date_validation")
    actions = ["approuver_demandes", "refuser_demandes"]

    @admin.action(description="Approuver les demandes sélectionnées")
    def approuver_demandes(self, request, queryset):
        count = 0
        for demande in queryset:
            try:
                demande.valider(par_utilisateur=request.user)
                count += 1
            except Exception as e:
                self.message_user(request, f"Demande #{demande.pk} : {e}", level="ERROR")
        self.message_user(request, f"{count} demande(s) approuvée(s).")

    @admin.action(description="Refuser les demandes sélectionnées (motif générique)")
    def refuser_demandes(self, request, queryset):
        count = 0
        for demande in queryset:
            try:
                demande.refuser(par_utilisateur=request.user, motif="Refusée depuis l'admin")
                count += 1
            except Exception as e:
                self.message_user(request, f"Demande #{demande.pk} : {e}", level="ERROR")
        self.message_user(request, f"{count} demande(s) refusée(s).")


@admin.register(Restitution)
class RestitutionAdmin(admin.ModelAdmin):
    list_display = ("demande", "date_retour", "etat_materiel", "receptionne_par")
    list_filter = ("etat_materiel",)
    date_hierarchy = "date_retour"


@admin.register(Emplacement)
class EmplacementAdmin(admin.ModelAdmin):
    list_display = ("demande", "libelle", "latitude", "longitude")
    search_fields = ("libelle", "adresse")
