# Generated by Django 5.1.7 on 2025-03-25 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
    ]
