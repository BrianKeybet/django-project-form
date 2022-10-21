# Generated by Django 3.2.14 on 2022-10-21 11:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('waste_management', '0067_auto_20221017_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='kgrn_item',
            name='closed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Accounts_Representative', to=settings.AUTH_USER_MODEL),
        ),
    ]
