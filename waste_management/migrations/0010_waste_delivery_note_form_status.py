# Generated by Django 2.2.5 on 2022-05-19 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_management', '0009_auto_20220518_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='waste_delivery_note',
            name='form_status',
            field=models.IntegerField(default='0', null=True),
        ),
    ]
