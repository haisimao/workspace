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
# my_engin = create_engine('mysql+pymysql://root:zx123ZX!@#@'+ip+':3306/to_balalaba?charset=utf8mb4')
my_engin = create_engine('mysql+pymysql://root:yq201808@localhost:3306/to_balalaba?charset=utf8mb4')
# 时间
createdAt = time.strftime('%Y-%m-%d %H:%M', time.localtime())

sem_pool = threading.Semaphore(50)  # 限制线程的最大数量为100个

lock = threading.Lock()

# 创建{'comp_name': 'hashid'} 的字典
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
with balalaba.cursor() as cursor_balalaba:
    cursor_balalaba.execute('''select comp_name, hashid from {};'''.format('comps'))
    result = cursor_balalaba.fetchall()
    print(len(result))
comp_name_hashid_dict = {}
for res in result:
    comp_name_hashid_dict[res['comp_name']] = res['hashid']


def change(importer=''):
    if importer in comp_name_hashid_dict.keys():
        return comp_name_hashid_dict.get(importer)
    else:
        return 0


def insert_data(data, custom):
    for i in data.index:
        dict(custom.iloc[i]).get('hashid')
        try:
            pd.io.sql.to_sql(DataFrame(dict(custom.iloc[i]), index=[0]), 'customs', con=my_engin, if_exists='append', index=False, chunksize=1)
            pd.io.sql.to_sql(DataFrame(dict(data.iloc[i]), index=[0]), 'custom_infos', con=my_engin, if_exists='append', index=False, chunksize=1)
        except Exception as e:
            print(e)


def main():
    # 按文件夹批量插入custom_infos数据
    for root, dirs, files in os.walk(r'D:\待清洗数据\美国海关数据汇总2019_2_13/', topdown=False):
        for name in files:
            # 读取excel文件
            file = os.path.join(root, name)
            data = pd.read_excel(file, header=0,)
            # 取部分字段, 重命名
            data = data[['日期', '商品描述', '国外企业', '通知人名称', '重量', '数量', '运输方式', '国内企业', 'HS编码', '估计金额', '数量单位',\
        '国外企业地址', '国内企业地址', '国外中转港', '出货港', '卸货港', '原产国', '船公司所属国家', '承运人简称']]
            data.rename(columns={
        '日期': 'port_time',
        '商品描述': 'prod_desc',
        '国外企业': 'exporter',
        '国内企业': 'importer',
        '国外企业地址': 'export_addr',
        '国内企业地址': 'import_addr',
        '通知人名称': 'import_cont',
        '重量': 'net_weight',
        '数量': 'prod_num',
        '运输方式': 'ship_type',
        'HS编码': 'hs_code',
        '估计金额': 'trans_price',
        '数量单位': 'num_unit',
        '国外中转港': 'transit_port',
        '出货港': 'source_port',
        '卸货港': 'destination_port',
        '原产国': 'origin_country',
        '船公司所属国家': 'transp_country',
        '承运人简称': 'ship_comp', }, inplace=True)
            data['createdAt'] = createdAt
            data['updatedAt'] = createdAt
            data['hashid'] = ''
            data.drop_duplicates(inplace=True)
            data['hashid'] = data['importer'].map(change)
            data = data[data['hashid'] != 0]
            if len(data) > 0:
                custom = data[['port_time', 'prod_desc', 'importer', 'hs_code', 'trans_price', 'createdAt', 'updatedAt', 'hashid']]
                custom.rename(columns={'importer': 'all_buyers', 'trans_price': 'value_sum', }, inplace=True)
                try:
                    sem_pool.acquire()
                    main_thread = Thread(target=insert_data, args=(data, custom))
                    main_thread.start()
                    sem_pool.release()
                    # insert_data(data, custom)
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    main()
























