# Generated by Django 2.2.5 on 2021-12-10 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0014_auto_20211210_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='rtsform',
            name='form_status',
            field=models.CharField(default='0', max_length=7, null=True),
        ),
    ]
