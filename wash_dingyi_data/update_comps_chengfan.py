import pandas as pd
import time
import pymysql

balalaba = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password="yq201808",
        database='to_balalaba',
        use_unicode=True,
        charset="utf8mb4",  # 指定字符编码
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )
data = pd.read_excel(r'C:\Users\YQ\Desktop\公司信息补充.xlsx', header=0)
xiaoman = pymysql.connect(
        host='rm-uf63r1m8zyr5k47j4qo.mysql.rds.aliyuncs.com',
        port=3306,
        user='root',
        password="zx123ZX!@#",
        database='balalaba',
        use_unicode=True,
        charset="utf8mb4",  # 指定字符编码
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )
# data.fillna(value=1, inplace=True)
# for comp in range(0, len(data)):
#     company = dict(data.iloc[comp])
#     with xiaoman.cursor() as cursor_balalaba:
#         comp_name = company.get('comp_name')
#         sic_code = int(company.get('sic_code'))
#         main_industry = company.get('main_industry')
#         home_page = company.get('home_page')
#         comp_tel = company.get('comp_tel')
#         year_found = company.get('year_found')
#         comp_addr = company.get('comp_addr')
#         try:
#             if int(company.get('sic_code')) != 1:
#                 print(comp_name)
#                 cursor_balalaba.execute('''update comps set sic_code = {} where comp_name = "{}";  '''.format(sic_code, comp_name))
#             if company.get('main_industry') != 1:
#                 cursor_balalaba.execute('''update comps set main_industry = "{}" where comp_name = "{}";  '''.format(main_industry, comp_name))
#             if company.get('home_page') != 1:
#                 cursor_balalaba.execute('''update comps set home_page = "{}" where comp_name = "{}";  '''.format(home_page, comp_name))
#             if company.get('comp_tel') != 1:
#                 cursor_balalaba.execute('''update comps set comp_tel = "{}" where comp_name = "{}";  '''.format(comp_tel, comp_name))
#             if company.get('year_found') != 1:
#                 cursor_balalaba.execute('''update comps set year_found = {} where comp_name = "{}";  '''.format(year_found, comp_name))
#             if company.get('comp_addr') != 1:
#                 cursor_balalaba.execute('''update comps set comp_addr = "{}" where comp_name = "{}";  '''.format(comp_addr, comp_name))
#         except:
#             print("出错", comp_name)

data.fillna(value=1, inplace=True)
for comp in range(0, len(data)):
    company = dict(data.iloc[comp])
    comp_name = company.get('comp_name')
    if company.get('email') != 1:
        try:
            with balalaba.cursor() as cursor_balalaba:
                cursor_balalaba.execute('''select hashid from comps where comp_name="{}"; '''.format(comp_name))
                hashid = cursor_balalaba.fetchone().get('hashid')
                email = company.get('email').strip()
                email = company.get('email').strip('\n')
                print(email)
                At = time.strftime('%Y-%m-%d %H:%M', time.localtime())
                cursor_balalaba.execute('''insert into conts (hashid, cont_email, createdAt, updatedAt) values (%s,%s, %s, %s)  ;''', (hashid, email, At, At))
        except:
            print('ccccc')































