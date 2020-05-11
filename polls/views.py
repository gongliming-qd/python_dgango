from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from .utils.utils import use_mysql, create_token, check_token

def use_mysql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows
# 加密解密算法
def index(request):
    print(request.GET.get('name'))
    cursor = connection.cursor()
    cursor.execute("select * from member")
    rows = cursor.fetchall()
    rows = list(rows)
    result = []
    for key in rows:
        list_value = list(key)
        result.append({'id': list_value[0], 'name': list_value[1], 'sec': list_value[2], 'bobby': list_value[3], 'introduction': list_value[4]})
        # result.append(list_value)
    print(result)
    return JsonResponse(result, safe=False)
from django.core import signing
def signings(request):
    admin = request.GET.get('admin')
    psw = request.GET.get('psw')
    person = {'admin': admin, 'psw': psw}
    person_change = signing.dumps(person)
    print(person_change)
    person_cancel = signing.loads(person_change)
    print(person_cancel)

    return HttpResponse('HELLO')
def setcache(request):
    username = request.GET.get('username')
    print(username)
    # results = use_mysql('INSERT INTO token (username, token)  VALUES("%s","%s")'%(username, token))
    results = create_token(username)
    return JsonResponse({"code": 200, "message": "success", "results": results}, safe=False)
def getcache(request):
    username = request.GET.get('username')
    # print(token)
    results = use_mysql('select token from token where username="%(username)s"' %{"username": username})[0][0]
    # results = check_token(token)
    return JsonResponse({"code": 200, "message": "success", "results": results}, safe=False)
from django.core.cache import cache #引入缓存模块
def testredis(request):
    username = request.GET.get('username')
    cache.set(username, username, 30*60)
    results = cache.has_key(username)
    return JsonResponse(results, safe=False)
def getredis(request):
    username = request.GET.get('username')
    results = cache.get(username)
    return JsonResponse(results, safe=False)


# 登录部分
import json
def tologin(request):
    if request.method == 'POST':
        # 1. 获取账号密码
        username = json.loads(request.body)['username']
        psw = json.loads(request.body)['psw']
        # 2. 数据库取账号密码
        return_psw = use_mysql('select  psw from login_username_psw where username="%(username)s"'%{'username': username})[0][0]
        if return_psw == psw:
            # 3. 创建token, 返回token
            token = create_token(username)
            results = {'code': 200, "message": 'success', "token": token, "results": {}}
            return JsonResponse(results, safe=False)
        else:
            results = {'code':200, "message":'false',"results":{}}
            return JsonResponse(results, safe=False)


# 验证token是否正确
def check_api_token(request):
    token = request.GET.get('token')
    results = check_token(token)
    if results:
        results = {'code': 200, "message": 'success'}
        return JsonResponse(results, safe=False)
    else:
        results = {'code':200, "message":'false'}
        return JsonResponse(results, safe=False)