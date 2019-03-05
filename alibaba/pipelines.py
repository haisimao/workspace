# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import time

import pymongo

from items import AlibabaItem
from settings import MONGO_URI, MONGODB_PORT


class AliBaBaTimePipeline(object):
    def process_item(self, item, spider):
        item['create_time'] = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        return item


class AliBaBaInsertPipeline(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(host=MONGO_URI, port=MONGODB_PORT)
        self.db = self.connection['weibo_news']
        self.table = self.db['news']

    def process_item(self, item, spider):
        if isinstance(item, AlibabaItem):
            self.table.insert({'title': item['title'],
                               'text': item['text']})
        return item
