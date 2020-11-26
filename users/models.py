
# #  Author: gideon gibeon <kipngeno.gibeon@gmail.com>

# from django.db import models
# from django.contrib.auth.models import User
# # from django.db import transaction
# from django.db.models import Sum #,Count, Sum, F ,OuterRef
# from datetime import datetime, timedelta #,timezone
# from random import randint
# from django.utils import timezone
# from core.models import TimeStamp


# # User
# # user_name = phone_number
# # email = email_address
# # first_name = '' # own_refer_code
# # second_name = ''# refer_code
# # password = password


# class UserDetail(TimeStamp):
#     user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='users',blank =True,null=True)
#     phone_number = models.CharField(max_length=30,blank =True,null=True)
#     refer_code = models.CharField(max_length=30,blank =True,null=True)
#     own_refer_code = models.CharField(max_length=30,blank =True,null=True)

#     def __str__(self):
#         return f'{self.user}'

#     def user_name(self):
#         return self.user.username

#     def save(self, *args, **kwargs):
#         try:
#             if not self.own_refer_code:
#                 self.own_refer_code = 'SC'+str(self.user.username)

#         except Exception as e :
#             print(f'ACCOUNT:{e}')
#             return e

#         super().save(*args, **kwargs)