# Generated by Django 2.2.5 on 2022-07-25 14:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waste_management', '0015_auto_20220708_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waste_delivery_note',
            name='waste_offloader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Acknowledged_By', to=settings.AUTH_USER_MODEL),
        ),
    ]
