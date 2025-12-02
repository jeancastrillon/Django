from rest_framework import serializers
from apps.gestion.models import Cliente, Proyecto, PlantillaFormulario, Ticket

# Cliente
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

# Proyecto
class ProyectoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)

    class Meta:
        model = Proyecto
        fields = '__all__'

# PlantillaFormulario
class PlantillaFormularioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantillaFormulario
        fields = '__all__'

# Ticket
class TicketSerializer(serializers.ModelSerializer):
    plantilla = PlantillaFormularioSerializer(read_only=True)
    proyecto = ProyectoSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'