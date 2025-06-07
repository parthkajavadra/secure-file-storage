from rest_framework import serializers
from .models import File
import pyclbr

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ["id", "owner", "uploaded_at"]
        
    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        