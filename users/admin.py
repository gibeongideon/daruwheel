
from django.contrib import admin
from .models import *

class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_no',)
    list_display_links = ('user',)
    search_fields = ('user',)
    ordering = ('user',)

admin.site.register(UserDetail, UserDetailAdmin)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user_id','user','number','balance', 'active','created_at','updated_at')
    list_display_links = ('number',)
    search_fields = ('number',)
    list_editable = ('active',)


admin.site.register(Account, AccountAdmin)


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user_bal','account_bal','amount','now_bal','trans_type','created_at','updated_at')
    list_display_links = ('user_bal',)
    search_fields = ('user_bal',)
    list_filter =('user_bal',)


admin.site.register(Balance, BalanceAdmin)


class CashDepositAdmin(admin.ModelAdmin):
    list_display = ('user_depo','source_no','deposited','user_record_done','amount','current_bal','created_at','updated_at')
    list_display_links = ('amount',)
    search_fields = ('amount',)
    list_filter =('user_depo',)


admin.site.register(CashDeposit, CashDepositAdmin)


class CashWithrawalAdmin(admin.ModelAdmin):
    list_display = ('user_withr','withrawned','user_record_done','amount','current_bal','created_at','updated_at')
    list_display_links = ('amount',)
    search_fields = ('amount',)
    list_filter =('user_withr',)


admin.site.register(CashWithrawal, CashWithrawalAdmin)

class StakeAdmin(admin.ModelAdmin):
    list_display = ('id','user_stake','marketinstant','marketselection','account_bal','current_bal','amount','stake_placed','user_record_done','outcome','update_account_on_win_lose','place_bet_is_active','start_at','ends_at')
    list_display_links = ('user_stake',)
    search_fields = ('user_stake',)
    # list_editable = ('outcome',)
    list_filter =('user_stake','marketinstant','marketselection')
    


admin.site.register(Stake, StakeAdmin)


class MarketSelectionAdmin(admin.ModelAdmin):
    list_display = ('id','odds','name',)
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(MarketSelection, MarketSelectionAdmin) 


class MarketInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','closed','amount_stake_per_market','total_bet_amount_per_marktinstance','black_bet_amount','white_bet_amount','offset','gain_after_relief','determine_result_algo','created_at','bet_expiry_time','closed_at','results_at','updated_at','place_stake_is_active','instance_is_active','get_result_active',)
    list_display_links = ('id',)
    #list_editable = ('place_stake_is_active',)
    # list_editable = ('closed',)


admin.site.register(MarketInstance, MarketInstanceAdmin) 

class CumulativeGainAdmin(admin.ModelAdmin):
    list_display = ('id','gain','gainovertime',)
    list_display_links = ('id',)
    # list_editable = ('',)


admin.site.register(CumulativeGain, CumulativeGainAdmin) 



class ResultAdmin(admin.ModelAdmin):
    list_display = ('id','closed','market','resu','created_at','updated_at',)
    list_display_links = ('id',)
    # list_editable = ('closed',)


admin.site.register(Result, ResultAdmin) 


class BetSettingVarAdmin(admin.ModelAdmin):
    list_display = ('id','per_return','bet_expiry_time','closed_at','results_at','created_at','updated_at',)
    list_display_links = ('id',)
    list_editable = ('per_return','bet_expiry_time','closed_at','results_at')


admin.site.register(BetSettingVar, BetSettingVarAdmin) 