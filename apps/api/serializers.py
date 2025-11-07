from rest_framework import serializers
from apps.core.models import TimeStampedModel

class BaseModelSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TimeStampedModel
        fields = '__all__'
        abstract = True