
from django.contrib import admin
from users.models import SetPasswordModel
class SetPasswordModelAdmin(admin.ModelAdmin):
    list_display = ('id','user','new_password1', 'new_password2',)
    list_display_links = ('user',)
    search_fields = ('user',)
    ordering = ('user',)

admin.site.register(SetPasswordModel, SetPasswordModelAdmin)