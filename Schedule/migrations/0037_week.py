# Generated by Django 3.1.1 on 2021-10-03 06:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0036_delete_organization2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime(2021, 10, 3, 6, 54, 2, 115156, tzinfo=utc))),
                ('num_week', models.IntegerField(default=0)),
                ('Day1_630', models.TextField(blank=True, max_length=50)),
                ('Day1_700_search', models.TextField(blank=True, max_length=50)),
                ('Day1_700_manager', models.TextField(blank=True, max_length=50)),
                ('Day1_720_1', models.TextField(blank=True, max_length=50)),
                ('Day1_720_pull', models.TextField(blank=True, max_length=50)),
                ('Day1_720_2', models.TextField(blank=True, max_length=50)),
                ('Day1_720_3', models.TextField(blank=True, max_length=50)),
                ('Day1_1400', models.TextField(blank=True, max_length=50)),
                ('Day1_1500', models.TextField(blank=True, max_length=50)),
                ('Day1_1500_1900', models.TextField(blank=True, max_length=50)),
                ('Day1_2300', models.TextField(blank=True, max_length=50)),
                ('Day1_notes', models.TextField(blank=True, max_length=50)),
                ('Day2_630', models.TextField(blank=True, max_length=50)),
                ('Day2_700_search', models.TextField(blank=True, max_length=50)),
                ('Day2_700_manager', models.TextField(blank=True, max_length=50)),
                ('Day2_720_1', models.TextField(blank=True, max_length=50)),
                ('Day2_720_pull', models.TextField(blank=True, max_length=50)),
                ('Day2_720_2', models.TextField(blank=True, max_length=50)),
                ('Day2_720_3', models.TextField(blank=True, max_length=50)),
                ('Day2_1400', models.TextField(blank=True, max_length=50)),
                ('Day2_1500', models.TextField(blank=True, max_length=50)),
                ('Day2_1500_1900', models.TextField(blank=True, max_length=50)),
                ('Day2_2300', models.TextField(blank=True, max_length=50)),
                ('Day2_notes', models.TextField(blank=True, max_length=50)),
                ('Day3_630', models.TextField(blank=True, max_length=50)),
                ('Day3_700_search', models.TextField(blank=True, max_length=50)),
                ('Day3_700_manager', models.TextField(blank=True, max_length=50)),
                ('Day3_720_1', models.TextField(blank=True, max_length=50)),
                ('Day3_720_pull', models.TextField(blank=True, max_length=50)),
                ('Day3_720_2', models.TextField(blank=True, max_length=50)),
                ('Day3_720_3', models.TextField(blank=True, max_length=50)),
                ('Day3_1400', models.TextField(blank=True, max_length=50)),
                ('Day3_1500', models.TextField(blank=True, max_length=50)),
                ('Day3_1500_1900', models.TextField(blank=True, max_length=50)),
                ('Day3_2300', models.TextField(blank=True, max_length=50)),
                ('Day3_notes', models.TextField(blank=True, max_length=50)),
                ('Day4_630', models.TextField(blank=True, max_length=50)),
                ('Day4_700_search', models.TextField(blank=True, max_length=50)),
                ('Day4_700_manager', models.TextField(blank=True, max_length=50)),
                ('Day4_720_1', models.TextField(blank=True, max_length=50)),
                ('Day4_720_pull', models.TextField(blank=True, max_length=50)),
                ('Day4_720_2', models.TextField(blank=True, max_length=50)),
                ('Day4_720_3', models.TextField(blank=True, max_length=50)),
                ('Day4_1400', models.TextField(blank=True, max_length=50)),
                ('Day4_1500', models.TextField(blank=True, max_length=50)),
                ('Day4_1500_1900', models.TextField(blank=True, max_length=50)),
                ('Day4_2300', models.TextField(blank=True, max_length=50)),
                ('Day4_notes', models.TextField(blank=True, max_length=50)),
                ('Day5_630', models.TextField(blank=True, max_length=50)),
                ('Day5_700_search', models.TextField(blank=True, max_length=50)),
                ('Day5_700_manager', models.TextField(blank=True, max_length=50)),
                ('Day5_720_1', models.TextField(blank=True, max_length=50)),
                ('Day5_720_pull', models.TextField(blank=True, max_length=50)),
                ('Day5_720_2', models.TextField(blank=True, max_length=50)),
                ('Day5_720_3', models.TextField(blank=True, max_length=50)),
                ('Day5_1400', models.TextField(blank=True, max_length=50)),
                ('Day5_1500', models.TextField(blank=True, max_length=50)),
                ('Day5_1500_1900', models.TextField(blank=True, max_length=50)),
                ('Day5_2300', models.TextField(blank=True, max_length=50)),
                ('Day5_notes', models.TextField(blank=True, max_length=50)),
                ('Day6_630', models.TextField(blank=True, max_length=50)),
                ('Day6_700_search', models.TextField(blank=True, max_length=50)),
                ('Day6_700_manager', models.TextField(blank=True, max_length=50)),
                ('Day6_720_1', models.TextField(blank=True, max_length=50)),
                ('Day6_720_pull', models.TextField(blank=True, max_length=50)),
                ('Day6_720_2', models.TextField(blank=True, max_length=50)),
                ('Day6_720_3', models.TextField(blank=True, max_length=50)),
                ('Day6_1400', models.TextField(blank=True, max_length=50)),
                ('Day6_1500', models.TextField(blank=True, max_length=50)),
                ('Day6_1500_1900', models.TextField(blank=True, max_length=50)),
                ('Day6_2300', models.TextField(blank=True, max_length=50)),
                ('Day6_notes', models.TextField(blank=True, max_length=50)),
                ('Day7_630', models.TextField(blank=True, max_length=50)),
                ('Day7_700_search', models.TextField(blank=True, max_length=50)),
                ('Day7_700_manager', models.TextField(blank=True, max_length=50)),
                ('Day7_720_1', models.TextField(blank=True, max_length=50)),
                ('Day7_720_pull', models.TextField(blank=True, max_length=50)),
                ('Day7_720_2', models.TextField(blank=True, max_length=50)),
                ('Day7_720_3', models.TextField(blank=True, max_length=50)),
                ('Day7_1400', models.TextField(blank=True, max_length=50)),
                ('Day7_1500', models.TextField(blank=True, max_length=50)),
                ('Day7_1500_1900', models.TextField(blank=True, max_length=50)),
                ('Day7_2300', models.TextField(blank=True, max_length=50)),
                ('Day7_notes', models.TextField(blank=True, max_length=50)),
            ],
        ),
    ]
