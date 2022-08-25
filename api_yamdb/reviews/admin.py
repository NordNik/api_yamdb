from django.contrib import admin

from .models import User, Categorie, Genre, Title, Comment


class UserAdmin(admin.ModelAdmin):
    exclude = ('groups', 'user_permissions', 'is_staff')
    search_fields = ('username', 'email')
    readonly_fields = ('last_login', 'date_joined')


admin.site.register(User, UserAdmin)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('title_name', 'categorie')
    search_fields = ('title_name',)
    list_filter = ('categorie',)


admin.site.register(Title, TitleAdmin)
admin.site.register(Categorie)
admin.site.register(Genre)
admin.site.register(Comment)
