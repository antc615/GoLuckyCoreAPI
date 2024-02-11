# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
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
    block_list = models.TextField(default="", blank=True)

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
    
class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.CharField(max_length=255, default='../assets/default_profile.jpg')
    biography = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    relationship_status = models.CharField(max_length=50, blank=True, null=True)
    height = models.CharField(max_length=50, blank=True, null=True)
    looking_for = models.TextField(blank=True, null=True)    
    # Add the phone number field
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

# apps/users/models.py (or wherever your UserProfile model is located)
class Image(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_profile_picture = models.BooleanField(default=False)