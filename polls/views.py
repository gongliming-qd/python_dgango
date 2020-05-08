from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from .utils.utils import use_mysql, create_token, check_token

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
    token = request.GET.get('token')
    # print(token)
    # results = use_mysql('select token from token where username="%s"' %(username))
    results = check_token(token)
    return JsonResponse({"code": 200, "message": "success", "results": results}, safe=False)



from django.core.cache import cache #引入缓存模块
def testredis(request):
    cache.set('lmgong', '帅哥', 30*60)
    results = cache.has_key('lmgong')
    return JsonResponse(results, safe=False)

def getredis(request):
    results = cache.get('lmgong')
    return JsonResponse(results, safe=False)
