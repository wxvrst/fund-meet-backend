from django.contrib.auth.models import AbstractUser
from django.db import models

class UserModel(AbstractUser):
    avatar = models.ImageField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.username


