from django.contrib import admin
from .models import Favorite


class AdminFavorite(admin.ModelAdmin):
    list_display = ('product', 'profile')
    list_filter = ('product', 'profile')
    ordering = ('profile', 'product')
    search_field = ('product', 'profile')


# Register your models here.
admin.site.register(Favorite, AdminFavorite)