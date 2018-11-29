from django.urls import path

from . import views

app_name = 'openfoodfacts'

urlpatterns = [
    path('/', views.search, name='search'),
    path('results/', views.results, name='results')
]
