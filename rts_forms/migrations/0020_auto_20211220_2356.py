# Generated by Django 2.2.5 on 2021-12-20 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0019_auto_20211220_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rtsform',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='rts_pics', verbose_name='Picture'),
        ),
    ]