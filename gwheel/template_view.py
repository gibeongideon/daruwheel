# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .forms import StakeForm


# @login_required(login_url='/spin/log_in/')
# def place_stake(request):

#     form = StakeForm()
#     if request.method == 'POST':
#         form = StakeForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             print('YES DONE')
#             # return redirect(reverse('cash_trans:trans_log'))
#         else:
#             print('ERRRRR',form.errors)
#     return render(request, '/.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
from gwheel.forms import StakeForm


@login_required(login_url='/users/login/')
def place_stake(request):

    stake_form = StakeForm()
    if request.method == 'POST':
        stake_form = StakeForm(data=request.POST)
        if stake_form.is_valid():
            stake_form.save()
            print('STAKE DONE')
            # return redirect(reverse('cash_trans:trans_log'))
        else:
            print('ERRRRR',stake_form.errors)

    context = {'user': request.user,'stake_form':stake_form}

    return render(request, 'gwheel/stake3.html',context)
    