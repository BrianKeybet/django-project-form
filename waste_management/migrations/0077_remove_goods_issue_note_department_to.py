# Generated by Django 3.2.14 on 2022-11-01 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waste_management', '0076_auto_20221101_1516'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods_issue_note',
            name='department_to',
        ),
    ]