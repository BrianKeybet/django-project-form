# Generated by Django 3.2.14 on 2022-11-01 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_management', '0073_auto_20221029_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='kgrn',
            name='pur_close_comment',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Purchase closing comment'),
        ),
    ]
