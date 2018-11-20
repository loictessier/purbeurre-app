from django.conf.urls import url

from . import views

app_name = 'user'

urlpatterns = [
    url(r'^login$', views.authentication, name='authentication'),
    url(r'^logout$', views.view_logout, name='logout'),
    url(r'^signup$', views.sign_up, name='signup')
]