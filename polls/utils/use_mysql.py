from django.db import connection

# 对数据库操作

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def use_mysql_by_dict(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = dictfetchall(cursor)
    return rows


def use_mysql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows