from django.contrib.auth.models import AbstractUser
from apps.core.models import TimeStampedModel
from django.db import models
from apps.users.managers import UserManager

class User(models.Model):
    email = None
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=150, unique=True)  # Necesario
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        abstract = True  # ← IMPORTANTE: misma tabla
