from django.urls import path
from . import views


urlpatterns = [
    path('api/liming/', views.index, name='index'),
    path('gong/', views.static, name='static'),
    path('signing/', views.signings, name='signings'),
    # path('gong/', views.static1, name='static1'),
]