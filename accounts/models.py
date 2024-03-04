from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.manager import UserManager
import uuid


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.email
