from django.http import HttpResponse, JsonResponse
from django.db import connection
from ..utils.utils import  create_token, check_token, get_username, encrypt_other, encrypt
from ..utils.use_mysql import use_mysql, use_mysql_by_dict


# 加密解密算法
def index(request):
    # cursor = connection.cursor()
    # cursor.execute("select * from member")
    result = use_mysql_by_dict("select * from member")
    # rows = cursor.fetchall()
    # rows = list(rows)
    # result = []
    # for key in rows:
    #     list_value = list(key)
    #     result.append({'id': list_value[0], 'name': list_value[1], 'sec': list_value[2], 'bobby': list_value[3], 'introduction': list_value[4]})
    #     result.append(list_value)
    # print(result)
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



# 获取图片
def get_img(request):

    # 获取用户名 touxiang.jpg
    # 通过用户名到数据库中求取图片的名字
    img_name = request.GET.get('img_name')
    # 通过名字, 到文件夹中读取, 并返回到前端中
    image_data = open('upload/img/' + img_name, "rb").read()
    return HttpResponse(image_data, content_type="image/png")



# 用户操作>修改信息 -----------------------------------------------------------
# 1. 获取用户信息
def get_userinfo_by_username(request):
    username = request.GET.get('username',None)
    print(username)
    if username:
        result = use_mysql_by_dict('select * from  login_username_psw where username="%(username)s"' %{"username": username})
        print(result)

        results = {'code': 0, "state": 'success', "results": result}
        return JsonResponse(results, safe=False)

    else:
        results = {'code': 0, "state": 'success', "results": {"message": 'username不存在'}}
        return JsonResponse(results, safe=False)


# 2. 修改用户信息
def update_userinfo_by_id(request):
    id = request.POST.get('id')
    username = request.POST.get('username')
    label = request.POST.get('label')
    # 1. 判断当前是否已经存在当前用户
    sql_username = use_mysql('select username from login_username_psw where id=%(id)s' % {"id": id})[0][0]
    if sql_username != username:
        num = use_mysql('select count(*) from login_username_psw where username="%(username)s"' % {"username": username})[0][0]
        if num != 0:
            # 1.2 说明不存在不能注册
            results = {'code': 0, "state": 'false', "results": {"message": '当前用户名已注册'}}
            return JsonResponse(results, safe=False)
    print(222222222222)
    if request.FILES.get('avatar_address'):
        file_img = request.FILES.get('avatar_address')
        # 2. 加密文件名
        avatar_address = encrypt(file_img.name)
        avatar_address += '.jpg'
        # 3. 文件名和上传的数据填到数据库中
        result = use_mysql('update login_username_psw set username="%(username)s",label="%(label)s", avatar_address="%(avatar_address)s" where id=%(id)s' % {
            "username": username,"label": label,"avatar_address": avatar_address,"id":id})
        # 4. 文件存储到文件夹
        with open('upload/img/'+avatar_address, 'wb') as pic:
            for c in file_img.chunks():
                pic.write(c)
        # 5. 返回数据
        results = {'code': 0, "message": 'true', 'results': result}
        return JsonResponse(results, safe=False)
    else:
        result = use_mysql(
            'update login_username_psw set username="%(username)s",label="%(label)s" where id=%(id)s' % {
                "username": username, "label": label, "id": id})
        results = {'code': 0, "message": 'true', 'results': result}
        return JsonResponse(results, safe=False)

# 3. 修改用户密码
def update_userpws_by_id(request):
    if request.method == 'POST':
        id = json.loads(request.body)['id']
        odd_psw = json.loads(request.body)['odd_psw']
        new_psw = json.loads(request.body)['new_psw']
        # 1. 验证旧密码是否正确
        # 1.1 取数据
        results_sql = use_mysql_by_dict('''select psw from login_username_psw where id=%(id)s''' %{"id": id})
        # 1.2 验证数据
        get_username_pws = get_username(results_sql)

        # 1.3 判断
        if get_username_pws != odd_psw:
            results = {'code': 1, "state": 'error', "results": {"message": "密码不正确"}}
            return JsonResponse(results, safe=False)
        else:
            use_mysql(''' update login_username_psw set psw="%(psw)s" where id="%(id)d"'''%{"psw": create_token(new_psw), "id":id})
            results = {'code': 0, "state": 'success', "results": {"message": "修改成功!!"}}
            return JsonResponse(results, safe=False)
# #    个人信息修改部分   -----------------------------------------------------------
# 1. 获取用户信息

