# Generated by Django 3.2.8 on 2022-01-24 13:05

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Schedule', '0056_auto_20220124_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='arming_log',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='שם משתמש'),
        ),
        migrations.AlterField(
            model_name='week',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 1, 24, 13, 5, 16, 184289, tzinfo=utc)),
        ),
    ]
