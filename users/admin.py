from django.contrib import admin

# Register your models here.

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
    list_display = ('id','balanc_id','balanc','current_bal','marketchoice','amount','outcome','start_at','ends_at')
    list_display_links = ('amount',)
    search_fields = ('amount',)


admin.site.register(Stake, StakeAdmin)



class MarketTypeAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(MarketType, MarketTypeAdmin) 


class MarketSelectionAdmin(admin.ModelAdmin):
    list_display = ('id','markt','odds','name',)
    list_display_links = ('markt',)
    search_fields = ('markt',)


admin.site.register(MarketSelection, MarketSelectionAdmin) 


class MarketChoiceAdmin(admin.ModelAdmin):
    list_display = ('id','markt','name',)
    list_display_links = ('markt',)
    search_fields = ('markt',)


admin.site.register(MarketChoice, MarketChoiceAdmin) 



