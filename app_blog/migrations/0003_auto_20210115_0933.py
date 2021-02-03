# Generated by Django 2.2 on 2021-01-15 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0002_blog_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='files/', verbose_name='изображения')),
            ],
        ),
        migrations.AlterField(
            model_name='blog',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_blog.Files'),
        ),
    ]
