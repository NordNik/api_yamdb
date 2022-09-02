from django.contrib import admin


from .models import User, Categorie, Genre, Title, Comment, Review


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'email')
    list_editable = ('role', 'email')
    exclude = ('groups', 'user_permissions', 'is_staff')
    search_fields = ('username', 'email')
    readonly_fields = ('last_login', 'date_joined', 'password',)


admin.site.register(User, UserAdmin)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'category', 'rating')
    search_fields = ('name',)
    list_filter = ('category',)


admin.site.register(Title, TitleAdmin)
admin.site.register(Categorie)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
