from rest_framework import serializers
from django.contrib.auth.models import User
from storage.models import File

class FileShareSerializer(serializers.Serializer):
    file_id = serializers.IntegerField()
    share_with_username = serializers.CharField()
    
    def validate(self, data):
        try:
            file = File.objects.get(id=data["file_id"])
        except File.DoesNotExist:
            raise serializers.ValidationError("File not found")
        try:
            shared_user = User.objects.get(username=data["share_with_username"])
        except User.DoesNotExist:
            raise serializers.ValidationError({"share_with_errors": ["User to share with not found"]})
        
        request_user = self.context["request"].user
        if file.owner != request_user:
            raise serializers.ValidationError({"permission denied": ["You do not have permission to share this file"]})
        data["file"] = file
        data["shared_user"] = shared_user
        return data
    
    def save(self):
        file = self.validated_data["file"]
        shared_user = self.validated_data["shared_user"]
        file.shared_with.add(shared_user)