from django.urls import path
from .views import RegisterUserAPIView, FileUploadView, FileListView

urlpatterns = [
    
    path("register/", RegisterUserAPIView.as_view(), name="register"),
    path("upload/", FileUploadView.as_view(), name="file-upload"),
    path("files/", FileListView.as_view(), name="file-list")
]
