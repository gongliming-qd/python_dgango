from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

class polls_middleware_class(MiddlewareMixin):
    EXCLUDE_IPS=['127.0.0.1']

    def process_view(self, request, view_func, *view_args, **view_kwares):
        print('1111111')
