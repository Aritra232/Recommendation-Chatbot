from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from chatbot.models import userinfo,Account
class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Accounts'

class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInline, )



admin.site.register (userinfo)



admin.site.unregister(User)
admin.site.register (User,CustomizedUserAdmin)