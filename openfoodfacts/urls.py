from django.urls import path

from . import views

app_name = 'openfoodfacts'

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('results/<int:rating_filter>/', views.results, name='results'),
    path('results_with_filter/<str:search_input>/', views.results_with_filter, name='results_with_filter'),
    path('detail/<int:product_id>/', views.product_detail, name='detail'),
    path('api/get_products/', views.get_products, name='get_products'),
]
