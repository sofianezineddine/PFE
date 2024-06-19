# Generated by Django 5.0.4 on 2024-05-11 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_alter_admin_aid_alter_cartorder_sku_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tags',
        ),
        migrations.AlterField(
            model_name='admin',
            name='aid',
            field=models.CharField(default='admLwrwLwuwqwFwiwDwXw2wkwnwSwZwmwPwXwAwBw3', max_length=50),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='sku',
            field=models.CharField(default='SKUEocoNoNo4oKoHoGoOozovo7oWoToyopovor', max_length=30),
        ),
        migrations.AlterField(
            model_name='category',
            name='cid',
            field=models.CharField(default='catNAvAYABAdAqAEAwAQALABA7ALAuA7AlAOAOAxAO', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=models.CharField(default='proIyjyYymyKyCydyvylyrynyjyuy4y9yly0ySybyR', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(default='skuco8ocoxoFosoDo0oNo7oIoJowoko0o4ojo4', max_length=30),
        ),
    ]
