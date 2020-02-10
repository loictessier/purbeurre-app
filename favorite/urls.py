from django.urls import path

from . import views

app_name = 'favorite'

urlpatterns = [
    path('', views.favorites, name='favorites'),
    path('api/add_favorite/<int:substitute_product_id>/<int:origin_product_id>', views.add_favorite, name='add_favorite')
]