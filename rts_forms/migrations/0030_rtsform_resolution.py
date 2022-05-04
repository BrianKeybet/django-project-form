# Generated by Django 2.2.5 on 2022-02-04 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0029_resolution'),
    ]

    operations = [
        migrations.AddField(
            model_name='rtsform',
            name='resolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='forms.Resolution', verbose_name='Resolution'),
        ),
    ]