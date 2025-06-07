from django.urls import path
from .views import RegisterUserAPIView, FileUploadView, FileListView, FileDownloadView, ShareFileView

urlpatterns = [
    
    path("register/", RegisterUserAPIView.as_view(), name="register"),
    path("upload/", FileUploadView.as_view(), name="file-upload"),
    path("files/", FileListView.as_view(), name="file-list"),
    path("download/<int:file_id>/", FileDownloadView.as_view(), name="file-download"),
    path("share/",ShareFileView.as_view(),name="share-file"),

]