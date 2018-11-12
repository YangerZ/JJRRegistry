from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
import urllib.request
import urllib.parse
import json
from django.http import Http404
from django.shortcuts import get_object_or_404,render
import time
from .models import  Communityinfo
from .models import  Houseinfo
from .models import  UserGains
from .models import  GainsSum
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt, csrf_protect
# Create your views here.

def index(request):
      users = get_object_or_404(Communityinfo)
      return render(request, 'infos/index.html', json.dumps({'results':1000}, ensure_ascii=False))

@csrf_exempt
def addCommunityInfo(request):
    datas = None
    result = {}
    pages = 0
    try:
        objects = []
        print(request.POST)
        json_str = json.loads(request.body.decode('utf-8'))  # json.dumps(request.POST)
        # data1 = {
        #     'name': 'yichengshangbei' ,
        #     'provice':'tianjin',
        #     'city':'tianjin',
        #     'region': 'binhaixinqu',
        #     'district': 'tanggusxingang',
        #      'flag':0
        # }
        #
        # json_str=json.dumps(data1)
        filters = json.loads(json_str)
        if request.method == "GET" or request.method == "POST":
            name_=filters['name']
            province_=filters['province']
            city_=filters['city']
            region_ = filters['region']
            district_ = filters['district']
            flag_ = filters['flag']
            addtime_=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            community= Communityinfo(addtime=addtime_,name=name_,province=province_,city=city_,region=region_,district=district_,flag=flag_)
            community.save()
    except Exception as e:
        print(e)
        result['status'] = 404  # /200/404
        result['data'] = None
        result['msg'] = 'error:addCommunityInfo'
        result['pages'] = 0
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    result['status'] = 200  # /200/404
    result['data'] = None
    result['msg'] = 'succeed'
    result['pages'] = 0
    return HttpResponse(json.dumps(result, ensure_ascii=False))

@csrf_exempt
def getCommunityInfo(request):
    datas = None
    result = {}
    pages = 0
    try:
        objects = []
        print(request.POST)
        json_str = json.loads(request.body.decode('utf-8'))  # json.dumps(request.POST)
        # data1 = {
        #     'flag': 0,# 0 1 null
        #     'scoreflag':''
        #     'filter': {'name': ''},  '0' havent score  '1' have score
        #     'limit': 5,
        #     'page': 1
        # }
        #
        # json_str=json.dumps(data1)
        filters = json.loads(json_str)
        if request.method == "GET" or request.method == "POST":

            flag_ = filters['flag']
            scoreflag_ = filters['scoreflag']
            conds_ = filters['filter']
            name_ = conds_.get('name')


            orderkey='addtime'
            if(flag_ is None or flag_ is ''):
                if (name_ == ''):
                    datas = Communityinfo.objects.all().order_by(orderkey)
                if (name_ is not ''):
                    datas = Communityinfo.objects.filter(name__contains=name_).order_by(orderkey)
            else:
                if (name_ == ''):
                    datas = Communityinfo.objects.filter(flag=flag_).order_by(orderkey)
                if (name_ is not '' ):
                    datas = Communityinfo.objects.filter(flag=flag_,name__contains=name_).order_by(orderkey)
            #scoreflag query score state
            if(datas.count()>0):
                if(scoreflag_ is  None or scoreflag_ ==''):
                    datas=datas
                else:
                    datas=datas.filter(scoreflag=scoreflag_)
            limit_ = filters['limit']
            page_ = filters['page']
            paginator = Paginator(datas, limit_)
            pages = paginator.num_pages
            infos = paginator.get_page(page_)
            # override result objects from paginator obj
            for list in infos.object_list:
                object = {}
                obj_dict=list.__dict__
                for propertykey in obj_dict.keys():
                    pro_name=str(propertykey)
                    if(pro_name=='_state'):
                        pass
                    else:
                        object[pro_name] = obj_dict[pro_name]
                objects.append(object)

    except Exception as e:
        print(e)
        result['status'] = 404  # /200/404
        result['data'] = None
        result['msg'] = 'error:getuserinfo'
        result['pages'] = 0
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    result['status'] = 200  # /200/404
    result['data'] = objects
    result['msg'] = 'succeed'
    result['pages'] = pages
    return HttpResponse(json.dumps(result, ensure_ascii=False))

