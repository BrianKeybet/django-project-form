# Generated by Django 3.2.14 on 2022-09-16 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_management', '0033_alter_goods_issue_note_item_qty2_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty2_sale',
            field=models.FloatField(blank=True, max_length=10, null=True, verbose_name=''),
        ),
    ]
