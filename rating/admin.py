from django.contrib import admin
from .models import RatingProduct


class AdminRatingProduct(admin.ModelAdmin):
    list_display = ('product', 'profile', 'rating')
    list_filter = ('product', 'profile', 'rating')
    ordering = ('product', 'rating', 'profile')
    search_field = ('product', 'rating', 'profile')


# Register your models here.
admin.site.register(RatingProduct, AdminRatingProduct)