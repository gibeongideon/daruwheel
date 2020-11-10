from users.serializers import *
from rest_framework import viewsets
from .models import *


from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from rest_framework import generics #, permissions, viewsets, serializers, permissions, filters, status

class UserRecordView(APIView):
    """
    API View to create or get a list of all the registered
    users. GET request returns the registered users whereas
    a POST request allows to create a new user.
    """
    # permission_classes = [IsAdminUser]

    def get(self, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )




class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = UserDetail.objects.all()
    serializer_class = UserProfileSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    

class MarketInstanceViewSet(viewsets.ModelViewSet):
    queryset = MarketInstance.objects.all()
    serializer_class = MarketInstanceSerializer


class StakeViewSet(viewsets.ModelViewSet):
    queryset = Stake.objects.all()
    serializer_class = StakeSerializer


class BalanceViewSet(viewsets.ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer

    search_fields = ('user_bal', )

class TransactionView(APIView):
    """
    API View to get a list of all the Balances for Balances
    """
    # permission_classes = [IsAdminUser]

    def get(self,request,pk, format=None):
        trans = Balance.objects.filter(user_bal= pk)
        serializer = BalanceSerializer(trans,many=True)
        return Response(serializer.data) 

