# Generated by Django 5.0.4 on 2024-05-10 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_admin_aid_alter_category_cid_alter_product_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='aid',
            field=models.CharField(default='admNKAKtKrKnKOKCKyKlK4K4KLK9KGKLKTKhKIK4KH', max_length=50),
        ),
        migrations.AlterField(
            model_name='category',
            name='cid',
            field=models.CharField(default='catHnDnqnjnNncnBnOnnnjnXnmnznanHnInonJnOnx', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=models.CharField(default='probVNV2VgVLVpV9VWVKVGVrV0V6VRV6V0V7VkV8VX', max_length=50),
        ),
    ]
