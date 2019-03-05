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

sem_pool = threading.Semaphore(100)  # 限制线程的最大数量为100个


def refer_data(table, frequency):
    with balalaba.cursor() as cursor_balalaba:
        # cursor_balalaba.execute('''select * from {} where custom_id >0; '''.format(table))
        cursor_balalaba.execute('''select * from {} order by id limit 800000, 200000000; '''.format(table))
        # cursor_balalaba.execute('''select * from {} where createdAt > '2019-02-18' and length(cont_email) > 0  and createdAt < '2019-02-20'; '''.format(table))
        result = cursor_balalaba.fetchall()
        print(len(result))
        data = DataFrame(result)
        # 添加去重策略, 不同的表有不同的去重逻辑, 需要一个一个判断添加
        if table == 'conts':
            data.drop(['id'], axis=1, inplace=True)
            data.drop_duplicates(['cont_email', 'cont_name'], keep='last', inplace=True)
        elif table == 'comps':
            data.drop_duplicates('hashid', inplace=True)
        else:
            # data.drop(['hashid'], axis=1, inplace=True)
            # data.drop_duplicates(inplace=True)
            pass
    # 按照量级区分, 分成十份写入
    print(data.shape)
    num = len(data)
    page = 200000 if table == 'comps' else 200000
    print('插入', data.shape)
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
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)
    refer_data('custom_infos', 1)













































