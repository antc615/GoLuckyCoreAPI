# Generated by Django 5.0.1 on 2024-01-18 22:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_userpreferences"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
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
                (
                    "profile_picture",
                    models.CharField(
                        default="../assets/default_profile.jpg", max_length=255
                    ),
                ),
                ("additional_images", models.JSONField(blank=True, default=list)),
                ("biography", models.TextField(blank=True, null=True)),
                ("age", models.IntegerField(blank=True, null=True)),
                ("location", models.CharField(blank=True, max_length=255, null=True)),
                ("hobbies", models.TextField(blank=True, null=True)),
                ("education", models.CharField(blank=True, max_length=255, null=True)),
                ("occupation", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "relationship_status",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("height", models.CharField(blank=True, max_length=50, null=True)),
                ("looking_for", models.TextField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
