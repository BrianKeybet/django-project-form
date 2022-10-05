# Generated by Django 3.2.14 on 2022-09-16 21:43

import computed_property.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waste_management', '0030_goods_issue_note_my_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods_issue_note',
            name='my_total',
            field=computed_property.fields.ComputedFloatField(blank=True, compute_from='double_it', editable=False, null=True, verbose_name='Total'),
        ),
    ]