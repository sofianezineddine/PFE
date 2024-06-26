# Generated by Django 5.0.4 on 2024-05-11 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_alter_admin_aid_alter_cartorder_sku_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.CharField(default='lotion,cream,product', max_length=100),
        ),
        migrations.AlterField(
            model_name='admin',
            name='aid',
            field=models.CharField(default='admkw5wpwpw3wCwFw2wtwOwRwewjwEwOwYwDwQw7wI', max_length=50),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='sku',
            field=models.CharField(default='SKUqJsJ4JjJ2JiJcJfJpJMJ2JSJYJTJxJAJmJ7', max_length=30),
        ),
        migrations.AlterField(
            model_name='category',
            name='cid',
            field=models.CharField(default='catLTUTITXTFTtTCTiTtTCTBTUTaTJTMTMT8TRTNTF', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=models.CharField(default='proVPOPwPgPDPLPrPSPTPfPrPIPVPZPhPuPmPYPFPl', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(default='skuuVIVZVoVBVpVEVIVsVrVBVeVNVvVxV3VGVH', max_length=30),
        ),
    ]
