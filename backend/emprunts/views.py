from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from .models import Demande, Restitution
from .serializers import DemandeSerializer, RestitutionSerializer


class DemandeViewSet(viewsets.ModelViewSet):
    """
    Endpoints emprunts :
      - GET    /api/demandes/        : liste les demandes (filtrées selon le rôle)
      - POST   /api/demandes/        : crée une demande (étudiant)
      - POST   /api/demandes/{id}/valider/  : approuve (admin)
      - POST   /api/demandes/{id}/refuser/  : refuse  (admin)
      - POST   /api/demandes/{id}/annuler/  : annule  (étudiant ou admin)
    """
    serializer_class = DemandeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Demande.objects.select_related("utilisateur", "emplacement").prefetch_related("lignes")
        # Un utilisateur normal ne voit que ses propres demandes
        if not (user.is_staff or getattr(user, "role", "") in {"ADMINISTRATEUR", "TECHNICIEN"}):
            qs = qs.filter(utilisateur=user)
        return qs

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def valider(self, request, pk=None):
        demande = self.get_object()
        try:
            demande.valider(par_utilisateur=request.user)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(demande).data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def refuser(self, request, pk=None):
        demande = self.get_object()
        motif = request.data.get("motif", "")
        try:
            demande.refuser(par_utilisateur=request.user, motif=motif)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(demande).data)

    @action(detail=True, methods=["post"])
    def annuler(self, request, pk=None):
        demande = self.get_object()
        if demande.utilisateur != request.user and not request.user.is_staff:
            return Response({"detail": "Permission refusée."}, status=status.HTTP_403_FORBIDDEN)
        try:
            demande.annuler()
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(demande).data)


class RestitutionViewSet(viewsets.ModelViewSet):
    queryset = Restitution.objects.all()
    serializer_class = RestitutionSerializer
    permission_classes = [permissions.IsAuthenticated]
