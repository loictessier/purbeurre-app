from django.urls import path

from . import views

app_name = 'openfoodfacts'

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('detail/<int:product_id>/', views.product_detail, name='detail'),
    path('api/get_products/', views.get_products, name='get_products')
]
