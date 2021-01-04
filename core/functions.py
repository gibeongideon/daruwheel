from .models import BetSettingVar

# @property
# def set_up():
#     try:
#         return BetSettingVar.objects.get(id =1)# Set up variables
#     except:
#         BetSettingVar.objects.update_or_create(id =1)
#         return BetSettingVar.objects.get(id =1)
    

set_up,_ = BetSettingVar.objects.get_or_create(id =1) #get_or_create return a tuple/ (<BetSettingVar: BetSettingVar object (2)>, True)