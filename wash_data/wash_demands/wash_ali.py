import json

import pandas as pd
import numpy as np
import time
from datetime import date, timedelta, datetime
from multiprocessing import Process
from threading import Thread
import hashlib

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
ip = 'rm-uf63r1m8zyr5k47j4qo.mysql.rds.aliyuncs.com'
my_engin = create_engine('mysql+pymysql://root:zx123ZX!@#@'+ip+':3306/to_balalaba?charset=utf8mb4')
# my_engin = create_engine('mysql+pymysql://root:yq201808@localhost:3306/to_balalaba?charset=utf8mb4')
# 时间
createdAt = time.strftime('%Y-%m-%d %H:%M', time.localtime())
with open(r'./comp_hashid.json', 'r+') as f:
    data = json.load(f)
comp_name_hashid_dict = data


def encrypt_md5(comp_name=''):
    if comp_name in comp_name_hashid_dict:
        return comp_name_hashid_dict.get(comp_name)
    else:
        md = hashlib.md5()  # 创建md5对象
        md.update(str(comp_name).encode(encoding='utf-8'))  # 这里必须用encode()函数对字符串进行编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
        return md.hexdigest()[9:25]




















































