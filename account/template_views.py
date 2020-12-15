
from django.shortcuts import render, redirect ,reverse
from django.contrib.auth.decorators import login_required
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .models import TransactionLog


# Use redis cashing here for speed
# @login_required(login_url='/users/login/')
def trans_log(request):
    trans_logz = list(TransactionLog.objects.filter(user =request.user))
    
    return render(request, 'account/trans_log.html',{'trans_logz': trans_logz})

