from django.urls import path
from . import views


urlpatterns = [
    path('testredis/', views.testredis, name='static'),
    path('getredis/', views.getredis, name='static'),
    path('liming/', views.index, name='index'),


    # 登录部分
    path('tologin/', views.tologin, name='signings'),
    path('check_api_token/', views.check_api_token, name='signings'),


    # 文件部分
    path('get_img/', views.get_img, name='signings'),


    # 用户操作>修改信息
    path('get_userinfo_by_username/', views.get_userinfo_by_username, name='signings'),
    path('update_userinfo_by_id/', views.update_userinfo_by_id, name='signings'),

    # 个人信息修改部分
    path('get_api_username_all_info/', views.get_api_username_all_info, name='signings'),
    path('get_api_username_all_info_by_search/', views.get_api_username_all_info_by_search, name='signings'),
    path('add_api_username_all_info/', views.add_api_username_all_info, name='signings'),
    path('update_api_username_all_info/', views.update_api_username_all_info, name='signings'),
    path('dele_api_username_all_info/', views.dele_api_username_all_info, name='signings'),

]