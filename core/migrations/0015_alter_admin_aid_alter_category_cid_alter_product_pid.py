# Generated by Django 5.0.4 on 2024-05-10 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_admin_aid_alter_category_cid_alter_product_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='aid',
            field=models.CharField(default='admga2aFasaba6avaXaVa0', max_length=10),
        ),
        migrations.AlterField(
            model_name='category',
            name='cid',
            field=models.CharField(default='catscgcNcecjcdcecccJcw', max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=models.CharField(default='prApmp3pHpNp7pNpLpfpu', max_length=10),
        ),
    ]
