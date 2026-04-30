from rest_framework import viewsets, permissions
from .models import Utilisateur
from .serializers import UtilisateurSerializer


class UtilisateurViewSet(viewsets.ModelViewSet):
    """API CRUD utilisateurs — réservée aux admins sauf /me."""
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

    def get_permissions(self):
        if self.action in {"list", "create", "destroy"}:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
