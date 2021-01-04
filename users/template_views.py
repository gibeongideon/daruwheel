
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect ,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login 
from django.http import HttpResponseNotFound
from django.contrib.auth import views as auth_views
# from django.contrib.auth.models import User
from .models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import  SignUpForm,SignUpForm2 ,LoginForm2


def login_view(request):
    form = LoginForm2(request.POST or None)

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
    


def mine_users(request):
    mine_users =list(User.objects.filter(last_name =request.user.first_name))
    print(f'Mine USERS{mine_users}')
    
    return render(request, 'users/mine_users.html',{'mine_users': mine_users})



# """Controll GET and POST requests for all casino functionality."""
# from autobahn.wamp.exception import ApplicationError
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib.auth import login, authenticate
# from django.utils import timezone
# from casino import settings
# from website.exceptions import NegativeTokens
# from website.models import (
#     User, Currency, Roulette_Bet, RouletteRound, Seed, User_Withdraw, Message
# )



class CustomLoginView(auth_views.LoginView):
    """Collect methods which extends django authentication functionality."""

    def form_valid(self, form):
        """Extend basic validation with user remember functionality.

        Check if remember checkbox was set by user and store session data
        in such case.
        """
        if self.request.POST.get('remember_me', None):
            self.request.session.set_expiry(0)
        return super().form_valid(form)


def register(request):
    """Responsible for validation and creation of new users.

    Check if all required inputs are filled, if password and
    password confirmation are equal, if user with posted username
    already not exists and then create new user with possible friend username
    or blank string. After succesed registration proceed authentication
    and redirect to index path, otherwise return error messages to source
    registration form.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            phone_number = form.cleaned_data.get('phone_number')
            user = authenticate(username=username, password=raw_password)
            user.phone_number = phone_number
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

