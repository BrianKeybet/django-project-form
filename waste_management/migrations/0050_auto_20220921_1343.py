# Generated by Django 3.2.14 on 2022-09-21 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_management', '0049_auto_20220921_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods_issue_note',
            name='time_in',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='goods_issue_note',
            name='time_out',
            field=models.TimeField(blank=True, null=True),
        ),
    ]