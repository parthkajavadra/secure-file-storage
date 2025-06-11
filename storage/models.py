import uuid
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    ACCESS_CHOICES = [
        ("private", "Private"),
        ("public","Public"),
        ("shared", "Shared"),
    ]
    
    file = models.FileField(upload_to="user_files/")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    title = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    access_level = models.CharField(max_length=10, choices=ACCESS_CHOICES, default="private")
    shared_with = models.ManyToManyField(User, related_name="shared_files", blank=True)
    
    def __str__(self):
        return self.title or self.file.name
    
    
class PublicShareLink(models.Model):
    file =  models.ForeignKey(File, on_delete=models.CASCADE, related_name="public_links")
    token = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__ (self):
        return f"Share Link for {self.file.name} (expires at {self.expires_at})"