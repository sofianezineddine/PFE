# Generated by Django 5.0.6 on 2024-05-30 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0014_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image'),
        ),
    ]
