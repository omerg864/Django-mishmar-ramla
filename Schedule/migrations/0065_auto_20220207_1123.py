# Generated by Django 3.2.8 on 2022-02-07 09:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0064_auto_20220207_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiftorganizer',
            name='json',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='week',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 2, 7, 9, 23, 29, 383128, tzinfo=utc)),
        ),
    ]