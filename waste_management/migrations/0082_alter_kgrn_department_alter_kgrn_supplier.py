# Generated by Django 4.1.3 on 2022-11-25 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("waste_management", "0081_kgrn_supplier"),
    ]

    operations = [
        migrations.AlterField(
            model_name="kgrn",
            name="department",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="kgrn",
            name="supplier",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]