from gwheel.serializers import MarketInstanceSerializer,StakeSerializer
from rest_framework import viewsets
from gwheel.models import  WheelSpin ,Stake


# from .serializers import UserSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAdminUser
# from django.contrib.auth.models import User
# from django.http import HttpResponse, Http404
# from rest_framework import generics #, permissions, viewsets, serializers, permissions, filters, status


class MarketInstanceViewSet(viewsets.ModelViewSet):
    queryset = WheelSpin.objects.all()
    serializer_class = MarketInstanceSerializer


class StakeViewSet(viewsets.ModelViewSet):
    queryset = Stake.objects.all()
    serializer_class = StakeSerializer

