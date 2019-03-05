import datetime
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
import urllib.parse


class YouKuSpider(CrawlSpider):
    name = 'youku'
    s_url = 'https://so.youku.com/search_video/q_%E4%BA%9A%E9%A9%AC%E9%80%8A%E5%B9%B3%E5%8F%B0?spm=a2h0k.11417342.pageturning.dnextpage&aaid=a80a4d7b7dbad1672d29482102404204&lengthtype=2&timemore={}&timeless={}&pg={}'

    def __init__(self):
        # 封装代理
        proxy_auth_plugin_path = create_proxy_auth_extension(
            proxy_host=proxyHost,
            proxy_port=proxyPort,
            proxy_username=proxyUser,
            proxy_password=proxyPass)
        option = webdriver.ChromeOptions()
        option.add_argument("--start-maximized")
        option.add_extension(proxy_auth_plugin_path)
        self.browser = webdriver.Chrome(chrome_options=option)
        self.browser.maximize_window()
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
        # url_list = [[30, 60], [10, 30], [60, 0]]
        url_list = [[60, 0], ]
        for i in url_list:
            yield Request(self.s_url.format(i[0], i[1], 1), callback=self.parse_index, meta={'page': 1, 'timemore': i[0], 'timeless': i[1]})

    def parse_index(self, response):
        res = Selector(response)
        items = YouKuItem()
        soup = BeautifulSoup(response.text, 'lxml')
        div_list = soup.find_all('div', attrs={'class': 'sk-mod'})
        for div in div_list:
            title = div.find_all('a')[1].get('title')
            a_url = 'http:' + div.find_all('a')[1].get('href')
            try:
                creat_time = div.find_all('span', attrs={'class': 'spc-lv-4'})[0].text
                creat_time = re.findall('\d*-\d*-\d*', creat_time)[0]
            except:
                yield
            try:
                img = 'http:' + div.find_all('img')[0].get('src')
            except:
                continue
            if 'alicdn' in div.find_all('img')[0].get('src'):
                img = 'nothing'
            #     img_title = urllib.parse.quote(title)
            #     yield Request('https://so.youku.com/search_video/q_{}?spm=a2h0k.11417342.pageturning.dpagenumber&f=1&kb=020200000000000__{}'.format(img_title, img_title), callback=self.parse_img, meta={
            #         'title': title,
            #         'url': a_url,
            #         'thumbnail': img,
            #         'createdAt': creat_time,
            #
            #     })
            # else:
            #     try:
            items['title'] = title
            items['url'] = a_url
            items['thumbnail'] = img
            items['createdAt'] = creat_time
            yield items
                # except:
                #     print('数据返回出错')

        page = response.meta.get('page')
        timemore = response.meta.get('timemore')
        timeless = response.meta.get('timeless')
        print(str(timemore) + str(timeless) + ',' + str(page))
        if page == 100:
            dispatcher.connect(self.closeSpider, signals.spider_closed)
            raise YouKuException('所有信息已爬取完毕')
        yield Request(self.s_url.format(timemore, timeless, page+1), callback=self.parse_index, meta={'page': page+1, 'timemore': timemore, 'timeless': timeless})

    # def parse_img(self, response):
    #     '''
    #     解析拿不到图片的链接
    #     :param response:
    #     :return:
    #     '''
    #     res = Selector(response)
    #     items = YouKuItem()
    #     soup = BeautifulSoup(response.text, 'lxml')
    #     # try:
    #     div_list = soup.find_all('div', attrs={'class': 'sk-mod'})
    #     try:
    #         img = 'http:' + div_list[0].find_all('img')[0].get('src')
    #         print('解析无有效链接的url')
    #         if img == '':
    #             yield
    #         else:
    #             items['title'] = response.meta.get('title')
    #             items['url'] = response.meta.get('url')
    #             items['thumbnail'] = img
    #             items['createdAt'] = response.meta.get('creat_time') if response.meta.get(
    #                 'creat_time') else datetime.datetime.now()
    #             yield items
    #     except:
    #         yield


























