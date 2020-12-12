from django.contrib import admin
from cash_trans.models import C2BTransaction

# Register your models here.
class C2BTransactionAdmin(admin.ModelAdmin):
    list_display = ('id','phone_number','amount','succided','created_at','updated_at')
    list_display_links = ('id',)
    # list_editable = ('',)

admin.site.register(C2BTransaction, C2BTransactionAdmin) 
