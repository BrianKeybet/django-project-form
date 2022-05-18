# Generated by Django 2.2.5 on 2022-05-17 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rts_forms', '0003_auto_20220511_1210'),
        ('waste_management', '0005_auto_20220517_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='waste_delivery_note',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='rts_forms.Supplier'),
        ),
        migrations.AddField(
            model_name='waste_delivery_note',
            name='waste_loader',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
