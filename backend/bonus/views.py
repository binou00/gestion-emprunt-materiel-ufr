"""
Vues HTML & API du module bonus :
- Dashboard administrateur (KPIs)
- Export CSV des demandes
"""
import csv
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from emprunts.models import Demande, StatutDemande
from materiel.models import Materiel, EtatMateriel
from users.models import Utilisateur, Role


@staff_member_required
def dashboard(request):
    """Dashboard administrateur — KPIs et synthèse."""
    aujourdhui = timezone.localdate()
    debut_mois = aujourdhui.replace(day=1)

    # KPIs principaux
    total_demandes = Demande.objects.count()
    demandes_par_statut = (
        Demande.objects.values("statut")
        .annotate(n=Count("id"))
        .order_by("-n")
    )
    statuts = {item["statut"]: item["n"] for item in demandes_par_statut}

    en_attente = statuts.get(StatutDemande.EN_ATTENTE, 0)
    approuvees = statuts.get(StatutDemande.APPROUVEE, 0)
    en_cours = statuts.get(StatutDemande.EN_COURS, 0)
    restituees = statuts.get(StatutDemande.RESTITUEE, 0)
    refusees = statuts.get(StatutDemande.REFUSEE, 0)

    taux_approbation = 0
    if (approuvees + refusees) > 0:
        taux_approbation = round(100 * approuvees / (approuvees + refusees), 1)

    # Retards : demandes EN_COURS avec date_fin dépassée
    retards = Demande.objects.filter(
        statut=StatutDemande.EN_COURS,
        date_fin__lt=aujourdhui,
    ).select_related("utilisateur").order_by("date_fin")[:10]

    # Top 5 matériels les plus demandés
    top_materiels = (
        Materiel.objects
        .annotate(nb_demandes=Count("lignes_demande"))
        .filter(nb_demandes__gt=0)
        .order_by("-nb_demandes")[:5]
    )

    # Activité du mois en cours
    demandes_mois = Demande.objects.filter(date_demande__gte=debut_mois).count()

    # Utilisateurs
    nb_etudiants = Utilisateur.objects.filter(role=Role.ETUDIANT, is_active=True).count()
    nb_techniciens = Utilisateur.objects.filter(role=Role.TECHNICIEN, is_active=True).count()

    # Matériel par état
    nb_materiels = Materiel.objects.count()
    nb_disponibles = Materiel.objects.filter(etat=EtatMateriel.DISPONIBLE).count()
    nb_empruntes = Materiel.objects.filter(etat=EtatMateriel.EMPRUNTE).count()
    nb_maintenance = Materiel.objects.filter(etat=EtatMateriel.EN_MAINTENANCE).count()

    contexte = {
        "total_demandes": total_demandes,
        "en_attente": en_attente,
        "approuvees": approuvees,
        "en_cours": en_cours,
        "restituees": restituees,
        "refusees": refusees,
        "taux_approbation": taux_approbation,
        "demandes_mois": demandes_mois,
        "retards": retards,
        "top_materiels": top_materiels,
        "nb_etudiants": nb_etudiants,
        "nb_techniciens": nb_techniciens,
        "nb_materiels": nb_materiels,
        "nb_disponibles": nb_disponibles,
        "nb_empruntes": nb_empruntes,
        "nb_maintenance": nb_maintenance,
        "aujourdhui": aujourdhui,
    }
    return render(request, "bonus/dashboard.html", contexte)


@staff_member_required
def export_demandes_csv(request):
    """
    Exporte toutes les demandes en CSV (UTF-8 BOM pour Excel).
    Filtres optionnels via querystring : ?statut=APPROUVEE&date_debut=2025-01-01
    """
    qs = Demande.objects.select_related("utilisateur", "valide_par").prefetch_related("lignes__materiel")

    statut = request.GET.get("statut")
    if statut:
        qs = qs.filter(statut=statut)
    date_debut = request.GET.get("date_debut")
    if date_debut:
        qs = qs.filter(date_demande__date__gte=date_debut)
    date_fin = request.GET.get("date_fin")
    if date_fin:
        qs = qs.filter(date_demande__date__lte=date_fin)

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = (
        f'attachment; filename="demandes_{timezone.localdate()}.csv"'
    )
    # BOM UTF-8 pour qu'Excel ouvre correctement les accents
    response.write("\ufeff")

    writer = csv.writer(response, delimiter=";", quoting=csv.QUOTE_MINIMAL)
    writer.writerow([
        "ID demande",
        "Date demande",
        "Demandeur",
        "Email",
        "Rôle",
        "Date début",
        "Date fin",
        "Statut",
        "Matériels demandés",
        "Validé par",
        "Date validation",
        "Motif",
    ])

    for d in qs:
        materiels = " | ".join(
            f"{l.quantite}× {l.materiel.nom}" for l in d.lignes.all()
        )
        writer.writerow([
            d.pk,
            d.date_demande.strftime("%Y-%m-%d %H:%M"),
            d.utilisateur.get_full_name() or d.utilisateur.username,
            d.utilisateur.email,
            d.utilisateur.get_role_display(),
            d.date_debut.strftime("%Y-%m-%d"),
            d.date_fin.strftime("%Y-%m-%d"),
            d.get_statut_display(),
            materiels,
            d.valide_par.get_full_name() if d.valide_par else "",
            d.date_validation.strftime("%Y-%m-%d %H:%M") if d.date_validation else "",
            (d.motif or "").replace("\n", " "),
        ])
    return response


@staff_member_required
def export_materiels_csv(request):
    """Exporte le catalogue matériel en CSV."""
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = (
        f'attachment; filename="materiels_{timezone.localdate()}.csv"'
    )
    response.write("\ufeff")
    writer = csv.writer(response, delimiter=";")
    writer.writerow([
        "Code", "Nom", "Marque", "Catégorie",
        "Quantité totale", "Quantité disponible", "État",
    ])
    for m in Materiel.objects.select_related("categorie").all():
        writer.writerow([
            m.code,
            m.nom,
            getattr(m, "marque", "") or "",
            m.categorie.nom if m.categorie else "",
            getattr(m, "quantite_totale", "") or "",
            getattr(m, "quantite_disponible", "") or "",
            m.get_etat_display(),
        ])
    return response
