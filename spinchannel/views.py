from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.shortcuts import render, redirect

from account.models import TransactionLog


User = get_user_model()


@login_required(login_url='/spin/log_in/')
def user_list(request):
    """
    NOTE: This is fine for demonstration purposes, but this should be
    refactored before we deploy this app to production.
    Imagine how 100,000 users logging in and out of our app would affect
    the performance of this code!
    """
    users = User.objects.select_related('logged_in_user')
    for user in users:
        user.status = 'Online' if hasattr(user, 'logged_in_user') else 'Offline'
    return render(request, 'spinchannel/user_list.html', {'users': users})
    
@login_required(login_url='/spin/login/')
def daru_spin(request):
    # try:
    print('logged in',request.user)
    user = request.user
    Account.objects.update_or_create(user=user)
    # user = User.objects.get_or_create('logged_in_user')
    return render(request, 'spinchannel/daru_spin.html',{'user': user})
    

@login_required(login_url='/spin/log_in/')
def history(request):
    try:
        stakes = TransactionLog.objects.filter(user= request.user)
        # user = User.objects.get_or_create('logged_in_user')
        context = {'stakes': stakes}
        print(stakes)
        return render(request, 'spinchannel/history.html',context)
    except Exception as e:
        print('HISS',e)

def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print('LOG U',request.user) 
            login(request, form.get_user())
            return redirect(reverse('spinchannel:daru_spin'))
        else:
            print(form.errors)
    # print('FORM',form)
    return render(request, 'spinchannel/accounts/login.html', {'form': form})


@login_required(login_url='/spin/log_in/')
def log_out(request):
    logout(request)
    return redirect(reverse('spinchannel:log_in'))


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('spinchannel:log_in'))
        else:
            print(form.errors)
    return render(request, 'spinchannel/sign_up.html', {'form': form})
    
    
    
  #vz]
  
  
 #from django.shortcuts import render

# Create your views here.
#from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm
from account.models import Account

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def register_user(request):

    # form = UserCreationForm()
    # if request.method == 'POST':
        # form = UserCreationForm(data=request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get("username")
            # raw_password = form.cleaned_data.get("password1")
            # authenticate(username=username, password=raw_password) #auto log in

            # msg     = 'User created.'
            # success = True

            return redirect(reverse('spinchannel:log_in'))
        else:
            print(form.errors)
        return render(request, 'spinchannel/accounts/register.html', {'form': form})

    # msg     = None
    # success = False
# 
    # if request.method == "POST":
    #     form = SignUpForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data.get("username")
    #         raw_password = form.cleaned_data.get("password1")
    #         user = authenticate(username=username, password=raw_password) #auto log in

    #         msg     = 'User created.'
    #         success = True
            
    #         #return redirect("/login/")

    #     else:
    #         msg = 'Form is not valid'    
    # else:
    #     form = SignUpForm()
