import datetime
import re
import time

from bs4 import BeautifulSoup
from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider

from selenium import webdriver
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from settings import COOKIES_DICT, proxyHost, proxyPort, proxyUser, proxyPass
from utils import create_proxy_auth_extension


class AliBaBaSpider(CrawlSpider):
    name = 'alibaba'
    starts_url = 'http://sourcing.alibaba.com/rfq_search_list.htm?spm=a2700.8073608.1998677545.2.1be565aa8H42yF&categoryIds={}&page={}'
    # 配置跟换cookies时间
    COOKIES_SWITCH_TIME = datetime.datetime.now()
    # COOKIES_SWITCH_TIME = datetime.datetime.now() + datetime.timedelta(hours=-2)

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
        ##############写死cookies
        url = 'http://sourcing.alibaba.com/?spm=a2700.8293689.scGlobalHomeHeader.376.46ce65aavJsBwp&tracelog=header_rfq_market'
        self.browser.get(url)
        time.sleep(2)
        for i in COOKIES_DICT:
            self.browser.add_cookie(i)
        time.sleep(2)
        self.browser.refresh()
        ###############
        super(AliBaBaSpider, self).__init__()
        # 传递信息,也就是当爬虫关闭时scrapy会发出一个spider_closed的信息,当这个信号发出时就调用closeSpider函数关闭这个浏览器.
        dispatcher.connect(self.closeSpider, signals.spider_closed)

    def closeSpider(self, spider):
        print('spider closed')
        self.browser.quit()

    def start_requests(self):
        yield Request(self.starts_url.format('1524',2), callback=self.parse_index, dont_filter=True, meta={'page': 2})

    def parse_index(self, response):
        '''
        解析分类页,构造详情页请求,构造下一页请求
        :param response:
        :return:
        '''
        res = Selector(response)
        url = response.url
        try:
            for i in range(20):
                # 分类页的页面返回新请求
                try:
                    x_path = '// *[ @ id = "rfqSearchindex"] / div / div / div[{}] / div / div / div / div[1] / h1 / a/@href'
                    a_url = res.xpath(x_path.format(i)).extract()[0]
                    yield Request('http:' + a_url, callback=self.parse_detil, meta={
                                                                    'previous_page': url,
                                                                    'xpath': x_path.format(i),
                                                                    'page': response.meta.get('page'),
                                                                                })
                except:
                    continue
        except:
            return
        finally:
            # 构造下一页请求l
            page = int(response.meta.get('page')) + 1
            yield Request(self.starts_url.format('1524',page), callback=self.parse_index, dont_filter=True, meta={'page': page})

    def parse_detil(self, response):
        res = Selector(response)
        title = res.xpath('// *[ @ id = "app"] / div / div[1] / div[3] / div[1] / div / div[1] / h3 / span/text()').extract()[0]
        # time = res.xpath('// *[ @ id = "app"] / div / div[1] / div[3] / div[1] / div / div[1] / h3 / div / div[3] / span/text()').extract()[0]
        soup = BeautifulSoup(response.text, 'lxml')
        times_ = soup.find('div', class_='tp-time').text
        release_time = re.findall('[\d-]*', times_)[6]
        buyer = res.xpath('// *[ @ id = "app"] / div / div[1] / div[3] / div[1] / div / div[1] / div[1] / ul / li[1] / span/text()').extract()[0]
        print(buyer + '在'+ release_time + '发起了' + title)
        return






















