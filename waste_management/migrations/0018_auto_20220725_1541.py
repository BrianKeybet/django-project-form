# Generated by Django 2.2.5 on 2022-07-25 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waste_management', '0017_checklist_form_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checklist',
            old_name='form_status',
            new_name='checklist_status',
        ),
    ]