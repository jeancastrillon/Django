from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'  # ← IMPORTANTE
    label = 'core'      # ← Esto hace que Django lo reconozca