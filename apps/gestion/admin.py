from django.contrib import admin
from .models import Cliente, Proyecto, PlantillaFormulario, Ticket

# Registro simple y limpio de todos los modelos
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'estado')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('estado',)

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre_proyecto', 'cliente', 'activo')
    search_fields = ('nombre_proyecto', 'cliente__nombre', 'cliente__apellido')
    list_filter = ('activo',)

@admin.register(PlantillaFormulario)
class PlantillaFormularioAdmin(admin.ModelAdmin):
    list_display = ('proyecto',)
    # Puedes ver el JSON en detalle si quieres, pero así está bien

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'proyecto', 'estado', 'creado_el')
    list_filter = ('estado', 'creado_el')
    search_fields = ('titulo', 'proyecto__nombre_proyecto')
    readonly_fields = ('creado_el',)