from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Categorie, Materiel, Maintenance
from .serializers import CategorieSerializer, MaterielSerializer, MaintenanceSerializer


class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [permissions.IsAuthenticated]


class MaterielViewSet(viewsets.ModelViewSet):
    """Catalogue du matériel : tout le monde authentifié peut lister, seuls les admins éditent."""
    queryset = Materiel.objects.select_related("categorie").all()
    serializer_class = MaterielSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["categorie", "etat"]
    search_fields = ["nom", "numero_serie", "description"]
    ordering_fields = ["nom", "date_acquisition", "quantite_disponible"]

    def get_permissions(self):
        if self.action in {"list", "retrieve"}:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.select_related("materiel").all()
    serializer_class = MaintenanceSerializer
    permission_classes = [permissions.IsAuthenticated]
