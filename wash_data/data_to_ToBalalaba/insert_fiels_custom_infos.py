import threading

import pandas as pd
import numpy as np
import time
from datetime import date, timedelta, datetime
from threading import Thread

import pymysql
from pandas import Series, DataFrame

from sqlalchemy import create_engine
import os

# 创建引擎
ip = 'rm-uf63r1m8zyr5k47j4qo.mysql.rds.aliyuncs.com'
my_engin = create_engine('mysql+pymysql://root:zx123ZX!@#@'+ip+':3306/balalaba?charset=utf8mb4')
# 时间
createdAt = time.strftime('%Y-%m-%d %H:%M', time.localtime())


def main():
    # 按文件夹批量插入custom_infos数据
    for root, dirs, files in os.walk(r'D:\已清洗数据\美国海关数据/', topdown=False):
        for name in files:
            # 读取excel文件
            file = os.path.join(root, name)
            data = pd.read_excel(file, header=0,)
            if len(data) > 0:
                custom = data[['port_time', 'prod_desc', 'importer', 'hs_code', 'trans_price', 'createdAt', 'updatedAt', 'hashid']]
                custom.rename(columns={'importer': 'all_buyers', 'trans_price': 'value_sum', }, inplace=True)
                try:
                    print('插入' + name)
                    pd.io.sql.to_sql(custom, 'customs', con=my_engin, if_exists='append', index=False, chunksize=1)
                    pd.io.sql.to_sql(data, 'custom_infos', con=my_engin, if_exists='append', index=False, chunksize=1)
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    main()
























