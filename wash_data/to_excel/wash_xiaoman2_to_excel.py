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
my_engin = create_engine('mysql+pymysql://root:yq201808@localhost:3306/to_balalaba?charset=utf8mb4')

# 云上balalaba数据库
# ip = 'rm-uf63r1m8zyr5k47j4qo.mysql.rds.aliyuncs.com'
# my_engin = create_engine('mysql+pymysql://root:zx123ZX!@#@'+ip+':3306/balalaba?charset=utf8mb4')


# 已完成
# def cash(my_data, j=0):
#     '''
#     cash清洗函数, 去重, 替换 '$' , 删除'$'多的行
#     :param data: 字典
#     :return:
#     '''
#     if len(my_data) == 0:
#         return
#     # 删除创建时间列
#     my_data.drop(['create_time'], axis=1, inplace=True)
#     # my_data.drop(['id'], axis=1, inplace=True)
#     #去重
#     my_data = my_data.drop_duplicates()
#     # 去掉数据中 '$' 很多的行
#     my_data = my_data.drop_duplicates([
#         'cash_begin',
#         'net_operate',
#         'net_invest',
#         'cash_end',
#         'capital_exp',
#         'net_change',
#     ])
#
#     # 替换非法字符
#     my_data.replace({
#         '$': '$0',
#     }, inplace=True)
#     my_data.replace(r'\$', '', regex=True, inplace=True)
#
#     # if_exists='append'以追加的方式写入,
#     # index=False 忽略index
#     try:
#         pd.io.sql.to_sql(my_data, 'cash', con=my_engin, if_exists='append', index=False, chunksize=1)         # 写入数据库
#     except:
#         with open('wash_xiaoman_log.txt', 'a', encoding='utf-8') as f:
#             f.write('*' * 10)
#             f.write('时间{},执行{}次插入{}表失败,hashid: {}\n'.format(datetime.now(), j, 'cash', my_data['hashid']))
#             f.write('*' * 10)
#     return None
#
#
# # 已完成
# def decash_all(my_data, j=0):
#     '''
#     decash_all清洗函数, 去重, 替换 '$' , 删除'$'多的行
#     :param data: 字典
#     :return:
#     '''
#     if len(my_data) == 0:
#         return
#     # 删除创建时间列
#     my_data.drop(['create_time'], axis=1, inplace=True)
#     # my_data.drop(['id'], axis=1, inplace=True)
#     #去重
#     my_data = my_data.drop_duplicates()
#     # 去掉数据中 '$' 很多的行
#     my_data = my_data.drop_duplicates([
#                                         'cash',
#                                         'net_receivables',
#                                         'net_fixed',
#                                         'total_assets',
#                                         'total_curassets',
#                                         'inventory',
#                                        ])
#     # 替换非法字符
#     my_data.replace({
#         '$': '0',
#     }, inplace=True)
#     my_data.replace(r'\$', '', regex=True, inplace=True)
#
#     try:
#         pd.io.sql.to_sql(my_data, 'decash_alls', con=my_engin, if_exists='append', index=False, chunksize=1)
#     except:
#         with open('wash_xiaoman_log.txt', 'a', encoding='utf-8') as f:
#             f.write('*' * 10)
#             f.write('时间{},执行{}次插入{}表失败,hashid: {}\n'.format(datetime.now(), j, 'decash_all', my_data['hashid']))
#             f.write('*' * 10)
#     return None

