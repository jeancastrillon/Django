from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()


try:
    from .views import ProyectoPublicoViewSet, TicketPublicoViewSet
    router.register(r'public/proyectos', ProyectoPublicoViewSet, basename='proyecto-publico')
    router.register(r'public/tickets', TicketPublicoViewSet, basename='ticket-publico')
except ImportError:
    pass  

urlpatterns = [
    path('', include(router.urls)),
]