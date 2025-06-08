from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from storage.models import File
from .UploadSerializer import FileUploadSerializer, FileSerializer
from .share_serializer import FileShareSerializer
from django.db.models import Q 
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .utils.virus_scan import scan_file_for_virus
from rest_framework.exceptions import ValidationError
from django.core.files.storage import default_storage
from .permissions import IsOwnerSharedOrPublic

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
    
    def perform_create(self, serializer):
        file = self.request.FILES["file"]
        # Save temp to scan
        temp_path = f"/tmp/{file.name}"
        with open (temp_path, "wb+") as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)     
        # Scan file
        scan_result = scan_file_for_virus(temp_path)
        if scan_result:
            raise ValidationError("File upload rejected due to virus detection!")
        
        serializer.save(owner=self.request.user)

    
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
        
class FileDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, reuqest, file_id):
        user = reuqest.user
        file = get_object_or_404(File, id = file_id)
        
        if file.owner == user or file.access_level == "public" or user in file.shared_with.all():
            response = FileResponse(file.file.open("rb"), as_attachment=True, filename=file.file.name)
            return response
        else:
            return Response({"detail": "You do not have permission to access this file."}, status=status.HTTP_403_FORBIDDEN)
        
        
class ShareFileView(generics.GenericAPIView):
    serializer_class = FileShareSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs ):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data["file"]
        username = serializer.validated_data["share_with_username"]
        
        from django.contrib.auth.models import User
        try:
            recipient_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        file.shared_with.add(recipient_user)
        file.save()
        
        return Response({"message": f'File shared with {recipient_user.username} successfully!'}, status=status.HTTP_200_OK)