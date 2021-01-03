from rest_framework import viewsets
from .models import SetPasswordModel

from .serializers import UserSerializer#,SetPasswordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
# from django.contrib.auth.models import User
from .models import User
from django.http import HttpResponse, Http404
from rest_framework import generics #, permissions, viewsets, serializers, permissions, filters, status

class UserRecordView(APIView):
    """
    API View to create or get a list of all the registered
    users. GET request returns the registered users whereas
    a POST request allows to create a new user.
    """
    # permission_classes = [IsAdminUser]

    # def check_if_code_exists(self):
    #     dacodes =[]
    #     for duser in User.objects.all():
    #         dacodes.append(duser.my_code)
    #     return dacodes

    def get(self, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


    def post(self, request):
        # print(request.data)#first_name to be own_refer_code
        request.data['my_code']= 'DA'+ request.data['username'] #USE  first_name as  own_refer_code

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



# class SetPasswordViewSet(viewsets.ModelViewSet):
#     queryset = SetPasswordModel.objects.all()
#     serializer_class = SetPasswordSerializer

# class UserIDView(APIView):
#     """
#     API View to get a a user details like id by passing username
#     # implement url /user_detail=<user_name>
#     """
#     def get(self,request,user_name,format=None):
#         try:
#             user_id =User.objects.get(username= str(user_name)).id
#             user_info ={'user_id':user_id,'username':user_name,}
#             return Response(user_info)

#         except :# Exception as e:
#             # return Response({'error':e.args})
#             raise Http404