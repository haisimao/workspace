import datetime
import re
import json

import pymysql
from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider
from urllib.request import quote

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


from db_redis import RedisClient


class YingDianTongSpider(CrawlSpider):
    name = 'yingdiantong'
    # 01类
    origin_url = '''https://server.onloon.cc/bshop/explore/dnb/search?industryCodes=0111%3B0112%3B0115%3B0116%3B0119%3B0131%3B0132%3B0133%3B0134%3B0139%3B0161%3B0171%3B0172%3B0173%3B0174%3B0175%3B0179%3B0181%3B0182%3B0191&pageNumber={}&pageSize=5'''
    linkman_url = '''https://server.onloon.cc/bshop/contacts/domain/searchForDnbList?page=1&size=9&companyNames={}'''
    previous_url = '''https://customapi.onloon.net/api/customtrade/detail?keywordsType=1&companyType=0&page=1&pageSize=1&dnb=1&country=&userId=56ef2ad7b1f74802ae7109d5b0d0edc1&mainUserId=56582028666a4fc89ba76be68b9552ab&keywords={}'''
    company_url = '''https://server.onloon.cc/bshop/explore/dnb/company/detail?id={}'''

    def __init__(self):
        super(YingDianTongSpider, self).__init__()
        # # 建立数据库连接
        # self.connection = pymysql.connect(
        #     host='127.0.0.1',
        #     port=3306,
        #     user='root',
        #     password='yq201808',
        #     database='linkedin_balalaba',
        #     use_unicode=True,
        #     charset="utf8mb4",  # 指定字符编码
        #     autocommit=True,
        #     cursorclass=pymysql.cursors.DictCursor,
        # )
        self.redis_conn = RedisClient('cookies', 'yingdiantong')
        # 传递信息,也就是当爬虫关闭时scrapy会发出一个spider_closed的信息,当这个信号发出时就调用closeSpider函数关闭这个浏览器.
        dispatcher.connect(self.closeSpider, signals.spider_closed)

    def closeSpider(self, spider):
        print('spider closed at {}'.format(datetime.dattime.now()))

    def start_requests(self):
        '''
        首次请求
        :return:
        '''
        yield Request(self.origin_url.format(1), callback=self.parse_index, meta={
            'page': 1,

                      })

    def parse_index(self, response):
        '''
        得到totalpages,,构造所有公司请求
        :param response:
        :return:
        '''
        res = json.loads(response.text)
        data = res.get('data')
        for i in int(data.get('totalPages')):
            stop_page = int(self.redis_conn.db.get('yidiantong_company_parse_page'))
            if stop_page:
                i += 1 + stop_page
            i += 1
            priority = int(data.get('totalPages')) - i
            # 构造所有公司请求
            yield Request(self.origin_url.format(i), priority=priority, callback=self.parse_company, meta={
                'page': i,
            })

    def parse_company(self, response):
        '''
        确认公司优先级,解析公司返回数据, 构造相应联系人请求
        :param response:
        :return:
        '''
        res = json.loads(response.text)
        data = res.get('data')
        #####
        # 解析公司基本信息
        #####
        records = data.get('records')
        page = response.meta.get('page')
        self.redis_conn.db.set('yidiantong_company_parse_page', page)
        # 构造相应联系人请求
        for record in records:
            comp_name = record.get('name')    #  公司名称
            home_page = 'www.' + record.get('website')
            comp_tel = record.get('baseInfo').get('primaryIndustryCodeList').get('telephone')
            id = record.get('id')   # 邓白氏编码
            comp_addr = record.get('baseInfo').get('address').get('address') + record.get('baseInfo').get('address').get('state') + record.get('baseInfo').get('address').get('city') + record.get('baseInfo').get('address').get('country')

            yield Request(self.linkman_url.format(record.get('name').repalce(' ', '+')),
                          callback=self.parse_linkman, meta={
                                                            'page': page,
                                                            'id': id,

                },)

    def parse_linkman(self, response):
        res = json.loads(response.text)
        data = res.get('data')
        id = response.meta.get('id')
        records = data.get('records')
        for record in records:
            pass









































