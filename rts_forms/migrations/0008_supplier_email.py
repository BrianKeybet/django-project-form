# Generated by Django 4.1.3 on 2023-03-23 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rts_forms", "0007_alter_rtsform_department_internal"),
    ]

    operations = [
        migrations.AddField(
            model_name="supplier",
            name="email",
            field=models.EmailField(default="kapaoil@gmail.com", max_length=254),
        ),
    ]
