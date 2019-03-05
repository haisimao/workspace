import time

import pymysql

from TenData_scrapyspider.items import Customs_InfoItem


class TendataTimePipeline(object):
    def process_item(self, item, spider):
        item['updatedAt'] = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        item['category'] = 'B2B'
        item['source'] = '土豆'
        return item


class TendataPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password="yq201808",
        database='up_balalaba',
        use_unicode=True,
        charset="utf8mb4",             # 指定字符编码
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
        )

    def process_item(self, item, spider):
        if isinstance(item, Customs_InfoItem):
            with self.conn.cursor() as cursor:
                # 解决数据库插入字符串编码的问题
                try:
                        cursor.execute('''insert into customs (hashid, port_time, all_buyers, prod_desc) values (%s,%s,%s,%s)  ;''',
                                       (
                                           item['hashid'],
                                           item['port_time'],
                                           item['exporter'],
                                           item['prod_desc'],
                                            )
                                       )
                        cursor.execute('''insert into custom_infos (
                         hashid,
                         port_time, 
                         prod_desc, 
                         importer, 
                         import_addr,
                         exporter,
                         export_addr,
                         net_amount,
                         prod_num,
                         ship_type,
                         source_port,
                         destination_port,
                         import_country
                        ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                           (
                               item['hashid'],
                               item['port_time'],
                               item['prod_desc'],
                               item['importer'],
                               item['import_addr'],
                               item['exporter'],
                               item['export_addr'],
                               item['net_amount'],
                               item['prod_num'],
                               item['ship_type'],
                               item['source_port'],
                               item['destination_port'],
                               item['import_country'],
                           )
                           )


                except:
                    print(item['importer'], '写入数据库失败')
        return item