from rest_framework import serializers
from .models import File

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["id", "file", "title", "owner", "uploaded_at",'access_level']
        read_only_fields = ["id", "owner", "uploaded_at"]
        
    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)