# # 已解决, 但数据太多,性能受影响
# def customs(my_data, j=0):
#     '''
#     cash清洗函数, 去重, 替换 '$' , 删除'$'多的行
#     :param data: 字典
#     :return:
#     '''
#     if len(my_data) == 0:
#         return
#     # 删除创建时间列
#     my_data.drop(['create_time'], axis=1, inplace=True)
#     my_data.drop(['customs_num'], axis=1, inplace=True)
#     my_data[['value_sum', ]] = ' '
#     #不去重
#     my_data = my_data.drop_duplicates()
#     # 用'comp_add_intro'列 , 填充'comp_intro'列
#     data_A = my_data[['ptype', ]]
#     data_B = my_data[['importer', ]]
#     data_C = my_data[['exporter', ]]
#     for index in range(len(data_A)):
#         if (data_A.iloc[index] != 'IMPORT')[0]:
#             data_B.iloc[index][0] = data_C.iloc[index][0]
#     my_data[['importer', ]] = data_B
#     my_data.rename(columns={
#         'importer': 'all_buyers',
#     }, inplace=True)
#     my_data.drop(['exporter'], axis=1, inplace=True)
#     my_data.drop(['ptype'], axis=1, inplace=True)
#     # 替换非法字符
#     my_data.replace({
#         -1: 0,
#         'XX': '',
#         '?': '',
#     }, inplace=True)
#     my_data.replace(r'\$', '', regex=True, inplace=True)
#
#     try:
#         pd.io.sql.to_sql(my_data, 'customs', con=my_engin, if_exists='append', index=False, chunksize=1)
#     except:
#         with open('wash_xiaoman_log.txt', 'a', encoding='utf-8') as f:
#             f.write('*' * 10)
#             f.write('时间{},执行{}次插入{}表失败,hashid: {}\n'.format(datetime.now(), j, 'custom', my_data['hashid']))
#             f.write('*' * 10)
#     return None
#
#
# # 已解决 , 但时间过长
# def customs_info(my_data, j=0):
#     '''
#     清洗函数, 去重, 替换 '$' , 删除'$'多的行
#     :param data: 字典
#     :return:
#     '''
#     if len(my_data) == 0:
#         return
#     # 删除创建时间列
#     my_data.drop(['create_time'], axis=1, inplace=True)
#     my_data.drop(['customs_num'], axis=1, inplace=True)
#     # my_data.drop(['id'], axis=1, inplace=True)
#
#     #不去重
#     my_data = my_data.drop_duplicates()
#     # 替换非法字符
#     my_data.replace({
#         -1: 0,
#         'None': '',
#         'XX': '',
#         '[]': '',
#         '?': '',
#     }, inplace=True)
#     my_data.replace(r'\$', '', regex=True, inplace=True)
#
#     try:
#         pd.io.sql.to_sql(my_data, 'custom_infos', con=my_engin, if_exists='append', index=False, chunksize=1)
#     except:
#         with open('wash_xiaoman_log.txt', 'a', encoding='utf-8') as f:
#             f.write('*' * 10)
#             f.write('时间{},执行{}次插入{}表失败,hashid: {}\n'.format(datetime.now(), j, 'custom_info', my_data['hashid']))
#             f.write('*' * 10)
#     return None
#
#
# # 已完成
# def decash(my_data, j=0):
#     '''
#     decashes清洗函数, 去重, 替换 '$' , 删除'$'多的行
#     :param data: 字典
#     :return:
#     '''
#     if len(my_data) == 0:
#         return
#     # 删除创建时间列
#     my_data.drop(['create_time'], axis=1, inplace=True)
#     # my_data.drop(['id'], axis=1, inplace=True)
#
#     #去重
#     my_data = my_data.drop_duplicates()
#     # 去掉数据中 '$' 很多的行
#     my_data = my_data.drop_duplicates([
#         'accounts_payable',
#         'short_debt',
#         'other_curliability',
#         'long_debt',
#         'total_liability',
#         'total_curliability',
#     ])
#     # 替换非法字符
#     my_data.replace({
#         '$': '$0',
#     }, inplace=True)
#
#     # 写入数据库
#     my_data.replace(r'\$', '', regex=True, inplace=True)
#
#     try:
#         pd.io.sql.to_sql(my_data, 'decashes', con=my_engin, if_exists='append', index=False, chunksize=1)
#     except:
#         with open('wash_xiaoman_log.txt', 'a', encoding='utf-8') as f:
#             f.write('*' * 10)
#             f.write('时间{},执行{}次插入{}表失败,hashid: {}\n'.format(datetime.now(), j, 'decash', my_data['hashid']))
#             f.write('*' * 10)
#     return None
#
#
# # 已完成
# def decash_eq(my_data, j=0):
#     '''
#     decash_eq清洗函数, 去重, 替换 '$' , 删除'$'多的行
#     :param data: 字典
#     :return:
#     '''
#     if len(my_data) == 0:
#         return
#     # 删除创建时间列
#     my_data.drop(['create_time'], axis=1, inplace=True)
#     # my_data.drop(['id'], axis=1, inplace=True)
#
#     #去重
#     my_data = my_data.drop_duplicates()
#     # 去掉数据中 '$' 很多的行
#     my_data = my_data.drop_duplicates([
#         'common_equity',
#         'total_equity',
#         'shares_outstanding',
#         'prefer_equity',
#     ])
#     # 替换非法字符
#     my_data.replace({
#         '$': '$0',
#     }, inplace=True)
#     my_data.replace(r'\$', '', regex=True, inplace=True)
#     try:
#         pd.io.sql.to_sql(my_data, 'decash_eqs', con=my_engin, if_exists='append', index=False, chunksize=1)         # 写入数据库
#     except:
#         with open('wash_xiaoman_log.txt', 'a', encoding='utf-8') as f:
#             f.write('*' * 10)
#             f.write('时间{},执行{}次插入{}表失败,hashid: {}\n'.format(datetime.now(), j, 'decash_eq', my_data['hashid']))
#             f.write('*' * 10)
#     return None
#
#
# # 已完成
# def profit(my_data, j=0):
#     '''
#     cash清洗函数, 去重, 替换 '$' , 删除'$'多的行
#     :param data: 字典
#     :return:
#     '''
#     if len(my_data) == 0:
#         return
#     # 删除创建时间列
#     my_data.drop(['create_time'], axis=1, inplace=True)
#     # my_data.drop(['id'], axis=1, inplace=True)
#
#     #去重
#     my_data = my_data.drop_duplicates()
#     my_data.replace(r'\$', '', regex=True, inplace=True)
#
#     try:
#         pd.io.sql.to_sql(my_data, 'profits', con=my_engin, if_exists='append', index=False, chunksize=1)           # 写入数据库
#     except:
#         with open('wash_xiaoman_log.txt', 'a', encoding='utf-8') as f:
#             f.write('*' * 10)
#             f.write('时间{},执行{}次插入{}表失败,hashid: {}\n'.format(datetime.now(), j, 'profit', my_data['hashid']))
#             f.write('*' * 10)
#     return None

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
        my_data.to_excel(r'D:\data_conts2.xls')
    except:
        with open('wash_xiaoman_log.txt', 'a', encoding='utf-8') as f:
            f.write('*' * 10)
            f.write('时间{},执行{}次插入{}表失败,hashid: {}\n'.format(datetime.now(), j, 'cont', my_data['hashid']))
            f.write('*' * 10)
    return None


