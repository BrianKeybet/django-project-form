# Generated by Django 2.2.5 on 2021-12-10 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0013_auto_20211130_1517'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rtsform',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='rtsform',
            name='hod_comment',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
