import datetime
import random
import re
import string
import time
from lxml import etree

import pymysql
from bs4 import BeautifulSoup
from scrapy import Request, FormRequest, Selector
from scrapy.spiders import CrawlSpider
import logging

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from urllib.request import unquote
import json

from Bizvibe_scrapy.items import CompItem
from Bizvibe_scrapy.settings import proxyHost, proxyPort, proxyUser, proxyPass, COOKIES_DICT, SICCODE, URL, CATEGORY, \
    SEARCH_PAGE, CATEGORY_SICCODE
from Bizvibe_scrapy.utils_ import *


class BizvibeSpoder(CrawlSpider):
    name = 'bizvibe'
    # 配置更换cookies时间
    COOKIES_SWITCH_TIME = datetime.datetime.now()

    def __init__(self):
        self.SEARCH_PAGE = 5
        with open(r'./comp_hashid.json', 'r+') as f:
            data = json.load(f)
        self.comp_name_hashid_dict = data
        super(BizvibeSpoder, self).__init__()
        dispatcher.connect(self.CloseSpider, signals.spider_closed)
        self.origin_url = 'https://www.bizvibe.com/bhapi/services/Search'

    def CloseSpider(self):
        '''
        关闭spider
        :return:
        '''
        print('爬虫正常关闭,At{}'.format(datetime.datetime.now()))

    def CloseExceptionSpider(self):
        '''
        关闭spider
        :return:
        '''
        print('响应超时爬虫正常关闭,At{}'.format(datetime.datetime.now()))

    def start_requests(self):
        '''
        第一个请求
        10008  10005
        '''
        try:
            data = {"category": "10021", "country": "", "location_type": "", "keyword": "", "domain": "",
                    "revenue": "0", "employee": "0", "type": "", "offset": '0', "limit": '12'}
            for ca in CATEGORY_SICCODE.keys():
                data['category'] = ca
                requests_data = json.dumps(data)
                yield Request(self.origin_url, method='POST', callback=self.parse_index,
                                meta={'data': requests_data, 'CATEGORY': ca},
                                body=requests_data, headers={'Content-Type': 'application/json'},dont_filter=True)
                print(data.get('offset'), 1)
        except:
            raise BizvibeException('爬取{}阻塞,{}.请重启'.format())

    def parse_index(self, response):
        '''
        拿到总页数, 构造所有公司请求
        :param response:
        :return:
        '''
        try:
            fildes = response.meta.get('CATEGORY')
            data_dict = json.loads(response.body)
            total_page = int(data_dict.get('hits').get('total'))
            print('统计记录', total_page)
            for page in range(SEARCH_PAGE, int(total_page/12) + 1):
                print('爬取', page)
                logging.info('爬取 {}'.format(page))
                data = {"category": "", "country": "", "location_type": "", "keyword": "", "domain": "", \
                        "revenue": "0", "employee": "0", "type": "", "offset": '', "limit": '12'}
                data['offset'] = str(page * 12)
                data['category'] = fildes
                requests_data = json.dumps(data)
                priority = int(total_page/12) + 1 - int(page)
                yield Request(self.origin_url, method='POST', priority=priority, callback=self.parse_detail,
                            meta={'data': requests_data, 'page': str(page), 'CATEGORY': fildes},
                            body=requests_data, headers={'Content-Type': 'application/json'}
                              )
        except Exception as e:
            print('报错', e)

    def parse_detail(self, response):
        items = CompItem()
        pg = response.meta.get('page')
        print(pg)
        data_dict = json.loads(response.body)
        hits = data_dict.get('hits').get('hits')
        try:
            for hit_ in hits:
                try:
                    hit = hit_.get('_source')
                    items['comp_name'] = hit.get('organization_name')
                    main_industrys = hit.get('categories')
                    main_industry = ''
                    if main_industrys:
                        for ca in range(len(main_industrys)):
                            main_industry += main_industrys[ca].get('level_2_name')
                    items['main_industry'] = main_industry
                    items['home_page'] = hit.get('organization_website')
                    items['comp_tel'] = hit.get('organization_phonenumber').replace(' ', '').replace('.', '')
                    items['comp_addr'] = hit.get('organization_address')
                    items['year_found'] = hit.get('yoe')
                    items['comp_sales'] = hit.get('revenue_count')
                    items['employees_num'] = hit.get('employee_count')
                    # 获取联系人
                    items['contact_email'] = hit.get('contact_email')
                    items['country'] = hit.get('country_name')
                    items['facebook'] = hit.get('fb_link')
                    items['twitter'] = hit.get('twitter_link')
                    items['linkedin'] = hit.get('linkedin_link')
                    items['source_'] = 'bizvibe'
                    ca = response.meta.get('CATEGORY')
                    items['sic_code'] = CATEGORY_SICCODE.get(ca)
                    if hit.get('organization_name') in self.comp_name_hashid_dict:
                        items['hashid'] = self.comp_name_hashid_dict.get(hit.get('organization_name'))
                    else:
                        items['hashid'] = encrypt_md5(hit.get('organization_name'))
                    yield items
                except Exception as e:
                    print('报错', e)
        except:
            print('无公司介绍')








