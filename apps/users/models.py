# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models  # Add this import
from django.contrib.auth import get_user_model

class User(AbstractUser):
    is_active = models.BooleanField(default=True)  # Add this line if not already present

class UserPreferences(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    # Match Preferences
    age_range_min = models.IntegerField(default=18)
    age_range_max = models.IntegerField(default=50)
    distance_range = models.IntegerField(default=50)
    gender_preference = models.CharField(max_length=50, default="All")
    interests = models.TextField(default="", blank=True)

    # Privacy Settings
    profile_visibility = models.BooleanField(default=True)
    location_sharing = models.BooleanField(default=True)
    block_list = models.TextField(default="", blank=True)  # Usernames or IDs of blocked users

    # Notification Settings
    new_match_notifications = models.BooleanField(default=True)
    message_notifications = models.BooleanField(default=True)
    app_updates_notifications = models.BooleanField(default=True)

    # Account Settings
    email_preferences = models.CharField(max_length=50, default="All")
    language_preference = models.CharField(max_length=50, default="English")
    account_deactivation = models.BooleanField(default=False)

    # Interface Customization
    theme = models.CharField(max_length=50, default="Light")  # Options like 'Light', 'Dark'
    accessibility_settings = models.CharField(max_length=200, default="Default")

    def __str__(self):
        return f"{self.user.username}'s preferences"