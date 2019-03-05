import datetime
import threading
from multiprocessing import Process

from threading import Thread

import pandas as pd
import pymysql
import numpy as np

from sqlalchemy import create_engine
my_engin = create_engine('mysql+pymysql://root:yq201808@localhost:3306/to_balalaba?charset=utf8')

counter_lock = threading.Lock()

data = pd.read_excel(r'C:\Users\YQ\Desktop\dingyi_contacts\comp_2018-12-11\comp0_.xls', header=0,)

data.rename(columns={'公司名称': 'comp_name', '网站': 'home_page', '电话': 'contact_phone', '地址': 'address'} ,inplace=True)
data.drop('传真', axis=1, inplace=True)
data.drop('comp_name', axis=1, inplace=True)
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


def wash_main(index):
    try:
        d = dict(data.iloc[index])
        with balalaba.cursor() as cursor_balalaba:
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
                                    cursor_balalaba.execute(
                                        '''insert into conts (hashid, cont_email) values (%s,%s)  ;''',
                                        (hashid, email))
                            else:
                                cursor_balalaba.execute('''insert into conts (hashid, cont_email) values (%s,%s)  ;''',
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
                    print('单次插入完成,{}.时间{}'.format(index, datetime.datetime.now()))
                else:
                    home = d.get('home_page').replace('http://', '')
                    cursor_balalaba.execute('''select hashid from comps where home_page = '{}' limit 1;'''.format(home))
                    result2 = cursor_balalaba.fetchone()
                    if result2:
                        hashid = result.get('hashid', 0)
                        if hashid != 0:
                            emails = d.get('Email')
                            if emails:
                                if ',' in emails:
                                    for email in emails.split(','):
                                        cursor_balalaba.execute(
                                            '''insert into conts (hashid, cont_email) values (%s,%s)  ;''',
                                            (hashid, email))
                                else:
                                    cursor_balalaba.execute(
                                        '''insert into conts (hashid, cont_email) values (%s,%s)  ;''',
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
                        print('单次插入完成,{}.时间{}'.format(index, datetime.datetime.now()))
                    else:
                        home = 'https://www.' + home
                        cursor_balalaba.execute('''select hashid from comps where home_page = '{}' limit 1;'''.format(home))
                        result3 = cursor_balalaba.fetchone()
                        if result3:
                            hashid = result.get('hashid', 0)
                            if hashid != 0:
                                emails = d.get('Email')
                                if emails:
                                    if ',' in emails:
                                        for email in emails.split(','):
                                            cursor_balalaba.execute(
                                                '''insert into conts (hashid, cont_email) values (%s,%s)  ;''',
                                                (hashid, email))
                                    else:
                                        cursor_balalaba.execute(
                                            '''insert into conts (hashid, cont_email) values (%s,%s)  ;''',
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
                            print('单次插入完成,{}.时间{}'.format(index, datetime.datetime.now()))
                        else:
                            home = 'https://www.' + home
                            cursor_balalaba.execute(
                                '''select hashid from comps where home_page = '{}' limit 1;'''.format(home))
                            result3 = cursor_balalaba.fetchone()
                            if result3:
                                hashid = result.get('hashid', 0)
                                if hashid != 0:
                                    emails = d.get('Email')
                                    if emails:
                                        if ',' in emails:
                                            for email in emails.split(','):
                                                cursor_balalaba.execute(
                                                    '''insert into conts (hashid, cont_email) values (%s,%s)  ;''',
                                                    (hashid, email))
                                        else:
                                            cursor_balalaba.execute(
                                                '''insert into conts (hashid, cont_email) values (%s,%s)  ;''',
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
                                print('单次插入完成,{}.时间{}'.format(index, datetime.datetime.now()))
                counter_lock.release()
    except:
        counter_lock.release()
        print('ddd')


def main():
    # 判断这个url与数据库里的那个hashid匹配, 写入公司信息 用查询的方式(in)
    # 拿到hashid插入conts表
    for index in range(len(data)):
        main_thread = Thread(target=wash_main, args=(index, ))
        main_thread.start()


if __name__ == '__main__':
    main()