@csrf_exempt
def setCommunityGround(request):
    queryDict = request.GET['0']
    params = json.loads(queryDict.decode('utf-8'))
    id_ =params['id']  # 'ohPYu5fW92gzHSTn1wLl6EPd2gQ0'#
    flag_ =params['flag']  # '1'#queryDict.get('statu')
    datas = None
    result = {}
    try:
        Communityinfo.objects.filter(id=id_).update(flag=flag_)
        #time?
        #times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #Communityinfo.objects.filter(openid=userid_).update(flag=times)
        #rebackToWXRequest(userid_)
    except Exception as e:
        print(e)
        result['status'] = 404  # /200/404
        result['data'] = datas
        result['msg'] = 'error:setUserRegistryStatu'
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    result['status'] = 200  # /200/404
    result['data'] = datas
    result['msg'] = 'succeed'
    return HttpResponse(json.dumps(result, ensure_ascii=False))



@csrf_exempt
def getHouseInfo(request):
    datas = None
    result = {}
    pages = 0
    try:
        objects = []
        print(request.POST)
        json_str = json.loads(request.body.decode('utf-8'))  # json.dumps(request.POST)
        # data1 = {
        #     'communityid': '34',  #  null or id?
        #     'scoreflag':'0'|'1'
        #     'filter': {'housetype': '', 'orientation': ''},
        #     'limit': 5,
        #     'page': 1
        # }
        # json_str = json.dumps(data1)
        if request.method == "GET" or request.method == "POST":
            filters = json.loads(json_str)
            id_ = filters['communityid']
            conds_ = filters['filter']
            field1_ = conds_.get('housetype')
            field2_ = conds_.get('orientation')
            scoreflag_ = filters['scoreflag']
            orderkey = 'updatetime'

            if (id_ is None or id_ is ''):
                if (field1_ == '') and (field2_ == ''):
                    datas = Houseinfo.objects.all().order_by(orderkey)
                if (field1_ is not '' and field2_ == ''):
                    datas = Houseinfo.objects.filter(housetype__contains=field1_).order_by(orderkey)
                if (field2_ is not '' and field1_ == ''):
                    datas = Houseinfo.objects.filter(orientation__contains=field2_).order_by(orderkey)
                if (field1_ is not '' and field2_ is not ''):  # contains like '%%'
                    datas = Houseinfo.objects.filter(housetype__contains=field1_,
                                                     orientation__contains=field2_).order_by(orderkey)
            else:
                if (field1_ == '') and (field2_ == ''):
                    datas = Houseinfo.objects.filter(communityid=id_).order_by(orderkey)
                if (field1_ is not '' and field2_ == ''):
                    datas = Houseinfo.objects.filter(communityid=id_, housetype__contains=field1_).order_by(orderkey)
                if (field2_ is not '' and field1_ == ''):
                    datas = Houseinfo.objects.filter(communityid=id_, orientation__contains=field2_).order_by(orderkey)
                if (field2_ is not '' and field1_ is not ''):  # contains like '%%'
                    datas = Houseinfo.objects.filter(communityid=id_, housetype__contains=field1_,
                                                     orientation__contains=field2_).order_by(orderkey)

            # scoreflag query score state
            if (datas.count() > 0):
                if (scoreflag_ is None or scoreflag_ == ''):
                    datas = datas
                else:
                    datas = datas.filter(scoreflag=scoreflag_)
            limit_ = filters['limit']
            page_ = filters['page']
            paginator = Paginator(datas, limit_)
            pages = paginator.num_pages
            infos = paginator.get_page(page_)
            # override result objects from paginator obj
            for list in infos.object_list:
                object = {}
                obj_dict = list.__dict__
                for propertykey in obj_dict.keys():
                    pro_name = str(propertykey)
                    if (pro_name == '_state'):
                        pass
                    else:
                        object[pro_name] = obj_dict[pro_name]
                objects.append(object)

    except Exception as e:
        print(e)
        result['status'] = 404  # /200/404
        result['data'] = None
        result['msg'] = 'error:getuserinfo'
        result['pages'] = 0
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    result['status'] = 200  # /200/404
    result['data'] = objects
    result['msg'] = 'succeed'
    result['pages'] = pages
    return HttpResponse(json.dumps(result, ensure_ascii=False))

