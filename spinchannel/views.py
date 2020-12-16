from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
from gwheel.forms import StakeForm
from gwheel.models import Stake


@login_required(login_url='/users/login/')
def daru_spin(request):

    stake_form = StakeForm()
    trans_logz =Stake.objects.filter(user =request.user)[:15]
    if request.method == 'POST':
        # trans = Stake.objects.filter(user_bal= pk).order_by('-id')[start:end]# cool huh
        stake_form = StakeForm(data=request.POST)
        if stake_form.is_valid():
            stake_form.save()
            print('STAKE DONE')
            # return redirect(reverse('cash_trans:trans_log'))
        else:
            print('ERRRRR',stake_form.errors)

    context = {'user': request.user,'stake_form':stake_form,'trans_logz':trans_logz}

    return render(request, 'spinchannel/daru_spin.html',context)
    

