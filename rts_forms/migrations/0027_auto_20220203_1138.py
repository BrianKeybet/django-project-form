# Generated by Django 2.2.5 on 2022-02-03 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0026_auto_20220124_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='rtsform',
            name='icon',
            field=models.ImageField(blank=True, default='Kapa_Logo_Landscape.png', null=True, upload_to='logo_pics', verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='rtsform',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='rts_pics', verbose_name='Picture'),
        ),
    ]