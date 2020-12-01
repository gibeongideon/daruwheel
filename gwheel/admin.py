from django.contrib import admin
from gwheel.models import Stake,WheelSpin,CumulativeGain,Result,Selection,MarketType

class WheelSpinAdmin(admin.ModelAdmin):

    list_display = ('id','market','active','place_stake_is_active','open_at','closed_at','results_at','updated_at','total_bet_amount_per_marktinstance','selection_bet_amount','black_bet_amount','white_bet_amount','offset','gain_after_relief','place_stake_is_active','get_result_active',)
    list_display_links = ('id',)
    #list_editable = ('place_stake_is_active',)
    # list_editable = ('closed',)
    readonly_fields = ('id','market','active','place_stake_is_active','open_at','closed_at','results_at','updated_at','total_bet_amount_per_marktinstance','selection_bet_amount','black_bet_amount','white_bet_amount','offset','gain_after_relief','place_stake_is_active','get_result_active',)

admin.site.register(WheelSpin, WheelSpinAdmin) 


class StakeAdmin(admin.ModelAdmin):
    list_display = ('id','user','market','marketselection','account_bal','current_bal','amount','stake_placed','has_record','update_account_on_win_lose','created_at','updated_at')
    list_display_links = ('user',)
    search_fields = ('user',)
    # list_editable = ('outcome',)
    list_filter =('user','market','marketselection')
    readonly_fields = ('current_bal','market')

admin.site.register(Stake, StakeAdmin)



class CumulativeGainAdmin(admin.ModelAdmin):
    list_display = ('id','gain','gainovertime','created_at','updated_at')
    list_display_links = ('id',)
    # list_editable = ('',)

admin.site.register(CumulativeGain, CumulativeGainAdmin) 



class ResultAdmin(admin.ModelAdmin):
    list_display = ('id','closed','market','resu','gain','created_at','updated_at',)
    list_display_links = ('id',)
    # list_editable = ('closed',)

admin.site.register(Result, ResultAdmin) 