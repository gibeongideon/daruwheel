
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect ,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm

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

    return render(request, "users/accounts/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'User created.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "users/accounts/register.html", {"form": form, "msg" : msg, "success" : success })

@login_required(login_url='/users/login/')
def logout(request):
 
    return redirect(reverse('users:login'))


@login_required(login_url='/users/login/')
def user_page(request):
 
    # return redirect(reverse('users:user_page'))
    return render(request, 'users/page-user.html',{'user': request.user})

@login_required(login_url='/users/login/')
def notification(request):
    context={}
    return render(request, 'users/notification.html',context)
    

