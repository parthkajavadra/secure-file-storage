from django.urls import path
from .views import RegisterUserAPIView, FileUploadView, AccessibleFileListView, FileDownloadView, ShareFileView,GeneratePublicLinkView,PublicFileDownloadView

urlpatterns = [
    
    path("register/", RegisterUserAPIView.as_view(), name="register"),
    path("upload/", FileUploadView.as_view(), name="file-upload"),
    path("files/", AccessibleFileListView.as_view(), name="file-list"),
    path("download/<int:file_id>/", FileDownloadView.as_view(), name="file-download"),
    path("share/",ShareFileView.as_view(),name="share-file"),
    path("share/<int:file_id>/", GeneratePublicLinkView.as_view(), name="generate-public-link"),
    path("public/<uuid:token>/", PublicFileDownloadView.as_view(), name="public-file.download"),

]