# Generated by Django 3.2.8 on 2022-01-20 21:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0041_auto_20220120_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arming_log',
            name='name',
            field=models.CharField(default='', max_length=50, verbose_name='שם'),
        ),
        migrations.AlterField(
            model_name='week',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 1, 20, 21, 10, 46, 782455, tzinfo=utc)),
        ),
    ]
