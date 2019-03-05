import re

import pymysql
# from fake_useragent import UserAgent
#
# ua = UserAgent()
# print(ua.chrome)  #随机打印chrome浏览器任意版本
connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password="yq201808",
            database='linkedin_balalaba',
            use_unicode=True,
            charset="utf8mb4",  # 指定字符编码
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
        )

with connection.cursor() as cursor:
    cursor.execute('select comp_name from comps limit 0,6')
    response = cursor.fetchall()

for comp in response:
    company_name = re.sub(',', '', comp.get('comp_name'))
    company_name = re.sub(' ', '-', company_name)
    print(company_name)








