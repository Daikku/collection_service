from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    list_display_links = ('id', 'username')
    exclude = ('password', 'last_login', 'groups', 'user_permissions',
               'is_superuser', 'is_active', 'is_staff', 'date_joined')