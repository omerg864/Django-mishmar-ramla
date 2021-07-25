# Generated by Django 3.1.1 on 2021-07-25 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0004_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(default='אין', max_length=20, verbose_name='כינוי')),
                ('night', models.IntegerField(default=0, verbose_name='לילה')),
                ('sat_night', models.IntegerField(default=0, verbose_name='שישי לילה/מוצ"ש')),
                ('sat_morning', models.IntegerField(default=0, verbose_name='שבת בוקר')),
                ('sat_noon', models.IntegerField(default=0, verbose_name='שבת צהריים')),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('sat', models.BooleanField(default=False, verbose_name='עושה רק מוצ"ש')),
                ('language', models.CharField(default='עברית', max_length=30, verbose_name='שפה')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
