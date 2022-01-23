# Generated by Django 3.2.8 on 2022-01-23 11:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0053_auto_20220123_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arming_log',
            name='signature',
            field=models.TextField(blank=True, null=True, verbose_name='signature'),
        ),
        migrations.AlterField(
            model_name='week',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 1, 23, 11, 51, 4, 134537, tzinfo=utc)),
        ),
    ]