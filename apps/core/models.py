from django.db import models


class TimeStampedModel(models.Model):
    """
    Modelo abstracto que agrega created_at y updated_at a cualquier modelo que lo herede.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']