
from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_no',)
    list_display_links = ('user',)
    search_fields = ('user',)
    ordering = ('user',)

admin.site.register(CustomUser, CustomUserAdmin)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','user','number', 'timestamp', 'active','created_at','updated_at')
    list_display_links = ('number',)
    search_fields = ('number',)


admin.site.register(Account, AccountAdmin)


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('id','acount_id','acount','total_balance','created_at','updated_at')
    list_display_links = ('acount',)
    search_fields = ('acount',)


admin.site.register(Balance, BalanceAdmin)


class CashDepositAdmin(admin.ModelAdmin):
    list_display = ('id','balanc_id','balanc','amount','created_at','updated_at')
    list_display_links = ('amount',)
    search_fields = ('amount',)


admin.site.register(CashDeposit, CashDepositAdmin)


class CashWithrawalAdmin(admin.ModelAdmin):
    list_display = ('id','balanc_id','balanc','amount','created_at','updated_at')
    list_display_links = ('amount',)
    search_fields = ('amount',)


admin.site.register(CashWithrawal, CashWithrawalAdmin)

class StakeAdmin(admin.ModelAdmin):
    list_display = ('id','balanc_id','balanc','marketinstant','marketselection','current_bal','amount','account_apdated','outcome','update_account_on_win_lose','place_bet_is_active','start_at','ends_at')
    list_display_links = ('amount',)
    search_fields = ('balanc',)
    # list_editable = ('outcome',)
    


admin.site.register(Stake, StakeAdmin)


class MarketSelectionAdmin(admin.ModelAdmin):
    list_display = ('id','odds','name',)
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(MarketSelection, MarketSelectionAdmin) 


class MarketInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','amount_stake_per_market','total_bet_amount_per_marktinstance','black_bet_amount','white_bet_amount','determine_result_algo','created_at','bet_expiry_time','closed_at','updated_at','place_stake_is_active','instance_is_active','get_result_active',)
    list_display_links = ('id',)
    #list_editable = ('place_stake_is_active',)


admin.site.register(MarketInstance, MarketInstanceAdmin) 

class CumulativeGainAdmin(admin.ModelAdmin):
    list_display = ('id','gain','gainovertime',)
    list_display_links = ('id',)
    # list_editable = ('',)


admin.site.register(CumulativeGain, CumulativeGainAdmin) 



# from users.models import MarketInstance
from time import sleep

from .models import MarketInstance


def control():
    try:
        while True:
            MarketInstance.objects.create()
            print('MARKET INSTANCE CREATED!!!')
            sleep(10)

    except Exception as e:
        print('CONTROL',e)
        return e



# if '__name__' = '__main__':
#     control()
