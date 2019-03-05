import datetime
import threading
from multiprocessing import Process

from threading import Thread

import pandas as pd
import pymysql
import numpy as np

from sqlalchemy import create_engine
my_engin = create_engine('mysql+pymysql://root:yq201808@localhost:3306/to_balalaba?charset=utf8')


data = pd.read_excel(r'C:\Users\YQ\Desktop\dingyi_contacts\comp_2018-12-11\comp0_.xls', header=0,)
# enquiry_data_2 = pd.read_excel(r'C:\Users\YQ\Desktop\dingyi_contacts\comp_0.xls', header=0,)
# enquiry_data_3 = pd.read_excel(r'C:\Users\YQ\Desktop\dingyi_contacts\comp_3.xls', header=0,)
# enquiry_data_4 = pd.read_excel(r'C:\Users\YQ\Desktop\dingyi_contacts\comp_5.xls', header=0,)
# enquiry_data_5 = pd.read_excel(r'C:\Users\YQ\Desktop\dingyi_contacts\comp_6.xls', header=0,)
# enquiry_data_6 = pd.read_excel(r'C:\Users\YQ\Desktop\dingyi_contacts\comp_9.xls', header=0,)
# enquiry_data_7 = pd.read_excel(r'C:\Users\YQ\Desktop\dingyi_contacts\comp_12.xls', header=0,)
# enquiry_data_8 = pd.read_excel(r'C:\Users\YQ\Desktop\dingyi_contacts\comp_18.xls', header=0,)
# enquiry_data_9 = pd.read_excel(r'C:\Users\YQ\Desktop\dingyi_contacts\comp_27.xls', header=0,)
# data = pd.concat((enquiry_data_1, enquiry_data_2, enquiry_data_3, enquiry_data_4, enquiry_data_5, enquiry_data_6, enquiry_data_7, enquiry_data_8, enquiry_data_9), ignore_index=True)


data.rename(columns={'公司名称': 'comp_name', '网站': 'home_page', '电话': 'contact_phone', '地址': 'address'} ,inplace=True)
data.drop('传真', axis=1, inplace=True)
data.drop('comp_name', axis=1, inplace=True)
# 找到符合条件的元素, 替换或者返回True/False
data.where(data.notnull(), None)
data.replace(np.nan, ' ', inplace=True)

