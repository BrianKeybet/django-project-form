# Generated by Django 4.1.3 on 2022-11-25 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("waste_management", "0080_alter_goods_issue_note_total_weight_wb"),
    ]

    operations = [
        migrations.AddField(
            model_name="kgrn",
            name="supplier",
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
