# Generated by Django 5.0.4 on 2024-05-09 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_admin_aid_category_cid_alter_product_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='aid',
            field=models.CharField(default='4admPadmxadmUadmCadmAadmpadmTadmOadmA', max_length=10),
        ),
        migrations.AlterField(
            model_name='category',
            name='cid',
            field=models.CharField(default='ecat2catqcat7catKcat5catScat5catccatj', max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=models.CharField(default='LprMpryprRprzpr8priprGprDprf', max_length=10),
        ),
    ]
