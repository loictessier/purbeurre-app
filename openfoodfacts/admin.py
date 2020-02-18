from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'nutriscore', 'category', 'popularity')
    list_filter = ('name', 'nutriscore', 'category',)
    ordering = ('category', 'nutriscore',)
    search_field = ('name')


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
