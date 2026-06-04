from django.contrib.auth.models import AbstractUser
from django.db import models

class UserModel(AbstractUser):
    avatar = models.ImageField(
        null=True,
        blank=True,
    )

    following = models.ManyToManyField(
        'self',
        related_name='followers',
        blank=True,
        symmetrical=False,
        default=0,
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
