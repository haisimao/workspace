import datetime
import json
import re
import time

import pymysql
import scrapy
from scrapy import Request , FormRequest
from scrapy.spiders import CrawlSpider
from urllib.request import quote

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from TenData_scrapyspider.items import Customs_InfoItem
from TenData_scrapyspider.utils import TendataException
from db import RedisClient


class TendataSpider(CrawlSpider):
    name = 'tendata'
    origin_url = 'http://wmt.tendata.cn/trade/search?_dc={}&queryCodesDesc={}&page={}'
    detail_url = "http://wmt.tendata.cn/shipment/north_america/imports/{}/{}?countryOfOriginCode={}&countryOfDestinationCode="

    def __init__(self):
        super(TendataSpider, self).__init__()
        self.connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='yq201808',
            database='to_balalaba',
            use_unicode=True,
            charset='utf8mb4',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
        )
        self.querycode = '%7B%22country%22%3A%22north_america%22%2C%22startDate%22%3A%222016-01-01%22%2C%22endDate%22%3A%222018-01-02%22%2C%22filterBlank%22%3Atrue%2C%22filterFields%22%3A%5B%22importer%22%5D%2C%22filterLogistics%22%3Atrue%2C%22highlights%22%3A%5B%22importer%22%5D%2C%22conditions%22%3A%7B%22importer%22%3A%5B%22%2B{}%22%5D%7D%2C%22rangeConditions%22%3A%7B%7D%2C%22description%22%3A%22%E7%AE%80%E8%BF%B0%EF%BC%9A2016-01-01-2018-01-02%EF%BC%8C%E8%BF%9B%E5%8F%A3%E5%95%86%EF%BC%9A%E5%8C%85%E5%90%AB%E2%80%9C{}%E2%80%9D%EF%BC%8C%22%2C%22catalog%22%3A%22imports%22%7D'
        self.conn = RedisClient('cookies', 'tendata')
        dispatcher.connect(self.CloseSpider, signals.spider_closed)

    def CloseSpider(self):
        '''
        关闭spider时
        :return:
        '''
        print('爬虫正常关闭')

    def start_requests(self):
        '''
        第一个请求
        :return:timemore={}&timeless={}
        '''
        with self.connection.cursor() as cursor:
            # cursor.execute('''select comp_name, comp_no from comps where comp_no < 904583  and comp_no > 733760;''')
            # cursor.execute('''select comp_name, hashid, country from comps where hashid in (select hashid from customs) limit 10;''')
            cursor.execute('''select comp_name, hashid, country, comp_no from comps where comp_no > 360000 order by comp_no desc ;''')
            response = cursor.fetchall()
            print('本次更新' + str(len(response)) + '条数据')
        for comp in response:
            # 规则公司搜索名
            try:
                company_name = quote(comp.get('comp_name'))
                hashid = comp.get('hashid')
                country = comp.get('country')
                comp_no = comp.get('comp_no')
                if company_name:
                    send_url = self.origin_url.format(int(time.time() * 1000),
                                                      self.querycode.format(company_name, company_name),
                                                      1)

                    yield FormRequest(send_url, callback=self.parse_index, priority=comp_no,
                                      meta={'company_name': comp.get('comp_name'), 'hashid': hashid, 'page': 1, 'country': country, 'comp_no': comp_no},
                                      formdata={'queryCodesDesc': self.querycode.format(company_name, company_name),
                                                      'page': '1'},
                                      )
            except:
                print('查询{}失败,{}'.format(comp.get('comp_no'), datetime.datetime.now()))
                raise TendataException('爬取{}阻塞,{}.请重启'.format(comp.get('comp_no'), datetime.datetime.now()))

    def parse_index(self, response):
        import json
        stadus = response.status

        results = json.loads(response.text)['results']
        content = results['content']
        company_name = response.meta.get('company_name')
        hashid = response.meta.get('hashid')
        country = response.meta.get('country')
        comp_no = response.meta.get('comp_no')
        if stadus != 200:
            raise TendataException('请重启爬虫, 公司ID{}'.format(comp_no))
        ids = ''
        for record in content:
            id = record['id']
            if content.index(record) != 24:
                ids = ids + record['id'] + ','
            else:
                ids = ids + record['id']
        for record in content:
            if 'countryOfOriginCode' in record:
                country = record['countryOfOriginCode']
            else:
                country = ''
            id = record['id']
            url = self.detail_url.format(id, ids, country)
            yield Request(url, callback=self.parse_detail, meta={'company_name': company_name, 'hashid': hashid, 'country': country, 'comp_no': comp_no})
        if int(response.meta['page']) == 1:
            total_page = results['totalPages']
            page = 2
            while page <= total_page:
                if page > 30:
                    break
                page += 1
                send_url = self.origin_url.format(int(time.time() * 1000),
                                                  self.querycode.format(company_name, company_name),
                                                  page)
                yield FormRequest(send_url, meta={'company_name': company_name, 'hashid': hashid, 'page': page, 'country': country, 'comp_no': comp_no},
                                      formdata={'queryCodesDesc': self.querycode.format(company_name, company_name),
                                                      'page': str(page)}, callback=self.parse_index)

    def parse_detail(self, response):
        comp_no = response.meta.get('comp_no')
        print(comp_no)
        item = Customs_InfoItem()
        company_name = response.meta.get('company_name')
        hashid = response.meta.get('hashid')
        country = response.meta.get('country')
        # 公司hashid
        item['hashid'] = hashid
        # 搜索公司所在国家
        item['import_country'] = country
        # 抵港日期
        item['port_time'] = response.xpath('/html/body/table/tr[4]/td/table/tr[2]/td/table/tr/td/table/tr[9]/td[4]/text()').extract()[0].strip('\r\n ')
        # 进口商
        # item['importer'] = response.xpath('/html/body/table/tr[2]/td/table/tr[3]/td/table/tr[2]/td/table/tr[1]/td[2]/text()').extract()[0]
        item['importer'] = company_name
        # 进口商地址
        item['import_addr'] = response.xpath('/html/body/table/tr[2]/td/table/tr[3]/td/table/tr[2]/td/table/tr[2]/td[2]/text()').extract()[0].strip('\r\n ')
        # 出口商
        item['exporter'] = response.xpath('/html/body/table/tr[2]/td/table/tr[2]/td/table/tr[2]/td/table/tr[1]/td[2]/text()').extract()[0]
        # 出口商地址
        item['export_addr'] = response.xpath('/html/body/table/tr[2]/td/table/tr[2]/td/table/tr[2]/td/table/tr[2]/td[2]/text()').extract()[0].strip('\r\n ')
        # 描述
        prod_desc = response.xpath('/html/body/table/tr[5]/td/table/tr[2]/td/table/tr/td/table/tr[2]/td[2]/text()').extract()
        prod_descs = ''
        for i in prod_desc:
            prod_descs += re.sub('[^A-Za-z0-9_:]*', '', i) + ' '
        item['prod_desc'] = prod_descs
        item['net_amount'] = re.sub(',', '', response.xpath('/html/body/table/tr[3]/td/table/tr[2]/td/table/tr/td/table/tr[1]/td[2]/text()').extract()[0])
        # 件数 re.sub('[^A-Za-z0-9_:]*','', prod_desc[0])
        item['prod_num'] = response.xpath('/html/body/table/tr[3]/td/table/tr[2]/td/table/tr/td/table/tr[2]/td[2]/text()').extract()[0]
        # 运输方式
        item['ship_type'] = response.xpath('/html/body/table/tr[4]/td/table/tr[2]/td/table/tr/td/table/tr[8]/td[4]/text()').extract()[0]
        # 启运港口
        item['source_port'] = response.xpath('/html/body/table/tr[4]/td/table/tr[2]/td/table/tr/td/table/tr[5]/td[4]/text()').extract()[0]
        # 抵达港口
        item['destination_port'] = response.xpath('/html/body/table/tr[4]/td/table/tr[2]/td/table/tr/td/table/tr[6]/td[4]/text()').extract()[0]

        yield item












