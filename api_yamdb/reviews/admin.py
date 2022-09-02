from django.contrib import admin


from .models import User, Categorie, Genre, Title, Comment, Review


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'email')
    list_editable = ('role', 'email')
    exclude = ('groups', 'user_permissions', 'is_staff')
    search_fields = ('username', 'email')
    readonly_fields = (
        'last_login', 'date_joined', 'password', 'confirmation_code')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'category', 'rating')
    search_fields = ('name',)
    list_filter = ('category',)


@admin.register(Genre, Categorie, Review, Comment)
class TitlePropertiesAdmin(admin.ModelAdmin):
    pass
