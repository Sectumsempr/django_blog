from django.contrib import admin
from .models import Blog, Files


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    model = Blog
    list_display = ['id', 'topic', 'created_at', 'author']


@admin.register(Files)
class BlogAdmin(admin.ModelAdmin):
    model = Blog
    list_display = ['id', 'file', 'blog']
