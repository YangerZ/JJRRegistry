from django.urls import path
from . import  views

app_name='polls'
urlpatterns=[


    path('user/login/',views.UserLoginHandle),
    path('user/info/',views.getUserInfo),
    path('user/logout/',views.UserLogoutHandle),

    #ex:/polls/
    path('',views.index,name='index'),

    path('Get/',views.getRegistryUserInfo,name='getRegistryUserInfo'),
    #
    path('Set/',views.setUserRegistryStatu,name='setUserRegistryStatu')
    #

    #path('Delete/',views.deleteRegistryUser,name='deleteRegistryUser')


]
