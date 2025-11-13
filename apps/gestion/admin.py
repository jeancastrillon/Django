from django.contrib import admin
from .models import (
    Cliente,
    Proyecto,
    PlantillaFormulario,
    CampoFormulario,
    Ticket,
    Funcion,
    ANS
)


class CampoFormularioInline(admin.TabularInline):
    model = CampoFormulario
    extra = 1


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'estado')  
    search_fields = ('nombre', 'apellido', 'email')


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre_proyecto', 'cliente', 'estado')
    list_filter = ('estado',)  
    search_fields = ('nombre_proyecto',)


@admin.register(PlantillaFormulario)
class PlantillaFormularioAdmin(admin.ModelAdmin):
    list_display = ('nombre_plantilla', 'proyecto', 'activo')
    list_filter = ('activo',)
    inlines = [CampoFormularioInline]
    search_fields = ('nombre_plantilla',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'titulo', 'proyecto', 'estado')
    list_filter = ('estado', 'prioridad')
    search_fields = ('titulo', 'ticket_id')


@admin.register(Funcion)
class FuncionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'estado')
    list_filter = ('estado',)


@admin.register(ANS)
class ANSAdmin(admin.ModelAdmin):
    list_display = ('nombre_ans', 'tiempo_respuesta_max', 'tiempo_resolucion_max')
    search_fields = ('nombre_ans',)


# Register your models here.
