import time

import pymysql

from LinkedinSpideScrapy.items import LinkedinspidescrapyItem


class LinkedinTimePipeline(object):
    def process_item(self, item, spider):
        item['updatedAt'] = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        item['category'] = 'B2B'
        item['source'] = '土豆'
        return item


class LinkedinPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password="yq201808",
        database='to_balalaba',
        use_unicode=True,
        charset="utf8mb4",             # 指定字符编码
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )

    def process_item(self, item, spider):
        if isinstance(item, LinkedinspidescrapyItem):
            # pass
            with self.conn.cursor() as cursor:
                # 解决数据库插入字符串编码的问题
                # try:
                    if item['employees_num']:
                        cursor.execute('''UPDATE comps SET employees_num=%s WHERE comp_name=%s order by hashid limit 2;''', \
                                       (item['employees_num'],
                                        item['company_name'],)
                                       )
                    cursor.execute('''select year_found from comps WHERE comp_name=%s limit 0,1;''', \
                                   (
                                    item['company_name'],
                                    ))
                    response = cursor.fetchall()[0]
                    if item['year_found'] and response.get('year_found') == 0:
                        cursor.execute('''UPDATE comps SET year_found=%s WHERE comp_name=%s order by hashid limit 2;''', \
                                       (item['year_found'],
                                       item['company_name'],
                                        ))
                    if item['home_page']:
                        cursor.execute('''UPDATE comps SET home_page=%s WHERE comp_name=%s order by hashid limit 2;''', \
                                       (item['home_page'],
                                       item['company_name'],
                                       ))

                    if item['comp_intro']:
                        cursor.execute('''UPDATE comps SET comp_intro=%s WHERE comp_name=%s order by hashid limit 2;''', \
                                       (item['comp_intro'],
                                       item['company_name'],
                                       ))
                    if item['comp_addr']:
                        cursor.execute('''UPDATE comps SET comp_addr=%s WHERE comp_name=%s order by hashid limit 2;''', \
                                       (item['comp_addr'],
                                       item['company_name'],
                                       ))

                    print('插入' + item['company_name'])
                # except:
                #     print('写入数据库失败')
        return item