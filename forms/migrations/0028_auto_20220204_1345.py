# Generated by Django 2.2.5 on 2022-02-04 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0027_auto_20220203_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rtsform',
            name='fm_comment',
        ),
        migrations.RemoveField(
            model_name='rtsform',
            name='icon',
        ),
    ]
