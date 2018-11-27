from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.authentication, name='authentication'),
    path('logout/', views.view_logout, name='logout'),
    path('signup/', views.sign_up, name='signup')
]