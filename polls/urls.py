from django.urls import path
from . import views


urlpatterns = [
    path('get_data', views.index, name='index'),
    path('index', views.static, name='static'),
    path('push_admin_psw', views.signings, name='signings'),
]