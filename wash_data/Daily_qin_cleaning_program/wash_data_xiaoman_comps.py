#-*-coding:utf-8-*-
import time
from datetime import date, timedelta, datetime
from multiprocessing import Process
from threading import Thread
import threading

import pandas as pd
import pymysql
from pandas import Series, DataFrame
import numpy as np
import io

from sqlalchemy import create_engine

# 指定用户, 密码, IP, port , 数据库, 编码

# 本地balalaba数据库
# 云上to_balalaba数据库
ip = 'rm-uf63r1m8zyr5k47j4qo.mysql.rds.aliyuncs.com'
my_engin = create_engine('mysql+pymysql://root:zx123ZX!@#@'+ip+':3306/to_balalaba?charset=utf8mb4')


# 已完成
def cont(my_data , j=0):
    '''
    :param data: 字典
    :return:
    '''
    if len(my_data) == 0:
        return
    #去重
    # my_data = my_data.drop_duplicates()
    # # 替换非法字符
    # my_data['cont_email'].replace([r'[A-Za-z1234567890\.]*:\D*:\S*', ], [' ', ], regex=True, inplace=True)
    # my_data['cont_email'].replace([r'\D*-', ], ['', ], regex=True, inplace=True)
    # 处理联系人名称
    data_A = my_data[['cont_first_name', ]]
    data_B = my_data[['cont_last_name', ]]
    for index in range(len(data_A)):
        data_B.iloc[index][0] = data_A.iloc[index][0] + ' ' + data_B.iloc[index][0]
    my_data[['cont_last_name', ]] = data_B
    my_data.rename(columns={
        'cont_last_name': 'cont_name',
    }, inplace=True)
    my_data.drop(['cont_first_name'], axis=1, inplace=True)
    my_data.replace(r'\$', '', regex=True, inplace=True)
    try:
        pd.io.sql.to_sql(my_data, 'conts', con=my_engin, if_exists='append', index=False, chunksize=1)
    except:
        with open('wash_xiaoman_log.txt', 'a', encoding='utf-8') as f:
            f.write('*' * 10)
            f.write('时间{},执行{}次插入{}表失败,hashid: {}\n'.format(datetime.now(), j, 'cont', my_data['hashid']))
            f.write('*' * 10)
    return None


def comp2(my_data, j=0):
    if len(my_data) == 0:
        return
    # 删除创建时间列
    # my_data.drop(['sic_code'], axis=1, inplace=True)
    # my_data.drop(['email_count'], axis=1, inplace=True)
    my_data.drop(['custom_import_count'], axis=1, inplace=True)
    my_data.drop(['custom_export_count'], axis=1, inplace=True)
    my_data.drop(['source', ], axis=1, inplace=True)
    my_data.drop(['create_time', ], axis=1, inplace=True)
    # 去重
    # my_data = my_data.drop_duplicates('hashid')
    # 用'comp_add_intro'列 , 填充'comp_intro'列
    data_A = my_data[['comp_add_intro', ]]
    data_B = my_data[['comp_intro', ]]
    for index in range(len(data_A)):
        if (data_A.iloc[index] != '')[0]:
            data_B.iloc[index][0] = data_B.iloc[index][0] + ';' + data_A.iloc[index][0]
    my_data[['comp_intro', ]] = data_B
    my_data.rename(columns={'id': 'comp_no', }, inplace=True)
    # 删除公司信息追加列
    my_data.drop(['comp_add_intro'], axis=1, inplace=True)
    # 替换非法字符
    my_data.replace({
        '$': '0',
        -1: 0,
    }, inplace=True)
    my_data.replace(r'\$', '', regex=True, inplace=True)
    # 写入新的数据库需修改
    try:
        pd.io.sql.to_sql(my_data, 'comps', con=my_engin, if_exists='append', index=False, chunksize=1)
    except:
        with open('wash_xiaoman_log.txt', 'a', encoding='utf-8') as f:
            f.write('*' * 10)
            f.write('时间{},执行{}次插入{}表失败,hashid: {}\n'.format(datetime.now(), j, 'comp', my_data['hashid']))
            f.write('*' * 10)
    return


def sum_wash_time(wash):
    '''
    计算运行时间
    :param wash:
    :return:
    '''
    def call_wash(*agrs, **kwargs):
        start_time = time.time()
        wash(*agrs, **kwargs)
        end_time = time.time()
        with open('wash_xiaoman_log.txt', 'a', encoding='utf-8') as f:
            f.write('执行时间:%is' % int(end_time - start_time))
    return call_wash


sem_pool = threading.Semaphore(100)  #限制线程的最大数量为100个


