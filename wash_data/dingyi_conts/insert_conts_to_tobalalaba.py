import datetime
import threading
import time

from threading import Thread

import pandas as pd
import pymysql
import numpy as np

from sqlalchemy import create_engine
ip = 'rm-uf63r1m8zyr5k47j4qo.mysql.rds.aliyuncs.com'
my_engin = create_engine('mysql+pymysql://root:zx123ZX!@#@'+ip+':3306/to_balalaba?charset=utf8mb4')

# 状态: 未插入
data = pd.read_excel(r'C:\Users\YQ\Desktop\dingyi_contacts\comp_2019-01-23\comp16_2019_01_23.xls', header=0,)
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
data.where(data.notnull(), None)
# 替换空值为一个空字符串
data.replace(np.nan, ' ', inplace=True)
print(data.shape)

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
counter_lock = threading.Lock()

with balalaba.cursor() as cursor_balalaba:
    cursor_balalaba.execute('''select home_page, hashid from {} where length(home_page)>1;'''.format('comps'))
    result = cursor_balalaba.fetchall()
    print(len(result), 'from comps')
comp_name_hashid_dict = {}
for res in result:
    comp_name_hashid_dict[res['home_page']] = res['hashid']

sem_pool = threading.Semaphore(50)  # 限制线程的最大数量为100个


def wash_main(data__, index, i):
    try:
        d = dict(data__.iloc[index])
        create_time = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        with balalaba.cursor() as cursor_balalaba:
            with xiaoman.cursor() as cursor_xiaoman:
                home = d.get('home_page').replace('http://', '')
                if counter_lock.acquire():
                    # 判断www      https
                    home = 'http://www.' + home
                    # 在字典里面查询hoem_page, 如果查到了,就返回hashid进入下一步
                    hashid = comp_name_hashid_dict.get(home)
                    if hashid:
                        emails = d.get('Email')
                        if emails:
                            if ',' in emails:
                                for email in emails.split(',')[:20]:
                                    if email != '':
                                        cursor_balalaba.execute(
                                            '''insert into conts (hashid, cont_email, createdAt, updatedAt) values (%s,%s,%s,%s)  ;''',
                                            (hashid, email, create_time, create_time))
                            else:
                                cursor_balalaba.execute('''insert into conts (hashid, cont_email, createdAt, updatedAt) values (%s,%s,%s,%s)  ;''',
                                            (hashid, emails, create_time, create_time))
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
                        home = d.get('home_page').replace('http://', 'www.')    # 'https://www.standardmodern.com'
                        hashid = comp_name_hashid_dict.get(home)
                        if hashid:
                            emails = d.get('Email')
                            if emails:
                                if ',' in emails:
                                    for email in emails.split(',')[:20]:
                                        if email != '':
                                            cursor_balalaba.execute(
                                                '''insert into conts (hashid, cont_email, createdAt, updatedAt) values (%s,%s,%s,%s)  ;''',
                                            (hashid, email, create_time, create_time))
                                else:
                                    cursor_balalaba.execute(
                                        '''insert into conts (hashid, cont_email, createdAt, updatedAt) values (%s,%s,%s,%s)  ;''',
                                            (hashid, emails, create_time, create_time))
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
                            home = d.get('home_page').replace('http://', '')
                            home = 'https://www.' + home
                            hashid = comp_name_hashid_dict.get(home)
                            if hashid:
                                emails = d.get('Email')
                                if emails:
                                    if ',' in emails:
                                        for email in emails.split(',')[:20]:
                                            if email != '':
                                                cursor_balalaba.execute(
                                                    '''insert into conts (hashid, cont_email, createdAt, updatedAt) values (%s,%s,%s,%s)  ;''',
                                            (hashid, email, create_time, create_time))
                                    else:
                                        cursor_balalaba.execute(
                                            '''insert into conts (hashid, cont_email, createdAt, updatedAt) values (%s,%s,%s,%s)  ;''',
                                            (hashid, emails, create_time, create_time))
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
                            else:
                                home = d.get('home_page').replace('http://', '')
                                hashid = comp_name_hashid_dict.get(home)
                                if hashid:
                                    emails = d.get('Email')
                                    if emails:
                                        if ',' in emails:
                                            for email in emails.split(',')[:20]:
                                                if email != '':
                                                    cursor_balalaba.execute(
                                                        '''insert into conts (hashid, cont_email, createdAt, updatedAt) values (%s,%s,%s,%s)  ;''',
                                                        (hashid, email, create_time, create_time))
                                        else:
                                            cursor_balalaba.execute(
                                                '''insert into conts (hashid, cont_email, createdAt, updatedAt) values (%s,%s,%s,%s)  ;''',
                                                (hashid, emails, create_time, create_time))
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


def main_(data_, i):
    '''
    # 判断这个url与数据库里的那个hashid匹配, 写入公司信息 用查询的方式(in)
    # 拿到hashid插入conts表
    :param data:
    :return:
    '''
    for index in range(len(data_)):
        with sem_pool:
            main_thread = Thread(target=wash_main, args=(data_, index, i))
            main_thread.start()
            # wash_main(data_, index, i)


if __name__ == '__main__':
    for i in range(0, 10):
        data_ = data[i*10000:(i+1)*10000]
        if not data_.empty:
            main_(data_, i)
