# Generated by Django 5.0.6 on 2024-05-24 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_remove_address_mobile_address_country_address_cp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
