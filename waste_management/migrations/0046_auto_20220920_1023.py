# Generated by Django 3.2.14 on 2022-09-20 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_management', '0045_alter_goods_issue_note_my_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty1',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Estimated Quantity'),
        ),
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty1_sale',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Estimated Quantity'),
        ),
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty2_sale',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Estimated Quantity'),
        ),
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty3_sale',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty4',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Estimated Quantity'),
        ),
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty4_sale',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty5',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Estimated Quantity'),
        ),
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty5_sale',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty6',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Estimated Quantity'),
        ),
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty6_sale',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty7',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Estimated Quantity'),
        ),
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty7_sale',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty8',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Estimated Quantity'),
        ),
        migrations.AlterField(
            model_name='goods_issue_note',
            name='item_qty8_sale',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='goods_issue_note',
            name='my_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Total'),
        ),
    ]