from rest_framework import viewsets, permissions
from apps.core.models import TimeStampedModel

class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter()  # Puedes filtrar por usuario aquí