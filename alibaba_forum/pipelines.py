# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time

import pymysql

from items import AlibabaForumItem


class AlibabaTimePipeline(object):
    def process_item(self, item, spider):
        item['updatedAt'] = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        item['category'] = 'B2B'
        item['source'] = 'Alibaba外贸论坛'
        return item


class AlibabaPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
        host='rm-uf63r1m8zyr5k47j4qo.mysql.rds.aliyuncs.com',
        port=3306,
        user='xiaoman',
        password="xiaoman2018!!",
        database='xiaoman',
        use_unicode=True,
        charset="utf8",             # 指定字符编码
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )

    def process_item(self, item, spider):
        if isinstance(item, AlibabaForumItem):
            # pass
            with self.conn.cursor() as cursor:
                # 解决数据库插入字符串编码的问题
                cursor.execute('insert into information (title, url, category, views, thumbnail, createdAt, updatedAt, source) values (%s,%s,%s,%s,%s,%s,%s,%s)', \
                                                   (item['title'],
                                                    item['url'],
                                                    item['category'],
                                                    item['views'],
                                                    item['thumbnail'],
                                                    item['createdAt'],
                                                    item['updatedAt'],
                                                    item['source'],
                                                    ))
        return item