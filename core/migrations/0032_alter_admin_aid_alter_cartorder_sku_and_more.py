# Generated by Django 5.0.4 on 2024-05-10 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_alter_admin_aid_alter_cartorder_sku_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='aid',
            field=models.CharField(default='admwmxmGm3mTmgmXm9mBm6mqmZmsmYmRmFmLmUm4mK', max_length=50),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='sku',
            field=models.CharField(default='SKUBVrVhV8VbVtVQVXVIVFV1VOVHVRV1VrVXVF', max_length=30),
        ),
        migrations.AlterField(
            model_name='category',
            name='cid',
            field=models.CharField(default='catPG4GzGYGCGYGdGrGBGUGPG7GKGUGhGmG3G7GlG6', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=models.CharField(default='provSASxS8S8S5SaSGSpSHSlSZScSTSySpSlSNSJS3', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(default='sku8tqtytRtQtOtDtNt8tUtbtstmtktit1t1te', max_length=30),
        ),
    ]
