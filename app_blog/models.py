from django.contrib.auth.models import User
from django.db import models


class Blog(models.Model):
    topic = models.CharField(max_length=100, verbose_name='заголовок')
    description = models.TextField(verbose_name='описание')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic


class Files(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/', verbose_name='изображения', null=True, blank=True)
