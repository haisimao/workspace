# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import time

import pymysql

from Bizvibe_scrapy.items import CompItem, CompDescItem


class BizvibePipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(
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

    def process_item(self, item, spider):
        if isinstance(item, CompItem):
            with self.conn.cursor() as cursor:
                # 解决数据库插入字符串编码的问题
                try:
                    # 写入cont表
                    contact_emails = item.get('contact_email')
                    if contact_emails:
                        if ',' in contact_emails:
                            emails = contact_emails.split(',')
                            for email in emails:
                                cursor.execute('''insert into cont (hashid, cont_email) values (%s,%s)  ;''', (item['hashid'], email.strip(),))
                        else:
                            cursor.execute('''insert into cont (hashid, cont_email) values (%s,%s)  ;''', (item['hashid'], contact_emails,))
                    # 写入comp表 ,
                    if item['year_found']:
                        cursor.execute('''insert into comp (comp_name,main_industry, home_page, comp_tel, comp_addr,year_found,comp_sales,employees_num,hashid,country,facebook,twitter,linkedin,source,sic_code) values ("{}","{}","{}","{}","{}",{},{},{},"{}","{}","{}","{}","{}","{}",{});'''.format(
                               item['comp_name'],
                               item['main_industry'],
                               item['home_page'],
                               item['comp_tel'],
                               item['comp_addr'],
                               item['year_found'],
                               item['comp_sales'],
                               item['employees_num'],
                               item['hashid'],
                               item['country'],
                               item['facebook'],
                               item['twitter'],
                               item['linkedin'],
                               item['source_'],
                               item['sic_code'],
                           ))
                    else:
                        cursor.execute(
                            '''insert into comp (comp_name,main_industry, home_page, comp_tel, comp_addr,comp_sales,employees_num,hashid,country,facebook,twitter,linkedin,source,sic_code) values ("{}","{}","{}","{}","{}",{},{},"{}","{}","{}","{}","{}","{}",{});'''.format(
                                item['comp_name'],
                                item['main_industry'],
                                item['home_page'],
                                item['comp_tel'],
                                item['comp_addr'],
                                item['comp_sales'],
                                item['employees_num'],
                                item['hashid'],
                                item['country'],
                                item['facebook'],
                                item['twitter'],
                                item['linkedin'],
                                item['source_'],
                                item['sic_code'],
                            ))
                except:
                    print(item['comp_name'], '写入数据库失败')
        # if isinstance(item, CompDescItem):
        #     try:
        #         with self.conn.cursor() as cursor:
        #             cursor.execute('''update low_priority comp set comp_intro="{}" where hashid='{}';'''.format(item['comp_intro'], item['hashid']))
        #     except:
        #         print('写入数据库失败')
        return item