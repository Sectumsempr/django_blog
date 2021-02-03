# Generated by Django 2.2 on 2021-01-14 13:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.TextField(blank=True, null=True, verbose_name='О себе')),
                ('user', models.OneToOneField(on_delete=True, to=settings.AUTH_USER_MODEL, verbose_name='Ник')),
            ],
            options={
                'verbose_name': 'профиль',
                'verbose_name_plural': 'профили',
            },
        ),
    ]
