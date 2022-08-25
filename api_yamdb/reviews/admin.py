from django.contrib import admin

from .models import User, Categorie, Genre, Title, Comment

admin.site.register(User)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('title_name', 'categorie')
    search_fields = ('title_name',)
    list_filter = ('categorie',)


admin.site.register(Title, TitleAdmin)
admin.site.register(Categorie)
admin.site.register(Genre)
admin.site.register(Comment)