@sum_wash_time
def wash_data(big_sql_list=['cash'], page=1):
    '''
    :param big_sql_list:  传入一个数据库表列表
    :return:
    '''
    conn = pymysql.connect(
        host='rm-uf63r1m8zyr5k47j4qo.mysql.rds.aliyuncs.com',
        port=3306,
        user='root',
        password="zx123ZX!@#",
        database='xiaoman2',
        use_unicode=True,
        charset="utf8mb4",  # 指定字符编码
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )
    # yesterday = (datetime.now() + timedelta(days=-1)).strftime('%Y-%m-%d')
    yesterday = '2019-02-21'
    # today = datetime.now().strftime('%Y-%m-%d')
    today = '2019-02-26'
    for i in big_sql_list:
        with conn.cursor() as cursor:
            # cursor.execute('select count(hashid) as num from {}  where create_time > "{}" and create_time < "{}" and hashid in (select hashid from comp) and source = "名录集消费品"  ORDER BY id, hashid limit 0, 500000;'.format(i, yesterday, today))
            # num = cursor.fetchone().get('num', 0)
            # cursor.execute('select * from {} where create_time > "{}" and create_time < "{}" and hashid in (select hashid from comp2) ORDER BY id, hashid limit 1000000, 200000000;'.format(i, yesterday, today))
            cursor.execute('select * from {} where createdAt > "{}" and createdAt < "{}" and hashid in (select hashid from comp2);'.format(i, yesterday, today))
            all_response = cursor.fetchall()
            num = len(all_response)
            if len(all_response) == 0:
                return
            # 记录一天的爬取量
            # num = len(all_response)
            with open('wash_xiaoman_log.txt', 'a', encoding='utf-8') as f:
                f.write('*' * 100)
                f.write('时间{},执行插入{}表, 总量{}\n'.format(datetime.now(), i, num))
                f.write('*' * 10)
            my_data = DataFrame(all_response)
            # 添加去重策略, 不同的表有不同的去重逻辑, 需要一个一个判断添加
            if i == 'cont':
                my_data.drop_duplicates('cont_email', inplace=True)
            elif i == 'comp2':
                my_data.drop_duplicates('hashid', inplace=True)
            else:
                my_data.drop(['id'], axis=1, inplace=True)
                my_data.drop_duplicates(inplace=True)
            # 按照量级区分, 查询
            print(len(all_response))
            for j in range(int(num/page)):
                try:
                    with sem_pool:
                        print('当前进度', (j / (int(num / page))*100), '%')
                        dynamic_wash_function = eval(i)
                        data = my_data[j * page:(j+1) * page].copy()
                        xiaoman_thread = Thread(target=dynamic_wash_function, args=(data, j))
                        xiaoman_thread.start()
                except:
                    with open('wash_xiaoman_log.txt', 'a', encoding='utf-8') as f:
                        f.write('*'*10)
                        f.write('时间{},执行插入{}表失败, 第{}次插入\n'.format(datetime.now(), i, j))
                        f.write('*' * 10)
            # 余量数据插入,  重要
            try:
                dynamic_wash_function = eval(i)
                data = my_data[num * page:].copy()
                xiaoman_thread_ = Thread(target=dynamic_wash_function, args=(data,))
                xiaoman_thread_.start()
            except:
                with open('wash_xiaoman_log.txt', 'a', encoding='utf-8') as f:
                    f.write('*' * 10)
                    f.write('没什么好插入的')
                    f.write('*' * 10)
            with open('wash_xiaoman_log.txt', 'a', encoding='utf-8') as f:
                f.write('*' * 10)
                f.write('{}表数据清洗完成'.format(i))
                f.write('*' * 10)


if __name__ == '__main__':
    # 主键关联, 首先插入comp
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=1)
    wash_data(big_sql_list=['comp2'], page=100)
    wash_data(big_sql_list=['comp2'], page=10)
    wash_data(big_sql_list=['comp2'], page=2)
    wash_data(big_sql_list=['comp2'], page=2)
    wash_data(big_sql_list=['comp2'], page=2)
    wash_data(big_sql_list=['comp2'], page=3)
    wash_data(big_sql_list=['comp2'], page=3)
    wash_data(big_sql_list=['comp2'], page=3)
    wash_data(big_sql_list=['comp2'], page=3)
    wash_data(big_sql_list=['comp2'], page=4)
    wash_data(big_sql_list=['comp2'], page=4)
    wash_data(big_sql_list=['comp2'], page=4)
    wash_data(big_sql_list=['comp2'], page=5)
    wash_data(big_sql_list=['comp2'], page=5)
    wash_data(big_sql_list=['comp2'], page=5)
    wash_data(big_sql_list=['comp2'], page=5)
    wash_data(big_sql_list=['comp2'], page=6)
    wash_data(big_sql_list=['comp2'], page=6)
    wash_data(big_sql_list=['comp2'], page=6)
    wash_data(big_sql_list=['comp2'], page=6)
    # cont 未运行,,, 修改查询语句...cont_url



