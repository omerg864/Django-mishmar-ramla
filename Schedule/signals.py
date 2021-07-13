from django.db.models.signals import post_save
from .models import Shift1 as Shift
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail
from datetime import datetime
import pytz
import os


@receiver(post_save, sender=Shift)
def send_number_served(sender, instance, created, **kwargs):
    if created:
        lenShifts = len(Shift.objects.all().filter(date=instance.date))
        shifts = Shift.objects.all().filter(date=instance.date)
        users = User.objects.all()
        guards_sent = []
        guards_not_sent = []
        admin_user = ""
        for user in users:
            if user.is_superuser:
                admin_user = user
        for s in shifts:
            guards_sent.append(users.filter(username=s.username).first().profile2.nickname)
        for u in users:
            if u.profile2.nickname not in guards_sent:
                guards_not_sent.append(users.filter(username=u.username).first().profile2.nickname)
        lenUsers = len(User.objects.all())
        tz_is = pytz.timezone('Israel')
        datetime_is = datetime.now(tz_is)
        date = str(datetime_is.strftime("%d/%m/%Y %H:%M:%S"))
        print("Israel time:", datetime_is.strftime("%H:%M:%S"))
        if lenShifts == lenUsers - 1 or int(datetime_is.strftime("%H")) > 12 or lenShifts % 5 == 0:
            message = f'עד עכשיו בשעה {date} הגישו {str(lenShifts)} אנשים סידור לתאריך {instance.date.strftime("%d/%m")}' \
                      + "\n" + f'אנשים שהגישו: {guards_sent}' + "\n" + f'אנשים שלא הגישו: {guards_not_sent}'
            send_mail(
                'כמות משתמשים שהגישו סידור',
                message,
                os.environ.get("DEFAULT_FROM_EMAIL_RAMLA"),
                [admin_user.email],
                fail_silently=False,
            )
            print("sent")
