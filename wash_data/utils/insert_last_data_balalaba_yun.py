import pandas as pd
import numpy as np
import time
from datetime import date, timedelta, datetime
from threading import Thread
import threading

import pymysql
from pandas import Series, DataFrame
import io

from sqlalchemy import create_engine

ip = 'rm-uf63r1m8zyr5k47j4qo.mysql.rds.aliyuncs.com'
my_engin = create_engine('mysql+pymysql://root:zx123ZX!@#@'+ip+':3306/balalaba?charset=utf8mb4')

balalaba = pymysql.connect(
        host='rm-uf63r1m8zyr5k47j4qo.mysql.rds.aliyuncs.com',
        port=3306,
        user='root',
        password="zx123ZX!@#",
        database='to_balalaba',
        use_unicode=True,
        charset="utf8mb4",  # 指定字符编码
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )
yun_balalaba = pymysql.connect(
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
with yun_balalaba.cursor() as cursor_yun_balalaba:
    cursor_yun_balalaba.execute('''select home_page, hashid from {};'''.format('comps'))
    result = cursor_yun_balalaba.fetchall()
    print(len(result), 'from comps')
comp_name_hashid_dict_yun = {}
for res in result:
    comp_name_hashid_dict_yun[res['home_page']] = res['hashid']

hashids = comp_name_hashid_dict_yun.values()


def distinct(value=''):
    if value in hashids:
        return True
    else:
        return False


sem_pool = threading.Semaphore(100)  # 限制线程的最大数量为100个


def refer_data(table, frequency):
    with balalaba.cursor() as cursor_balalaba:
        cursor_balalaba.execute('''select * from {} where createdAt > '2019-01-14' and createdAt < '2019-01-22'; '''.format(table))
        result = cursor_balalaba.fetchall()
        print(len(result))
        data = DataFrame(result)
        # 添加去重策略, 不同的表有不同的去重逻辑, 需要一个一个判断添加
        if table == 'conts':
            data.drop_duplicates('cont_email', inplace=True)
        elif table == 'comps':
            data.drop_duplicates('hashid', inplace=True)
        else:
            data.drop(['id'], axis=1, inplace=True)
            data.drop_duplicates(inplace=True)
    # 按照量级区分, 分成十份写入
    data['new'] = data['hashid'].map(distinct)
    data = data[data['new']]
    data.drop(['new', ], axis=1, inplace=True)
    num = len(data)
    page = 10000
    for j in range(int(num/page)):
        try:
            with sem_pool:
                print('当前进度', (j / (int(num / page))*100), '%')
                my_data = data[j * page:(j+1) * page].copy()
                xiaoman_thread = Thread(target=insert_data, args=(my_data, table, frequency))
                xiaoman_thread.start()
        except:
            print('1, ')
    # 余量数据插入,  重要
    try:
        print('当前进度100%')
        my_data = data[num * page:].copy()
        xiaoman_thread_ = Thread(target=insert_data, args=(my_data, table, frequency))
        xiaoman_thread_.start()
    except:
         print('2, ')


def insert_data(in_data, table, frequency):
    for i in range(len(in_data)):
        data_ = dict(in_data.iloc[i])
        data__ = pd.DataFrame(data_, index=[0])
        try:
            pd.io.sql.to_sql(data__, table, con=my_engin, if_exists='append', index=False, chunksize=frequency)
        except Exception as e:
            print(str(e), i)


if __name__ == '__main__':
    refer_data('comps', 1)
    # refer_data('conts', 100)

    # tables = [
    #     'customs',
    #     'custom_infos',
    #     #     'cash',
    #     'conts',
    #     #     'decash_alls',
    #     #     'profits',
    #     #     'decash_eqs',
    #     #     'decashes',
    #     #     'users',
    #     #     'user_marks',
    #     #     'comp_marks',
    #     #     'big_comps',
    #     #     'big_demands',
    #     #     'demands',
    #     #     'feedbacks',
    #     #     'information',
    #     #     'products',
    #     #     'videos',
    #     #     'tengdata',
    #
    # ]
    #
    # for i in tables:
    #     refer_data(i, 1000)












































