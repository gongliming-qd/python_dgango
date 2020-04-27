from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.core import signing
import json

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
    print(result)
    # return JsonResponse(result, safe=False)
    return HttpResponse(json.dumps(result), content_type="application/json")


def static(request):
    return render(request, 'index.html')


def static1(request):
    return render(request, 'index.html')


def signings(request):
    admin = request.GET.get('admin')
    psw = request.GET.get('psw')
    person = {'admin': admin, 'psw': psw}
    person_change = signing.dumps(person)
    print(person_change)
    person_cancel = signing.loads(person_change)
    print(person_cancel)

    return HttpResponse('HELLO')
