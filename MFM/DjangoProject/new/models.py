
from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female")])
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)  # Hashed password

    def __str__(self):
        return self.username
