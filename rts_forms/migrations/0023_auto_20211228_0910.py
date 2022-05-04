# Generated by Django 2.2.5 on 2021-12-28 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0022_rtsform_qao_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='rtsform',
            name='fm_comment',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Resolution'),
        ),
        migrations.AlterField(
            model_name='rtsform',
            name='hod_comment',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='HOD comment'),
        ),
        migrations.AlterField(
            model_name='rtsform',
            name='qao_comment',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='QAO comment'),
        ),
    ]