# Generated by Django 3.2.8 on 2022-01-21 10:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0046_alter_week_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='week',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 1, 21, 10, 10, 38, 476238, tzinfo=utc)),
        ),
    ]
