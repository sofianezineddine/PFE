# Generated by Django 5.0.4 on 2024-05-10 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_remove_product_stock_count_alter_admin_aid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='sku',
            field=models.CharField(default='SKUnRyRXRFRCRSR9R9RvRXRXRXRSR6RaRmRjRS', max_length=30),
        ),
        migrations.AlterField(
            model_name='admin',
            name='aid',
            field=models.CharField(default='admKqDqKqAqyqfqIqhqRqsqsqSqQqKqjqIqaq6qRqI', max_length=50),
        ),
        migrations.AlterField(
            model_name='category',
            name='cid',
            field=models.CharField(default='catXQYQzQ6QdQOQHQRQUQzQ5QiQSQ0QdQTQGQLQtQc', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=models.CharField(default='pro9t4t5t5tztqtotEtOtbt0tDtRtAtGtBtBtqtWt8', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(default='skuoo5oLokooo4oVoAoWoroyoEobooohoyogol', max_length=30),
        ),
    ]
