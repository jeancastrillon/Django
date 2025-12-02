from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.gestion.models import Cliente, Proyecto, PlantillaFormulario, Ticket
from .serializers import (
    ClienteSerializer, ProyectoSerializer,
    PlantillaFormularioSerializer, TicketSerializer
)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('-id')
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Cliente.objects.all()
        email = self.request.query_params.get('email')  
        if email:
            queryset = queryset.filter(email__icontains=email)
        return queryset.order_by('-created_at')


class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.select_related('cliente').all()
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Proyecto.objects.select_related('cliente').all()
        cliente_id = self.request.query_params.get('cliente')
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        return queryset

class PlantillaFormularioViewSet(viewsets.ModelViewSet):
    queryset = PlantillaFormulario.objects.all()
    serializer_class = PlantillaFormularioSerializer
    permission_classes = [IsAuthenticated]

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]