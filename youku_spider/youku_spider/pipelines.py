import time

import pymysql

from youku_spider.items import YouKuItem


class YouKuTimePipeline(object):
    def process_item(self, item, spider):
        item['updatedAt'] = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        item['category'] = 'B2B'
        item['source'] = '优酷'
        item['views'] = 0
        return item


class YouKuPipeline(object):
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
        if isinstance(item, YouKuItem):
            # pass
            with self.conn.cursor() as cursor:
                # 解决数据库插入字符串编码的问题
                try:
                    cursor.execute('insert into videos (title, url, category, views, thumbnail, createdAt, updatedAt, source) values (%s,%s,%s,%s,%s,%s,%s,%s)', \
                                                   (
                                                    item['title'],
                                                    item['url'],
                                                    item['category'],
                                                    item['views'],
                                                    item['thumbnail'],
                                                    item['createdAt'],
                                                    item['updatedAt'],
                                                    item['source'],
                                                    ))
                except:
                    print('写入数据库失败')
        return item