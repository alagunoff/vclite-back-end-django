from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username', 'password',
         'first_name', 'last_name', 'avatar']}),
        ('Permissions', {'fields': [
         'is_admin', 'is_superuser', 'groups', 'user_permissions']}),
    ]


admin.site.register(User, UserAdmin)
