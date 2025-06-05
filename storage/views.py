from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from storage.models import File
from .UploadSerializer import FileUploadSerializer, FileSerializer
from django.db.models import Q 

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username","password")
        extra_kwargs = {"password": {"write_only": True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
    )
        return user

class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
class FileUploadView(generics.CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class FileListView(generics.ListAPIView):
    serializer_class = FileUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return File.objects.filter(owner=self.request.user)
    
class FileListView(generics.ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(
            Q(owner=user) |
            Q(access_level="public") |
            Q(shared_with=user)
        ).distinct()
    