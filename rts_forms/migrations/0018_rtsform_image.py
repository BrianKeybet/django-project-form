# Generated by Django 2.2.5 on 2021-12-20 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0017_remove_rtsform_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='rtsform',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='rts_pics'),
        ),
    ]