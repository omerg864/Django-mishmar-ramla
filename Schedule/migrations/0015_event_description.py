# Generated by Django 3.1.1 on 2021-04-28 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0014_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.CharField(default='', max_length=50, verbose_name='תאור'),
        ),
    ]
