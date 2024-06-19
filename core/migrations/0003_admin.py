# Generated by Django 5.0.4 on 2024-05-09 18:24

import core.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_product_tags_remove_product_user_delete_admin_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Nestify', max_length=100)),
                ('image', models.ImageField(default='vendor.jpg', upload_to=core.models.admin_directory_path)),
                ('cover_image', models.ImageField(default='vendor.jpg', upload_to=core.models.admin_directory_path)),
                ('description', models.TextField(blank=True, default='I am am Amazing Vendor', null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Admins',
            },
        ),
    ]
