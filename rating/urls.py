from django.urls import path

from . import views

app_name = 'rating'

urlpatterns = [
    path('post_rating_product/<int:product_id>', views.post_rating_product, name='post_rating_product'),
    path('api/add_rating_product/<int:product_id>/<int:rating>', views.add_rating_product, name='add_rating_product'),
    path('api/remove_rating_product/<int:product_id>', views.remove_rating_product, name='remove_rating_product'),
]