# Generated by Django 5.0.6 on 2024-05-29 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0072_remove_cartorder_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='cp',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
