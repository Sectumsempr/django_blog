from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=True, verbose_name='Ник')
    about = models.TextField(null=True, blank=True, verbose_name='О себе')
    photo = models.FileField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватарка')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
