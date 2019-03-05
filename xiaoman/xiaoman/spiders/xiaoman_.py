import datetime
import random
import re
import time
from urllib.parse import quote

import pymysql
from scrapy import Spider, Request
from items import CompItem, ContItem, CustomsItem, Customs_InfoItem
from scrapy import FormRequest
import json
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from utils import XiaoManException


class XiaomanSpider(Spider):
    name = 'xiaoman_'
    start_url = 'https://x.xiaoman.cn/api/company-read/search-list?industryType=sic&keyword={}&realtime=0&searchType=company&page_size=25'

    def __init__(self):
        # 建立数据库连接
        self.connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password="yq201808",
            database='to_balalaba',
            use_unicode=True,
            charset="utf8mb4",  # 指定字符编码
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
        )
        self.conn = pymysql.connect(
            host='rm-uf63r1m8zyr5k47j4qo.mysql.rds.aliyuncs.com',
            port=3306,
            user='root',
            password="zx123ZX!@#",
            database='balalaba',
            use_unicode=True,
            charset="utf8mb4",  # 指定字符编码
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
        )
        # 传递信息,也就是当爬虫关闭时scrapy会发出一个spider_closed的信息,当这个信号发出时就调用closeSpider函数关闭这个浏览器.
        dispatcher.connect(self.closeSpider, signals.spider_closed)

    def closeSpider(self, spider):
        print('spider closed at {}'.format(datetime.datetime.now()))

    def start_requests(self):
        '''
       第一个请求
       :return:timemore={}&timeless={}
       '''
        with self.connection.cursor() as cursor:
            # 41492  39300
            # demands写入balalaba, comp写入xiaoman2
            cursor.execute('''select comp_name, id from demands where id < 39300 order by id desc;''')
            response = cursor.fetchall()
            print('本次查询' + str(len(response)) + '条数据')
        for comp in response:
            # 规则公司搜索名
            if comp.get('comp_name'):
                try:
                    company_name = comp.get('comp_name')
                    if company_name == None:
                        yield
                    # 批量进行公司信息提取
                    send_url = self.start_url.format(quote(company_name))
                    priority = int(comp.get('id'))
                    print('公司', priority)
                    time.sleep(random.randint(60, 120))
                    yield Request(send_url, priority=priority, callback=self.parse_index, meta={'company_name': comp.get('comp_name'), 'changed_comp_name': comp.get('comp_name')})
                    # LTD
                    if ' LTD' in company_name:
                        company_name_ = comp.get('comp_name').replace(' LTD', ' Limited')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                    if ' LTD' in company_name:
                        company_name_ = comp.get('comp_name').replace(' LTD', ' LTD.')

                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                    if ' Limited' in company_name:
                        company_name_ = comp.get('comp_name').replace(' Limited', ' LTD')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                    if ' Limited' in company_name:
                        company_name_ = comp.get('comp_name').replace(' Limited', ' LTD.')

                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                    if ' LTD.' in company_name:
                        company_name_ = comp.get('comp_name').replace(' LTD.', ' LTD')

                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                    if ' LTD.' in company_name:
                        company_name_ = comp.get('comp_name').replace(' LTD.', ' LTD')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})

                    # inc
                    if ' Inc' in company_name:
                        company_name_ = comp.get('comp_name').replace(' Inc', ' Inc.')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                    if ' Inc' in company_name:
                        company_name_ = comp.get('comp_name').replace(' Inc', ' incorporation')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                    if ' incorporation' in company_name:
                        company_name_ = comp.get('comp_name').replace(' incorporation', ' Inc')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                    if ' incorporation' in company_name:
                        company_name_ = comp.get('comp_name').replace(' incorporation', ' Inc.')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                    if ' Inc.' in company_name:
                        company_name_ = comp.get('comp_name').replace(' Inc.', ' incorporation')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                    if ' Inc.' in company_name:
                        company_name_ = comp.get('comp_name').replace(' Inc.', ' Inc')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})

                    # WLL
                    if ' WLL' in company_name:
                        company_name_ = comp.get('comp_name').replace(' WLL', ' W.L.L')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                    if ' W.L.L' in company_name:
                        company_name_ = comp.get('comp_name').replace(' W.L.L', ' WLL')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})

                    # CO
                    if ' CO' in company_name:
                        company_name_ = comp.get('comp_name').replace(' CO', ' CO.')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                    if ' CO' in company_name:
                        company_name_ = comp.get('comp_name').replace(' CO', ' CO.,')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                    if ' CO.' in company_name:
                        company_name_ = comp.get('comp_name').replace(' CO.', ' CO')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                    if ' CO.' in company_name:
                        company_name_ = comp.get('comp_name').replace(' CO.', ' CO.,')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                    if ' CO.,' in company_name:
                        company_name_ = comp.get('comp_name').replace(' CO.,', ' CO.')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                    if ' CO.,' in company_name:
                        company_name_ = comp.get('comp_name').replace(' CO.,', ' CO')
                        send_url = self.start_url.format(quote(company_name_))
                        # 批量进行公司信息提取
                        priority = int(comp.get('id'))
                        print('公司', priority)
                        time.sleep(random.randint(60, 120))
                        yield Request(send_url, priority=priority, callback=self.parse_index,
                                      meta={'company_name': comp.get('comp_name'),
                                            'changed_comp_name': company_name_})
                except:
                    print('查询{}失败,{}'.format(comp.get('comp_no'), datetime.datetime.now()))
                    raise XiaoManException('爬取{}阻塞,{}.请重启'.format(comp.get('comp_no'), datetime.datetime.now()))

    def parse_index(self, response):
        data = json.loads(response.text)
        try:
            changed_comp_name = response.meta.get('changed_comp_name')
            company_name = response.meta.get('company_name')
            hash_id = data['data']['list'][0]['companyHashId']   # data为companyHashId列表
            if hash_id:
                # 公司信息
                companyName = data['data']['list'][0]['companyName']
                if companyName == changed_comp_name:
                    print('查询成功')
                    comp_url = 'https://x.xiaoman.cn/api/company-read/profile?brief_only=true" + "&id=' + hash_id
                    time.sleep(60)
                    print(hash_id)
                    yield Request(url=comp_url, callback=self.parse_item, meta={'hashid': hash_id, 'company_name': company_name}, dont_filter=True, )
                    # 联系人信息
                    time.sleep(60)
                    cont_url = 'https://x.xiaoman.cn/api/company-read/profile-emails?id={}&sort=&keyword=&page=1'.format(hash_id)
                    yield Request(url=cont_url, callback=self.parse_cont, meta={'hashid': hash_id, 'page': 1}, dont_filter=True)
        except:
            print('查无此公司')

    def parse_item(self, response):
        item_comp = CompItem()
        # comp 公司信息表（13项）
        data = json.loads(response.text)['data']
        item_comp['comp_name'] = data['companyName'] if 'companyName' in data else ''
        item_comp['main_industry'] = data['sicName'] if 'sicName' in data else ''
        item_comp['home_page'] = data['homepage'] if 'homepage' in data else ''
        item_comp['comp_tel'] = data['phone'] if 'phone' in data else ''
        item_comp['comp_addr'] = data['address'] if 'address' in data else '' + ',' + data['city'] if 'city' in data else '' \
                                + ',' + data['province'] if 'province' in data else '' + ',' + data['postcode'] if 'postcode' in data else '' \
                                + ',' + data['country'] if 'country' in data else ''
        item_comp['comp_intro'] = data['description'] if 'description' in data else ''
        item_comp['comp_type'] = data['companyType'] if 'companyType' in data else ''
        item_comp['year_found'] = data['foundedYear'] if 'foundedYear' in data else -1
        item_comp['comp_sales'] = data['sales'] if 'sales' in data else ''
        item_comp['employees_num'] = data['employees'] if 'employees' in data else -1
        item_comp['comp_assets'] = data['asserts'] if 'asserts' in data else ''
        item_comp['trade_style'] = data['tradestyle'] if 'tradestyle' in data else ''
        item_comp['hashid'] = response.meta['hashid']
        item_comp['createdAt'] = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        item_comp['updatedAt'] = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        with self.conn.cursor() as cursor_balalaba:
            cursor_balalaba.execute('''update demands set hashid="{}" where comp_name="{}";'''.format(response.meta['hashid'], response.meta.get('company_name')))  # 执行SQL
            # self.conn.commit()
        yield item_comp

    def parse_cont(self, response):
        item = ContItem()
        if json.loads(response.text)['code'] == 0:
            data = json.loads(response.text)['data']
            if data['contactCount'] > 0:
                total_page = data['contactCount'] // 9 + 1
                for email in data['emails']:
                    item['hashid'] = response.meta['hashid']
                    first_name = email['first_name'] if email['first_name'] else ' '
                    last_name = email['last_name'] if email['last_name'] else ' '
                    item['cont_name'] = first_name + last_name
                    item['cont_post'] = email['position']
                    item['cont_email'] = email['value']
                    item['cone_url'] = [source['url'] for source in email['sources'] if email['sources'] != []]
                    item['createdAt'] = time.strftime('%Y-%m-%d %H:%M', time.localtime())
                    item['updatedAt'] = time.strftime('%Y-%m-%d %H:%M', time.localtime())
                    yield item



























