# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

import pymysql

from items import TradeatlasScrapySpiderItem, CompsItems


class TradeatlasPipeline(object):
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
        if isinstance(item, TradeatlasScrapySpiderItem):
            with self.conn.cursor() as cursor:
                # 解决数据库插入字符串编码的问题
                try:
                    if item['hashid'] != (None,):
                        cursor.execute('''insert into customs (hashid, port_time, prod_desc, hs_code, all_buyers, value_sum) values (%s,%s,%s,%s,%s,%s)  ;''',
                                       (
                                           item['hashid'],
                                           item['port_time'],
                                           item['prod_desc'],
                                           item['HS_Code'],
                                           item['exporter'],
                                           item['trans_price'],
                                       ))
                        cursor.execute('''insert into custom_infos (
                            hashid,
                            import_country,
                            importer,
                            import_email,
                            import_fax,
                            import_tel,
                            import_addr,
                            port_time,
                            hs_code,
                            prod_desc,
                            exporter,
                            origin_country,
                            trans_price
                        ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                           (
                               item['hashid'],
                               item['import_country'],
                               item['importer'],
                               item['import_email'],
                               item['import_fax'],
                               item['import_tel'],
                               item['import_addr'],
                               item['port_time'],
                               item['HS_Code'],
                               item['prod_desc'],
                               item['exporter'],
                               item['origin_country'],
                               item['trans_price'],
                           ))
                except:
                    print(item['importer'], '海关写入数据库失败')
        if isinstance(item, CompsItems):
            with self.conn.cursor() as cursor:
                # 解决数据库插入字符串编码的问题
                try:
                    # 写入cont表
                    contact_emails = item.get('emails')
                    if contact_emails:
                        if ',' in contact_emails and '@' in contact_emails:
                            emails = contact_emails.split(',')
                            for email in emails:
                                cursor.execute('''insert into cont (hashid, cont_email) values (%s,%s)  ;''',
                                               (item['hashid'], email.strip(),))
                        elif '@' in contact_emails:
                            cursor.execute('''insert into cont (hashid, cont_email) values (%s,%s)  ;''',
                                           (item['hashid'], contact_emails,))
                    # 写入comp表 ,
                    cursor.execute(
                        '''insert into comp2 (comp_name, home_page, comp_tel, comp_addr,hashid,country,source) values ("{}","{}","{}","{}","{}","{}","{}");'''.format(
                            item['comp_name'],
                            item['home_page'],
                            item['comp_tel'],
                            item['comp_addr'],
                            item['hashid'],
                            item['country'],
                            item['source'],

                        ))
                except:
                    print(item['comp_name'], '公司写入数据库失败')
        return item