import io
import tempfile
from django.contrib.auth.models import User
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from storage.models import File, PublicShareLink
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
import os
from rest_framework.test import APITestCase, APIClient



@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class SecureStorageTests(APITestCase):
    def setUp(self):
        self.client = Client()
    
    # Main test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
    
    # Additional user to share files with
        self.other_user = User.objects.create_user(username='otheruser', password='otherpass')

    # JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    # Use APIClient with the token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        self.auth_header = {
        "HTTP_AUTHORIZATION": f"Bearer {self.access_token}"
    }


    def test_token_authentication(self):
        url = reverse('token_obtain_pair') 
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)

    def test_file_upload(self):
        file_content = b'Test file content'
        test_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")
        response = self.client.post(reverse('file-upload'), {'file': test_file}, **self.auth_header)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(File.objects.filter(owner=self.user).exists())

    def test_file_download(self):
        stored_file = File.objects.create(owner=self.user, file=SimpleUploadedFile("dl.txt", b"download me"))
        url = reverse('file-download', args=[stored_file.id])
        response = self.client.get(url, **self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b"".join(response.streaming_content), b"download me")


    def test_file_share_link_creation(self):
        stored_file = File.objects.create(owner=self.user,file=SimpleUploadedFile("testfile.txt", b"test content"),access_level="private")
        url = reverse("generate-public-link", kwargs={"file_id": stored_file.id})
        data = {"expires_in_minutes": 2 }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("share_link", response.data)


    def test_access_logging_middleware(self):
        other_user = User.objects.create_user(username="hacker", password="hackerpass")
        stored_file = File.objects.create(
        owner=other_user,file=SimpleUploadedFile("secret.txt", b"secret content"),access_level="private")
        url = reverse("file-download", kwargs={"file_id": stored_file.id})
        response = self.client.get(url)

    def test_expired_public_link(self):
        file = File.objects.create(owner=self.user, file=SimpleUploadedFile("exp.txt", b"expire test"))
        expired_link = PublicShareLink.objects.create(file=file, expires_at=timezone.now() - timezone.timedelta(minutes=1))
        url = reverse('public-file.download', args=[expired_link.token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        

    def tearDown(self):
        for f in File.objects.all():
            if f.file:
                try:
                    os.remove(f.file.path)
                except Exception:
                    pass
