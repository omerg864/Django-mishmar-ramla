# Generated by Django 3.1.1 on 2021-04-29 12:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0022_auto_20210429_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization2',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
