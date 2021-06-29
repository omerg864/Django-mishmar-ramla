# Generated by Django 3.1.1 on 2021-04-29 11:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0016_auto_20210428_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date2',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='תאריך'),
        ),
        migrations.AlterField(
            model_name='organization2',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
