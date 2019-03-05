import datetime
import threading

from threading import Thread

from pandas import DataFrame

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
    cursor_balalaba.execute('''select hashid from comps where comp_no < '733760' and length(country) < 1;''')
    result = cursor_balalaba.fetchall()


data = DataFrame(result)

counter_lock = threading.Lock()


def wash_main(data__, index):
    try:
        d = dict(data__.iloc[index])
        hashid = d.get('hashid')
        with balalaba.cursor() as cursor_balalaba:
            if counter_lock.acquire():
                cursor_balalaba.execute('''select country from comp where hashid=%s;''', (hashid))
                response = cursor_balalaba.fetchone()
                if response != None and response:
                    country = response.get('country')
                    cursor_balalaba.execute('''update IGNORE comps set country=%s where hashid=%s;''', (country, hashid))
                    print('单次插入完成,{}.时间{}----hashid{}'.format(index, datetime.datetime.now(), hashid))
            counter_lock.release()
    except:
        counter_lock.release()
        print('some things error')


def main(data_):
    '''
    插入数据库
    :param data:
    :return:
    '''
    for index in range(len(data_)):
        # main_thread = Thread(target=wash_main, args=(data_, index,))
        # main_thread.start()
        wash_main(data_, index,)


if __name__ == '__main__':
    # for i in range(0, 150):
    #     data_ = data[i*10000:(i+1)*10000]
    #     if not data_.empty:
    #         # p1 = Process(target=main, args=(data_, i))
    #         # p1.start()
    main(data,)
