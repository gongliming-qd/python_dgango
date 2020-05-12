from django.db import connection

# 对数据库操作
def use_mysql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows