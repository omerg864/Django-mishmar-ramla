# Generated by Django 3.2.8 on 2022-01-21 09:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0044_auto_20220121_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arming_log',
            name='id_num',
            field=models.CharField(default='', max_length=9, verbose_name='תעודת זהות'),
        ),
        migrations.AlterField(
            model_name='week',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 1, 21, 9, 44, 15, 705207, tzinfo=utc)),
        ),
    ]
