# Generated by Django 2.2.5 on 2022-04-06 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0034_auto_20220406_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rtsform',
            name='delivery_quantity',
            field=models.IntegerField(verbose_name='Delivery quantity'),
        ),
    ]
