# Generated by Django 2.2.5 on 2021-11-09 11:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0003_bpinspectionform_boolean'),
    ]

    operations = [
        migrations.CreateModel(
            name='RTSform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date')),
                ('serial_number', models.CharField(max_length=40, verbose_name=' Form Serial')),
                ('department', models.CharField(max_length=40, verbose_name='Department')),
                ('supplier', models.CharField(max_length=40, verbose_name='Supplier')),
                ('vehicle_number', models.CharField(max_length=40, verbose_name='Vehicle Number')),
                ('dnote_number', models.CharField(max_length=40, verbose_name='D/Note number')),
                ('dnote_date', models.CharField(max_length=40, verbose_name='D/Note Date')),
                ('material_description', models.CharField(max_length=40, verbose_name='Description')),
                ('quality_issue', models.CharField(max_length=40, verbose_name='Issue')),
                ('reason_for_rejection', models.CharField(max_length=40, verbose_name='Reason for rejection')),
                ('delivery_quantity', models.CharField(max_length=40, verbose_name='Delivery quantity')),
                ('sampled_quantity', models.CharField(max_length=40, verbose_name='Sampled quantity')),
                ('quantity_affected', models.CharField(max_length=40, verbose_name='Quantity affected')),
                ('acceptable_level', models.CharField(max_length=40, verbose_name='Acceptable level')),
                ('batches_sampled', models.CharField(max_length=40, verbose_name='Batches sampled')),
                ('mould', models.CharField(max_length=40, verbose_name='Mould')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
