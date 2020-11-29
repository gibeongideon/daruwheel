from account.serializers import AccountSerializer,TransactionLogSerializer
from rest_framework import viewsets
from account.models import Account,TransactionLog

from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAdminUser
# # from django.contrib.auth.models import User
from django.http import Http404 # HttpResponse
# from rest_framework import generics #, permissions, viewsets, serializers, permissions, filters, status



class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    

class TransactionLogViewSet(viewsets.ModelViewSet):
    queryset = TransactionLog.objects.all()
    serializer_class = TransactionLogSerializer

    search_fields = ('user', )

class TransactionView(APIView):
    """
    API View to get a list of all the TransactionLogs for TransactionLogs
    """
    # permission_classes = [IsAdminUser]

    def get(self,request,pk,start,limit, format=None):
        try:
            end =start+limit
            trans = TransactionLog.objects.filter(user_bal= pk).order_by('-id')[start:end]# cool huh
            # print(f'TRANS VIEW{trans}')
            serializer = TransactionLogSerializer(trans,many=True)
            return Response(serializer.data)
        except:
            raise Http404

