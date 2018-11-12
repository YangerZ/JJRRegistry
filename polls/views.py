from django.http import HttpResponse
from .models import UserInfoStatu
from .models import UserApprove
from .models import CollectFormid
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
import urllib.request
import urllib.parse
import json
from django.http import Http404
from django.shortcuts import get_object_or_404,render
import time

from django.core import serializers
from django.views.decorators.csrf import csrf_exempt, csrf_protect

# Create your views here.
def UserLoginHandle(req):
    status = 200  # 404/500/0
    data = {'token':'1'}
    msg = 'ok'
    resp = {'status': status, 'msg': msg, 'data': data}
    return HttpResponse(json.dumps(resp), content_type="application/json")
def getUserInfo(req):
    status = 200  # 404/500/0
    data = {'roles':[1],'name':'admin','avatar':'https://cdn.v2ex.com/avatar/774c/13cb/138371_large.png?m=1443502327'}
    msg = 'ok'
    resp = {'status': status, 'msg': msg, 'data': data}
    return HttpResponse(json.dumps(resp), content_type="application/json")
def UserLogoutHandle(req):
    status = 200  # 404/500/0
    data = { }
    msg = 'ok'
    resp = {'status': status, 'msg': msg, 'data': data}
    return HttpResponse(json.dumps(resp), content_type="application/json")

def index(request):
    users = get_object_or_404(UserInfoStatu)
    return render(request, 'polls/index.html', {'UserInfoStatu': users})


#not used now
def addUserInfo(request):
    # try:
    #     jsonData = '{"username":"test","sex":"male","tel":"220334","company":"sws","registry":"0","time":"20181023","desc":"sadsadsa","other":"dsasad"}';
    #     formdata = json.loads(jsonData)
    #     username_=formdata['username']
    #     sex_ = formdata['sex']
    #     tel_ = formdata['tel']
    #     company_ = formdata['company']
    #     registry_ = formdata['registry']
    #     time_=  formdata['time']
    #     desc_ = formdata['desc']
    #     other_ =  formdata['other']
    #     newuser= Managerregistry(username=username_,sex=sex_,tel=tel_,company=company_,registry=registry_)
    #     newuser.save()
    # except Managerregistry.DoesNotExist:
    #     raise Http404("Question does not exist")
    return HttpResponse("<p>Success add!</p>")
@csrf_exempt
def getRegistryUserInfo(request):
    datas = None
    result = {}
    pages=0
    try:

        objects = []
        print(request.POST)
        json_str = json.loads(request.body.decode('utf-8'))# json.dumps(request.POST)
        # data1 = {
        #     'statu': 1,
        #     'filter': {'name': '', 'phone': ''},
        #     'limit': 1,
        #     'page': 1
        # }
        #json_str=json.dumps(data1)
        if request.method == "GET" or request.method == "POST":
            filters=json.loads(json_str)
            statu_=filters['statu']
            conds_ = filters['filter']
            name_ = conds_.get('name')
            telnumber_ = conds_.get('phone')


            orderkey='datetimes' if statu_==1 else 'approvetimes'
            if(name_=='') and (telnumber_==''):
                datas = UserInfoStatu.objects.filter(flag=statu_).order_by(orderkey)
            if(name_ is not '' and telnumber_==''):
                datas = UserInfoStatu.objects.filter(flag=statu_,name__contains=name_).order_by(orderkey)
            if(telnumber_ is not '' and name_ == ''):
                datas = UserInfoStatu.objects.filter(flag=statu_,phone__contains=telnumber_).order_by(orderkey)
            if(telnumber_ is not '' and name_ is not ''):#contains like '%%' registry ==0,1,2
                datas = UserInfoStatu.objects.filter(flag=statu_,name__contains=name_,phone__contains=telnumber_).order_by(orderkey)

            limit_ = filters['limit']
            page_ = filters['page']
            paginator = Paginator(datas,limit_)
            pages=paginator.num_pages
            userinfos=paginator.get_page(page_)

            for list in userinfos.object_list:
                object={}
                object['id']=list.id
                object['userid'] = list.userid
                object['flag'] = list.flag
                object['datetimes'] = list.datetimes
                object['approvetimes'] = list.approvetimes
                object['name'] = list.name
                object['age'] = list.age
                object['phone'] = list.phone
                object['sex'] = list.sex
                object['worktype'] = list.worktype
                object['workcompany'] = list.workcompany
                objects.append(object)

    except Exception as e:
        print(e)
        result['status'] = 404  # /200/404
        result['data'] = None
        result['msg'] = 'error:getuserinfo'
        result['pages'] =0
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    result['status']=200 #/200/404
    result['data']=objects
    result['msg']='succeed'
    result['pages']=pages
    return HttpResponse(json.dumps(result, ensure_ascii=False))
@csrf_exempt
def setUserRegistryStatu(request):
    queryDict=request.GET['0']
    params=json.loads(queryDict)
    id_=params['userid']#'ohPYu5fW92gzHSTn1wLl6EPd2gQ0'#
    statu_ =params['statu']#'1'#queryDict.get('statu')
    datas = None
    result = {}
    try:
        UserApprove.objects.filter(iduser_approve=id_).update(flag=statu_)
        times=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        UserApprove.objects.filter(iduser_approve=id_).update(user_approvecol=times)
        rebackToWXRequest(id_)
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


def rebackToWXRequest(id):
    APPID = "wx8e7dbabea90c2fe8"
    APPSECRET = "b407bdfa1fd447ecba7796961b95a91b"
    geturl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + APPID + "&secret=" + APPSECRET

    req = urllib.request.Request(geturl)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    result = json.loads(the_page.decode('utf-8'))
    ACCESSTOKEN = result["access_token"]
    posturl = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=" + ACCESSTOKEN

    #get approve info from db
    #userid='ohPYu5fW92gzHSTn1wLl6EPd2gQ0'
    userinfo=UserApprove.objects.get(iduser_approve=id)
    forminfos=CollectFormid.objects.filter(openid=userinfo.openid,frombtn='reg',other1=None).order_by('-datetime')
    print(userinfo.flag)
    print(forminfos[0])
    forminfo=forminfos[0]
    print(forminfo.formid)

    #userapprovestatus falg 1unapprove  2 yes 3 no
    flag_=userinfo.flag
    statu_=""
    bz_=""
    if(flag_==0 or flag_==1):
        return
    if(flag_==2):
        statu_="通过"
        bz_="管理员已审核通过您的注册信息"
    if(flag_==3):
        statu_="未通过"
        bz_="您的注册信息暂不满足要求"
    approvetime_=userinfo.user_approvecol
    openid = userinfo.openid
    formid = forminfo.formid
    print("openid:"+openid,"flag:"+str(flag_),"approvetime:"+approvetime_,"formid:"+formid)
    # old template id is "DHy9FxplFYFB4KYH79_6670Xuvs7qsyW08EHBpRg-80"
    data = json.dumps(
        {"access_token": "", "touser": openid, "template_id":"PN-rXAtzhuVZP94ygITqQOuZrpUG6xG26WWhJMLLSwo"
 ,
         "page": "subscribes", "form_id": formid,
         "data": {
             "keyword1": {
                 "value": statu_
             },
             "keyword2": {
                 "value": approvetime_
             },
             "keyword3": {
                 "value": bz_
             }
         }
         })
    d=data.encode('utf-8')
    req = urllib.request.Request(posturl, d, {'Content-Type': 'application/json'})
    f = urllib.request.urlopen(req)
    response = f.read()
    print(response)
    f.close()
    #insert sql to db

    CollectFormid.objects.filter(openid=openid,frombtn='reg').update(other1='1')
    return