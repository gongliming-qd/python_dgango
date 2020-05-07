from django.urls import path
from . import views


urlpatterns = [
    path('gong/', views.static, name='static'),
    path('index/', views.index, name='index'),
    path('api/liming/', views.index, name='index'),
    path('signing/', views.signings, name='signings'),
    # path('gong/', views.static1, name='static1'),
]