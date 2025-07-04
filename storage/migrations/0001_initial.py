# Generated by Django 5.2.1 on 2025-06-04 21:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="File",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="user_files/")),
                ("title", models.CharField(blank=True, max_length=255)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "access_level",
                    models.CharField(
                        choices=[
                            ("private", "Private"),
                            ("public", "Public"),
                            ("shared", "Shared"),
                        ],
                        default="private",
                        max_length=10,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "shared_with",
                    models.ManyToManyField(
                        blank=True,
                        related_name="shared_files",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
