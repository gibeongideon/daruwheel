# from django.shortcuts import render
# from django.contrib.auth.models import User
# from rest_framework.views import APIView
from django.contrib.auth.models import User

from users.serializers import *
from rest_framework import viewsets
from .models import *



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer