from django import forms
from cash_trans.models import C2BTransaction

class C2BTransactionForm(forms.ModelForm):
    class Meta:
        model = C2BTransaction
        fields = ('phone_number', 'amount',)

