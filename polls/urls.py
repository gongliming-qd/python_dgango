from django.urls import path
from . import views


urlpatterns = [
    path('setcache/', views.setcache, name='static'),
    path('getcache/', views.getcache, name='static'),
    path('testredis/', views.testredis, name='static'),
    path('getredis/', views.getredis, name='static'),
    path('index/', views.index, name='index'),
    path('liming/', views.index, name='index'),
    path('signing/', views.signings, name='signings'),
]