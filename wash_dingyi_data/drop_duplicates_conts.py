import datetime
import threading
from multiprocessing import Process

from threading import Thread

from pandas import Series, DataFrame

import pandas as pd
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

with balalaba.cursor() as cursor_balalaba:
    # ID 记录 1537447
    cursor_balalaba.execute('''select * from conts;''')
    result = cursor_balalaba.fetchall()


data = DataFrame(result)

data.drop_duplicates('cont_email', inplace=True)

counter_lock = threading.Lock()

linkedin = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password="yq201808",
        database='linkedin_balalaba',
        use_unicode=True,
        charset="utf8",  # 指定字符编码
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )


def wash_main(data__, index, i):
    try:
        d = dict(data__.iloc[index])
        with linkedin.cursor() as cursor_linkedin:
            if counter_lock.acquire():
                cursor_linkedin.execute(
                    '''insert into conts (hashid, cont_name, cont_post, cont_email, cont_url) values (%s, %s, %s, %s, %s);''', (d.get('hashid'), d.get('cont_name'), d.get('cont_post'), d.get('cont_email'), d.get('cont_url'),))
            counter_lock.release()
            print('{}单次插入完成,{}.时间{}'.format(i, index, datetime.datetime.now()))
    except:
        counter_lock.release()
        print('dddd')


def main(data_, i):
    '''
    插入数据库
    :param data:
    :return:
    '''
    for index in range(len(data_)):
        main_thread = Thread(target=wash_main, args=(data_, index, i))
        main_thread.start()


if __name__ == '__main__':
    for i in range(0, 150, 3):
        data_ = data[i*10000:(i+3)*10000]
        if not data_.empty:
            p1 = Process(target=main, args=(data_, i))
            p1.start()
