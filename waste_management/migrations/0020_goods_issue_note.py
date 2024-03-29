# Generated by Django 2.2.5 on 2022-08-18 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('waste_management', '0019_kgrn'),
    ]

    operations = [
        migrations.CreateModel(
            name='goods_issue_note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date')),
                ('department', models.CharField(blank=True, max_length=20)),
                ('form_status', models.IntegerField(default='0', null=True)),
                ('delivered_by', models.CharField(blank=True, max_length=20, null=True, verbose_name='Delivered By')),
                ('item_qty1', models.FloatField(blank=True, max_length=40, null=True, verbose_name='Estimated Quantity')),
                ('item_qty2', models.FloatField(blank=True, max_length=40, null=True, verbose_name='Estimated Quantity')),
                ('item_qty3', models.FloatField(blank=True, max_length=40, null=True, verbose_name='Estimated Quantity')),
                ('item_qty4', models.FloatField(blank=True, max_length=40, null=True, verbose_name='Estimated Quantity')),
                ('item_qty5', models.FloatField(blank=True, max_length=40, null=True, verbose_name='Estimated Quantity')),
                ('item_qty6', models.FloatField(blank=True, max_length=40, null=True, verbose_name='Estimated Quantity')),
                ('item_qty7', models.FloatField(blank=True, max_length=40, null=True, verbose_name='Estimated Quantity')),
                ('item_qty8', models.FloatField(blank=True, max_length=40, null=True, verbose_name='Estimated Quantity')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('item1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material01', to='waste_management.Material', verbose_name='Material Description')),
                ('item2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material02', to='waste_management.Material', verbose_name='Material Description')),
                ('item3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material03', to='waste_management.Material', verbose_name='Material Description')),
                ('item4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material04', to='waste_management.Material', verbose_name='Material Description')),
                ('item5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material05', to='waste_management.Material', verbose_name='Material Description')),
                ('item6', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material06', to='waste_management.Material', verbose_name='Material Description')),
                ('item7', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material07', to='waste_management.Material', verbose_name='Material Description')),
                ('item8', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material08', to='waste_management.Material', verbose_name='Material Description')),
                ('received_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Received_By', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
