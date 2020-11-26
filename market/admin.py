from django.contrib import admin
from .models import Stake,MarketInstance,CumulativeGain,Result

class StakeAdmin(admin.ModelAdmin):
    list_display = ('id','user','marketinstant','marketselection','mrkt_selection','account_bal','current_bal','amount','stake_placed','has_record','outcome','update_account_on_win_lose','place_bet_is_active','created_at','updated_at')
    list_display_links = ('user',)
    search_fields = ('user',)
    # list_editable = ('outcome',)
    list_filter =('user','marketinstant','marketselection')
    


admin.site.register(Stake, StakeAdmin)


# class MarketSelectionAdmin(admin.ModelAdmin):
#     list_display = ('id','odds','name',)
#     list_display_links = ('name',)
#     search_fields = ('name',)


# admin.site.register(MarketSelection, MarketSelectionAdmin) 


class MarketInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','closed','created_at','closed_at','results_at','updated_at','total_bet_amount_per_marktinstance','black_bet_amount','white_bet_amount','offset','gain_after_relief','place_stake_is_active','instance_is_active','get_result_active',)
    list_display_links = ('id',)
    #list_editable = ('place_stake_is_active',)
    # list_editable = ('closed',)


admin.site.register(MarketInstance, MarketInstanceAdmin) 

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


