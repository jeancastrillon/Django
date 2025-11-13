from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL  

class Cliente(models.Model):
    """
    Representa a un cliente externo que solicita servicios o reporta incidencias.
    
    Atributos:
        nombre (str): Nombre del cliente.
        apellido (str): Apellido del cliente.
        email (EmailField): Correo electrónico (único) usado para login y notificaciones.
        estado (str): Estado actual del cliente: 'activo' o 'inactivo'.
        fecha_registro (DateTime): Fecha y hora de registro automático.
    """
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    email = models.EmailField(unique=True)  
    estado = models.CharField(
        max_length=20,
        choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')],
        default='activo'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name_plural = "Clientes"


class Proyecto(models.Model):
    """
    Proyecto asociado a un cliente. Este contiene formulario, ANS y tickets.
    
    Atributos:
        nombre_proyecto (str): Nombre descriptivo del proyecto.
        cliente (Cliente): Cliente propietario del proyecto.
        estado (str): Estado del proyecto: en progreso, completado, cancelado.
        plantilla_formulario (PlantillaFormulario): Formulario asociado. relacion:(1:1).
        ans (ANS): Acuerdo de nivel de servicio. Relacion:(1:1).
    """
    proyecto_id = models.AutoField(primary_key=True)
    nombre_proyecto = models.CharField(max_length=200)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='proyectos')
    
    
    estado = models.CharField(
        max_length=20,
        choices=[
            ('en_progreso', 'En Progreso'),
            ('completado', 'Completado'),
            ('cancelado', 'Cancelado')
        ],
        default='en_progreso'
    )

    
    plantilla_formulario = models.OneToOneField(
        'PlantillaFormulario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='proyecto_relacionado'
    )
    ans = models.OneToOneField(
        'ANS',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='proyecto_ans'
    )

    def __str__(self):
        return self.nombre_proyecto

    class Meta:
        verbose_name_plural = "Proyectos"




class PlantillaFormulario(models.Model):
    """
    Plantilla de formulario para crear tickets. Define campos y validaciones.
    
    Atributos:
        nombre_plantilla (str): Nombre descriptivo de la plantilla.
        proyecto (Proyecto): Proyecto al que pertenece. Relacion: (1:1).
        campo_formulario (JSON): Estructura de campos en formato JSON.
        activo (bool): Indica si la plantilla está activa.
    """
    formulario_id = models.AutoField(primary_key=True)
    proyecto = models.OneToOneField(
        'Proyecto',
        on_delete=models.CASCADE,
        related_name='plantilla_relacionada' 
    )
    
    nombre_plantilla = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    
    campo_formulario = models.JSONField(
        default=list,
        help_text="Ej: [{'nombre': 'urgencia', 'tipo': 'select', 'opciones': ['Alta', 'Media']}]"
    )

    def __str__(self):
        return f"{self.nombre_plantilla} - {self.proyecto}"

    class Meta:
        verbose_name_plural = "Plantillas de Formulario"
        

class CampoFormulario(models.Model):
    """
    Campo dentro de una plantilla de formulario.
    
    Atributos:
        plantilla (PlantillaFormulario): Plantilla principal.
        nombre (str): Nombre del campo (ej: 'urgencia').
        tipo (str): Tipo de campo como: text, select, checkbox, etc.
        requerido (bool): Si el campo es obligatorio.
        opciones (JSON): Opciones para campos tipo select.
    """
    plantilla = models.ForeignKey(
        PlantillaFormulario,
        on_delete=models.CASCADE,
        related_name='campos_detalle'
    )
    nombre = models.CharField(max_length=200)
    etiqueta = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=[
        ('texto', 'Texto Corto'),
        ('textarea', 'Texto Largo'),
        ('numero', 'Número'),
        ('fecha', 'Fecha'),
        ('seleccion', 'Selección'),
        ('checkbox', 'Casilla'),
        ('radio', 'Radio'),
        ('archivo', 'Archivo'),
    ])
    requerido = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)
    opciones = models.JSONField(blank=True, null=True)


    def __str__(self):
        return self.etiqueta

    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Campos de Formulario"


class Ticket(models.Model):
    """
    Ticket creado desde formulario. Contiene datos estructurados y seguimiento.
    
    Atributos:
        ticket_id (str): ID único del ticket.
        titulo (str): Título descriptivo.
        proyecto : Proyecto al que pertenece.
        plantilla :PlantillaFormulario (Plantilla usada).
        datos (JSON): Datos del formulario rellenado.
        estado (str): Estado del ticket como: nuevo, en_proceso, resuelto, cerrado.
        prioridad (str): nivel de prioridad: baja, media, alta, crítica.
        asignado_a (User): persona interna asignado.
        creado_por (User): Quién creó el ticket.
        funciones (ManyToMany): Funciones de creacion.
        fecha_creacion (DateTime): Fecha de creación.
        fecha_cierre (DateTime): Fecha de cierre.
    """
    ticket_id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=300)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=20, choices=[
        ('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')
    ])
    estado = models.CharField(max_length=20, choices=[
        ('abierto', 'Abierto'),
        ('en_proceso', 'En Proceso'),
        ('resuelto', 'Resuelto')
    ], default='abierto')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    tiempo_resolucion = models.DurationField(null=True, blank=True)

    
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tickets')
    plantilla = models.ForeignKey(
        PlantillaFormulario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets'
    )
    creado_por = models.ForeignKey(
        'users_app.User',
        on_delete=models.CASCADE,
        related_name='tickets_creados'
    )
    asignado_a = models.ForeignKey(
        'users_app.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets_asignados'
    )
    funciones = models.ManyToManyField('Funcion', related_name='tickets', blank=True)

    
    datos_formulario = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"#{self.ticket_id} - {self.titulo}"


class Funcion(models.Model):
    """
    Tiene multiplesfunciones, entre ellas notificar al cliente.
    
    Atributos:
        nombre (str): Nombre de la función.
        tipo (str): Tipo: frontend, backend, base de datos, etc.
        estado (str): Estado actual de la función.
    """
    funcion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=50)
    ultima_ejecucion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[
        ('activo', 'Activo'), ('inactivo', 'Inactivo')
    ], default='activo')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Funciones"


class ANS(models.Model):
    """
    Acuerdo de Nivel de Servicio (ANS/SLA).
    
    Atributos:
        nombre_ans (str): Nombre del ANS.
        tiempo_respuesta_max (int): Horas máximas para primera respuesta.
        tiempo_resolucion_max (int): Horas máximas para resolución.
        personalizacion (Text): Detalles personalizados.
        fecha_vigencia (Date): Fecha de vigencia.
        estado (str): Activo o inactivo.
        horario_atencion (JSON): Horarios de atención por día.
    """
    # Django crea 'id' automáticamente, no se necesita ans_id
    nombre_ans = models.CharField(max_length=200)
    tiempo_respuesta_max = models.PositiveIntegerField()
    tiempo_resolucion_max = models.PositiveIntegerField()
    personalizacion = models.TextField(blank=True)
    fecha_vigencia = models.DateField()
    estado = models.CharField(max_length=20, choices=[
        ('activo', 'Activo'), ('inactivo', 'Inactivo')
    ])
    horario_atencion = models.JSONField(
        default=dict,
        help_text="Ej: {'lunes': ['09:00-18:00']}"
    )

    def __str__(self):
        return self.nombre_ans

    class Meta:
        verbose_name_plural = "ANS"


