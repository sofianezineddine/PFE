# Generated by Django 5.0.6 on 2024-05-18 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0004_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='verified',
        ),
    ]
