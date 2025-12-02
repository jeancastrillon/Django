
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import uuid

User = settings.AUTH_USER_MODEL

def generar_codigo_cliente():
    from django.db.models import Max
    from django.db import transaction

    with transaction.atomic():
        ultimo = Cliente.objects.aggregate(Max('id'))['id__max']
        if ultimo is None:
            return "CLI-0001"
        return f"CLI-{int(ultimo) + 1:04d}"

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    codigo = models.CharField(max_length=50, unique=True, editable=False, default=generar_codigo_cliente)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-id']

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def __str__(self):
        return f"{self.codigo} - {self.nombre_completo()}"


class Proyecto(models.Model):
    nombre_proyecto = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_proyecto

class PlantillaFormulario(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    campos_json = models.JSONField(default=dict)  # ejemplo: {"nombre": "text", "problema": "textarea"}

class Ticket(models.Model):
    ESTADOS = [('nuevo','Nuevo'), ('en_proceso','En proceso'), ('resuelto','Resuelto')]
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    datos_formulario = models.JSONField(default=dict)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='nuevo')
    creado_el = models.DateTimeField(auto_now_add=True)