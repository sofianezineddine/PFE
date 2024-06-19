# Generated by Django 5.0.4 on 2024-05-10 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_alter_admin_aid_alter_cartorder_sku_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='aid',
            field=models.CharField(default='admnbAbubDbLbebebcbybUbCbYb3bbb1bDbzbFb3bZ', max_length=50),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='sku',
            field=models.CharField(default='SKUzGzGKG1GTGGGZGqGRGFGBGTGPGYGAGKGZGh', max_length=30),
        ),
        migrations.AlterField(
            model_name='category',
            name='cid',
            field=models.CharField(default='catnzpzDzNzQzKzHznz1zNzfz0zWzPzZzazNzaznzf', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=models.CharField(default='procOPOBO0OKOBONOrOdOjOTOfOmOZOKOAOAOiOZOn', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(default='skuXdudBd3d5d8dUdOd7didAdadBdAd1dNdFdr', max_length=30),
        ),
    ]
