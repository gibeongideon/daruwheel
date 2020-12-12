from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cash_trans.forms import C2BTransactionForm
from cash_trans.models import C2BTransaction

@login_required(login_url='/spin/log_in/')
def mpesa_deposit(request):
    print(request.user)
    form = C2BTransactionForm()
    if request.method == 'POST':
        form = C2BTransactionForm(data=request.POST)
        if form.is_valid():
            form.save()
            print('YES DONE')
            # return redirect(reverse('cash_trans:trans_log'))
        else:
            print('ERRRRR',form.errors)
    return render(request, 'cash_trans/mp_deposit.html', {'form': form})