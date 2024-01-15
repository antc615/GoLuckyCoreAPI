from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass  # Extend the user model with additional fields if needed
