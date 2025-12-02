from rest_framework import serializers
from .models import Cliente, Proyecto, PlantillaFormulario, Ticket


# ================== CLIENTE ==================
class ClienteSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.CharField()

    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'apellido', 'email', 'codigo', 'estado', 'created_at', 'updated_at', 'nombre_completo']
        
        def get_nombre_completo(self, obj):
            return f"{obj.nombre} {obj.apellido}"

# ================== PROYECTO PÚBLICO ==================
class PublicProyectoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)

    class Meta:
        model = Proyecto
        fields = ['id', 'nombre_proyecto', 'descripcion', 'cliente']


# ================== PROYECTO PARA STAFF (CRUD) ==================
class ProyectoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    cliente_id = serializers.IntegerField(write_only=True, required=True)
    cliente_nombre = serializers.CharField(source='cliente.nombre_completo', read_only=True)

    class Meta:
        model = Proyecto
        fields = [
            'id',
            'nombre_proyecto',      # ← CORRECTO
            'descripcion',
            'activo',
            'cliente',
            'cliente_id',
            'cliente_nombre'
        ]
        read_only_fields = ['cliente_nombre']


# ================== TICKET ==================
class TicketCreateSerializer(serializers.ModelSerializer):
    proyecto_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ticket
        fields = ['proyecto_id', 'titulo', 'descripcion', 'datos_formulario']