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


def refer_data(table):
    with balalaba.cursor() as cursor_balalaba:
        # cursor_balalaba.execute('''select * from {} where createdAt > '2019-01-22' and createdAt < '2019-01-23'; '''.format(table))
        # cursor_balalaba.execute('''select * from {} where createdAt = '2019-01-23 11:42:00'; '''.format(table))
        cursor_balalaba.execute('''select * from {}; '''.format(table))
        result = cursor_balalaba.fetchall()
        print(len(result))
        data = DataFrame(result)
        # 添加去重策略, 不同的表有不同的去重逻辑, 需要一个一个判断添加
        if table == 'conts':
            data.drop_duplicates(['cont_email', 'cont_name'], keep='last', inplace=True)
        elif table == 'comps':
            data.drop_duplicates('hashid', inplace=True)
        else:
            data.drop(['id'], axis=1, inplace=True)
            data.drop_duplicates(inplace=True)
    try:
        data.to_excel(r'D:\data_to_yun_custom_infos_20190124.xlsx')
    except:
         print('2, ')


if __name__ == '__main__':
    # 适用于除comps表以外的其他表
    # refer_data('conts')
    refer_data('custom_infos')

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
    # for i in tables:
    #     refer_data(i, 1000)
