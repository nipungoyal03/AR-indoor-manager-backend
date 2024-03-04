from rest_framework import serializers
from main.models import UploadedModel
from rest_framework import serializers


class UploadedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedModel
        fields = ("model_file",)
