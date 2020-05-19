from django.http import HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .utils.utils import create_token, check_token, get_username
from .utils.use_mysql import use_mysql

class polls_middleware_class(MiddlewareMixin):
    EXCLUDE_IPS=['127.0.0.1']

    def process_view(self, request, view_func, *view_args, **view_kwares):

        # 0. 获取图片
        if '/api/get_img/' in request.path:
            return
        # 1. 如果不是登录接口, 都要进行token验证
        if request.path != '/api/tologin/':
            # 2. 获取token
            token = request.META.get("HTTP_AUTHORIZATION")
            # 3. 判断是否有传递token
            if token != 'hello_world':
                # 3.1 验证token信息
                results = check_token(token)
                if results:
                    # 3.1.1. 不做任何事情
                    print('token验证通过')
                else:
                    # 3.1.2 返回false
                    results = {'code': 200, "state": 'false', "results": {"message": "token验证不通过"}}
                    return JsonResponse(results, safe=False)
            else:
                # 3.2 返回false
                results = {'code': 200, "state": 'false', "results": {"message": "token验证不通过"}}
                return JsonResponse(results, safe=False)