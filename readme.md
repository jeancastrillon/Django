# Proyecto Django (backend)

Resumen
- Proyecto Django con app principal `backend` y apps locales en `apps/` (ej. `users`, `api`, `core`).
- Endpoints públicos disponibles:
  - /admin/ — panel de administración de Django
  - /api/ — raíz del router (DefaultRouter). Actualmente el router está vacío si no hay viewsets registrados.
  - /swagger/ — documentación Swagger (drf_yasg)
  - /redoc/ — documentación Redoc (drf_yasg)

Requisitos
- Python 3.10+ (o la versión usada por el proyecto)
- pip
- Virtualenv (recomendado)
- PostgreSQL (recomendado según settings) o SQLite si está configurado

Instalación (Windows, PowerShell)
1. Clonar repo y entrar al directorio
   ```powershell
   git clone <repo-url>
   cd "c:\Users\USUARIO\Desktop\Django"
   ```

2. Crear y activar virtualenv
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```

3. Instalar dependencias
   ```powershell
   pip install -r requirements.txt
   ```

Configuración de base de datos
- El proyecto usa la configuración en `backend/settings.py`. Si está apuntando a PostgreSQL, cree la BD y el usuario:
  ```powershell
  # usando psql (ajusta nombres)
  psql -U postgres -c "CREATE DATABASE mydb;"
  psql -U postgres -c "CREATE USER myuser WITH PASSWORD 'mypass';"
  psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;"
  ```
- Alternativa rápida de desarrollo: usar `db.sqlite3` si está presente o ajustar `DATABASES` para sqlite.

Migraciones y superusuario
```powershell
# desde la raíz del proyecto
python manage.py migrate
python manage.py createsuperuser
```

Ejecutar servidor (desarrollo)
```powershell
python manage.py runserver
# abrir en navegador:
# http://127.0.0.1:8000/admin/
# http://127.0.0.1:8000/api/
# http://127.0.0.1:8000/swagger/
# http://127.0.0.1:8000/redoc/
```

Registrar endpoints en /api/
- El router está en `apps/api/urls.py`. Para exponer recursos registra viewsets en el router. Ejemplo:
```python
// filepath: c:\Users\USUARIO\Desktop\Django\apps\api\urls.py
# ...existing code...
from rest_framework.routers import DefaultRouter
from apps.api.viewsets import UserViewSet  # ejemplo: importa tu ViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
# ...existing code...
```

Tests
```powershell
python manage.py test
```

Comandos útiles
- Ver tablas en SQLite:
  ```powershell
  sqlite3 db.sqlite3 ".tables"
  ```
- Mostrar URLs (necesita django-extensions):
  ```powershell
  pip install django-extensions
  # añadir 'django_extensions' a INSTALLED_APPS
  python manage.py show_urls
  ```

Solución al error "no existe la relación «django_session»"
- Causa: la tabla `django_session` no existe. Solución típica:
  1. Asegúrate de que `DATABASES` en `backend/settings.py` apunta a la BD correcta.
  2. Ejecuta migraciones:
     ```powershell
     python manage.py migrate
     ```
  3. Verifica que `django.contrib.sessions` está en `INSTALLED_APPS`.
  4. Si usas PostgreSQL, confirma que la BD que estás migrando es la misma que se usa al iniciar el servidor (credenciales/host/port).

Estructura relevante del proyecto
- backend/ (settings, urls, wsgi/asgi)
- apps/
  - api/ (router, viewsets, serializers)
  - users/ (User model personalizado, AppConfig con label `my_users`)
  - core/ (modelos base)
- manage.py
- db.sqlite3 (posible archivo local)
- requirements.txt

Contribuir
- Abrir issue → crear branch → PR
- Ejecutar linters/tests antes de enviar PR

Licencia
- Añade la licencia que corresponda (ej. MIT) en LICENSE.md

Contacto / Ayuda
- Si necesitas que genere el README con más detalle (secciones adicionales, badges, ejemplo de env file), indícame y lo actualizo.