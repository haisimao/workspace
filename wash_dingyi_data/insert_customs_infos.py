import pandas as pd
import numpy as np
import time
from datetime import date, timedelta, datetime
from multiprocessing import Process
from threading import Thread

import pymysql
from pandas import Series, DataFrame
import io
import re
import random
import string

import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
# 创建引擎
my_engin = create_engine('mysql+pymysql://root:yq201808@localhost:3306/to_balalaba?charset=utf8mb4')

# 创建{'comp_name': 'hashid'} 的字典
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
    cursor_balalaba.execute('''select comp_name, hashid from {};'''.format('comps'))
    result = cursor_balalaba.fetchall()
    print(len(result))
comp_name_hashid_dict = {}
for res in result:
    comp_name_hashid_dict[res['comp_name']] = res['hashid']


data = pd.read_excel(r'C:/Users/YQ/Desktop/17years_customs/0276bb48-62e4-4b1c-8c78-f359e5bdfc41.xls', header=0,)
data = data[['日期','商品描述','国外企业','通知人名称','重量','数量','运输方式','国内企业','HS编码','估计金额','数量单位',\
    '国外企业地址','国内企业地址','国外中转港','出货港','卸货港','原产国','船公司所属国家','承运人简称']]
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
    '承运人简称': 'ship_comp',}, inplace=True)
createdAt = time.strftime('%Y-%m-%d %H:%M', time.localtime())
data['createdAt'] = createdAt
data['updatedAt'] = createdAt
data['hashid'] = ''
custom = data[['port_time', 'prod_desc', 'importer', 'hs_code', 'trans_price', 'createdAt', 'updatedAt', 'hashid']]
custom.rename(columns={'importer': 'all_buyers', 'trans_price': 'value_sum', }, inplace=True)

for i in range(len(data)):
    importer = data['importer'][i]
    if importer not in comp_name_hashid_dict.keys():
        # 生成hashid , 写入comps
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        new_hashid = re.sub('[^\w]', '', importer) + random_str
        company = DataFrame({'comp_name': importer,
                         'hashid': new_hashid,
                         'comp_no': 100000000+i,
                          'createdAt': createdAt,
                          'updatedAt': createdAt,
                         }, index=[0])
        data['hashid'][i] = new_hashid
        custom['hashid'][i] = hashid
        pd.io.sql.to_sql(company, 'comps', con=my_engin, if_exists='append', index=False, chunksize=1)
        pd.io.sql.to_sql(DataFrame(dict(custom.iloc[i]), index=[0]), 'customs', con=my_engin, if_exists='append', index=False, chunksize=1)
        pd.io.sql.to_sql(DataFrame(dict(data.iloc[i]), index=[0]), 'custom_infos', con=my_engin, if_exists='append', index=False, chunksize=1)
    else:
        # 获取hashid 更新custom_infos表
        hashid = comp_name_hashid_dict[importer]
        print(hashid)
        data['hashid'][i] = hashid
        custom['hashid'][i] = hashid
        pd.io.sql.to_sql(DataFrame(dict(custom.iloc[i]), index=[0]), 'customs', con=my_engin, if_exists='append', index=False, chunksize=1)
        pd.io.sql.to_sql(DataFrame(dict(data.iloc[i]), index=[0]), 'custom_infos', con=my_engin, if_exists='append', index=False, chunksize=1)





















