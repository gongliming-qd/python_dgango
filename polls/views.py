from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.core import signing

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
        result.append(list_value)
    print(result)
    return HttpResponse(result)


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