@csrf_exempt
def setScoreOnInfo(request):
    datas = None
    result = {}
    pages = 0
    try:
        objects = []
        print(request.POST)
        json_str = json.loads(request.body.decode('utf-8'))  # json.dumps(request.POST)
        # data1 = {
        #     'openid': '34',  #user openid  null or id?
        #     'infoid': '', #communityid or houseinfoid
        #     'scorer':'',  #person who score this info
        #     'gains_reson':'',  #type community or house 1 or 2
        #     'gains_value':2.30  # the value is double
        #     'operate':'' #score|get|balabala
        #     'img':'' #not used now
        #     'others':'' some message about this
        #
        # }
        # json_str = json.dumps(data1)
        if request.method == "GET" or request.method == "POST":
            filters = json.loads(json_str)
            openid_ = filters['openid']
            infoid_ = filters['infoid']
            scorer_ = filters['scorer']
            gains_reson_ = filters['gains_reson']
            gains_value_ = filters['gains_value']
            operate_=filters['operate']
            others_=filters['others']
            addtime_ = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if(infoid_ is not ''):
                if(gains_reson_ =='1' and operate_=='score'):
                    Communityinfo.objects.filter(id=infoid_).update(scoreflag='1')
                if(gains_reson_=='2' and operate_=='score'):
                    Houseinfo.objects.filter(id=infoid_).update(scoreflag='1')
                    house=Houseinfo.objects.get(id=infoid_)
                    communitys=Communityinfo.objects.filter(id=house.communityid)
                    openid_=communitys[0].openid
            gains = UserGains(openid=openid_, infoid=infoid_, scorer=scorer_, gains_reson=gains_reson_, gains_value=gains_value_,gains_datetime=addtime_,operate=operate_,others=others_)
            gains.save()
    except Exception as e:
        print(e)
        result['status'] = 404  # /200/404
        result['data'] = None
        result['msg'] = 'error:setScoreOnInfo'
        result['pages'] = 0
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    result['status'] = 200  # /200/404
    result['data'] = objects
    result['msg'] = 'succeed'
    result['pages'] = pages
    return HttpResponse(json.dumps(result, ensure_ascii=False))

@csrf_exempt
def getGainsSum(request):
    datas = None
    result = {}
    pages = 0
    try:
        objects = []
        print(request.POST)
        json_str = json.loads(request.body.decode('utf-8'))  # json.dumps(request.POST)
        # data1 = {
        #
        #
        #     'name':'',
        #     'phone':'',
        #     'limit': 5,
        #     'page': 1
        # }
        #
        # json_str=json.dumps(data1)
        filters = json.loads(json_str)
        if request.method == "GET" or request.method == "POST":
            name_ = filters['name']
            phone_=filters['phone']
            if (name_ is '' and  phone_ is ''):
                datas = GainsSum.objects.all()
            if(name_ is not '' and phone_ is ''):
                datas = GainsSum.objects.filter(name__contains=name_)
            if (phone_ is not '' and name_ is ''):
                datas = GainsSum.objects.filter(phone__contains=phone_)
            if (phone_ is not '' and name_ is not ''):
                datas = GainsSum.objects.filter(name__contains=name_,phone__contains=phone_)
            limit_ = filters['limit']
            page_ = filters['page']
            paginator = Paginator(datas, limit_)
            pages = paginator.num_pages
            infos = paginator.get_page(page_)
            # override result objects from paginator obj
            for list in infos.object_list:
                object = {}
                obj_dict = list.__dict__
                for propertykey in obj_dict.keys():
                    pro_name = str(propertykey)
                    if (pro_name == '_state'):
                        pass
                    else:
                        object[pro_name] = obj_dict[pro_name]
                objects.append(object)

    except Exception as e:
        print(e)
        result['status'] = 404  # /200/404
        result['data'] = None
        result['msg'] = 'error:getGainsSum'
        result['pages'] = 0
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    result['status'] = 200  # /200/404
    result['data'] = objects
    result['msg'] = 'succeed'
    result['pages'] = pages
    return HttpResponse(json.dumps(result, ensure_ascii=False))

