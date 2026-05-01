"""URLs du module bonus (dashboard + exports)."""
from django.urls import path

from . import views

app_name = "bonus"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("export/demandes.csv", views.export_demandes_csv, name="export_demandes_csv"),
    path("export/materiels.csv", views.export_materiels_csv, name="export_materiels_csv"),
]
