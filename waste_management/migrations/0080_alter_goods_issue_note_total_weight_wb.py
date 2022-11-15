# Generated by Django 4.1.3 on 2022-11-15 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("waste_management", "0079_alter_goods_issue_note_received_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="goods_issue_note",
            name="total_weight_wb",
            field=models.DecimalField(
                decimal_places=2, max_digits=15, null=True, verbose_name=""
            ),
        ),
    ]
