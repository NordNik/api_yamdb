from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    exclude = ('groups', 'user_permissions', 'is_staff')
    search_fields = ('username', 'email')
    readonly_fields = ('last_login', 'date_joined')


admin.site.register(User, UserAdmin)
