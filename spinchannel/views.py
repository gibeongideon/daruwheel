from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect


@login_required(login_url='/authentication/login/')
def daru_spin(request):
    # try:
    print('logged in',request.user)
    user = request.user
    return render(request, 'spinchannel/daru_spin.html',{'user': user})
    


# @login_required(login_url='/authentication/login/')
def spin(request):
    return render(request, 'spinchannel/daru_spin.html', {'user':request.user})