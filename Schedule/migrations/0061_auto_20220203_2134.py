# Generated by Django 3.2.8 on 2022-02-03 19:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0060_auto_20220203_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='armingrequest',
            name='date',
        ),
        migrations.RemoveField(
            model_name='armingrequest',
            name='valid_in',
        ),
        migrations.RemoveField(
            model_name='armingrequest',
            name='valid_out',
        ),
        migrations.AlterField(
            model_name='week',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 2, 3, 19, 34, 19, 929298, tzinfo=utc)),
        ),
    ]
