from django.contrib import admin
from account.models import Account,RefCredit,TransactionLog,CashDeposit,CashWithrawal

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','user','balance','actual_balance','refer_balance','trial_balance', 'active','created_at','updated_at')
    list_display_links = ('user_id',)
    search_fields = ('user_id',)
    list_editable = ('active',)

admin.site.register(Account, AccountAdmin)

class RefCreditAdmin(admin.ModelAdmin):
    list_display = ('user_id','user','amount','credit_from','current_bal','approved','closed', 'has_record','created_at','updated_at')
    list_display_links = ('user_id',)
    search_fields = ('user_id',)
    list_editable = ('approved',)

admin.site.register(RefCredit, RefCreditAdmin)

class TransactionLogAdmin(admin.ModelAdmin):
    list_display = ('id','user','amount','now_bal','trans_type','created_at','updated_at')
    list_display_links = ('user',)
    search_fields = ('user',)
    list_filter =('user','trans_type')


admin.site.register(TransactionLog, TransactionLogAdmin)


class CashDepositAdmin(admin.ModelAdmin):
    list_display = ('user','deposited','has_record','amount','current_bal','created_at','updated_at')
    list_display_links = ('amount',)
    search_fields = ('amount',)
    list_filter =('user',)
    # readonly_fields = ('user','deposited','has_record','amount','current_bal','created_at','updated_at')


admin.site.register(CashDeposit, CashDepositAdmin)


class CashWithrawalAdmin(admin.ModelAdmin):
    list_display = ('id','user','active','approved','withrawned','withraw_status','has_record','amount','user_account','created_at','updated_at')
    list_display_links = ('id',)
    search_fields = ('user',)
    list_filter =('user','approved','active')
    readonly_fields =('withrawned','has_record','active','user_account','created_at','updated_at')


admin.site.register(CashWithrawal, CashWithrawalAdmin)
