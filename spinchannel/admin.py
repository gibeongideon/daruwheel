from django.contrib import admin
from spinchannel.models import LoggedInUser

class LoggedInUserAdmin(admin.ModelAdmin):
    list_display = ('id','user')
    list_display_links = ('id',)
    # list_editable = ('',)

admin.site.register(LoggedInUser, LoggedInUserAdmin) 

