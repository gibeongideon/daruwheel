from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect


@login_required(login_url='/users/login/')
def daru_spin(request):
    user = request.user
    return render(request, 'spinchannel/daru_spin.html',{'user': user})
    

