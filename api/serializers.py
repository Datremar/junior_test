from rest_framework import serializers
from .models import Task, Deal


class FileSerializer(serializers.Serializer):
    file = serializers.FileField()


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = '__all__'
