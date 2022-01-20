# Generated by Django 3.2.8 on 2022-01-20 20:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0040_auto_20220120_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='arminglog',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='arminglog',
            name='name',
            field=models.CharField(default='', max_length=50, verbose_name='שם'),
        ),
        migrations.AlterField(
            model_name='arminglog',
            name='radio',
            field=models.BooleanField(default=False, verbose_name='קשר, blank=False'),
        ),
        migrations.AlterField(
            model_name='arminglog',
            name='shift',
            field=models.CharField(default='', max_length=50, verbose_name='משמרת'),
        ),
        migrations.AlterField(
            model_name='week',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 1, 20, 20, 57, 59, 121019, tzinfo=utc)),
        ),
    ]