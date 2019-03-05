import re

from bs4 import BeautifulSoup
from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from selenium import webdriver

from youku_spider.items import YouKuItem
from youku_spider.settings import *
from youku_spider.utils import YouKuException, create_proxy_auth_extension


class YouKuSpider(CrawlSpider):
    name = 'tudou'
    s_url = 'http://www.soku.com/nt/search/q_%E4%BA%9A%E9%A9%AC%E9%80%8A%E5%B9%B3%E5%8F%B0_orderby_1_lengthtype_{}_limitdate_0?spm=a2h0k.8191414.0.0&site=14&_lg=10&page={}'

    def __init__(self):
        super(YouKuSpider, self).__init__()
        # 传递信息,也就是当爬虫关闭时scrapy会发出一个spider_closed的信息,当这个信号发出时就调用closeSpider函数关闭这个浏览器.
        dispatcher.connect(self.closeSpider, signals.spider_closed)

    def closeSpider(self, spider):
        print('spider closed')
        self.browser.quit()

    def start_requests(self):
        '''
        第一个请求
        :return:timemore={}&timeless={}
        '''
        url_list = [2, 4, 3]
        for i in url_list:
            yield Request(self.s_url.format(i, 1), callback=self.parse_index, meta={'page': 1, 'lengthtype': i})

    def parse_index(self, response):
        items = YouKuItem()
        soup = BeautifulSoup(response.text, 'lxml')
        div_list = soup.find_all('div', attrs={'class': 'v'})

        for div in div_list:
            title = div.find_all('a')[0].get('title')
            a_url = 'http:' + div.find_all('a')[0].get('href')
            img = 'http:' + div.find_all('img')[0].get('src')

            creat_time = div.find_all('div', attrs={'class': 'v-meta-data'})[-1].find_all('span')[-1].text

            title = re.sub(r'[】【\n]', '', title)
            try:
                views = div.find_all('div', attrs={'class': 'v-meta-data'})[-1].find_all('span')[0].text
                views = re.sub(',', '', views)
                views = int(views)
            except:
                views = ''
            items['title'] = title
            items['url'] = a_url
            items['views'] = views
            items['thumbnail'] = img
            items['createdAt'] = creat_time
            yield items

        page = response.meta.get('page')
        lengthtype = response.meta.get('lengthtype')
        print(str(lengthtype) + ',' + str(page))
        if page == 101:
            dispatcher.connect(self.closeSpider, signals.spider_closed)
            raise YouKuException('所有信息已爬取完毕')
        yield Request(self.s_url.format(lengthtype, page+1), callback=self.parse_index, meta={'page': page+1, 'lengthtype': lengthtype})

