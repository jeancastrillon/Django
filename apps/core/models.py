from django.db import models

class PruebaCore(models.Model):
    nombre = models.CharField(max_length=100)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Prueba Core"
        verbose_name_plural = "Pruebas Core"
