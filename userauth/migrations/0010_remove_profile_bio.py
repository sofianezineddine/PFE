# Generated by Django 5.0.6 on 2024-05-24 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0009_alter_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
    ]
