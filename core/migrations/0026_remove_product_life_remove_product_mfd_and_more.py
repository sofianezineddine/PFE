# Generated by Django 5.0.4 on 2024-05-10 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_admin_aid_alter_category_cid_alter_product_pid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='life',
        ),
        migrations.RemoveField(
            model_name='product',
            name='mfd',
        ),
        migrations.RemoveField(
            model_name='product',
            name='specifications',
        ),
        migrations.RemoveField(
            model_name='product',
            name='type',
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(default='Black', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='origin',
            field=models.CharField(default='India', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(default='skuczizKzIzhzBz7z6zDzaz8z5z6zVzMzhzizFzqz6', max_length=50),
        ),
        migrations.AlterField(
            model_name='admin',
            name='aid',
            field=models.CharField(default='adm0NQNnNMNWNhNsN9NBNYNPNQNJNfNRNfNXNvNFND', max_length=50),
        ),
        migrations.AlterField(
            model_name='category',
            name='cid',
            field=models.CharField(default='catVHxHeHAHnH8HiH8HWHMHFH9HAHwHiHiHVHRH0HG', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=models.CharField(default='proXL5LoLYLQLRLrLlLMLSLkLRLTLUL5LwLHLRLiLQ', max_length=50),
        ),
    ]
