# Generated by Django 4.2.1 on 2023-07-26 08:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('waste_management', '0085_alter_kgrn_serial_num_alter_kgrn_item_serial_num'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='goods_issue_note',
            new_name='GoodsIssueNote',
        ),
    ]
