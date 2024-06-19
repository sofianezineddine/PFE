# Generated by Django 5.0.6 on 2024-05-31 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0074_delete_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('draft', 'Draft'), ('in_review', 'In Review'), ('published', 'Published')], default='in_review', max_length=10),
        ),
    ]
