# Generated by Django 4.1.3 on 2023-03-21 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("waste_management", "0083_rename_isinternal_goods_issue_note_isinternal"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="department",
            options={"ordering": ["name"]},
        ),
    ]
