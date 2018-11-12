from django.urls import path
from . import  views

app_name='infos'
urlpatterns=[
    #ex:/infos/
    path('CommunityInfos/Add/',views.addCommunityInfo,name='addCommunityInfo'),
    path('CommunityInfos/Get/',views.getCommunityInfo,name='getCommunityInfo'),
    path('CommunityGround/Set/',views.setCommunityGround,name='setCommunityGround'),
    path('HouseInfos/Get/',views.getHouseInfo,name='getHouseInfo'),
    path('ScoreInfos/Set/',views.setScoreOnInfo,name='setScoreOnInfo'),
    path('InfoGains/Get/',views.getInfoGains,name='getInfoGains'),
    path('UserGains/Get/',views.getGainsSum,name='getGainsSum'),
    path('CheckUserBalance/Get/',views.checkUserBalance,name='checkUserBalance')
]