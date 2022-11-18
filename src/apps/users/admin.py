from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    search_fields = ('username', 'first_name', 'last_name')
    list_display = ('username',)
    list_filter = ('is_admin',)
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'avatar'),
        }),
        ('Permissions', {'fields': ('is_admin', 'is_superuser')})
    )
    fieldsets = (
        (None, {'fields': ('username', 'password',
         'first_name', 'last_name', 'avatar', 'avatar_preview')}),
        ('Permissions', {'fields': ('is_admin',
         'is_superuser', 'groups', 'user_permissions')}),
    )
    readonly_fields = ('avatar_preview',)

    def avatar_preview(self, obj: User) -> str:
        return obj.avatar_preview

    avatar_preview.short_description = 'Avatar Preview'
    avatar_preview.allow_tags = True


admin.site.register(User, UserAdmin)