def comp(my_data, j=0):
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
        my_data.to_excel(r'D:\data.xls')
    except:
        with open('wash_xiaoman_log.txt', 'a', encoding='utf-8') as f:
            f.write('*' * 10)
            f.write('时间{},执行{}次插入{}表失败,hashid: {}\n'.format(datetime.now(), j, 'comp', my_data['hashid']))
            f.write('*' * 10)
    return


def sum_wash_time(wash):
    '''
    计算运行时间
    :param wash: 传入一个函数, 计算它的运行时间
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
    yesterday = '2019-01-14'
    # today = datetime.now().strftime('%Y-%m-%d')
    today = '2019-01-18'
    for i in big_sql_list:
        with conn.cursor() as cursor:
            cursor.execute('select * from {} where hashid in (select hashid from comp) and cont_url = "名录集消费品";'.format(i))
            all_response = cursor.fetchall()
            if len(all_response) == 0:
                return
            my_data = DataFrame(all_response)
            # 添加去重策略, 不同的表有不同的去重逻辑, 需要一个一个判断添加
            if i == 'cont':
                my_data.drop_duplicates(['cont_email', 'cont_name'], keep='last', inplace=True)
            elif i == 'comp':
                my_data.drop_duplicates('hashid', inplace=True)
            else:
                my_data.drop(['id'], axis=1, inplace=True)
                my_data.drop_duplicates(inplace=True)
            print(len(all_response))
            try:
                dynamic_wash_function = eval(i)
                xiaoman_thread = Thread(target=dynamic_wash_function, args=(my_data, 1))
                xiaoman_thread.start()
            except:
                print('你好，bbg')


if __name__ == '__main__':
    big_sql_list = [
                'decash_all',
                'cash',
                'profit',
                'decash_eq',
                'decash',
                # 'customs',
                # 'customs_info',
                ]
    # 主键关联, 首先插入comp

    wash_data(big_sql_list=['comp'], page=10000)

    # cont 未运行,,, 修改查询语句...cont_url
    # time.sleep(600)
    # wash_data(big_sql_list=['cont'], page=1)

    # for table_name in big_sql_list:
    #     wash_data([table_name], page=1)