xiaoman = pymysql.connect(
        host='rm-uf63r1m8zyr5k47j4qo.mysql.rds.aliyuncs.com',
        port=3306,
        user='root',
        password="zx123ZX!@#",
        database='xiaoman2',
        use_unicode=True,
        charset="utf8",  # 指定字符编码
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
counter_lock = threading.Lock()


def wash_main(data__, index, i):
    try:
        d = dict(data__.iloc[index])
        with balalaba.cursor() as cursor_balalaba:
            with xiaoman.cursor() as cursor_xiaoman:
                home = d.get('home_page').replace('http://', '')
                if counter_lock.acquire():
                    # 判断www      https
                    home = 'http://www.' + home
                    cursor_balalaba.execute('''select hashid from comps where home_page = '{}' limit 1;'''.format(home))
                    result = cursor_balalaba.fetchone()
                    if result:
                        hashid = result.get('hashid', 0)
                        if hashid != 0:
                            emails = d.get('Email')
                            if emails:
                                if ',' in emails:
                                    for email in emails.split(','):
                                        cursor_xiaoman.execute(
                                            '''insert into cont (hashid, cont_email) values (%s,%s)  ;''',
                                            (hashid, email))
                                else:
                                    cursor_xiaoman.execute('''insert into cont (hashid, cont_email) values (%s,%s)  ;''' , (hashid, emails))
                            cursor_balalaba.execute(
                                    '''update low_priority comps set facebook=%s,twitter=%s,linkedin=%s,instagram=%s where hashid=%s''', \
                                    (
                                        d.get('Facebook') if d.get('Facebook') else ' ',
                                        d.get('Twitter') if d.get('Twitter') else ' ',
                                        d.get('Linkedin') if d.get('Linkedin') else ' ',
                                        d.get('Instagram') if d.get('Instagram') else ' ',
                                        hashid,
                                    )
                                )
                        print('{}单次插入完成,{}.时间{}'.format(i, index, datetime.datetime.now()))
                    else:
                        home = d.get('home_page').replace('http://', '')
                        cursor_balalaba.execute('''select hashid from comps where home_page = '{}' limit 1;'''.format(home))
                        result2 = cursor_balalaba.fetchone()
                        if result2:
                            hashid = result2.get('hashid', 0)
                            if hashid != 0:
                                emails = d.get('Email')
                                if emails:
                                    if ',' in emails:
                                        for email in emails.split(','):
                                            cursor_xiaoman.execute(
                                                '''insert into cont (hashid, cont_email) values (%s,%s)  ;''',
                                                (hashid, email))
                                    else:
                                        cursor_xiaoman.execute(
                                            '''insert into cont (hashid, cont_email) values (%s,%s)  ;''',
                                            (hashid, emails))
                                # with xiaoman.cursor() as cursor_xiaoman:
                                cursor_balalaba.execute(
                                        '''update low_priority comps set facebook=%s,twitter=%s,linkedin=%s,instagram=%s where hashid=%s''', \
                                        (
                                            d.get('Facebook') if d.get('Facebook') else ' ',
                                            d.get('Twitter') if d.get('Twitter') else ' ',
                                            d.get('Linkedin') if d.get('Linkedin') else ' ',
                                            d.get('Instagram') if d.get('Instagram') else ' ',
                                            hashid,
                                        )
                                    )
                            print('{}单次插入完成2,{}.时间{}'.format(i, index, datetime.datetime.now()))
                        else:
                            home = 'https://www.' + home
                            cursor_balalaba.execute('''select hashid from comps where home_page = '{}' limit 1;'''.format(home))
                            result3 = cursor_balalaba.fetchone()
                            if result3:
                                hashid = result3.get('hashid', 0)
                                if hashid != 0:
                                    emails = d.get('Email')
                                    if emails:
                                        if ',' in emails:
                                            for email in emails.split(','):
                                                cursor_xiaoman.execute(
                                                    '''insert into cont (hashid, cont_email) values (%s,%s)  ;''',
                                                    (hashid, email))
                                        else:
                                            cursor_xiaoman.execute(
                                                '''insert into cont (hashid, cont_email) values (%s,%s)  ;''',
                                                (hashid, emails))
                                    # with xiaoman.cursor() as cursor_xiaoman:
                                    cursor_balalaba.execute(
                                            '''update low_priority comps set facebook=%s,twitter=%s,linkedin=%s,instagram=%s where hashid=%s''', \
                                            (
                                                d.get('Facebook') if d.get('Facebook') else ' ',
                                                d.get('Twitter') if d.get('Twitter') else ' ',
                                                d.get('Linkedin') if d.get('Linkedin') else ' ',
                                                d.get('Instagram') if d.get('Instagram') else ' ',
                                                hashid,
                                            )
                                        )
                                print('{}单次插入完成3,{}.时间{}'.format(i, index, datetime.datetime.now()))

                    counter_lock.release()
    except:
        counter_lock.release()
        print('dddd')


def main(data_, i):
    '''
    # 判断这个url与数据库里的那个hashid匹配, 写入公司信息 用查询的方式(in)
    # 拿到hashid插入conts表
    :param data:
    :return:
    '''
    for index in range(len(data_)):
        main_thread = Thread(target=wash_main, args=(data_, index, i))
        main_thread.start()


if __name__ == '__main__':
    for i in range(0, 10):
        data_ = data[i*10000:(i+1)*10000]
        if not data_.empty:
            p1 = Process(target=main, args=(data_, i))
            p1.start()
            # main(data_)
