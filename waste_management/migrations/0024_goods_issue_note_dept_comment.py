# Generated by Django 2.2.5 on 2022-08-23 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_management', '0023_goods_issue_note_fm_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods_issue_note',
            name='dept_comment',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Dept comment'),
        ),
    ]
