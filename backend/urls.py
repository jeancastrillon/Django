"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from drf_spectacular.utils import extend_schema
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny


# JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Documentación
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
# Tus ViewSets internos
from apps.gestion.views import ClienteViewSet, ProyectoViewSet

# Vista personalizada para que aparezca en Swagger con nombre bonito
@extend_schema(
    tags=['auth'],
    summary="Obtener token de acceso",
    description="Introduce usuario y contraseña. Devuelve access y refresh token."
)
class TokenObtainPairViewWithDoc(TokenObtainPairView):
    pass

@extend_schema(
    tags=['auth'],
    summary="Refrescar token",
    description="Usa el refresh token para obtener un nuevo access token."
)
class TokenRefreshViewWithDoc(TokenRefreshView):
    pass

router_clientes = DefaultRouter()
router_clientes.register(r'clientes', ClienteViewSet, basename='cliente')

# Router SOLO para proyectos
router_proyectos = DefaultRouter()
router_proyectos.register(r'proyectos', ProyectoViewSet, basename='proyecto')

urlpatterns = [
    # TOKEN CON DESPLEGABLE BONITO
    path('api/token/', TokenObtainPairViewWithDoc.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshViewWithDoc.as_view(), name='token_refresh'),

    path('api/public/', include('apps.gestion.urls')),

    # AQUÍ LA MAGIA: dos rutas separadas → dos grupos en Swagger
    path('api/', include('apps.gestion.urls')),
    path('api/', include(router_clientes.urls)),
    path('api/', include(router_proyectos.urls)),

    # Documentación
    path('api/schema/', SpectacularAPIView.as_view(permission_classes=[AllowAny]), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]