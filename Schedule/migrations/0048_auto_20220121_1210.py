# Generated by Django 3.2.8 on 2022-01-21 10:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0047_alter_week_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arming_log',
            name='time_out',
            field=models.TimeField(blank=True, default=django.utils.timezone.now, verbose_name='זמן יציאה'),
        ),
        migrations.AlterField(
            model_name='week',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 1, 21, 10, 10, 54, 733249, tzinfo=utc)),
        ),
    ]