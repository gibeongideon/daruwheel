# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import PaymentTransaction, Wallet

class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('id','phone_number','amount','isFinished','isSuccessFull','closed')
    list_display_links = ('id',)
    # list_editable = ('isFinished','isSuccessFull')


admin.site.register(PaymentTransaction, PaymentTransactionAdmin) 


class WalletAdmin(admin.ModelAdmin):
    list_display = ('id','phone_number','available_balance','actual_balance',)
    list_display_links = ('id',)
    # list_editable = ('isFinished','isSuccessFull')


admin.site.register(Wallet, WalletAdmin)