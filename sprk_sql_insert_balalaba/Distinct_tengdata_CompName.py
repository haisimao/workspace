import datetime
import re
import threading
from multiprocessing import Process

from threading import Thread

import pandas as pd
import pymysql
import numpy as np

from sqlalchemy import create_engine
my_engin = create_engine('mysql+pymysql://root:yq201808@localhost:3306/up_balalaba?charset=utf8')

xiaoman = pymysql.connect(
        host='rm-uf63r1m8zyr5k47j4qo.mysql.rds.aliyuncs.com',
        port=3306,
        user='root',
        password="zx123ZX!@#",
        database='xiaoman2',
        use_unicode=True,
        charset="utf8mb4",  # 指定字符编码
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )

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

with balalaba.cursor() as cursor_balalaba:
    cursor_balalaba.execute('''select comp_name, id from tengdata;''')
    result = cursor_balalaba.fetchall()

    data = pd.DataFrame(result)

    counter_lock = threading.Lock()


def wash_data(data_, index, i):
    d = dict(data_.iloc[index])
    try:
        comp_name = d.get('comp_name')
        comp_name_ = comp_name
        id = d.get('id')
        if comp_name:
            print(comp_name)
            comp_name = re.sub(r'\(.*\)', '', comp_name)
            comp_name = re.sub(r'.*\)', '', comp_name)
            comp_name = comp_name.replace('#', '')
            comp_name = comp_name.replace('"', '')
            comp_name = comp_name.replace("'", '')
            # comp_name = comp_name.replace(',', ' ')
            comp_name = comp_name.replace('/', '')
            comp_name = comp_name.replace('$', '')
            if ' INC' in comp_name:
                comp_name = comp_name.split(' INC')[0] + ' INC'
            if ' LLC' in comp_name:
                comp_name = comp_name.split(' LLC')[0] + ' LLC'
            if ' LTD' in comp_name:
                comp_name = comp_name.split(' LTD')[0] + ' LTD'
            if ' Inc' in comp_name:
                comp_name = comp_name.split(' Inc')[0] + ' Inc'
            if ' Ltd' in comp_name:
                comp_name = comp_name.split(' Ltd')[0] + ' Ltd'
            comp_name = comp_name.strip('. ,:123456789')
            comp_name = comp_name.rstrip('. ,:123456789')
            print(id)
            print(comp_name)
            if comp_name_ == comp_name:
                return
            # if counter_lock.acquire():
            with balalaba.cursor() as cursor_balalaba_:
                cursor_balalaba_.execute(''' update tengdata set comp_name="{}" where id={} ;'''.format(comp_name, str(id)))

                # counter_lock.release()

            print('单次插入完成i{},{}.时间{}'.format(i, index, datetime.datetime.now()))
    except:
        print('ddd')


def main(data_, i):
    '''
    # 判断这个url与数据库里的那个hashid匹配, 写入公司信息 用查询的方式(in)
    # 拿到hashid插入conts表
    :param data:
    :return:
    '''
    for index in range(len(data_)):
        wash_data(data_, index, i)


if __name__ == '__main__':
    for i in range(0, 30):
        data_ = data[i*20000:(i+1)*20000]
        if not data_.empty:
            main(data_, i)
