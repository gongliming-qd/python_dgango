from django.urls import path
from . import views


urlpatterns = [
    path('liming/shuijj/', views.index, name='index'),
    path('liming/gong/', views.static, name='static'),
    path('liming/signing/', views.signings, name='signings'),
    path('liming/signing111/', views.index, name='signings'),
    # path('gong/', views.static1, name='static1'),
]