# apps/users/models.py
from django.contrib.auth.models import AbstractUser  
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Correo")
    rol = models.CharField(
        max_length=50,
        choices=[
            ('admin', 'Administrador'),
            ('soporte', 'Soporte'),
            ('cliente', 'Cliente')
        ],
        default='cliente'
    )
    ultimo_acceso = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def save(self, *args, **kwargs):
        if self.pk:
            self.ultimo_acceso = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

# Create your models here.
