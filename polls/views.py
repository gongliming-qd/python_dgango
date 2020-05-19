from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from .utils.utils import  create_token, check_token, get_username, encrypt_other
from .utils.use_mysql import use_mysql


# 加密解密算法
def index(request):
    cursor = connection.cursor()
    cursor.execute("select * from member")
    rows = cursor.fetchall()
    rows = list(rows)
    result = []
    for key in rows:
        list_value = list(key)
        result.append({'id': list_value[0], 'name': list_value[1], 'sec': list_value[2], 'bobby': list_value[3], 'introduction': list_value[4]})
        result.append(list_value)
    print(result)
    results = {'code': 0, "state": 'true', "results": {"message": "获取数据成功","lists":result}}
    return JsonResponse(results, safe=False)
# redis学习部分
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
        # 2. 验证是否有当前账号
        num = use_mysql('select  count(*) from login_username_psw where username="%(username)s"'%{'username': username})[0][0]
        if num != 1:
            results = {'code': 200, "state": 'false', "results": {"message":'当前用户或密码不正确'}}
            return JsonResponse(results, safe=False)
        # 3. 数据库取账号密码
        return_psw = use_mysql('select  psw from login_username_psw where username="%(username)s"'%{'username': username})[0][0]
        # 4. 解密数据库密码
        return_psw = get_username(return_psw)
        # 5. 验证密码是否正确
        if return_psw == psw:
            # 5.1. 密码正确创建token, 返回token
            token = create_token(username)
            results = {'code': 0, "state": 'success', "token": token, "results": {"message": '登录成功'}}
            return JsonResponse(results, safe=False)
        else:
            # 5.2. 密码不正确
            results = {'code': 0, "state": 'false', "results": {"message": '当前用户或密码不正确'}}
            return JsonResponse(results, safe=False)

# 注册用户部分
def register_user(request):
    if request.method == 'POST':
        username = json.loads(request.body)['username']
        psw = json.loads(request.body)['psw']
        psw_confirm = json.loads(request.body)['psw_confirm']
        # 1. 验证该用户是否已经存在
        num = use_mysql('select count(*) from login_username_psw where username="%(username)s"'%{"username": username})[0][0]
        if num == 0:
            # 1.1 说明不存在可以注册
            ## 1.1.1 验证密码
            ### 1.1.2 验证密码和再次输入密码是否一致
            if psw == psw_confirm:
                # 1.1.2.1 加密密码
                psw = encrypt_other(psw)
                # 1.1.2.1 写入数据库中
                results_sql = use_mysql('insert into login_username_psw(username, psw) values ("%(username)s","%(psw)s")'%{"username": username, "psw": psw})
                results = {'code': 0, "state": 'success', "results": {"message": results_sql}}
                return JsonResponse(results, safe=False)
            else:
                results = {'code': 0, "state": 'success', "results": {"message": "密码和确认密码不一致"}}
                return JsonResponse(results, safe=False)
        else:
            # 1.2 说明不存在不能注册
            results = {'code': 0, "state": 'false', "results": {"message": '当前用户已注册'}}
            return JsonResponse(results, safe=False)

# 验证token是否正确
def check_api_token(request):
    # 1. 获取请求头中的token
    token = request.META.get("HTTP_AUTHORIZATION")
    results = check_token(token)
    if results:
        results = {'code': 0, "message": 'success'}
        return JsonResponse(results, safe=False)
    else:
        results = {'code':0, "message":'false'}
        return JsonResponse(results, safe=False)


# 存储图片
def check_pass(request):
    psw = request.POST.get('psw');
    file_img = request.FILES.get('file_img')
    print(file_img)

    # 加密文件名
    file_name = encrypt_other(file_img.name)

    # 文件名和上传的数据填到数据库中


    # 文件存储到文件夹
    with open('upload/img/'+file_name, 'wb') as pic:
        for c in file_img.chunks():
            pic.write(c)

    results = {'code': 0, "message": 'true'}
    return JsonResponse(results, safe=False)

# 获取图片
def get_img(request):

    # 获取用户名 touxiang.jpg
    # 通过用户名到数据库中求取图片的名字
    img_name = request.GET.get('img_name')
    # 通过名字, 到文件夹中读取, 并返回到前端中
    image_data = open('upload/img/' + img_name, "rb").read()
    return HttpResponse(image_data, content_type="image/png")