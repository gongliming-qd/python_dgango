from django.urls import path
from . import views


urlpatterns = [
    path('liming', views.index, name='index'),
    path('/', views.static, name='static'),
    path('signing/', views.signings, name='signings'),
]