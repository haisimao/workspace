import datetime
import re
import json

import pandas as pd
import pymysql
from bs4 import BeautifulSoup
from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider
from urllib.request import quote

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from items import TradeatlasScrapySpiderItem, CompsItems
from settings import COOKIES
from utils_ import TradeatlasException, comps_hashid, encrypt_md5


class TradeatlasSpider(CrawlSpider):
    name = 'tradeatlas'
    origin_url = '''https://www.tradeatlas.com/p7search/US/HS_CODE/{}/1293832800000/1356991199000?page={}'''

    def __init__(self):
        with open(r'./comp_hashid.json', 'r+') as f:
            data = json.load(f)
        self.comp_name_hashid_dict = data
        super(TradeatlasSpider, self).__init__()
        # 传递信息,也就是当爬虫关闭时scrapy会发出一个spider_closed的信息,当这个信号发出时就调用closeSpider函数关闭这个浏览器.
        dispatcher.connect(self.closeSpider, signals.spider_closed)

    def closeSpider(self, spider):
        print('spider closed at {}'.format(datetime.datetime.now()))

    def start_requests(self):
        '''
        第一个请求
        :return:
        '''
        data = pd.read_excel(r'C:\Users\YQ\Desktop\to teyi shaorong.xlsx', header=None, )
        HS_CODE = list(data[0])
        for hs in HS_CODE:
            try:
                # 批量进行公司信息提取
                send_url = self.origin_url.format(hs, 1)
                yield Request(send_url, callback=self.parse_index, meta={'page': '1', 'hs_code': hs})
            except:
                raise TradeatlasException('爬取{}阻塞,{}.请重启'.format(hs, datetime.datetime.now()))

    def parse_index(self, response):
        '''
        解析进口商页面,拿到总页数,发起details请求
        :return:
        '''
        hs_code = response.meta.get('hs_code')
        page_ = response.meta.get('page')
        soup = BeautifulSoup(response.text, 'lxml')
        ul = soup.find('ul', attrs={'class': 'pagination'})
        total_page = ul.find_all('li')[-2].string if ul else 1          # 拿到总页数
        div_searchresult = soup.find_all('div', attrs={'class': 'searchresult'})[0] if soup.find_all('div', attrs={'class': 'searchresult'}) else None
        if div_searchresult:
            tr_list = div_searchresult.find_all('tr')
            for tr in tr_list:
                a_tag = tr.find_all('a')[0] if tr.find_all('a') else None
                if a_tag != None:
                    a_src = a_tag.get('href')
                    yield Request(a_src, callback=self.parse_detail, meta={'page': page_, 'hs_code': hs_code})
        for page in range(2, int(total_page)+1):
            send_url = self.origin_url.format(hs_code, page)
            yield Request(send_url, callback=self.parse_index, meta={'page': page, 'hs_code': hs_code})

    def parse_detail(self, response):
        '''
        解析具体海关数据页面
        :param response:
        :return:
        '''
        items = CompsItems()
        soup = BeautifulSoup(response.text, 'lxml')
        ul_list = soup.find_all('ul', attrs={'class': 'dt-sc-fancy-list'})
        comp_ul = ul_list[0] if ul_list else None
        email_ul = ul_list[-1] if ul_list else None
        if comp_ul:
            comp_lis = comp_ul.find_all('li')
            items['comp_name'] = comp_lis[0].text.replace('Name : ', '').replace('\n', '').strip() if comp_lis[0].text else ''
            items['comp_addr'] = comp_lis[1].text.replace('Address :', '').replace('\n', '').strip() if comp_lis[1].text else ''
            items['country'] = comp_lis[-1].text.replace('Country :', '').replace('\n', '').strip() if comp_lis[-1].text else ''
        if email_ul:
            email_lis = email_ul.find_all('li')
            items['home_page'] = email_lis[0].text.replace('Web Page', '').replace(':', '').replace('\n', '').strip() if email_lis[0].text else ''
            items['emails'] = email_lis[1].text.replace('E-Mail', '').replace(':', '').replace('\n', '').strip() if email_lis[1].text else ''
            items['comp_tel'] = email_lis[2].text.replace('Telephone', '').replace(':', '').replace('\n', '').strip() if email_lis[2].text else ''
            fax = email_lis[3].text.replace('Fax :', '').replace('\n', '').strip() if email_lis[3].text else ''
        if items['comp_name'] in self.comp_name_hashid_dict.keys():
            items['hashid'] = self.comp_name_hashid_dict.get(items['comp_name'])
            hashid = self.comp_name_hashid_dict.get(items['comp_name'])
        else:
            items['hashid'] = encrypt_md5(items['comp_name'])
            hashid = encrypt_md5(items['comp_name'])
        items['source'] = 'Tradeatlas'
        ul = soup.find('ul', attrs={'class': 'pagination'})
        total_page = ul.find_all('li')[-2].string if ul.find_all('li')[-2] else 1
        for page in range(2, int(total_page) + 1):
            send_url = response.url + '?page={}'.format(page)
            yield Request(send_url, callback=self.parse_customs, meta={
                'import_country': items['country'],
                'importer': items['comp_name'],
                'import_email': items['emails'],
                'import_fax': fax,
                'import_tel': items['comp_tel'],
                'import_addr': items['comp_addr'],
                'hashid': hashid,
            })
        yield items

    def parse_customs(self, respons):
        '''
        解析海关数据
        :param respons:
        :return:
        '''
        # items = TradeatlasScrapySpiderItem()
        # items['import_country'] = respons.meta.get('import_country'),
        # items['importer'] = respons.meta.get('importer'),
        # items['import_email'] = respons.meta.get('import_email'),
        # items['import_fax'] = respons.meta.get('import_fax'),
        # items['import_tel'] = respons.meta.get('import_tel'),
        # items['import_addr'] = respons.meta.get('import_addr'),
        # items['hashid'] = respons.meta.get('hashid'),
        soup = BeautifulSoup(respons.text, 'lxml')
        custom_div = soup.find('div', attrs={'class': 'searchresult'})
        tr_list = custom_div.find_all('tr')[1:]
        for tr in tr_list:
            items = TradeatlasScrapySpiderItem()
            items['import_country'] = respons.meta.get('import_country'),
            items['importer'] = respons.meta.get('importer'),
            items['import_email'] = respons.meta.get('import_email'),
            items['import_fax'] = respons.meta.get('import_fax'),
            items['import_tel'] = respons.meta.get('import_tel'),
            items['import_addr'] = respons.meta.get('import_addr'),
            items['hashid'] = respons.meta.get('hashid'),
            td_list = tr.find_all('td')
            items['port_time'] = td_list[0].string.strip() if td_list[0].string else ''
            items['HS_Code'] = td_list[1].string.strip() if td_list[1].string else ''
            items['prod_desc'] = td_list[2].string.strip() if td_list[2].string else ''
            items['exporter'] = td_list[3].string.strip() if td_list[3].string else ''
            items['origin_country'] = td_list[4].string.strip() if td_list[4].string else ''
            items['trans_price'] = td_list[-1].string.strip() if td_list[-1].string else ''
            yield items


















































