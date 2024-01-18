# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models  # Add this import

class User(AbstractUser):
    is_active = models.BooleanField(default=True)  # Add this line if not already present