@csrf_exempt
def getInfoGains(request):
    datas = None
    result = {}
    pages = 0
    try:
        objects = []
        print(request.POST)
        json_str = json.loads(request.body.decode('utf-8'))  # json.dumps(request.POST)
        # data1 = {
        #     'openid':'',
        #     'infoid':'',
        #     'operate':'',
        #     'gains_reson': 5,
        # }
        #
        # json_str=json.dumps(data1)
        filters = json.loads(json_str)
        if request.method == "GET" or request.method == "POST":
            openid_ = filters['openid']
            infoid_ = filters['infoid']
            operate_ = filters['operate']
            gains_reson_ = filters['gains_reson']

            if(gains_reson_=='2'):

                house = Houseinfo.objects.get(id=infoid_)
                communitys = Communityinfo.objects.filter(id=house.communityid)
                openid_ = communitys[0].openid
            datas=UserGains.objects.filter(openid=openid_,infoid=infoid_,operate=operate_,gains_reson=gains_reson_)
            limit_ = '1'
            page_ = '1'
            paginator = Paginator(datas, limit_)
            pages = paginator.num_pages
            infos = paginator.get_page(page_)
            # override result objects from paginator obj
            for list in infos.object_list:
                object = {}
                obj_dict = list.__dict__
                for propertykey in obj_dict.keys():
                    pro_name = str(propertykey)
                    if (pro_name == '_state'):
                        pass
                    else:
                        object[pro_name] = obj_dict[pro_name]
                objects.append(object)

    except Exception as e:
        print(e)
        result['status'] = 404  # /200/404
        result['data'] = None
        result['msg'] = 'error:getInfoGains'
        result['pages'] = 0
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    result['status'] = 200  # /200/404
    result['data'] = objects
    result['msg'] = 'succeed'
    result['pages'] = pages
    return HttpResponse(json.dumps(result, ensure_ascii=False))

@csrf_exempt
def checkUserBalance(request):

    datas = None
    result = {}
    pages = 0
    try:
        objects = []
        print(request.POST)
        json_str = json.loads(request.body.decode('utf-8'))  # json.dumps(request.POST)
        # data1 = {
        #     'openid':'',
        # }
        #
        # json_str=json.dumps(data1)
        filters = json.loads(json_str)
        if request.method == "GET" or request.method == "POST":
            openid_ = filters['openid']
            datas=GainsSum.objects.filter(openid=openid_)
            limit_ =1
            page_ =1
            paginator = Paginator(datas, limit_)
            pages = paginator.num_pages
            infos = paginator.get_page(page_)
            # override result objects from paginator obj
            for list in infos.object_list:
                object = {}
                obj_dict = list.__dict__
                for propertykey in obj_dict.keys():
                    pro_name = str(propertykey)
                    if (pro_name == '_state'):
                        pass
                    else:
                        object[pro_name] = obj_dict[pro_name]
                objects.append(object)

    except Exception as e:
        print(e)
        result['status'] = 404  # /200/404
        result['data'] = None
        result['msg'] = 'error:checkUserBalance'
        result['pages'] = 0
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    result['status'] = 200  # /200/404
    result['data'] = objects
    result['msg'] = 'succeed'
    result['pages'] = pages
    return HttpResponse(json.dumps(result, ensure_ascii=False))