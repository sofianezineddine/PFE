# Generated by Django 5.0.4 on 2024-05-10 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_admin_aid_alter_category_cid_alter_product_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='aid',
            field=models.CharField(default='uadmuadmCadmnadmAadm7admqadm7admJadm8admhadmpadmVadmIadmQadm4admVadm1admxadmz', max_length=20),
        ),
        migrations.AlterField(
            model_name='category',
            name='cid',
            field=models.CharField(default='XcatNcatecat6cat8cathcat6catDcatscatmcatxcatEcat6catOcatpcatgcatrcatacatBcatl', max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=models.CharField(default='YpreprxproprQprpprKprXpriprspr9pr7prlpr2prppr2prSprfprGprx', max_length=20),
        ),
    ]
