from .models import BetSettingVar

# def set_up():
#     try:
#         return BetSettingVar.objects.get(id =1)# Set up variables
#     except:
#         BetSettingVar.objects.update_or_create(id =1)
#         return BetSettingVar.objects.get(id =1)
    

set_up,_ = BetSettingVar.objects.get_or_create(id =1) #get_or_create return a tuple/ (<BetSettingVar: BetSettingVar object (2)>, True)

# set_up = {'return_val':0,'min_redeem_refer_credit':1000,'refer_per':0,'closed_at':4.7,'results_at':4.8,'wheelspin_id':1,'ksh_unit':10}