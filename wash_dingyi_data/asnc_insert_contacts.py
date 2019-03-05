import asyncio
import threading

import pandas as pd
import pymysql
import numpy as np

from sqlalchemy import create_engine
my_engin = create_engine('mysql+pymysql://root:yq201808@localhost:3306/up_balalaba?charset=utf8')

counter_lock = threading.Lock()

data = pd.read_excel(r'C:\Users\YQ\Desktop\comp2_.xls', header=0,)

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


async def select_db(cursor, hoem_page):
    cursor.execute('''select hashid from comps where home_page = '{}' limit 1;'''.format(hoem_page))


async def wash_main(index):
    try:
        d = dict(data.iloc[index])
        with balalaba.cursor() as cursor_balalaba:
            home = d.get('home_page').replace('http://', '')
            home = 'http://www.' + home
            await select_db(cursor_balalaba, home)
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
                            '''update low_priority comps set Facebook=%s,Twitter=%s,Linkedin=%s,Instagram=%s where hashid=%s''', \
                            (
                                d.get('Facebook') if d.get('Facebook') else ' ',
                                d.get('Twitter') if d.get('Twitter') else ' ',
                                d.get('Linkedin') if d.get('Linkedin') else ' ',
                                d.get('Instagram') if d.get('Instagram') else ' ',
                                hashid,
                            )
                        )
                print('单次插入完成,{}'.format(index))
            else:
                home = d.get('home_page').replace('http://', '')
                await select_db(cursor_balalaba, home)
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
                                '''update low_priority comps set Facebook=%s,Twitter=%s,Linkedin=%s,Instagram=%s where hashid=%s''', \
                                (
                                    d.get('Facebook') if d.get('Facebook') else ' ',
                                    d.get('Twitter') if d.get('Twitter') else ' ',
                                    d.get('Linkedin') if d.get('Linkedin') else ' ',
                                    d.get('Instagram') if d.get('Instagram') else ' ',
                                    hashid,
                                )
                            )
                    print('单次插入完成,{}'.format(index))
                else:
                    home = 'https://www.' + home
                    await select_db(cursor_balalaba, home)
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
                                    '''update low_priority comps set Facebook=%s,Twitter=%s,Linkedin=%s,Instagram=%s where hashid=%s''', \
                                    (
                                        d.get('Facebook') if d.get('Facebook') else ' ',
                                        d.get('Twitter') if d.get('Twitter') else ' ',
                                        d.get('Linkedin') if d.get('Linkedin') else ' ',
                                        d.get('Instagram') if d.get('Instagram') else ' ',
                                        hashid,
                                    )
                                )
                        print('单次插入完成,{}'.format(index))
    except:
        print('ddd')


# 判断这个url与数据库里的那个hashid匹配, 写入公司信息 用查询的方式
# 拿到hashid插入conts表
async def main():
    for index in range(len(data)):
        await wash_main(index)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = asyncio.wait([main()])
    loop.run_until_complete(tasks)























