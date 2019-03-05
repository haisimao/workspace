import datetime
import threading
from multiprocessing import Process

from threading import Thread

from pandas import Series, DataFrame

import pandas as pd
import pymysql

from port_file import port_list

balalaba = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password="yq201808",
        database='up_balalaba',
        use_unicode=True,
        charset="utf8",  # 指定字符编码
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )

with balalaba.cursor() as cursor_balalaba:
    # cursor_balalaba.execute('''select * from custom_infos;''')
    cursor_balalaba.execute('''select export_country, source_port, id from custom_infos;''')
    result = cursor_balalaba.fetchall()


data = DataFrame(result)

data.drop_duplicates(inplace=True)

counter_lock = threading.Lock()


def wash_main(data__, index, i):
    try:
        d = dict(data__.iloc[index])
        export_country = d.get('export_country')
        source_port = d.get('source_port')
        if export_country:
            if 'CHINA' in export_country:
                export_country = 'Mainland China'
            else:
                return
        elif source_port and source_port in port_list:
            source_port = 'Mainland China'
        else:
            return
        id = d.get('id')
        if export_country == 'Mainland China' or source_port == 'Mainland China':
            with balalaba.cursor() as cursor_balalaba:
                if counter_lock.acquire():
                        cursor_balalaba.execute('''update custom_infos set export_country = 'Mainland China' where id={};'''.format(id),)

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
    for i in range(0, 110):
        data_ = data[i*10000:(i+1)*10000]
        if not data_.empty:
            p1 = Process(target=main, args=(data_, i))
            p1.start()










































