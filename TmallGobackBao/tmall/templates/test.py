# -*- coding: utf-8 -*- 
# @Time : 2019/12/9 15:10 
# @Author : WuXi 
# @File : test.py

from django.db import connection

cursor = connection.cursor()
cursor.execute('select * from t_commodity_sale_info where merchant_id = `1`')
t = cursor.fetchall()
print(t)