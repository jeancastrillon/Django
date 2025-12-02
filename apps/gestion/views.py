from rest_framework import viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import Cliente, Proyecto, PlantillaFormulario, Ticket
from .serializers import (
    PublicProyectoSerializer,
    TicketCreateSerializer,
    ClienteSerializer,
    ProyectoSerializer,     
)
from django.core.mail import send_mail
from django.conf import settings
from .permissions import IsStaffUser
from rest_framework.permissions import BasePermission
from drf_yasg.utils import swagger_auto_schema


# ==================== PERMISOS ====================


class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

# ==================== CRUD PRIVADO (solo staff) ====================
@extend_schema_view(
    list=extend_schema(tags=['Clientes'], description='Listar todos los clientes'),
    create=extend_schema(tags=['Clientes'], description='Crear nuevo cliente'),
    retrieve=extend_schema(tags=['Clientes'], description='Ver detalle de cliente'),
    update=extend_schema(tags=['Clientes'], description='Actualizar cliente'),
    partial_update=extend_schema(tags=['Clientes'], description='Actualizar parcialmente'),
    destroy=extend_schema(tags=['Clientes'], description='Eliminar cliente'),
)
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('-id')
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated & IsStaffUser]

@extend_schema_view(
    list=extend_schema(tags=['Proyectos'], description='Listar proyectos (staff)'),
    create=extend_schema(tags=['Proyectos'], description='Crear nuevo proyecto'),
    retrieve=extend_schema(tags=['Proyectos'], description='Detalle de proyecto'),
    update=extend_schema(tags=['Proyectos'], description='Actualizar proyecto'),
    partial_update=extend_schema(tags=['Proyectos'], description='Actualizar parcialmente'),
    destroy=extend_schema(tags=['Proyectos'], description='Eliminar proyecto'),
)


class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all().select_related('cliente').order_by('-id')
    serializer_class = ProyectoSerializer
    permission_classes = [IsStaffUser]
    
# ==================== API PÚBLICA (sin login) ====================
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre_proyecto', 'apellido', 'empresa', 'email', 'telefono']


class PublicProyectoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)

    class Meta:
        model = Proyecto
        fields = [
            'id',
            'nombre_proyecto',
            'descripcion',
            'activo',                    
            'cliente'                    
        ]
        read_only_fields = fields


class TicketCreateSerializer(serializers.ModelSerializer):
    proyecto_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ticket
        fields = ['proyecto_id', 'titulo', 'descripcion', 'datos_formulario']