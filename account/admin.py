from django.contrib import admin
from account.models import Account,RefCredit,TransactionLog,CashDeposit,CashWithrawal

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','user','balance','refer_balance', 'active','created_at','updated_at')
    list_display_links = ('user_id',)
    search_fields = ('user_id',)
    list_editable = ('active',)

admin.site.register(Account, AccountAdmin)

class RefCreditAdmin(admin.ModelAdmin):
    list_display = ('user_id','user','amount','current_bal','closed', 'has_record','created_at','updated_at')
    list_display_links = ('user_id',)
    search_fields = ('user_id',)
    # list_editable = ('amount',)

admin.site.register(RefCredit, RefCreditAdmin)

class TransactionLogAdmin(admin.ModelAdmin):
    list_display = ('id','user','account_bal','amount','now_bal','trans_type','created_at','updated_at')
    list_display_links = ('user',)
    search_fields = ('user',)
    list_filter =('user',)


admin.site.register(TransactionLog, TransactionLogAdmin)


class CashDepositAdmin(admin.ModelAdmin):
    list_display = ('user','source_no','deposited','has_record','amount','current_bal','created_at','updated_at')
    list_display_links = ('amount',)
    search_fields = ('amount',)
    list_filter =('user',)
    # readonly_fields = ('user_depo','source_no','deposited','has_record','amount','current_bal','created_at','updated_at')


admin.site.register(CashDeposit, CashDepositAdmin)


class CashWithrawalAdmin(admin.ModelAdmin):
    list_display = ('id','user','withrawned','has_record','amount','current_bal','created_at','updated_at')
    list_display_links = ('id',)
    search_fields = ('user',)
    list_filter =('user',)
    # readonly_fields =('user_withr','withrawned','has_record','amount','current_bal','created_at','updated_at')


admin.site.register(CashWithrawal, CashWithrawalAdmin)
