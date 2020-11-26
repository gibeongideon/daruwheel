
#  Author: gideon gibeon <kipngeno.gibeon@gmail.com>

from django.db import models
from django.utils import timezone


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank =True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank =True,null=True)
    # is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class BetSettingVar(TimeStamp):
    per_retun = models.FloatField(default = 0,blank =True,null= True)
    min_redeem_refer_credit = models.FloatField(default = 1000,blank =True,null= True)
    closed_at = models.FloatField(default =8,blank =True,null= True)
    results_at = models.FloatField(default =8.1,blank =True,null= True)
