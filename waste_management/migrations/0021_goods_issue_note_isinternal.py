# Generated by Django 2.2.5 on 2022-08-18 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_management', '0020_goods_issue_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods_issue_note',
            name='isInternal',
            field=models.BooleanField(default=False),
        ),
    ]