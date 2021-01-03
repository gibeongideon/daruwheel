from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

from .models import  User#
# (
    # User)# Currency, User_Deposit, User_Withdraw, Roulette_Bet, RouletteRound,
 #   Seed, Message
#)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','phone_number','email','first_name', 'last_name','my_code','daru_code','last_login',)
    list_display_links = ('id',)
    search_fields = ('id',)
    ordering = ('id',)
    readonly_fields =('password',)

admin.site.register(User, UserAdmin)

















# from django.contrib import admin
from .models import SetPasswordModel
class SetPasswordModelAdmin(admin.ModelAdmin):
    list_display = ('id','user','new_password1', 'new_password2',)
    list_display_links = ('user',)
    search_fields = ('user',)
    ordering = ('user',)

admin.site.register(SetPasswordModel, SetPasswordModelAdmin)


# # from django.contrib import admin
# # from spinchannel.models import LoggedInUser

# # class LoggedInUserAdmin(admin.ModelAdmin):
# #     list_display = ('id','user')
# #     list_display_links = ('id',)
# #     # list_editable = ('',)

# # admin.site.register(LoggedInUser, LoggedInUserAdmin) 
