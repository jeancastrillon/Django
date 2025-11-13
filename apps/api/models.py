from django.db import models

class PruebaAPI(models.Model):
    titulo = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Prueba API"
        verbose_name_plural = "Pruebas API"

# Create your models here.
