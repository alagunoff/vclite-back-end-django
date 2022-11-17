from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username')
    list_filter = ('is_admin',)
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'avatar'),
        }),
        ('Permissions', {'fields': ('is_admin', 'is_superuser')})
    )
    fieldsets = (
        (None, {'fields': ('username', 'password',
         'first_name', 'last_name', 'avatar')}),
        ('Permissions', {'fields': ('is_admin',
         'is_superuser', 'groups', 'user_permissions')}),
    )


admin.site.register(User, UserAdmin)
