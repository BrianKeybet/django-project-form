# Generated by Django 3.2.14 on 2022-10-04 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rts_forms', '0004_auto_20220831_1340'),
        ('waste_management', '0058_auto_20220930_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='kgrn_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date')),
                ('department', models.CharField(blank=True, max_length=20)),
                ('form_status', models.IntegerField(default='0', null=True)),
                ('waste_loader', models.CharField(blank=True, max_length=20, null=True, verbose_name='Loaded By')),
                ('collected_by', models.CharField(blank=True, max_length=20, null=True, verbose_name='Collected By')),
                ('id_number', models.CharField(blank=True, max_length=20, verbose_name='ID Number')),
                ('vehicle_no', models.CharField(blank=True, max_length=20, null=True, verbose_name='Vehicle No')),
                ('item_qty1', models.FloatField(blank=True, max_length=40, null=True, verbose_name='Estimated Quantity')),
                ('item_qty2', models.FloatField(blank=True, max_length=40, null=True, verbose_name='Estimated Quantity')),
                ('item_qty3', models.FloatField(blank=True, max_length=40, null=True, verbose_name='Estimated Quantity')),
                ('item_qty4', models.FloatField(blank=True, max_length=40, null=True, verbose_name='Estimated Quantity')),
                ('item_qty5', models.FloatField(blank=True, max_length=40, null=True, verbose_name='Estimated Quantity')),
                ('item_qty6', models.FloatField(blank=True, max_length=40, null=True, verbose_name='Estimated Quantity')),
                ('item_qty7', models.FloatField(blank=True, max_length=40, null=True, verbose_name='Estimated Quantity')),
                ('item_qty8', models.FloatField(blank=True, max_length=40, null=True, verbose_name='Estimated Quantity')),
                ('hod_comment', models.CharField(blank=True, max_length=100, null=True, verbose_name='HOD comment')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('hod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Head_of_Dept', to=settings.AUTH_USER_MODEL)),
                ('item1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material001', to='waste_management.material', verbose_name='Material Description')),
                ('item2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material002', to='waste_management.material', verbose_name='Material Description')),
                ('item3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material003', to='waste_management.material', verbose_name='Material Description')),
                ('item4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material004', to='waste_management.material', verbose_name='Material Description')),
                ('item5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material005', to='waste_management.material', verbose_name='Material Description')),
                ('item6', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material006', to='waste_management.material', verbose_name='Material Description')),
                ('item7', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material007', to='waste_management.material', verbose_name='Material Description')),
                ('item8', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material008', to='waste_management.material', verbose_name='Material Description')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='rts_forms.supplier')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
