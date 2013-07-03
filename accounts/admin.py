from accounts.models import RegistrationManager
from django.contrib import admin

class RegistrationManagerAdmin(admin.ModelAdmin):
    list_display = ('email', 'confirmation_code')
    search_fields = ['email', 'confirmation_code']

admin.site.register(RegistrationManager, RegistrationManagerAdmin)