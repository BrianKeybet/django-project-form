# Generated by Django 3.2.14 on 2022-11-01 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waste_management', '0077_remove_goods_issue_note_department_to'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods_issue_note',
            old_name='department_to1',
            new_name='department_to',
        ),
    ]
