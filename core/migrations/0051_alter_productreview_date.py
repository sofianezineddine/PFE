# Generated by Django 5.0.6 on 2024-05-12 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_alter_productreview_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
