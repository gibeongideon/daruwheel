
#  Author: gideon gibeon <kipngeno.gibeon@gmail.com>

from django.db import models
from django.utils import timezone
from datetime import timedelta ,datetime
# from core.functions.models_settings import set_up


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank =True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank =True,null=True)
    # is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True



class BetSettingVar(TimeStamp):
    per_retun = models.FloatField(default = 0,blank =True,null= True)
    min_redeem_refer_credit = models.FloatField(default = 1000,blank =True,null= True)
    refer_per = models.FloatField(default = 0,blank =True,null= True)
    closed_at = models.FloatField(help_text ='sensitive settings value.Dont edit',default =8,blank =True,null= True)
    results_at = models.FloatField(help_text ='sensitive settings value.Dont edit',default =8.1,blank =True,null= True)
    wheelspin_id= models.IntegerField(help_text ='super critical setting value.DONT EDIT!',default=1,blank=True,null=True)
    ksh_unit = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null= True)
    



class Market(models.Model):
    '''Market place '''
    open_at = models.DateTimeField(default= timezone.now,blank =True,null=True) 
    closed_at = models.DateTimeField(blank =True,null=True)                
    results_at =  models.DateTimeField(blank =True,null=True)

    updated_at = models.DateTimeField(auto_now=True,blank =True,null=True)
    active = models.BooleanField(default=True,blank =True,null= True)
    receive_results = models.BooleanField(default=False,blank =True,null= True)

    class Meta:
        abstract = True

    @property
    def place_stake_is_active(self):
        try:
            if timezone.now() >  self.open_at and timezone.now() < self.closed_at:
                return True
            return False
        except Exception as e:
            return e

    @property
    def get_result_active(self):
        try:
            if timezone.now() > self.results_at:# and timezone.now() > self.closed_at:
                return True
            return False
        except Exception as e:
            return e



class MarketType(TimeStamp):
    name = models.CharField(max_length=100,default='M', blank =True,null=True)

    def __str__(self):
        return '{0}:{1}'.format(self.id,self.name)

    def all_selection(self):
        return Selection.objects.filter(mrtype_id = self.id).all()

    def this_market_selection_id_list(self):
        return [_mselect.id for _mselect in self.all_selection() ]

    def this_market_selection_verbose_list(self):
        return [(_mselect.id,_mselect.name,_mselect.odds) for _mselect in self.all_selection()]


class Selection(TimeStamp):
    mrtype = models.ForeignKey(MarketType,on_delete=models.CASCADE,related_name='mrtypes',blank =True,null= True)
    name = models.CharField(max_length=100, blank =True,null=True)
    odds = models.FloatField(max_length=10 ,blank =True,null=True )

    def __str__(self):
        return f'{self.name}'

    def market_id(self):
        return self.mrtype


class Subselection(TimeStamp):
    selection = models.ForeignKey(Selection,on_delete=models.CASCADE,related_name='selections',blank =True,null= True)
    name = models.CharField(max_length=100, blank =True,null=True)
    odds = models.FloatField(max_length=10 ,blank =True,null=True )

    def __str__(self):
        return '{0}SubSelect:{1}'.format(self.selection.name,self.name)

    def market_id(self):
        return self.selection



# def variables_settings():
#     # try:
#     BetSettingVar.objects.get_or_create(id=1)
#     sett = BetSettingVar.objects.update(id=1)
#     print(sett)

#     return sett

    # except:
    #     pass

# set_up = variables_settings()


set_up ={'return_val':0,'min_redeem_refer_credit':1000,'refer_per':0,'closed_at':4.7,'results_at':4.8,'wheelspin_id':1,'curr_unit':10}

from account.models import Currency
class SettingsVar(TimeStamp):
    per_retun = models.FloatField(default = 0,blank =True,null= True)
    # min_redeem_refer_credit = models.FloatField(default = 1000,blank =True,null= True)
    # refer_per = models.FloatField(default = 0,blank =True,null= True)
    # closed_at = models.FloatField(help_text ='sensitive settings value.Dont edit',default =8,blank =True,null= True)
    # results_at = models.FloatField(help_text ='sensitive settings value.Dont edit',default =8.1,blank =True,null= True)
    # wheelspin_id= models.IntegerField(help_text ='super critical setting value.DONT EDIT!',default=1,blank=True,null=True)
    curr_unit= models.DecimalField(max_digits=6, decimal_places=2,blank=True,null= True)
    
    def save(self, *args, **kwargs):
       
        try:
            Curr_Variable.update_curr_unit(self.curr_unit)
            # set_up['curr_unit'] = self.curr_unit
        except:
            pass
        
        # try:
        #     WheelSpin.objects.filter(user_id =user_id).update(curr_unit= self.curr_unit)
        # except:
        #     pass
            
        super().save(*args, **kwargs)