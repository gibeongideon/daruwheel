from django.conf import settings
from django.db import models
from core.models import TimeStamp


class LoggedInUser(TimeStamp):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING, related_name='logged_in_user')