import pandas as pd
from pandas import DataFrame
import numpy as np
import time
from datetime import date, timedelta, datetime
from multiprocessing import Process
from threading import Thread

import pandas as pd
import pymysql
from pandas import Series, DataFrame
import numpy as np
import io

from sqlalchemy import create_engine
import random
my_engin = create_engine('mysql+pymysql://root:yq201808@localhost:3306/balalaba?charset=utf8')

conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password="yq201808",
        database='up_balalaba',
        use_unicode=True,
        charset="utf8",             # 指定字符编码
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )

with conn.cursor() as cursor:
    cursor.execute('select * from {} ORDER BY comp_no DESC;'.format('comps'))
    res = cursor.fetchall()
if len(res) != 0:
    my_data = DataFrame(res)


def main(data):
    pd.io.sql.to_sql(data, 'comps', con=my_engin, if_exists='append', index=False, chunksize=100)
    print('插入{}'.format(data['comp_name']))


hashlist = ['a', 'b', 'f', '1', '2', '3', '4', 'g', 'e', 's', 'p','q','w','e','r','t','y','u','i','o','p','s','d','g','h','j','k','z','x','c','v','n','m','n','5','6','7','8','9','0']
for index in range(len(my_data)):
    try:
        if 'Inc' in my_data.iloc[index]['comp_name']:
            d = dict(my_data.iloc[index])
            d['comp_name'] = my_data.iloc[index].copy()['comp_name'].replace('Inc', '')
            d['hashid'] = my_data.iloc[index]['hashid'] + hashlist[random.randint(0, 36)] + hashlist[random.randint(0, 36)]
            my_data.iloc[index] = pd.Series(d)
            data = my_data[index:(index + 1)]
            xiaoman_thread = Thread(target=main, args=(data,))
            xiaoman_thread.start()
        if 'Ltd' in my_data.iloc[index]['comp_name']:
            d = dict(my_data.iloc[index])
            d['comp_name'] = my_data.iloc[index].copy()['comp_name'].replace('Ltd', '')
            d['hashid'] = my_data.iloc[index]['hashid'] + hashlist[random.randint(0, 36)] + hashlist[random.randint(0, 36)]
            my_data.iloc[index] = pd.Series(d)
            data = my_data[index:(index + 1)]
            xiaoman_thread = Thread(target=main, args=(data,))
            xiaoman_thread.start()
        if 'LTD' in my_data.iloc[index]['comp_name']:
            d = dict(my_data.iloc[index])
            d['comp_name'] = my_data.iloc[index].copy()['comp_name'].replace('LTD', '')
            d['hashid'] = my_data.iloc[index]['hashid'] + hashlist[random.randint(0, 36)] + hashlist[random.randint(0, 36)]
            my_data.iloc[index] = pd.Series(d)
            data = my_data[index:(index + 1)]
            xiaoman_thread = Thread(target=main, args=(data,))
            xiaoman_thread.start()
        if 'INC' in my_data.iloc[index]['comp_name']:
            d = dict(my_data.iloc[index])
            d['comp_name'] = my_data.iloc[index].copy()['comp_name'].replace('INC', '')
            d['hashid'] = my_data.iloc[index]['hashid'] + hashlist[random.randint(0, 36)] + hashlist[random.randint(0, 36)]
            my_data.iloc[index] = pd.Series(d)
            data = my_data[index:(index + 1)]
            xiaoman_thread = Thread(target=main, args=(data,))
            xiaoman_thread.start()
        if 'LLC' in my_data.iloc[index]['comp_name']:
            d = dict(my_data.iloc[index])
            d['comp_name'] = my_data.iloc[index].copy()['comp_name'].replace('LLC', '')
            d['hashid'] = my_data.iloc[index]['hashid'] + hashlist[random.randint(0, 36)] + hashlist[random.randint(0, 36)]
            my_data.iloc[index] = pd.Series(d)
            data = my_data[index:(index + 1)]
            xiaoman_thread = Thread(target=main, args=(data,))
            xiaoman_thread.start()
        if 'Corporation' in my_data.iloc[index]['comp_name']:
            d = dict(my_data.iloc[index])
            d['comp_name'] = my_data.iloc[index].copy()['comp_name'].replace('Corporation', '')
            d['hashid'] = my_data.iloc[index]['hashid'] + hashlist[random.randint(0, 36)] + hashlist[random.randint(0, 36)]
            my_data.iloc[index] = pd.Series(d)
            data = my_data[index:(index + 1)]
            xiaoman_thread = Thread(target=main, args=(data,))
            xiaoman_thread.start()
        if 'OOO' in my_data.iloc[index]['comp_name']:
            d = dict(my_data.iloc[index])
            d['comp_name'] = my_data.iloc[index].copy()['comp_name'].replace('OOO', '')
            d['hashid'] = my_data.iloc[index]['hashid'] + hashlist[random.randint(0, 36)] + hashlist[random.randint(0, 36)]
            my_data.iloc[index] = pd.Series(d)
            data = my_data[index:(index + 1)]
            xiaoman_thread = Thread(target=main, args=(data,))
            xiaoman_thread.start()
        else:
            d = dict(my_data.iloc[index])
            d['comp_name'] = my_data.iloc[index].copy()['comp_name'] + ' Corporation'
            d['hashid'] = my_data.iloc[index]['hashid'] + hashlist[random.randint(0, 36)] + hashlist[random.randint(0, 36)]
            my_data.iloc[index] = pd.Series(d)
            data = my_data[index:(index + 1)]
            xiaoman_thread = Thread(target=main, args=(data,))
            xiaoman_thread.start()
    except:
        print('ddd')

# 删除








































