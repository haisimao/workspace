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
    cursor.execute('select * from {} where comp_no > 65700;'.format('comps'))
    res = cursor.fetchall()
if len(res) != 0:
    my_data = DataFrame(res)

hashlist = ['a', 'b', 'f', '1', '2', '3', '4', 'g', 'e', 's', 'p','q','w','e','r','t','y','u','i','o','p','s','d','g','h','j','k','z','x','c','v','n','m','n','5','6','7','8','9','0']


def main(index):
    try:
        d = dict(my_data.iloc[index])
        d['comp_name'] = ' ' + my_data.iloc[index].copy()['comp_name']
        d['hashid'] = hashlist[random.randint(0, 36)] + my_data.iloc[index]['hashid'] + hashlist[random.randint(0, 36)] + hashlist[random.randint(0, 36)]
        my_data.iloc[index] = pd.Series(d)
        data = my_data[index:(index + 1)]
        pd.io.sql.to_sql(data, 'comps', con=my_engin, if_exists='append', index=False, chunksize=100)
        print('插入{}'.format(data['comp_name']))
    except:
        print('ddd')


for index in range(len(my_data)):
        xiaoman_thread = Thread(target=main, args=(index,))
        xiaoman_thread.start()


# 删除









