def get_api_username_all_info(request):
        # 1. 取出所有数据
        weight = request.GET.get('weight',None)
        xxx = (())
        if weight:
            xxx = use_mysql('select * from login_username_psw where weight="%(weight)s"' %{"weight": weight})
        else:
            results = {'code': 0, "state": 'true', "results": {"message": "无权限参数", "lists": None}}
            return JsonResponse(results, safe=False)
        if weight == '0':
            xxx = use_mysql('select * from login_username_psw')
        rows = list(xxx)
        result = []
        for key in rows:
            list_value = list(key)
            print(get_username(list_value[2]))
            print(list_value[2])
            result.append({'id': list_value[0], 'username': list_value[1], 'psw': get_username(list_value[2]), 'avatar_address': list_value[3],
                           'label': list_value[4],'weight': list_value[5]})
        results = {'code': 0, "state": 'true', "results": {"message": "获取数据成功", "lists": result}}
        return JsonResponse(results, safe=False)


# 1. 获取关键字搜索用户信息
def get_api_username_all_info_by_search(request):
        # 1. 取出所有数据
        weight = request.GET.get('weight', None)
        search = request.GET.get('search', None)
        xxx = (())
        print(weight)
        print(search)

        if weight == '0':
            xxx = use_mysql('select * from login_username_psw where concat(id,username,psw,label,weight) like "%(search)s"' %{"search": search})
        elif weight == None :
            results = {'code': 0, "state": 'true', "results": {"message": "无权限参数", "lists": None}}
            return JsonResponse(results, safe=False)
        else:
            xxx = use_mysql('select * from login_username_psw where weight="%(weight)s" and concat(id,username,psw,label,weight) like "%(search)s"' %{"weight": weight,"search":search})
        rows = list(xxx)
        result = []
        for key in rows:
            list_value = list(key)
            print(get_username(list_value[2]))
            print(list_value[2])
            result.append({'id': list_value[0], 'username': list_value[1], 'psw': get_username(list_value[2]), 'avatar_address': list_value[3],
                           'label': list_value[4],'weight': list_value[5]})
        results = {'code': 0, "state": 'true', "results": {"message": "获取数据成功", "lists": result}}
        return JsonResponse(results, safe=False)


# 2. 新增用户
def add_api_username_all_info(request):
    if request.method == 'POST':
        username = json.loads(request.body)['username']
        psw = json.loads(request.body)['psw']
        label = json.loads(request.body)['label']
        weight = json.loads(request.body)['weight']
        # 1. 验证该用户是否已经存在
        num = use_mysql('select count(*) from login_username_psw where username="%(username)s"'%{"username": username})[0][0]
        if num == 0:
            # 1.1 说明不存在可以注册
            # 1.1.2.1 写入数据库中
            results_sql = use_mysql(
                'insert into login_username_psw(username, psw, label, weight) values ("%(username)s","%(psw)s","%(label)s","%(weight)s")' % {
                    "username": username, "psw": encrypt_other(psw), "label": label, "weight": weight})
            results = {'code': 0, "state": 'success', "results": {"message": results_sql}}
            return JsonResponse(results, safe=False)
        else:
            # 1.2 说明不存在不能注册
            results = {'code': 0, "state": 'false', "results": {"message": '当前用户已注册'}}
            return JsonResponse(results, safe=False)


# 3. 修改用户
def update_api_username_all_info(request):
    if request.method == 'POST':
        id = json.loads(request.body)['id']
        username = json.loads(request.body)['username']
        psw = json.loads(request.body)['psw']
        label = json.loads(request.body)['label']
        weight = json.loads(request.body)['weight']

        results_sql = use_mysql(
            'update login_username_psw set  username="%(username)s", psw="%(psw)s", label="%(label)s", weight="%(weight)s" where id=%(id)s' % {
               "username": username, "psw": encrypt_other(psw), "label": label, "weight": weight, "id": id})
        results = {'code': 0, "state": 'success', "results": {"message": results_sql}}
        return JsonResponse(results, safe=False)
        # 1.2 说明不存在不能注册


# 4. 删除用户
def dele_api_username_all_info(request):
    if request.method == 'POST':
        id = json.loads(request.body)['id']
        print(id)
        results_sql = use_mysql(
            'delete from login_username_psw where id="%(id)s"' % {
                "id": id})
        results = {'code': 0, "state": 'success', "results": {"message": results_sql}}
        return JsonResponse(results, safe=False)
