# Generated by Django 5.0.4 on 2024-05-10 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_admin_aid_alter_category_cid_alter_product_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='aid',
            field=models.CharField(default='admBaPaCaDaQapaaazaXaWaTalabauaK', max_length=20),
        ),
        migrations.AlterField(
            model_name='category',
            name='cid',
            field=models.CharField(default='catzc8cCcNcDcjcycycTcxcYcbcAcbca', max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=models.CharField(default='prNpxpfpTpbpXplpopBpQpZpcpGpSpS', max_length=20),
        ),
    ]
