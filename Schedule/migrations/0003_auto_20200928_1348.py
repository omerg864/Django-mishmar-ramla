# Generated by Django 3.1.1 on 2020-09-28 10:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0002_organization_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='published',
            field=models.BooleanField(default=False, verbose_name='פרסום'),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='תאריך'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(blank=True, verbose_name='טקסט'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=30, verbose_name='כותרת'),
        ),
    ]
