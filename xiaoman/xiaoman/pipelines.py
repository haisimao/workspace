# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

import pymysql
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem

from scrapy import Item, Request
from scrapy.pipelines.images import ImagesPipeline

from MySQL import MySQLConnection

settings = get_project_settings()
mysql = MySQLConnection(settings)


class MySQLPipeline(object):
    """
    保存到数据库中对应的表
    """
    def __init__(self):
        self.mysql_cursor = mysql

    # pipeline默认调用
    def process_item(self, item, spider):
        if isinstance(item, Item):
            table_name = item.__class__.__name__.split('Item')[0].lower()  # 获取item的表名
            # table_name = item.name  # 获取item的表名
            col_str = ''
            row_str = ''
            for key in item.keys():
                col_str = col_str + " " + key + ","
                if item[key] == None:
                    row_str = "{}'{}',".format(row_str, item[key])
                elif not isinstance(item[key], int) and not isinstance(item[key], float):
                    row_str = "{}'{}',".format(row_str, item[key] if "'" not in item[key] else item[key].replace("'", "\\'"))
                else:
                    row_str = "{}'{}',".format(row_str, item[key])

                sql = "insert INTO {} ({}) VALUES ({}) ON DUPLICATE KEY UPDATE ".format(table_name, col_str[1:-1], row_str[:-1])

            for key, value in item.items():
                if item[key] == None:
                    sql += "{} = '{}', ".format(key, value)
                elif not isinstance(value, int) and not isinstance(value, float):
                    sql += "{} = '{}', ".format(key, value if "'" not in value else value.replace("'", "\\'"))
                else:
                    sql += "{} = '{}', ".format(key, value)
            item_sql = sql[:-2]
            self.mysql_cursor.cursor.execute(item_sql)  # 执行SQL
            print('写入成功')
            mysql.conn.commit()  # 写入操作

        return item


def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path