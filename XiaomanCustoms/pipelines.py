# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
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
            mysql.conn.commit()  # 写入操作
        return item


class MyImagesPipeline(ImagesPipeline):
    """
    下载管道
    """
    def get_media_requests(self, item, info):
        """
        :param item: spider.py返回的item
        :param info:
        :return:
        """
        for image_url in item['image_urls']:
            referer = item['url']
            yield Request(url=image_url, meta={'item': item, 'referer': referer})
        # image_urls = []
        # image_urls.append(item['cover_picture_url'])
        # for image_url in image_urls:
        #     yield Request(url=image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        """
        :param self:
        :param request: 每一个图片下载管道的请求
        :param response:
        :param info:
        :return: 每套图的分类目录
        """
        item = request.meta['item']
        folder = item['image_path']
        folder_strip = strip(folder)
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(folder_strip, image_guid)
        # folder = item['title']
        # folder_strip = strip(folder)
        # filename = u'full/{0}'.format(folder_strip)
        return filename

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item


def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path