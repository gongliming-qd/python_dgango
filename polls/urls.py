from django.urls import path
from . import views


urlpatterns = [
    path('testredis/', views.testredis, name='static'),
    path('getredis/', views.getredis, name='static'),
    path('liming/', views.index, name='index'),



    path('tologin/', views.tologin, name='signings'),
    path('check_api_token/', views.check_api_token, name='signings'),
    path('check_pass/', views.check_pass, name='signings'),
    path('get_img/', views.get_img, name='signings'),


#    个人信息修改部分

    path('get_api_username_all_info/', views.get_api_username_all_info, name='signings'),
    path('get_api_username_all_info_by_search/', views.get_api_username_all_info_by_search, name='signings'),
    path('add_api_username_all_info/', views.add_api_username_all_info, name='signings'),
    path('update_api_username_all_info/', views.update_api_username_all_info, name='signings'),
    path('dele_api_username_all_info/', views.dele_api_username_all_info, name='signings'),

]