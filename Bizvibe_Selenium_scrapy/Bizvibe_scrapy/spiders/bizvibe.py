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

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from urllib.request import unquote
import json

from Bizvibe_scrapy.items import CompItem, CompDescItem
from Bizvibe_scrapy.settings import proxyHost, proxyPort, proxyUser, proxyPass, COOKIES_DICT, SICCODE, URL
from Bizvibe_scrapy.utils_ import *


class BizvibeSpoder(CrawlSpider):
    name = 'bizvibe'
    # 配置跟换cookies时间
    COOKIES_SWITCH_TIME = datetime.datetime.now()
    # custom_settings = {
    #     'LOG_LEVEL': 'INFO',  # 减少Log输出量，仅保留必要的信息
    #     # ...... 在爬虫内部用custom_setting可以让这个配置信息仅对这一个爬虫生效
    # }

    def __init__(self):
        self.SEARCH_PAGE = 5
        # 封装代理
        proxy_auth_plugin_path = create_proxy_auth_extension(
            proxy_host=proxyHost,
            proxy_port=proxyPort,
            proxy_username=proxyUser,
            proxy_password=proxyPass)
        option = webdriver.ChromeOptions()
        option.add_argument("--start-maximized")
        # 暂时不用代理
        # option.add_extension(proxy_auth_plugin_path)
        # option.add_argument('--headless')
        option.add_argument('--disable-gpu') #禁用 GPU 硬件加速，防止出现bug
        self.browser = webdriver.Chrome(chrome_options=option)
        # self.browser = webdriver.PhantomJS()
        self.browser.maximize_window()
        ##############写死cookies
        self.browser.get(URL)
        time.sleep(2)
        for i in COOKIES_DICT:
            self.browser.add_cookie(i)
        time.sleep(2)
        self.browser.refresh()
        time.sleep(2)
        self.browser.find_element_by_xpath('//*[@id="new-filter-options-employee"]/div/div[1]/h3/i').click()
        time.sleep(2)
        self.browser.find_element_by_xpath('// *[ @ id = "nfo-employee-list"] / ul / li[7] / div').click()
        # self.browser.find_element_by_xpath('//*[@id="nfo-employee-list"]/ul/li[6]/div').click()
        # self.browser.find_element_by_xpath('// *[ @ id = "nfo-employee-list"] / ul / li[5] / div').click()
        # self.browser.find_element_by_xpath('// *[ @ id = "nfo-employee-list"] / ul / li[4] / div').click()
        # self.browser.find_element_by_xpath('// *[ @ id = "nfo-employee-list"] / ul / li[3] / div').click()
        # self.browser.find_element_by_xpath('// *[ @ id = "nfo-employee-list"] / ul / li[2] / div').click()
        time.sleep(2)
        html = etree.HTML(self.browser.page_source)
        total_page = int(html.xpath('//*[@id="result-summary"]/div/span/b[1]/text()')[0].replace(',', ''))
        # 判断是否重头开始
        try:
            with open('D:\workspace\Bizvibe_Selenium_scrapy\Bizvibe_scrapy\page.json', 'r+') as f:
                data = json.load(f)
        except :
            print('FileNotFoundError')
        page = data.get('page') if data.get('page') else '1'
        data = {'page': page, 'total_page': str(total_page)}
        with open('D:\workspace\Bizvibe_Selenium_scrapy\Bizvibe_scrapy\page.json', 'w+') as f:
            json.dump(data, f)
        ###############
        super(BizvibeSpoder, self).__init__()
        dispatcher.connect(self.CloseSpider, signals.spider_closed)
        self.origin_url = 'https://www.bizvibe.com/bhapi/services/Search'
        self.must_url = 'https://www.bizvibe.com/bhapi/services/l2list/0/10021/0'

    def CloseSpider(self):
        '''
        关闭spider
        :return:
        '''
        self.browser.quit()
        print('爬虫正常关闭,At{}'.format(datetime.datetime.now()))

    def CloseExceptionSpider(self):
        '''
        关闭spider
        :return:
        '''
        self.browser.quit()
        print('响应超时爬虫正常关闭,At{}'.format(datetime.datetime.now()))

    def start_requests(self):
        '''
        第一个请求
        10008  10005
        '''
        try:
            data = {"category": "10021", "country": "", "location_type": "", "keyword": "", "domain": "",
                    "revenue": "0", "employee": "0", "type": "", "offset": '0', "limit": '12'}
            yield FormRequest(self.origin_url, callback=self.parse_index, meta={'data': data, 'page': '1'}, formdata=data, )
            print(data.get('offset'), 1)
        except:
            raise BizvibeException('爬取{}阻塞,{}.请重启'.format())

    def parse_index(self, response):
        # 先判断有没有新元素
        pg = response.meta.get('page')
        url_page = re.findall('\?page=(\d)\?', response.url)[0] if re.findall('\?page=(\d)\?', response.url) else 0
        if response.text == '已下载页面':
            # 构造新的请求
            page = int(pg) + 1
            with open('D:\workspace\Bizvibe_Selenium_scrapy\Bizvibe_scrapy\page.json', 'r+') as f:
                data = json.load(f)
            if page > int(data.get('total_page')):
                self.CloseSpider()
                raise BizvibeException('爬取完毕, 请修改参数重新爬取')
            data = response.meta.get('data')
            offset = int(data['offset']) + 12
            data['offset'] = str(offset)
            print(data.get('offset'), page)
            self.SEARCH_PAGE = page
            yield FormRequest(self.origin_url, callback=self.parse_index,
                              meta={'data': data, 'page': str(page)},
                              formdata=data,
                              )
        else:
            soup = BeautifulSoup(response.text, 'lxml')
            for i in range(1, 13):
                try:
                    x_path_page = 'Page' + pg + '-li-' + str(i)
                    print(x_path_page)
                    li = soup.find('li', id=x_path_page)
                    url_div = li.find('div', attrs={'class': 'box-inner relative w3-row'})
                    home_page_old = re.findall(r'"(.*)"', url_div['onclick'])[0]
                    # 公司detail_url
                    company_detail_page = 'https://www.bizvibe.com/company/'
                    company_detail_page += home_page_old
                    print(company_detail_page)
                    a_company_detail = soup.find('a', attrs={'data-liid': x_path_page})
                except:
                    print('解析元素错误')
                ######## 解析数据 ###########
                try:
                    items = CompItem()
                    data_item = json.loads(unquote(a_company_detail['data-item']))
                    items['comp_name'] = data_item.get('organization_name')
                    main_industrys = data_item.get('categories')
                    main_industry = ''
                    if main_industrys:
                        for ca in range(len(main_industrys)):
                            main_industry += main_industrys[ca].get('level_2_name')
                    items['main_industry'] = main_industry
                    items['home_page'] = data_item.get('organization_website')
                    items['comp_tel'] = data_item.get('organization_phonenumber').replace('.', '')
                    items['comp_addr'] = data_item.get('address')[0].get('address') + ' ' + data_item.get('address')[0].get('country_name') if data_item.get('address') else ''
                    # items['year_found'] = data_item.get('yoe') if data_item.get('yoe') else 0
                    items['year_found'] = data_item.get('yoe')
                    items['comp_sales'] = data_item.get('revenue_count')
                    items['employees_num'] = data_item.get('employee_count')
                    hashid = encrypt_md5(data_item.get('organization_name'))
                    items['hashid'] = hashid
                    # 获取联系人
                    items['contact_email'] = data_item.get('contact_email')
                    items['country'] = data_item.get('country_name')
                    items['facebook'] = data_item.get('fb_link')
                    items['twitter'] = data_item.get('twitter_link')
                    items['linkedin'] = data_item.get('linkedin_link')
                    items['source_'] = 'bizvibe'
                    items['sic_code'] = SICCODE
                    yield items
                except:
                    print('获取数据错误')
                try:
                    if company_detail_page != 'https://www.bizvibe.com/company/':
                        yield Request(company_detail_page, callback=self.parse_detail,
                                      meta={'spider_url': 'detail', 'hashid': hashid, 'page': pg}, )
                except:
                    print('公司介绍获取失败')            # 构造新的请求
            page = int(pg) + 1
            with open('D:\workspace\Bizvibe_Selenium_scrapy\Bizvibe_scrapy\page.json', 'r+') as f:
                data = json.load(f)
            with open('D:\workspace\Bizvibe_Selenium_scrapy\Bizvibe_scrapy\page.json', 'w+') as w:
                data['page'] = str(page)
                json.dump(data, w)
            if page > int(data.get('total_page')):
                self.CloseSpider()
                raise BizvibeException('爬取完毕, 请修改参数重新爬取')
            data = response.meta.get('data')
            offset = int(data['offset']) + 12
            data['offset'] = str(offset)
            print(data.get('offset'), page)
            self.SEARCH_PAGE = page
            yield FormRequest(self.origin_url, callback=self.parse_index,
                              meta={'data': data, 'page': str(page)},
                              formdata=data,
                              )

    def parse_detail(self, response):
        items = CompDescItem()
        res = Selector(response)
        try:
            hashid = response.meta.get('hashid')
            comp_intro = res.xpath('//*[@id="cp-basic-info"]/div[2]/div/div/div/div/div/text()').extract()[0]
            if comp_intro:
                items['comp_intro'] = comp_intro
                items['hashid'] = hashid
                yield items
            else:
                yield
        except:
            print('无公司介绍')








