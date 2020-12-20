
from django.contrib import admin
from .models import SetPasswordModel
class SetPasswordModelAdmin(admin.ModelAdmin):
    list_display = ('id','user','new_password1', 'new_password2',)
    list_display_links = ('user',)
    search_fields = ('user',)
    ordering = ('user',)

admin.site.register(SetPasswordModel, SetPasswordModelAdmin)


# from django.contrib import admin
# from spinchannel.models import LoggedInUser

# class LoggedInUserAdmin(admin.ModelAdmin):
#     list_display = ('id','user')
#     list_display_links = ('id',)
#     # list_editable = ('',)

# admin.site.register(LoggedInUser, LoggedInUserAdmin) 
