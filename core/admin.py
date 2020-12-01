from django.contrib import admin
from core.models import MarketType,Selection ,BetSettingVar



class MarketTypeAdmin(admin.ModelAdmin):
    list_display = ('id','name','this_market_selection_id_list','this_market_selection_verbose_list','created_at','updated_at',)
    list_display_links = ('id',)
    # list_editable = ('closed',)


admin.site.register(MarketType, MarketTypeAdmin) 


class SelectionAdmin(admin.ModelAdmin):
    list_display = ('id','market_id','odds','name','created_at','updated_at')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('mrtype','odds')

admin.site.register(Selection, SelectionAdmin) 

class BetSettingVarAdmin(admin.ModelAdmin):
    list_display = ('id','per_retun','min_redeem_refer_credit','closed_at','results_at','wheelspin_id','created_at','updated_at',)
    list_display_links = ('id',)
    list_editable = ('per_retun','min_redeem_refer_credit','closed_at','results_at','wheelspin_id')


admin.site.register(BetSettingVar, BetSettingVarAdmin) 