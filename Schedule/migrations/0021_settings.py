# Generated by Django 3.1.1 on 2021-04-29 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0020_auto_20210429_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitting', models.BooleanField(default=True, verbose_name='ניתן להגיש/לשנות הגשות')),
                ('pin_code', models.IntegerField(default=1234, verbose_name='קוד זיהוי')),
                ('officer', models.CharField(max_length=20, verbose_name='קצין מתקן')),
            ],
        ),
    ]
