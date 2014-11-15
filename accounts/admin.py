from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from accounts.models import Client, Lawyer

class ClientInline(admin.StackedInline):
	model = Client
	# can_delete = False
	verbose_name_plural = 'client'

class LawyerInline(admin.StackedInline):
	model = Lawyer
	# can_delete = False
	verbose_name_plural = 'lawyer'

class UserAdmin(UserAdmin):
	inlines = (ClientInline, LawyerInline)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
