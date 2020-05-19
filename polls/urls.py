from django.urls import path
from . import views


urlpatterns = [
    path('testredis/', views.testredis, name='static'),
    path('getredis/', views.getredis, name='static'),
    path('liming/', views.index, name='index'),



    path('tologin/', views.tologin, name='signings'),
    path('check_api_token/', views.check_api_token, name='signings'),
    path('register_user/', views.register_user, name='signings'),
    path('check_pass/', views.check_pass, name='signings'),
    path('get_img/', views.get_img, name='signings'),

]