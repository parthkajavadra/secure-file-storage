from rest_framework import serializers
from .models import File
import pyclbr
from django.core.exceptions import ValidationError

MAX_FILE_SIZE = 2 * 1024 * 1024
ALLOWED_CONTENT_TYPES = [
    "application/pdf",
    "image/jpeg",
    "image/png",
    "text/plain",
]
class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ["id", "owner", "uploaded_at"]
        
        
    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

    def validate_file(self, uploaded_file):
        if uploaded_file.size > MAX_FILE_SIZE:
            raise ValidationError("File is too large (max 02 MB).")
        if uploaded_file.content_type not in ALLOWED_CONTENT_TYPES:
            raise ValidationError(f"Unsupported file type: {uploaded_file.content_type}")
        return uploaded_file
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        