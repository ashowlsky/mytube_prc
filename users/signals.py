from users.models import User
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out
from .models import Logout_time_records
import datetime as dt

@receiver(user_logged_out, sender=User)
def logout_sniffer(sender, user, request, **kwargs):
    if Logout_time_records.objects.filter(user=user).exists():
        record = Logout_time_records.objects.get(user=user)
        record.last_logout_time = dt.datetime.now() - dt.timedelta(hours=3)
        record.save()
    else:
        Logout_time_records.objects.create(user=user, last_logout_time=dt.datetime.now())
    


