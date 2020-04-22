from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('liming/', views.static, name='static'),
    path('signing/', views.signings, name='signings'),
]